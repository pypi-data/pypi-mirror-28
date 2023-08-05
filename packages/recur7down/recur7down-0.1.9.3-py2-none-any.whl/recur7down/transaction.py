# coding: utf-8

import sys
import os
try:
    reload(sys)
    sys.setdefaultencoding("utf-8")
except:
    print('python3')
    
import requests
import json
from json2df import flatten_dict
import pandas as pd

from time import time, ctime, strftime, localtime
from multiprocessing import cpu_count
from multiprocessing.dummy import Pool as ThreadPool


class Transaction(object):
    def __init__(self,  PID):
        self.link = link.format(PID, '{}')
        self.index=1
        self.content = []
        self.pid=PID
        
    def initial(self):
        if self.index==1:
            try:
                r = requests.get(self.link.format(self.index))
                d = json.loads(r.text)
                
                self.page, self.all = int(d['pages']['all']), int(d['pages']['all_num'])
                c = d['list']
                
                if len(c)>0:
                    self.content = self.content+c
                    self.index+= 1   
                    
                print 'page:',self.page,'all:', self.all,
                print '{}/{}'.format(self.index-1,self.page),
            except Exception as e:
                print 'N', 
                try:
                    if self.all==0:
                        print '0',
                    
                #print e
                except:
                    self.initial()
        
    def process(self):
        if self.page >= self.index:
        
            try:
                r = requests.get(self.link.format(self.index))
                d = json.loads(r.text)
                c = d['list']

                if len(c)>0:
                    self.content = self.content+c
                    #print '{}/{}'.format(self.index,self.page),
                    print 'O',
                    self.index+= 1
                    self.process()
                else:
                    print '<',
                    self.process()
            except Exception as e:
                #print e,
                print 'X',
                self.process()
        else:
            print 'R',
            if self.all==0:
                print '0e',
            elif len(self.content)==self.all:
                try:
                    self.df = pd.DataFrame(self.content)
                    print self.df.shape,
                    self.df.to_excel(folder+str(self.pid)+'.xlsx', index=False)
                    print str(self.pid)+'.xlsx Done ',
                except Exception as e:
                    print e,
                    print 'S',
            else:
                print 'gather', len(self.content), 'exists', self.all
    def __repr__(self):
        return str(self.pid)+' instance'
    
def helper(ID):
    c = Transaction(ID)
    c.initial()
    c.process()
    
    
    
    
    
def transaction_main():
    global link, folder
    
    try:
        sys.path.append(os.getcwd())
        from info import transaction as link
        print 'imported transaction link from info'
        sys.path.remove(os.getcwd())

    except Exception as e:
        print e
        print 'lack of info.py'
        exit(0)    
    
    
    ct = ctime().split()
    folder= ct[2]+ct[1]+ct[-1]+'_transaction/'
    try:
        os.mkdir(folder)
    except:
        print 'D'    
        
    # cancat to one excel after down
    flag = raw_input('merge into one excel? do this after done scraping!  y/n: ')
    if flag.lower()=='y':

        print 'start concating data'
        start2=time()        
        
        files = os.listdir(folder)
        print len(files)

        tmp = []
        for i in files:
            try:
                one = pd.read_excel(folder+i)
                one['PID']=int(i.split('.')[0])
                tmp.append(one)
            except:
                print i,
        print len(tmp)
        df = pd.concat(tmp)
        print df.shape        
    
        col = list(df.columns)
        change_order = ['PID',]
        col = [col.pop(col.index(i)) for i in change_order]+col
        df = df[col]

        end2 = time()
        elapse2 = end2 - start2 
        print 'used {:.2f} s, {:.2f} mins'.format(elapse2, elapse2/60)
        print 'saving to transactions.xlsx'
        df.to_excel(strftime("%Y-%m-%d-%H-%M",localtime())+ ' transaction.xlsx', encoding='utf-8', index=False)
        print 'done!', ctime()
#### start
    content = pd.read_csv('./transaction_products.csv')['pid'].tolist()
    cpu = int(raw_input('(multi-processing) how many process to run ? '))

    have = list(map(lambda x: int(x.split('.')[0]) ,os.listdir(folder)))
    want = list(set(content)-set(have))
    
    print 'all product diary - already scraped'
    print len(content), len(have), len(want)
    
    
    
    start=time()

    pool = ThreadPool(cpu)
    
    results = pool.map(helper, want)
    
    pool.close()
    pool.join()
    
    end = time()
    elapse = end - start 
    
    print 'used {:.2f} s, {:.2f} mins'.format(elapse, elapse/60)
        
    