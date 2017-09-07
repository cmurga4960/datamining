# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 22:16:27 2017

@author: the4960

get info on UTEP library
"""
from mpi4py import MPI
import time
import os
import requests
import random


def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def getPage(page,output,rank):
    url = 'http://encore.utep.edu/iii/encore/search/C__S*__Ff%3Afacetmediatype%3Aa%3Aa%3ABOOK%3A%3A__P'+str(page)+'__Orightresult?lang=eng&suite=cobalt'
    response = requests.get(url)
    hit=0
    my_line=""
    for line in response:
        find_title='<!-- please read c1063106, c1063117, c1044421, c1060576a before changing title -->'
        if find_title in line:
            hit=1
        elif hit==1:
            my_line+=line
            if '</a>' in my_line:
                output.write(str(page)+","+find_between(my_line,'>','</a>').strip()+'\n')
                hit=0
                my_line=""
    
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
nprocs = comm.Get_size()
if not os.path.exists('library/'):
    os.makedirs('library/')

for i in range(rank,1723884/25,nprocs):
    print(str(i)+","+str(rank))
    output = open('library/library'+str(rank)+'.csv','a')
    getPage(i,output,rank)
    output.close()
    time.sleep(random.randint(1,5))
