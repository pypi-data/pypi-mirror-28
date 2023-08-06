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

fail=[]
n=0
cpu=24


ct = ctime().split()
folder= ct[2]+ct[1]+ct[-1]+'_htmls_diary/'

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
        one=requests.get(diary_link.format(ID), timeout=10)
        if one.status_code==200:
        
            with open(folder+'{}.html'.format(ID), 'w+') as fl:

                fl.write(one.text)
    #     print 'O',        
        else:
            print 'X:',one.status_code,
            
    except:
#         print 'X',
        try:
            getsingle(ID)
        
        except:
            try:
                getsingle(ID)
            except:
                fail.append(ID)
                
        
        
        

    



def batch(all_IDs):
    global n
    n=0
    start=time()

    pool = ThreadPool(cpu)
    
    results = pool.map(getsingle, all_IDs)
    
    pool.close()
    pool.join()
    
    end = time()
    elapse = end - start 
    now=ctime()[4:]

    print 'diary ',len(all_IDs),'  used {:.2f} s {:.2f} mins'.format(elapse, elapse/60) ,now

    
def html_main():
    print os.argv
    
    global cpu, diary_link
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
    

        
    df=pd.read_csv('diary_all.csv', usecols=['group_id'])
    print 'start scraping', ctime()
    print len(df['group_id'].unique()), df.shape

    all_ids=df['group_id'].tolist()
    
    have = list(map(lambda x: int(x.split('.')[0]) ,os.listdir(folder)))
    want = list(set(all_ids)-set(have))
    
    print 'all diary htmls - already scraped'
    print len(all_ids), len(have), len(want)    
    

    print len(want)

    fail=[]
    batch(want)
    
    

    if len(fail)>0:
        print 'logging fail IDs'
        
        pd.DataFrame(fail, columns=['group_id']).to_csv(ct[2]+ct[1]+ct[-1]+'_diary_html_fail.csv',index=False)
    else:
        print 'done!', ctime()
