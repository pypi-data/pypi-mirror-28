# coding: utf-8



import sys
try:
    reload(sys)
    sys.setdefaultencoding("utf-8")
except:
    print('python3')
    
import pandas as pd
import json
import requests
import os
from json2df import flatten_dict


from time import time, ctime, strftime, localtime
from multiprocessing import cpu_count
from multiprocessing.dummy import Pool as ThreadPool




    
diary = "http://y.soyoung.com/cp{}?action=calendarlist"



ct = ctime().split()
folder= ct[2]+ct[1]+ct[-1]+'_diary/'
try:
    os.mkdir(folder)
    except:
        print 'R' 




def One(ID):
    link = diary.format(ID)
    
    base = json.loads(requests.get(link, timeout=6).text)
    lists = base['group_list']['list']
    df = pd.DataFrame(map(lambda p: flatten_dict(p, layers=3), lists))
    
    
    try:
        col = list(self.df.columns)
        col = [col.pop(col.index('group_id')), col.pop(col.index('uid')), col.pop(col.index('user_name')), col.pop(col.index('top.summary'))]+col
        df = df[col]
        df.pop('other.summary')
        df['from_product']=ID
        df = df.set_index('from_product')
        df.to_excel(folder + str(ID)+'.xlsx', encoding='utf-8')
        print 'O',
    except Exception as e:
        print e,
        One(ID)

def diary_main():
    content = pd.read_csv('./diary_products.csv', names=['product_id'])['product_id'].tolist()
    cpu = int(raw_input('(multi-processing) how many process to run ? '))

    start=time()

    pool = ThreadPool(cpu)
    
    results = pool.map(One, content)
    
    pool.close()
    pool.join()
    
    end = time()
    elapse = end - start 
    
    print 'used {:.2f} s, {:.2f} mins'.format(elapse, elapse/60)
    
    
    
    print 'start concating data'
    
    
    files = os.listdir(folder)
    print len(files)
    df = pd.concat([pd.read_excel(folder + i) for i in files])
    print df.shape
    print 'removing duplicates'
    
    #col = list(df.columns)
    #col = [col.pop(col.index('pid')), col.pop(col.index('title'))]+col
    #df = df[col]
    #df = df.reset_index(drop=True)
    
    #df = df.loc[df['pid'].drop_duplicates().index,:]
    print df.shape
    print 'saving to products.xlsx'
    
    df.to_excel(strftime("%Y-%m-%d-%H-%M",localtime())+ ' diary.xlsx', encoding='utf-8', index=False)
    print 'done!', ctime()
    
    
    
    
