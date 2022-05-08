from random import seed
from time import sleep
import requests
from bs4 import BeautifulSoup
import csv
import multiprocessing as mp
import os
import datetime
import time
from multiprocessing import Value

totalPages = None
class childPage:
        def __init__(self, url, hops):
            self.url = url
            self.hops = hops

def init(args):
    #shared page counter
    global totalPages
    totalPages = args


def saveFile(fname, data, mode):
    #print(fname)
    f = open(fname, mode)
    f.write(data)
    f.close()


def LogFile(school, url, fileCounter,fSize):
    fileDir = os.path.dirname(__file__)
    path = os.path.join(fileDir, "log.csv")
    with open(path, 'a', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([datetime.datetime.now(),school, fileCounter, url,fSize])
    # saveFile("log.txt",f"{school},{fileCounter},{url}\n",'a')


def ParseHTML(child, hops, childrenPages, fileCounter, logUrl, school):
    global totalPages
    #print('hhhhhhhhhhhh')
    #print(child.hops)
    try:
        response = requests.get(child.url)
        saveFile(f"Part A/DataFiles/{school}_{fileCounter}.html", response.text, 'w')
        LogFile(school, child.url, fileCounter,len(response.content))
        allPage = BeautifulSoup(response.content, "html.parser")
        #print(allPage)
        
        hyperLinks = allPage.findAll("a", href=True)
        
        for link in hyperLinks:
            
            partialLink = link['href']
            # print(link['href'])
            if partialLink[0] == '/':
                partialLink = child.url + partialLink[1:]
                if partialLink not in logUrl and partialLink != child.url:
                    childrenPages.append(childPage(partialLink,child.hops+1))
                    logUrl.append(partialLink)
        return


    except:
        #print("error at this url: " + child.url +" Skiped")
        return 


def eduCrawler(seed,MAX_PAGE,MAX_HOPS):
    global totalPages
    
    if totalPages.value >= int(MAX_PAGE):
        return 
    school = seed[0]
    print(f"Starting new edu: {school}")
    
    logUrl = []
    childrenPages = []
    fileCounter = 0
    logUrl.append(seed[1])
    childrenPages.append(childPage(seed[1],0))
    
    while len(childrenPages):
        #print(f'max hop: {MAX_HOPS}')
        #print(f"Queue: {len(childrenPages)}, saved: {fileCounter} current Hop: {childrenPages[0].hops}")
        if totalPages.value >= int(MAX_PAGE) or childrenPages[0].hops> int(MAX_HOPS) :
            return 
        #print(f"Queue: {len(childrenPages)}, saved: {fileCounter} current Hop: {childrenPages[0].hops}")
        #print(f"working on url: {childrenPages[0].url}")
        #print(f"page saved so far: {totalPages}")
        ParseHTML(childrenPages[0], 0, childrenPages, fileCounter, logUrl, school)
        if totalPages.value %100 ==0: 
            print(f"total: {totalPages.value} max: {MAX_PAGE}")
        
        #print(f"totalPages {totalPages.value}")
        with totalPages.get_lock():
            totalPages.value += 1
        fileCounter += 1
        childrenPages.pop(0)
        sleep(0.01)
    childrenPages =[]
    logUrl=[]
    return fileCounter
    

if __name__ == '__main__':
    path =  "us_universities.csv"
    if os.path.exists(path):
        print('file not exits')
    else:print('file aaaaaaaaaa exits')
    fileDir = os.path.dirname(__file__)
    path = os.path.join(fileDir, path)
    print(path) 
        #path = input("Enter Seeds file path:")
    
    MAX_PAGE = input("Enter Max number of pages:")
    #print(f"max : {MAX_PAGE}")
    MAX_HOPS = input("Enter Max number of Hops:")
    print(f"max : {MAX_HOPS}")
    num_cores = int(mp.cpu_count())
    mp.freeze_support()
    print("This PC has: " + str(num_cores) + " cores")
    numProcess = input("Enter number of process, or 'Enter' to use default core value:")
    if numProcess != "":
        if int(numProcess) > 0 and int(numProcess) <99:
            num_cores = int(numProcess)
    
    csv_reader = csv.reader(open(path))
    seeds = [line for line in csv_reader]
    if 'http' not in seeds[0]:seeds.pop(0) #remove head
    # for seed in seeds:
    #     a=eduCrawler(seed)
    #     exit(1)
    start_t=datetime.datetime.now()
    totalPages = Value('i', 0)
    try:
        pool = mp.Pool(num_cores, initializer = init, initargs = (totalPages, ))
        for seed in seeds:
            if totalPages.value >= int(MAX_PAGE):
                break
            i =pool.apply_async(eduCrawler, args=(seed,MAX_PAGE,MAX_HOPS,), callback=None)

        pool.close()
        pool.join()
    except KeyboardInterrupt:
        pool.terminate()
        pool.join()
    end_t = datetime.datetime.now()
    elapsed_sec = (end_t - start_t).total_seconds()
    elapsed_min = elapsed_sec // 60
    elapsed_sec = elapsed_sec % 60
    print("Total Time :" "{:.0f}".format(elapsed_min) + " Minutes " + "{:.2f}".format(elapsed_sec) + "sec")