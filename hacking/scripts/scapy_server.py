import os
import rstr
import time
import threading
import netifaces as ni
from scapy.all import *
from colorama import Fore, Back, Style

# Interacts with a client by going through the three-way handshake.
# Shuts down the connection immediately after the connection has been established.
# Akaljed Dec 2010, https://akaljed.wordpress.com/2010/12/12/scapy-as-webserver/

'''
Use expression from /usr/share/nmap/nmap-service-probes
For example from nmap-service-probes file....
--------------------------------------------------------------------------------------------------------------------
# NoMachine Network Server
# Announce client version 5.6.7 (could be anything)
Probe TCP NoMachine q|NXSH-5.6.7\n|
ports 4000
rarity 9

match nomachine-nx m|^NXD-([\d.]+)\n| p/NoMachine NX Server remote desktop/ v/$1/ cpe:/a:nomachine:nx_server:$1/
--------------------------------------------------------------------------------------------------------------------
set tcp_experssion = r'^NXD-([\d.]+)\n'

- Note, not all services will work due to the limitations of rstr.xeger and nmaps usage of perl's 'i' and 's' options
- Avoid services that have "|s" or "|i" in them.
- Nmap rules that use the response to print the version may also lead to warnings or bad results.
- Expressions with non-zero bytes may be ify?

See notes at the bottom for more details.
'''

#EXTRAS
color = True
tcp_color = Fore.LIGHTMAGENTA_EX if color else ''
udp_color = Fore.LIGHTBLUE_EX if color else ''
reset_color = Style.RESET_ALL if color else ''
red = Fore.RED if color else ''
green = Fore.GREEN if color else ''
#EXTRAS


class NmapServiceServer:
	def __init__(self, port, net_iface, expression=r'', service_name='', tcp=True, line="", regex=""):
		self.port = port
		self.service_name = service_name.strip()
		if expression:
			self.expression = expression
		elif self.service_name:
			self.expression = NmapServiceServer.findExpression(self.service_name)
			if not self.expression:
				raise Exception('Service not found by name')
		else:
			raise Exception('Must set expression or service_name')
		self.iface = net_iface
		self.tcp = tcp
		self.udp = not tcp
		# TODO add tcp + udp logic
		self.thread = Thread(target=self._startService)
		self.thread.daemon = True
		self._stopper = True

		ni.ifaddresses(self.iface)
		self.ip_addr = ni.ifaddresses(self.iface)[ni.AF_INET][0]['addr']

		self.line = line
		self.regex = regex

	def start(self):
		self._stopper = False
		self.thread.start()

	def stop(self):
		self._stopper = True
		self._cleanIPTables()

	@staticmethod
	def findExpression(service_name):
		services = open('/usr/share/nmap/nmap-service-probes', 'r')
		lines = services.read().split('\n')
		services.close()
		hits = []
		query = 'match ' + str(service_name) + ' '
		for line in lines:
			if query in line:
				hits.append(line)
		# if we can, remove any complex regex's
		#hit = hits[1]
		for hit in hits:
			test = hit[len(query):]
			delim = test[1]
			regex = NmapServiceServer.find_between(test, delim, delim)
			if delim+"i" in hit:
				continue
			if delim+"s" in hit:
				continue
			#print("found regex:" + regex, "from hit:"+hit)
			return regex
		return ''

	@staticmethod
	def find_between(s, first, last):
		try:
			start = s.index(first) + len(first)
			end = s.index(last, start)
			return s[start:end]
		except ValueError:
			return ""

	def _genRegexString(self):
		return rstr.xeger(self.expression)

	def _setIPTables(self):
		if self.tcp:
			set_iptable = 'iptables -A OUTPUT -p tcp --tcp-flags RST RST --sport ' + str(self.port) + ' -j DROP'
		elif self.udp:
			set_iptable = 'iptables -I OUTPUT -p icmp --icmp-type destination-unreachable -j DROP'
		if not set_iptable in os.popen('iptables-save').read():
			os.system(set_iptable)

	def _cleanIPTables(self):
		# TODO change to restore iptables
		os.system('iptables -F')
		os.system('iptables -X')

	def _stopFilter(self, packet):
		return self._stopper

	# called as daemon
	def _startService(self):
		self._setIPTables()
		if self.tcp:
			print(tcp_color + 'tcp server starting:', self.ip_addr, ":", self.port, reset_color)
			sniff(filter="tcp[tcpflags] & tcp-syn != 0 and dst host " + self.ip_addr + " and port " + str(self.port),
				  prn=self.answerTCP, iface=self.iface, stop_filter=self._stopFilter)
		elif self.udp:
			#print(udp_color + 'udp server starting:', self.ip_addr, ":", self.port)
			#print(reset_color, end="")
			sniff(filter="udp and dst host " + self.ip_addr + " and port " + str(self.port),
				  prn=self.answerUDP, iface=self.iface, stop_filter=self._stopFilter)
		#print(reset_color + 'sniffing set for '+str(self.port))

		while not self._stopper:
			try:
				time.sleep(.75)
			except KeyboardInterrupt:
				break
			except:
				break
		#print(green + "Server Done for "+str(self.port) + reset_color)

	def answerTCP(self, packet):
		#print(tcp_color + 'New tcp client:')
		#packet.summary()
		#print(reset_color, end="")

		ValueOfPort = packet.sport
		SeqNr = packet.seq
		AckNr = packet.seq+1
		victim_ip = packet['IP'].src

		# send syn ack
		ip = IP(src=self.ip_addr, dst=victim_ip)
		tcp_synack = TCP(sport=self.port, dport=ValueOfPort, flags="SA", seq=SeqNr, ack=AckNr, options=[('MSS', 1460)])
		handshake = ip/tcp_synack
		#print(tcp_color, end="")
		ANSWER = sr1(handshake, timeout=8, verbose=0)
		#print(reset_color, end="")
		if not ANSWER:
			#print(red + "TIMEOUT on syn ack" + reset_color)
			return ""

		# Capture next TCP packet if the client talks first
		#GEThttp = sniff(filter="tcp and src host "+str(victim_ip)+" and port "+str(server_port),count=1)
		#GEThttp = GEThttp[0]
		#AckNr = AckNr+len(GEThttp['Raw'].load)

		# send psh ack (main tcp packet)
		SeqNr += 1
		#payload="HTTP/1.1 200 OK\x0d\x0aDate: Wed, 29 Sep 2010 20:19:05 GMT\x0d\x0aServer: Testserver\x0d\x0aConnection: Keep-Alive\x0d\x0aContent-Type: text/html; charset=UTF-8\x0d\x0aContent-Length: 291\x0d\x0a\x0d\x0a<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\"><html><head><title>Testserver</title></head><body bgcolor=\"black\" text=\"white\" link=\"blue\" vlink=\"purple\" alink=\"red\"><p><font face=\"Courier\" color=\"blue\">-Welcome to test server-------------------------------</font></p></body></html>"
		payload = self._genRegexString()
		tcp_pshack = TCP(sport=self.port, dport=ValueOfPort, flags="PA", seq=SeqNr, ack=AckNr, options=[('MSS', 1460)])
		tcp_main = ip/tcp_pshack/payload
		#print(tcp_color, end="")
		ACKDATA = sr1(tcp_main, timeout=5, verbose=0)
		#print(reset_color, end="")
		if not ACKDATA:
			#print(red + "TIMEOUT on syn ack" + reset_color)
			return ""

		# send fin
		SeqNr = ACKDATA.ack
		tcp_fin_ack = TCP(sport=self.port, dport=ValueOfPort, flags="FA", seq=SeqNr, ack=AckNr, options=[('MSS', 1460)])
		#print(tcp_color, end="")
		send(ip/tcp_fin_ack, verbose=0)
		#print(tcp_color+'tcp client done' + reset_color)
		return ""

	def answerUDP(self, packet):
		#print(udp_color + 'New udp client:')
		packet.summary()
		#print(reset_color, end="")
		ValueOfPort = packet.sport
		victim_ip = packet['IP'].src

		ip = IP(src=self.ip_addr, dst=victim_ip)
		udp = UDP(sport=self.port, dport=ValueOfPort)
		payload = self._genRegexString()
		udp_main = ip/udp/payload
		#print(udp_color, end="")
		send(udp_main)
		#print(udp_color + 'udp client done' + reset_color)
		return ""


def findnth(haystack, needle, n):
	parts = haystack.split(needle, n+1)
	if len(parts) <= n+1:
		return -1
	return len(haystack)-len(parts[-1])-len(needle)


if __name__ == '__main__':
	#'''
	# Nmap Test Suite
	''' batch method
	import paramiko
	i_port = 20000
	resume_port = i_port
	eth = 'eth0'
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect('10.0.0.8', 22, 'root', 'toor')
	time.sleep(3)
	services = open('/usr/share/nmap/nmap-service-probes', 'r')
	lines = services.read().split('\n')
	services.close()
	results_file_good = '/root/nmap2_results_good.txt'
	results_file_bad = '/root/nmap2_results_bad.txt'
	servers = []
	smallest_port = 700000
	largest_port = 0
	for line in lines:
		if not 'match ' in line:
			continue
		if line[0] == '#':
			continue
		test = line[findnth(line, ' ', 1)+1:]
		delim = test[1]
		service_name = NmapServiceServer.find_between(test,' ',' ')
		regex = NmapServiceServer.find_between(test, delim, delim)
		if delim + "i" in line:
			continue
		if delim + "s" in line:
			continue
		#print("test:" + test)
		#print("delim:" + delim)
		#print("regex:" + regex)
		#print("line:" + line)
		#try:
		server = NmapServiceServer(i_port, eth, expression=regex, service_name=service_name, line=line, regex=regex)
		server.start()
		servers.append(server)
		if i_port < smallest_port:
			smallest_port = i_port
		if i_port > largest_port:
			largest_port = i_port
		i_port += 1

		if len(servers) >= 500:
			print('wait for threads to catch up')
			time.sleep(15) #wait for servers to start
			command = "nmap 10.0.0.9 -T5 -sV --version-all -p " + str(smallest_port) + "-"+\
					  str(largest_port)+" -oN /root/nmap_test2/" + str(smallest_port) + "_"+\
					  str(largest_port) + ".txt"
			print(command, "... make take a while...")
			stdin, stdout, stderr = ssh.exec_command(command)
			results = stdout.read()
			results = results.decode('utf-8')
			print('nmap done')
			for server in servers:
				for line in results.split('\n'):
					if str(server.port)+"/tcp " in line:
						if "?" in line:
							w = open(results_file_bad, 'a+')
							w.write(str(server.port) + ",,,unrecognized,,,"+ server.service_name +
									",,," + server.line + ",,," + server.regex + "\n")
							w.close()
						elif str(server.port)+"/tcp closed" in results:
							w = open(results_file_bad, 'a+')
							w.write(str(server.port) + ",,,closed,,," + server.service_name +
									",,," + server.line + ",,," + server.regex + "\n")
							w.close()
						elif 'tcpwrapped' in results:
							w = open(results_file_bad, 'a+')
							w.write(str(server.port) + ",,,tcpwrapped,,," + server.service_name +
									",,," + server.line + ",,," + server.regex + "\n")
							w.close()
						else:
							w = open(results_file_good, 'a+')
							w.write(str(server.port) + ",,,good,,," + server.service_name +
									",,," + server.line + ",,," + server.regex + "\n")
							w.close()
				server.stop()
			servers.clear()

			smallest_port = 700000
			largest_port = 0
			print('wait for threads to die')
			time.sleep(30)
			print('next round...')
		#except Exception as e:
		#	print(e)
		#	w = open('/root/nmap2_err.txt', 'a+')
		#	w.write(str(i_port) + "," + str(e) + "," + line + ",,," + regex + "\n")
		#	w.close()

	print(green + "Done Done " +str(len(servers))+ reset_color)
	while 1:
		try:
			time.sleep(1)
		except Exception:
			break
	for s in servers:
		s.close()
	'''


	''' slow way
	# Nmap Test Suite
	import paramiko
	i_port = 20000
	resume_port = i_port
	eth = 'eth0'
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect('10.0.0.8', 22, 'root', 'toor')
	time.sleep(3)
	services = open('/usr/share/nmap/nmap-service-probes', 'r')
	lines = services.read().split('\n')
	services.close()
	results_file_good = '/root/nmap_results_good.txt'
	results_file_bad = '/root/nmap_results_bad.txt'
	for line in lines:
		if not 'match ' in line:
			continue
		test = line[findnth(line, ' ', 1)+1:]
		delim = test[1]
		regex = NmapServiceServer.find_between(test, delim, delim)
		if delim + "i" in line:
			continue
		if delim + "s" in line:
			continue
		#print("test:" + test)
		#print("delim:" + delim)
		#print("regex:" + regex)
		#print("line:" + line)
		try:
			server = NmapServiceServer(i_port, eth, expression=regex)
			server.start()
			time.sleep(1.5)
			if i_port < resume_port:
				i_port += 1
				server.stop()
				time.sleep(2)
				continue
			command = "nmap 10.0.0.9 -T5 -sV --version-all -p "+str(i_port)+" -oN /root/nmap_test/"+str(i_port)+".txt"
			print(command)
			stdin,stdout,stderr = ssh.exec_command(command)
			results = stdout.read()
			results = results.decode('utf-8')
			server.stop()
			dst = ""
			if 'unrecognized despite returning data' in results:
				w = open(results_file_bad, 'a+')
				w.write(str(i_port)+",unrecognized,"+line+",,,"+regex+"\n")
				w.close()
				dst = 'unrecognized'
			elif 'tcp closed' in results:
				w = open(results_file_bad, 'a+')
				w.write(str(i_port)+",closed,"+line+",,,"+regex+"\n")
				w.close()
				dst = 'closed'
			elif 'tcpwrapped' in results:
				w = open(results_file_bad, 'a+')
				w.write(str(i_port)+",tcpwrapped,"+line+",,,"+regex+"\n")
				w.close()
				dst = 'tcpwrapped'
			else:
				w = open(results_file_good, 'a+')
				w.write(str(i_port)+","+line+",,,"+regex+"\n")
				w.close()
				dst = 'good'
			print('result was '+dst)
			stdin, stdout, stderr = ssh.exec_command("cp /root/nmap_test/" + str(i_port) + ".txt /root/nmap_test/" + dst)
			stdout.read()
			i_port += 1
			time.sleep(2)
		except Exception as e:
			print(e)
			w = open('/root/nmap_err.txt', 'a+')
			w.write(str(i_port) + ","+str(e)+"," + line + ",,," + regex + "\n")
			w.close()

	print(green + "Done Done" + reset_color)
	'''



	#'''
	#'''
	# Start "servers"
	#udp_expression = r'^2;http://[\d.]+:\d+/;[\d.]+;\d+:\d+;\w+,[\d.]+,PLUGIN_LOADED'  # r'^ok$'  #r'^BUSY$'
	#tcp_expression = r'^ok$'
	servers = [NmapServiceServer(80, 'eth0', expression=r'^ok$'),
			   NmapServiceServer(8000, 'eth0', expression=r'^2;http://[\d.]+:\d+/;[\d.]+;\d+:\d+;\w+,[\d.]+,PLUGIN_LOADED', tcp=False),
			   NmapServiceServer(1000, 'eth0', expression=r'^S\xf5\xc6\x1a{'), #r'^HELP\r\n$'), #expression=r'^BUSY$'),
			   NmapServiceServer(1001, 'eth0', service_name='1c-server ')]
	for server in servers:
		server.start()
	print(reset_color+'Servers started')

	# Wait till killed
	while 1:
		try:
			time.sleep(1)
		except KeyboardInterrupt:
			break
		except:
			break
	for server in servers:
		server.stop()
	#TODO clean iptables - not super important for RST though on high ports
	print(green + "Done Done" + reset_color)
	#'''

'''
NOTES
- If nmap flags as tcpwrapped service, its likely you are not responding (or responding incorrectly) after handshake.  E.g. bad ack or seq #
- If nmap does not recognize the service, you may need to set --version-intensity 9  or --version-all   (default is 7)
- Nmap skips ports 9100-9107 for -sV scan, even upon adding "-p 9100".  Use --allports  to bypass this.  
- Note, not all services will work due to the limitations of rstr.xeger and nmaps usage of perl's 'i' and 's' options.  
  In general, dynamically generating string that fit regex is a hard problem
- Nmap -O (OS scan) and -sU (UDP scan) options require root (at least on Android's Termux).
- The -sV option will not send UDP packet at all unless -sU is specified. Jeez nmap, letting me down here xD


LINKS
- Scapy send vs sendp  http://abunchofbaloney.blogspot.com/2014/09/scapy-send-vs-sendp.html\
- Nmap version options   https://nmap.org/book/man-version-detection.html
- Nmap service detction file format  https://nmap.org/book/vscan-fileformat.html#vscan-fileformat-example
- Nmap os dection workings  https://nmap.org/book/osdetect-methods.html
- Linux routing  https://www.cyberciti.biz/faq/linux-route-add/
- BPF syntax http://biot.com/capstats/bpf.html
'''

