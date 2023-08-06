# coding: utf-8

import sys
try:
    reload(sys)
    sys.setdefaultencoding("utf-8")
except:
    print('python3')


import pandas as pd
from lxml import etree
import os
from time import time, ctime, strftime, localtime


class Hparser(object):
    collection = []
    df=None
    N=0
    def __init__(self, html):
        self.coll = []
        self.diaryID = html.split('/')[-1].split('.html')[0]
        try:
            with open(html) as fh:self.tree = etree.HTML(fh.read())
        except Exception as e:
            print e, 'X0'
            print diaryID        
        #print self.diaryID, self.tree
        
        
        self.main()
        
        
        
    @classmethod
    def _update(cls, new):
        cls.N += 1
        cls.collection+=new
        #if cls.N%3000==0:
        #    print cls.N,
        
    def _product(self):
        try: self.pid = self.tree.xpath('//div[@class="value product-name"]/a/@href')[0].split('/')[-1]
        except: print 'X pid'
    def _content(self):
        try:self.content = self.tree.xpath('//li[@class="diary-item"]'); self.dn = len(self.content)
        except: print 'X content'
            
    def _image(self, node):
        dic={}
        dic['diary_id']=self.diaryID
        dic['product_id']=self.pid
        
        dic['type']='image_post'
        dic['title']=node[0].xpath('text()')[0]
        dic['text']=node[1][0].xpath('text()')[0]
        dic['post_id']=node[1][0].xpath('./@href')[0].split('?')[0].split('/')[-1]
        for n, i in enumerate(node[2]):
            dic['image_'+str(n+1)] = i[0][0].xpath('./@data-img')[0]
        n=0
        for i in node[3]:
            if i.tag=='div': dic['time']=i.xpath('text()')[0]
            else:
                if len(i)!=0:
                    n+=1
                    if n==1:
                        dic['views']=i[0].xpath('text()')[0]
                    elif n==2:
                        dic['comments']=i[0].xpath('text()')[0]
                    else:
                        dic['favor']=i[0].xpath('text()')[0]
        return dic        
    def _video(self, node):
        dic={}
        dic['diary_id']=self.diaryID
        dic['product_id']=self.pid
        dic['type']='video_post'
        dic['text']=node[1][0].xpath('text()')[0]
        dic['title']=node[0].xpath('text()')[0]
        dic['post_id']=node[1][0].xpath('./@href')[0].split('?')[0].split('/')[-1]
        
        dic['video_link']=node[2][0].xpath('./@href')[0]
        dic['video_image']=node[2][0].xpath('./img')[0].xpath('./@data-img')[0]   
        
        n=0
        for i in node[3]:
            if i.tag=='div': dic['time']=i.xpath('text()')[0]
            else:
                if len(i)!=0:
                    n+=1
                    if n==1:
                        dic['views']=i[0].xpath('text()')[0]
                    elif n==2:
                        dic['comments']=i[0].xpath('text()')[0]
                    else:
                        dic['favor']=i[0].xpath('text()')[0]        
        return dic
    
    def loop(self):
        for p in self.content:
            
            if p[2].tag == 'ul':
                self.coll.append(self._image(p))
            else:
                self.coll.append(self._video(p))
                
    def main(self):
        self._product()
        self._content()
        self.loop()
        self._update(self.coll)
        
    def __repr__(self):
        return "diary: {} of product: {} has {} posts, all {} posts finished parsing"\
    .format(self.diaryID, self.pid, self.dn, self.N)
    
    
def parse_diary_main():
    folder = raw_input('the PATH of folder contains all diary htmls: ')
    htmls = os.listdir(folder)
    folder = folder if folder.endswith('/') else folder+'/'
    
    n=0
    for d in htmls:
        Hparser(folder+d)
        n+=1
        start0=time()
        start=time()
        if n%5000==0:
            end=time()
            elapse = end - start 
            print '{} {:.2f} s'.format(n, elapse),        
            start=time()
    print 'done parsing all'
    elapse0=time()-start0
    print 'used {:.2f} s, {:.2f} mins'.format(elapse0, elapse0/60)
    print 'start to making csv file'
    df = pd.DataFrame(Hparser.collection)
    df.to_csv(strftime("%Y-%m-%d-%H-%M",localtime())+'diary_post_data.csv', encoding='utf-8', index=False)
        
            