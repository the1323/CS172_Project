from functools import partial
from random import seed
from re import S
from time import sleep
from urllib import response
import requests 
from bs4 import BeautifulSoup 
import json
import copy
import csv
import os.path
import time
import multiprocessing as mp

MAX_PAGE = 1000
MAX_HOPS = 3



def collect_result(result):
    global results
    results.append(result)

def saveFile(fname,data,mode):
    #print(f"response : {data.url}")
   # global fileCounter
    #print(f"cc: {fileCounter}")
    f = open(fname, mode)
    f.write(data)
    f.close()
    print("save done")

def LogFile(school,url,fileCounter):
    
    saveFile("log.txt",f"{school},{fileCounter},{url}\n",'a')

def ParseHTML(url,hops,childrenPages, fileCounter,logUrl,school):
    try:
        
        #print("asdasd without ///")
        #print(homepage)
        print(f"hop: {hops}")
        if hops > MAX_HOPS:
            return
        response = requests.get(url)
        print(fileCounter)
        saveFile(f"Part A/DataFiles/{school}_{fileCounter}.html",response.text,'w')
        LogFile(school,url,fileCounter)
        
        allPage = BeautifulSoup(response.content, "html.parser")
        #print(allPage)
        hyperLinks = allPage.findAll("a", href=True)
        for link in hyperLinks:

            partialLink = link['href']
            #print(link['href'])
            if partialLink[0] == '/':
                partialLink = url + partialLink[1:]
                if partialLink not in logUrl and partialLink != url:
                    childrenPages.append(partialLink)
                    logUrl.append(partialLink)
                    
                    #print(partialLink)
        
        # if len(childrenPages) >0:
        #     print(f"child : {childrenPages[0]}")
        #     temp = childrenPages[0]
        #     childrenPages.pop(0)
        #     ParseHTML(temp,hops+1)
        #     #sleep(1)
            
        #     print(f"after : {childrenPages[0]}")
    except:
        print("error at this url: " + url)
        print("skipping to next url")
        return

def eduCrawler(seed):
    school = seed[0]
    print(f"Starting new edu: {eduCrawler}")
    logUrl = []
    childrenPages = []
    fileCounter = 0
    logUrl.append(seed[1])
    childrenPages.append(seed[1])
    while len(childrenPages):
        print(f"working on: {fileCounter} of {len(childrenPages)}")
        print(f"working on url: {childrenPages[0]}")
        ParseHTML(childrenPages[0],0,childrenPages, fileCounter,logUrl,school)
        fileCounter +=1
        childrenPages.pop(0)
        sleep(0.5)


def aaa(s):
    print (f'aaaa: {s}')

if __name__ == '__main__':
    path =  r'C:\Users\tongy\Desktop\CS172\project\CS172_Project\Part A\us_universities.csv'
    csv_reader = csv.reader(open(path))
    seeds = [line for line in csv_reader]
    print(len(seeds))

    
    

    num_cores = int(mp.cpu_count())
    mp.freeze_support()
    print("This PC has: " + str(num_cores) + " cores")
    
    pool = mp.Pool(num_cores)
    for seed in seeds:
        pool.apply_async(eduCrawler, args = (seed, ), callback = None)

    pool.close()
    #pool.join()

    # for seed in seeds:
    #     p=mp.Process(target=eduCrawler,args=(seed,))
    #     p.start()

    # for i in range(50) :
    #     print("here ")
    #     p=mp.Process(target=aaa,args=(i,))
    #     p.start()
        #pool.apply_async(eduCrawler,args=(seeds[i]))

        #eduCrawler(seed)

    #pool.close()
    
    
    
    


