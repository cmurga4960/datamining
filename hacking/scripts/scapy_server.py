from scapy.all import *
import rstr
import netifaces as ni
import os

# Interacts with a client by going through the three-way handshake.
# Shuts down the connection immediately after the connection has been established.
# Akaljed Dec 2010, https://akaljed.wordpress.com/2010/12/12/scapy-as-webserver/

# Use expression from /usr/share/nmap/nmap-service-probes
'''
# NoMachine Network Server
# Announce client version 5.6.7 (could be anything)
Probe TCP NoMachine q|NXSH-5.6.7\n|
ports 4000
rarity 9

match nomachine-nx m|^NXD-([\d.]+)\n| p/NoMachine NX Server remote desktop/ v/$1/ cpe:/a:nomachine:nx_server:$1/
'''

#CUSTOMIZE ME
iface = 'eth0'
server_port = 3000
expression = r'^NXD-([\d.]+)\n'
#CUSTOMIZE ME

ni.ifaddresses(iface)
ip_addr = ni.ifaddresses(iface)[ni.AF_INET][0]['addr']
set_iptable = 'iptables -A OUTPUT -p tcp --tcp-flags RST RST --sport '+str(server_port)+' -j DROP'
os.system(set_iptable)

def answerTCP(packet):
	print('New client:')
	packet.summary()

	ValueOfPort = packet.sport
	SeqNr = packet.seq
	AckNr = packet.seq+1
	victim_ip = packet['IP'].src
	
	# send syn ack
	ip=IP(src=ip_addr, dst=victim_ip)
	TCP_SYNACK=TCP(sport=server_port, dport=ValueOfPort, flags="SA", seq=SeqNr, ack=AckNr, options=[('MSS', 1460)])
	synack = ip/TCP_SYNACK
	ANSWER=sr1(synack)

	# Capture next TCP packet if the client talks first
	#GEThttp = sniff(filter="tcp and src host "+str(victim_ip)+" and port "+str(server_port),count=1)
	#GEThttp = GEThttp[0]
	#AckNr = AckNr+len(GEThttp['Raw'].load)
	
	# send psh ack
	SeqNr += 1
	#payload="HTTP/1.1 200 OK\x0d\x0aDate: Wed, 29 Sep 2010 20:19:05 GMT\x0d\x0aServer: Testserver\x0d\x0aConnection: Keep-Alive\x0d\x0aContent-Type: text/html; charset=UTF-8\x0d\x0aContent-Length: 291\x0d\x0a\x0d\x0a<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\"><html><head><title>Testserver</title></head><body bgcolor=\"black\" text=\"white\" link=\"blue\" vlink=\"purple\" alink=\"red\"><p><font face=\"Courier\" color=\"blue\">-Welcome to test server-------------------------------</font></p></body></html>"
	payload = str(rstr.xeger(expression))	
	data1=TCP(sport=server_port, dport=ValueOfPort, flags="PA", seq=SeqNr, ack=AckNr, options=[('MSS', 1460)])
	http_reply = ip/data1/payload
	ackdata1=sr1(http_reply)
	
	# send fin
	SeqNr=ackdata1.ack
	Bye=TCP(sport=server_port, dport=ValueOfPort, flags="FA", seq=SeqNr, ack=AckNr, options=[('MSS', 1460)])
	send(ip/Bye)
	print('client done')
	return ""

print('tcp server starting:', ip_addr,":",server_port)
sniff(filter="tcp[tcpflags] & tcp-syn != 0 and dst host "+ip_addr+" and port "+str(server_port), prn=answerTCP)

