# -*- coding: utf-8 -*-
"""
Created on Fri Aug 25 18:59:00 2017

@author: the4960
random context data
"""

from bs4 import BeautifulSoup
from random import randint
import requests
from urlparse import urlparse

google_url = "https://google.com/search?q="
output = 'contexts/'
MAX_DEPTH = 4
data ={}
blacklist = open('blacklist.txt','r').read().split('\n')
eval_list = {} #TODO eval_list['domain'] = (out_count,in_count) #use this ratio to blacklist

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def outputCSV():
    outputCSVHelper(data)

def outputCSVHelper(dictionary):
    for i in dictionary:
        if dictionary[i] == {}:
            csv.write(i+',4\n')
        else:
            csv.write(i+',\n')
            outputCSVHelper(dictionary[i])
            
def inBlackList(domain):
    if domain.startswith('www.'):
        domain=domain[4:]
    for i in blacklist:
        if i in domain or domain in i:
            return True
    return False
        
def getRandomContext():
    WORDS = open('dictionary.txt','r').read().split('\n')
    word = (WORDS[randint(0, len(WORDS))])
    return word  

def googleIt(query):
    print query
    url = google_url+query
    try:
        response = requests.get(url)
    except:
        print('EERRRRRRRRRRORRRRR:',query,url)
    if response.status_code != 200:
        print 'GOT ! 200'
        print query
        return
    #NO ERRORS...
    google_key = (google_url+context).replace('.',';')
    data[google_key]={}
    url = url.replace('.',';').replace(',','~')
    soup = BeautifulSoup(response.content, 'html.parser')
    for a in soup.find_all('a'):
        if '/url?' in str(a['href']) and 'googleusercontent' not in str(a['href']) :
            link = 'https://google.com'+a['href']
            link = find_between(link,'https://google.com/url?q=','&sa=')
            parsed_uri = urlparse(link)
            link_domain = '{uri.netloc}'.format(uri=parsed_uri)
            if inBlackList(link_domain):
                continue
            path = url+'.'+link_domain.replace('.',';').replace(',','~')
            data[google_key][path] = spider(link,1,path)
            
def spider(url,current_depth,path):
    dic={}
    current_depth = path.count('.')
    if(current_depth>=MAX_DEPTH):
        return {}
    print('SPIDERING:',url,current_depth)
    try:
        response = requests.get(url)
    except:
        print('EERRRRRRRRRRORRRRR:',url)
        return dic
    if response.status_code != 200:
        print 'GOT ! 200',url
        return dic
    #NO ERRORS...
    soup = BeautifulSoup(response.content, 'html.parser')
    for a in soup.find_all('a'):
        try:
            if 'http' in str(a['href']):
                link = str(a['href'])
                parsed_uri = urlparse(link)
                link_domain = '{uri.netloc}'.format(uri=parsed_uri)
                if inBlackList(link_domain) or '.exe' in link or '.pdf' in link:
                    continue
                new_path = path+'.'+link_domain.replace('.',';').replace(',','~')
                dic[new_path] = spider(link,current_depth+1,new_path)
                #dic[new_path] = spider(link,current_depth+1,new_path)
        except:
            a=1
    return dic

context = getRandomContext()
csv = open('csvs/'+context+'_spider'+str(MAX_DEPTH)+'.csv','w')
csv.write('id,value\n')
googleIt(context)
outputCSV()
csv.close()

print'DONE DONE DONE DONE'
print'DONE DONE DONE DONE'
print'DONE DONE DONE DONE'
print'DONE DONE DONE DONE'
print'DONE DONE DONE DONE'
print context
