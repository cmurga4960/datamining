# -*- coding: utf-8 -*-
"""
Created on Fri Aug 25 18:59:00 2017

@author: the4960
random context data
"""

from bs4 import BeautifulSoup
from random import randint
import requests
import random
import networkx as nx
import matplotlib.pyplot as plt
from urlparse import urlparse

google_url = "https://google.com/search?q="
output = 'contexts/'
MAX_DEPTH = 3
def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""
        
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
    soup = BeautifulSoup(response.content, 'html.parser')
    for a in soup.find_all('a'):
        if '/url?' in str(a['href']) and 'googleusercontent' not in str(a['href']) :
            link = 'https://google.com'+a['href']
            link = find_between(link,'https://google.com/url?q=','&sa=')
            path = url.replace('.',';')+'.'+link.replace('.',';')
            csv.write(path+',\n')
            print path
            spider(link,1,path)
            
def spider(url,current_depth,path):
    current_depth = path.count('.')
    if(current_depth>=MAX_DEPTH):
        return
    print('SPIDERING:',url,current_depth)
    try:
        response = requests.get(url)
    except:
        print('EERRRRRRRRRRORRRRR:',url)
        return
    if response.status_code != 200:
        print 'GOT ! 200',url
        return
    #NO ERRORS...
    soup = BeautifulSoup(response.content, 'html.parser')
    for a in soup.find_all('a'):
        try:
            if 'http' in str(a['href']):
                link = str(a['href'])
                new_path = path+'.'+link.replace('.',';')
                if(current_depth+1 >= MAX_DEPTH):
                    csv.write(new_path+',7\n')
                else:
                    csv.write(new_path+',\n')
                spider(link,current_depth+1,new_path)
        except:
            a=1

context = getRandomContext()
csv = open(context+'_spider'+str(MAX_DEPTH)+'.csv','w')
csv.write('id,value\n')
csv.write((google_url+context).replace('.',';')+'\n')
googleIt(context)
csv.close()

print'DONE DONE DONE DONE'
print'DONE DONE DONE DONE'
print'DONE DONE DONE DONE'
print'DONE DONE DONE DONE'
print'DONE DONE DONE DONE'
print context
