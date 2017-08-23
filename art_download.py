# -*- coding: utf-8 -*-
"""
Created on Tue Aug 22 20:46:31 2017

@author: the4960
Input last name of an artist to download their art.  Utilizes http://www.wga.hu/
"""
import requests
import sys
import urllib
import os

base_url = "http://www.wga.hu/art/"

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def getArtistDirUrl(artist_last_name):
    artist_last_name =  artist_last_name.lower()
    letter = (artist_last_name.strip())[0]
    return base_url+letter+"/"+artist_last_name+"/"

                
def download(artist_last_name,img_url,name):
    if not os.path.exists(artist_last_name):
        os.makedirs(artist_last_name)
    urllib.urlretrieve(img_url, artist_last_name+"/"+name)
    print(img_url)

def downloadArt(artist_last_name):
    url = getArtistDirUrl(artist_last_name)
    try:
        response = requests.get(url)
    except:
        print('EERRRRRRRRRRORRRRR:',artist_last_name,url)
    if response.status_code != 200:
        print 'GOT ! 200'
        sys.exit()
    harvesting = False
    for line in response.content.split("\n"):
        harvesting = '<tbody>' in line or harvesting
        if harvesting:
            target_url = find_between(line,'<a href="','">')
            if target_url and not ('../' in target_url):
                if 'class="t">Directory' in line:
                    print('Found a dir')
                    downloadArt(artist_last_name+"/"+(target_url[:-1]))
                else:
                    if '.png' in target_url or '.jpg' in target_url or '.jpeg' in target_url:
                        download(artist_last_name,url+target_url,target_url)
            elif '</tbody>' in line:
                print("DONE w/ dir "+artist_last_name)
                return
    print("DONE w/ dir "+artist_last_name)
            
downloadArt("maella")