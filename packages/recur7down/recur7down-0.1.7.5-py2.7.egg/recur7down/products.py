from recur7down import Collect
import sys
from time import time, ctime, strftime, localtime
from multiprocessing import cpu_count
from multiprocessing.dummy import Pool as ThreadPool
import pandas as pd
import os



#cpu = cpu_count()*6




    

def helper((link, place, cat)):
   
    instance = Collect(link,  place, cat)
    instance.main()
    instance.save()
    
    
    
    
    
def product_main():
    
    try:
        sys.path.append(os.getcwd())
        from info import link, cat, large, small
        print 'imported data from info'
        sys.path.remove(os.getcwd())

    except:
        print 'lack of info.py'
        exit(0)
        
        
    #path = raw_input('the PATH of file contains a single string of the url link: ')
    #with open(path) as fh:
    #    link = fh.read()
    cpu = int(raw_input('(multi-processing) how many process to run ? '))


    #cat = [10020, 10021, 10010, 10001, 10003, 10006, 10019, 10008, 10009, 10011, 10013, \
    #      10023, 10022, 10015, 10012, 10007, 10017, 10018]

    #large = [19, 1, 17, 9, 10, 11, 23, 18, 15, 16, 12, 22, 13, 6]
    #small = [25, 27, 14, 3, 2, 556, 8, 20, 31, 7, 21, 4, 24, 28, 5, 32, 30, 33, 29, 561, 560, 34]

    
    try:
        from info import link, cat, large, small
        print 'imported data from info'
    except:
        print 'lack of info.py'
        exit(0)    



    swim = []

    for i in small:
        swim.append((link, i, 0))

    for p in large:
        for c in cat:
            swim.append((link, p, c))
    
    
    
    
    
    
    
    print "combinations: "+str(len(swim))
    start=time()

    pool = ThreadPool(cpu)
    
    results = pool.map(helper, swim)
    pool.close()
    pool.join()
    
    end = time()
    elapse = end - start 
    print 'used {:.2f} s, {:.2f} mins'.format(elapse, elapse/60)
    
    print 'start concating data'
    
    ct = ctime().split()
    path = ct[2]+ct[1]+ct[-1]+'_product/'
    
    files = os.listdir(path)
    len(files)
    df = pd.concat([pd.read_excel(path + i) for i in files])
    print df.shape
    print 'removing duplicates'
    
    col = list(df.columns)
    col = [col.pop(col.index('pid')), col.pop(col.index('title'))]+col
    df = df[col]
    df = df.reset_index(drop=True)
    
    df = df.loc[df['pid'].drop_duplicates().index,:]
    print df.shape
    print 'saving to products.xlsx'
    
    df.to_excel(strftime("%Y-%m-%d-%H-%M",localtime())+ ' Products.xlsx', encoding='utf-8', index=False)
    print 'done!', ctime()

