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

#a=27246 
#e=24014 
#i=20495 
#o=18297 
#u=9135
#y=4860


#293 people left e.e
#https://adminapps.utep.edu/campusdirectory/People/All
#epcc http://www.epcc.edu/Search/Directory/Pages/default.aspx

output = open('all_usernames_y.txt','w')
letter = ord('y')
print chr(letter)
base_url = "https://myaccount.nmsu.edu/phonebook?txtFirstName=%2A%2A&txtLastName=&txtEmail=&chkStudents=Students&chkEmployees=Employees&p="
page = 1
while page <= 27235:
    time.sleep(2)
    url = "https://myaccount.nmsu.edu/phonebook?txtFirstName=%2A%2A&txtLastName=&txtEmail=&chkStudents=Students&chkEmployees=Employees&p="+str(page)
    
    print ('https://adminapps.utep.edu/campusdirectory/People/All/'+str(page)+'?queryString='+chr(letter)+'#results')
    response = requests.get('https://adminapps.utep.edu/campusdirectory/People/All/'+str(page)+'?queryString='+chr(letter)+'#results')
    if response.status_code != 200:
        print 'GOT ! 200'
        break
    for line in response.content.split('\n'):
        if 'mailto' in line:
            output.write(find_between(line, '">','</a>')+'\n')
    page = page + 10
output.close()
print 'END'