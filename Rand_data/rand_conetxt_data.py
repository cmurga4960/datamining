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
MAX_DEPTH = 2
queried_geo ={}

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def getRandomContext():
    #word_site = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"
    #response = requests.get(word_site)
    #WORDS = response.content.splitlines()
    WORDS = open('dictionary.txt','r').read().split('\n')
    word = WORDS[randint(0, len(WORDS))]
    return word
    
def getLabels():
    labels={}
    for i in G.node:
        print i
        labels[i]=i
    return labels
    
def oldgetLabels():
    labels={}
    for i in G.node:
        domain=''
        if 'https://google.com/url?q=' in i:
            site = find_between(i,'https://google.com/url?q=','&usg=')
            parsed_uri = urlparse( site )
            domain = '{uri.netloc}'.format(uri=parsed_uri)
        elif 'https://google.com/' in i:
            domain='google.com'
        else:
            parsed_uri = urlparse( i )
            domain = '{uri.netloc}'.format(uri=parsed_uri)
        print domain
        labels[i]=domain
    return labels
    
def makePicture():
    pos_map = nx.spring_layout(G)
    scale=500000*MAX_DEPTH
    for p in pos_map:
        r=random.uniform(.5, 1)
        pos_map[p]=pos_map[p]*scale
        pos_map[p]=[pos_map[p][0],pos_map[p][1]*scale*r]
    
    fig = plt.gcf()
    fig.set_size_inches(100, 20)
    nx.draw_networkx(G,pos=pos_map,labels=getLabels(),arrows=True,font_color='blue',linewidth=.1)
    
    plt.axis('off')
    plt.title('Spidering: '+context+' w/ depth: '+str(MAX_DEPTH))
    plt.savefig(context+"_path.png")
    plt.show() # display

def urlToGeo(url):
    parsed_uri = urlparse( url )
    url = '{uri.netloc}'.format(uri=parsed_uri)
    if url.startswith('www.'):
        url = url[4:]
    if url in queried_geo:
        return queried_geo[url]
    try:
        response = requests.get('https://tools.keycdn.com/geo.json?host='+url)
    except:
        print('EERRRRRRRRRRORRRRR geo:',url)
    if response.status_code != 200:
        print 'GOT ! 200 geo',url
        return '0','0'
    lat = find_between(response.content,'latitude":"','"')
    log = find_between(response.content,'longitude":"','"')
    if lat =='' or log =='':
        lat = '0'
        log = '0'
    queried_geo[url]=(lat,log)
    print('Adding:',url,lat,log)
    return lat,log

def makeJSON():
    output = open('test.json','w')
    for e in G.edges():
        geo1 = urlToGeo(e[0])
        geo2 = urlToGeo(e[1])
        output.write(','+'{origin: {latitude: '+geo1[0]+',longitude: '+geo1[1]+'},destination: {latitude: '+geo2[0]+',longitude: '+geo2[1]+'}}\n')
    output.close()

def googleIt(query):
    print query
    url = google_url+query
    try:
        response = requests.get(url)
    except:
        print('EERRRRRRRRRRORRRRR:',query,url)
    if response.status_code != 200:
        print 'GOT ! 200',query
        return
    #NO ERRORS...
    G.add_node(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    for a in soup.find_all('a'):
        if '/url?' in str(a['href']) and 'googleusercontent' not in str(a['href']) :
            link = 'https://google.com'+a['href']
            link = find_between(link,'https://google.com/url?q=','&sa=')
            G.add_node(link)
            G.add_edge(url,link,weight=1)
            spider(link,MAX_DEPTH)
            
def spider(url,depth_to_go):
    if(depth_to_go==0):
        return
    print('SPIDERING:',url,depth_to_go)
    try:
        response = requests.get(url)
    except:
        print('EERRRRRRRRRRORRRRR:',url)
        return
    if response.status_code != 200:
        print 'GOT ! 200',url
        return
    #NO ERRORS...
    parsed_uri = urlparse( url )
    url_domain = '{uri.netloc}'.format(uri=parsed_uri)
    soup = BeautifulSoup(response.content, 'html.parser')
    for a in soup.find_all('a'):
        try:
            if 'http' in str(a['href']):
                link = str(a['href'])
                parsed_uri = urlparse( link )
                link_domain = '{uri.netloc}'.format(uri=parsed_uri)
                G.add_node(link_domain)#TODO should i simplifie this to jsut the domain? would cut down on data... and save time
                G.add_edge(url_domain,link_domain,weight=depth_to_go+5)
                spider(link,depth_to_go-1)
        except:
            a=1

context = getRandomContext()
G=nx.DiGraph(subject=context)
googleIt(context)
makeJSON()
print'DONE DONE DONE DONE'
print'DONE DONE DONE DONE'
print'DONE DONE DONE DONE'
print context
