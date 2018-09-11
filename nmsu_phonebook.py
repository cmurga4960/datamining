# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 18:18:44 2017

@author: the4960
"""

import requests
import time
#https://adminapps.utep.edu/campusdirectory/People/All


def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

#https://adminapps.utep.edu/campusdirectory/People/All
#epcc http://www.epcc.edu/Search/Directory/Pages/default.aspx


#left off at 385


output = open('nmsu_phonebook.txt','w')
page = 1
while page <= 908:
    time.sleep(2)
    url = "https://myaccount.nmsu.edu/phonebook?txtFirstName=%2A%2A&txtLastName=&txtEmail=&chkStudents=Students&chkEmployees=Employees&p="+str(page)
    print (url)
    response = requests.get(url)
    if response.status_code != 200:
        print 'GOT ! 200'
        break
    for line in response.content.split('\n'):
        if 'class="detailsLeft"' in line:
            try:
                phone,address,location = find_between(line, 'class="detailsLeft">','</div>').split("<br />")
                output.write(phone+";"+address+";"+location+"\n")
            except:
                a=0
    page = page + 1
output.close()
print 'END'