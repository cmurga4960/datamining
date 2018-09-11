# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 14:42:32 2017

@author: the4960

"""

import datetime
from dateutil.relativedelta import relativedelta
import requests
import time
from random import randint

alaska='https://www.wunderground.com/history/airport/PAMR/2006/1/7/DailyHistory.html?req_city=Anchorage&req_state=AK&req_statename=&reqdb.zip=99501&reqdb.magic=1&reqdb.wmo=99999'
ny='https://www.wunderground.com/history/airport/KNYC/2006/1/7/DailyHistory.html?req_city=New+York&req_state=NY&req_statename=&reqdb.zip=10001&reqdb.magic=1&reqdb.wmo=99999'
australia = "https://www.wunderground.com/history/airport/YSSY/2006/1/7/DailyHistory.html?req_city=Sydney&req_statename=Australia&reqdb.zip=00000&reqdb.magic=16&reqdb.wmo=94768"
org_url = "https://www.wunderground.com/history/airport/KELP/1942/1/1/DailyHistory.html?req_city=&req_state=&req_statename=&reqdb.zip=&reqdb.magic=&reqdb.wmo="

url1 ="https://www.wunderground.com/history/airport/PAMR/"  #"https://www.wunderground.com/history/airport/KELP/"
url2 ="DailyHistory.html?req_city=Anchorage&req_state=AK&req_statename=&reqdb.zip=99501&reqdb.magic=1&reqdb.wmo=99999"  #"DailyHistory.html?req_city=&req_state=&req_statename=&reqdb.zip=&reqdb.magic=&reqdb.wmo="
path = "C:\\Users\\the4960\\.spyder2\\WundergroundTemp\\"
final_out = path+"AK_temp_data_7days_part1.csv"

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""
        
        
def getTemp(date_index):
    url = url1+str(date_index.year)+"/"+str(date_index.month)+"/"+str(date_index.day)+"/"+url2
    try:
        response = requests.get(url)
    except:
        print('EERRRRRRRRRRORRRRR:',date_index,url)
        return
    if response.status_code != 200:
        print 'GOT ! 200'
        print date_index
        return
    #NO ERRORS...
    record  = [0,0,0]
    index = 0
    getting_val = False
    for line in response.content.split('\n'):
        getting_val = '<td class="indent"><span>Mean Temperature</span></td>' in line or '<td class="indent"><span>Max Temperature</span></td>' in line or '<td class="indent"><span>Min Temperature</span></td>' in line or getting_val
        if getting_val:
            if '<span class="wx-data"><span class="wx-value">' in line:
                val = find_between(line,'<span class="wx-data"><span class="wx-value">','</span><span class="wx-unit">')
                record[index] = int(val)
                index += 1
                getting_val = False
                if index == 3:
                    break
        
    output = open(final_out,'a')
    output.write(str(date_index)+","+str(record[0])+","+str(record[1])+","+str(record[2])+"\n")
    output.close()
        
date_start = datetime.date(1946,04,07)#1942
date_end =  datetime.date(2006,01,07)#datetime.date.today() - datetime.timedelta(days=1)
while(date_start < date_end):
    print(date_start)
    getTemp(date_start)
    date_start = date_start + datetime.timedelta(days=7)
    time.sleep(randint(0,1))

print("DONE DONE DONE DONE")