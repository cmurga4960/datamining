# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 00:19:12 2017

@author: the4960
get more than 100 images from google
http://stackoverflow.com/questions/20716842/python-download-images-from-google-image-search
"""

from bs4 import BeautifulSoup
import urllib2
import os
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import sys

max_scroll = 2500

def pageContent(url):
    driver = webdriver.Firefox()
    driver.get(url)
    for _ in range(max_scroll):#increase # to get more content
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    return driver.page_source.encode("utf-8")

def get_soup(url,header):
    return BeautifulSoup(pageContent(url),'html.parser')


query = raw_input("Enter query:")# you can change the query for the image  here
image_type="ActiOn"
query= query.split()
query='+'.join(query)
url="https://www.google.co.in/search?q="+query+"&source=lnms&tbm=isch"
print url
#add the directory for your image here
DIR="Pictures"
header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
}
soup = get_soup(url,header)


ActualImages=[]# contains the link for Large original images, type of  image
for a in soup.find_all("div",{"class":"rg_meta"}):
    link , Type =json.loads(a.text)["ou"]  ,json.loads(a.text)["ity"]
    ActualImages.append((link,Type))

print  "there are total" , len(ActualImages),"images"

if not os.path.exists(DIR):
            os.mkdir(DIR)
DIR = os.path.join(DIR, query.split()[0])

if not os.path.exists(DIR):
            os.mkdir(DIR)
###print images
for i , (img , Type) in enumerate( ActualImages):
    try:
        req = urllib2.Request(img, headers={'User-Agent' : header})
        raw_img = urllib2.urlopen(req).read()
        cntr = len([i for i in os.listdir(DIR) if image_type in i]) + 1        
        print cntr
        if len(Type)==0:
            f = open(os.path.join(DIR , image_type + "_"+ str(cntr)+".jpg"), 'wb')
        else :
            f = open(os.path.join(DIR , image_type + "_"+ str(cntr)+"."+Type), 'wb')


        f.write(raw_img)
        f.close()
    except Exception as e:
        print "could not load : "+img
        print e