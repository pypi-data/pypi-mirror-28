# coding: utf-8

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import pandas as pd
import os
from time import time, ctime
import requests

# import recur7down
from multiprocessing.dummy import Pool as ThreadPool


ct = ctime().split()
folder= ct[2]+ct[1]+ct[-1]+'_htmls_diary/'
from info import diary_link

try:
    os.mkdir(folder)
except:
    print 'exists'
    
    
def getsingle(ID):
    global fail, n
    n+=1
    if n%5000==0 or n==1:
        print ctime(), 'of ', n, 'failed', len(fail)
    try:
        one=requests.get(diary_link.format(ID))
    except:
#         print 'X',
        fail.append(ID)
    with open(folder+'{}.html'.format(ID), 'w+') as fl:
        fl.write(one.text)
#     print 'O',
    



def batch(allnames):
    global n
    n=0
    start=time()

    pool = ThreadPool(cpu)
    
    results = pool.map(getsingle, allnames)
    
    pool.close()
    pool.join()
    
    end = time()
    elapse = end - start 
    now=ctime()[4:]

    print 'diary ',len(allnames),'  used ',elapse,'s', now

    
def html_main():

    try:
        sys.path.append(os.getcwd())
        from info import diary_link
        print 'imported data from info'
        sys.path.remove(os.getcwd())

    except:
        print 'lack of info.py'
        exit(0)        
    
    
    n=0
    fail=[]
    cpu = int(raw_input('(multi-processing) how many process to run ? '))
    
    try:
        f=pd.read_csv('diary_html_fail.csv')
        print 'fail exists'
        if f.shape[0]>20:
            fail=[]
            batch(f.values)
            os.remove('diary_html_fail.csv')
            print 'Done!'
            print 1
            exit()
            # pd.DataFrame(fail, columns=['username']).to_csv('fail.csv',index=False)
            
        else:
            print 'Scrape Success!!!'
            print len(os.listdir(folder))
            os.remove('diary_html_fail.csv')
            print 2
            exit()
        
    except:
        print 3
        print 'fail not exists'
        
        df=pd.read_csv('diary_all.csv', usecols=['group_id'])
        print 'start scraping', ctime()
        print len(df['group_id'].unique()), df.shape

        all_ids=df['group_id'].tolist()

        print len(all_ids)

        fail=[]
        batch(all_ids)
            
    if len(fail)>-1:
        
        pd.DataFrame(fail, columns=['group_id']).to_csv('diary_html_fail.csv',index=False)
    else:
        print 'done!', ctime()
