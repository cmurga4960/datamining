# -*- coding: utf-8 -*-
"""
Created on Sun Jan 29 19:44:18 2017

@author: the4960
Downloads geometry art from http://geometrydaily.tumblr.com/
"""
import requests
import urllib
import urllib.request
print('running...')
def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

max = 38
posts = []
for page in range(1,max+1):
    url = "https://geometrydaily.tumblr.com/page/"+str(page)
    response = requests.get(url)
    if response.status_code != 200:
        print ('GOT ! 200')
        break
    content = str(response.content)[1:-1]
    for line in content.split('\n'):
        if 'href="' in line:
            splitter = line.split('href="')
            for elem in splitter:
                if ('>' in elem) and 'https://geometrydaily.tumblr.com/' in elem:
                    elem = elem[:elem.index('">')]
                    print(elem)
                    if elem.index('https://geometrydaily.tumblr.com/') == 0 and '/post/' in elem:
                        posts.append(elem)
    
for page in posts:
    response = requests.get(page)
    if response.status_code != 200:
        print ('GOT ! 200')
        break
    for line in str(response.content)[1:-1].split('\n'):
        if '<div class="index"><div class="detail">' in line:
            splitter = line.split('<div class="index"><div class="detail">')
            elem = find_between( splitter[1],'src="','" style=')
            name = elem.split("/")[-1]
            print(elem+"\n")
            urllib.request.urlretrieve(elem, "geom/"+name)
            
            #urllib.urlretrieve(elem, "geom/"+name)
    
print("END END END END")
