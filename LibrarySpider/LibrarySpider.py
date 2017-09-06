# -*- coding: utf-8 -*-
"""
Created on Wed Sep 06 15:34:49 2017

@author: the4960

LibrarySpider
Gets plaintext book links from https://openlibrary.org
"""

from bs4 import BeautifulSoup
import requests
import time

page = 1
max_page = 3000
search = 'a'
url0='https://openlibrary.org'
url1= url0+'/search?q='
url2='&has_fulltext=true&page='
url3='&mode=ebooks'
  
def queryBook(book_url):
    try:
        response = requests.get(book_url)
        time.sleep(.5)
    except:
        print('EERRRRRRRRRRORRRRR:',book_url)
        return
    if response.status_code != 200:
        print 'GOT ! 200',book_url
        return
    #NO ERRORS...
    #<a href="//archive.org/download/cu31924026485809/cu31924026485809_djvu.txt" title="Download a plain text version">Plain text</a>
    soup = BeautifulSoup(response.content, 'html.parser')
    versions = soup.find_all('a',{'title':'Download a plain text version'})
    for book in versions:
        link = str(book['href'][2:])
        print 'GOT BOOK:',link
        book_list = open('book_list.txt','a')
        book_list.write(link+'\n')
        book_list.close()
        return
    
def queryPage():
    url = url1+search+url2+str(page)+url3
    try:
        response = requests.get(url)
        time.sleep(.5)
    except:
        print('EERRRRRRRRRRORRRRR:',url)
        return
    if response.status_code != 200:
        print 'GOT ! 200',url
        return
    #NO ERRORS...
    #eg <a itemprop="name" href="/works/OL20890W/Silas_Marner" class="results">Silas Marner: the weaver of Raveloe</a>
    soup = BeautifulSoup(response.content, 'html.parser')
    book_pages = soup.find_all('a',{'itemprop':'name','class':'results'})
    for book_url in book_pages:
        try:
            queryBook(url0+str(book_url['href']))
        except:
            continue
    return


#resume
try:
    book_list = open('book_list.txt','r')
    page = book_list.split('\n').count('')+1
    book_list.close()
except:
    a=1
#query loop
while page < max_page:
    queryPage()
    page = page+1
    book_list = open('book_list.txt','a')
    book_list.write('\n')
    book_list.close()