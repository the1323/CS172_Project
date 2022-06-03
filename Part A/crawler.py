from random import seed
from time import sleep
import requests
from bs4 import BeautifulSoup, Comment
import csv
import multiprocessing as mp
import os
import datetime
from timeit import default_timer as timer
from multiprocessing import Value
import json
import unicodedata
import urllib3
import lxml
import cchardet
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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
    fileDir = os.getcwd()
    path = os.path.join(fileDir, "log.csv")
    with open(path, 'a', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([datetime.datetime.now(),school, fileCounter, url,fSize])
    # saveFile("log.txt",f"{school},{fileCounter},{url}\n",'a')


def ParseHTML(seed,child, hops, childrenPages, fileCounter, logUrl, school):
    global totalPages

    try:

        response = requests.get(child.url, verify = False)
        
        if response.ok == False:
            print("status false ")
            return 0
        #saveFile(f"DataFiles/{school}_{fileCounter}.html", response.text, 'w')
        LogFile(school, child.url, fileCounter,len(response.content))
        
        allPage = BeautifulSoup(response.content, "lxml",from_encoding="iso-8859-1")
        #print(allPage)
       
        #remove all comment tags 
        div = allPage.find('div')
        for element in div(text=lambda text: isinstance(text, Comment)):
            element.extract()


        title = allPage.find('title').string.replace( ',', '')
        
        allowlist = [
        'p',
        'div',
        'span'
        ]
        
        text = [t for t in allPage.findAll(text=True) if t.parent.name in allowlist]
          
        
        # get all visible text, since some site write stuff outside of body tag, I just get everything, even though lots of useless data..
        textStr = " "
        for t in text:
            if t != "\n":
                textStr+=(" " +t.replace( ',', ''))
        textStr=(unicodedata.normalize('NFKD', textStr).encode('ascii', 'ignore'))
          
        childUrls = []
        hyperLinks = allPage.findAll("a", href=True)
        
        
        for link in hyperLinks:
            partialLink = link['href']
            
            if partialLink[0] == '/':
                partialLink = seed + partialLink[1:]
                if partialLink not in logUrl and partialLink != child.url:
                    childrenPages.append(childPage(partialLink,child.hops+1))
                    logUrl.append(partialLink)
                    childUrls.append(partialLink)

        # Data to be written
        
        with open(f"DataFiles/{school}.csv", 'a',newline='') as f:
            writer = csv.writer(f)
            
            writer.writerow([title,child.url,textStr,childUrls])

        return 1


    except:
        print("error at this url: " + child.url +" Skiped")
        return 0


def eduCrawler(seed,MAX_PAGE,MAX_HOPS):
    global totalPages
    perEduCounter =0
    start = timer()
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
        end = timer()
        # if cant finish 30 doc in 1 minute, skip this edu
        if (end - start)>60 and perEduCounter < 30:
            print(f"edu limit too restrict, skip {school}")
            return 
        else:
            start = timer()
            perEduCounter = 0
        #print(f"Queue: {len(childrenPages)}, saved: {fileCounter} current Hop: {childrenPages[0].hops}")
        if totalPages.value >= int(MAX_PAGE) or childrenPages[0].hops> int(MAX_HOPS) :
            childrenPages.clear()
            logUrl.clear()
            return 
            
        #print(f"Queue: {len(childrenPages)}, saved: {fileCounter} current Hop: {childrenPages[0].hops}")
        #print(f"working on url: {childrenPages[0].url}")
        #print(f"page saved so far: {totalPages}")
        count = ParseHTML(seed[1],childrenPages[0], 0, childrenPages, fileCounter, logUrl, school)
        if totalPages.value %10 ==0: 
            print(f"total: {totalPages.value} max: {MAX_PAGE}...")
        
        #print(f"totalPages {totalPages.value}")
        with totalPages.get_lock():
            totalPages.value += count
        fileCounter += 1
        perEduCounter +=count
        childrenPages.pop(0)
        #sleep(0.01)
    childrenPages.clear()
    logUrl.clear()
    print(f"ending edu: {school}")
    
    

if __name__ == '__main__':
    ENABLE_MULTIPROCESSING = False
    mp.freeze_support()
    #print(os.getcwd())
    #path =  "us_universities.csv"
    path = input("Enter Seeds file path:")
    fileDir = os.getcwd()
    path = os.path.join(fileDir, path)

    while not os.path.exists(path):
        path = input("File not found, Enter Seeds file path:")
        fileDir = os.path.dirname(__file__)
        path = os.path.join(fileDir, path)

    # if os.path.exists(path):
    #     print('file not exits')
    # else:print('file aaaaaaaaaa exits')
    
    print(path) 
    
    MAX_PAGE = input("Enter Max number of pages:")
    #print(f"max : {MAX_PAGE}")
    MAX_HOPS = input("Enter Max number of Hops:")
    #print(f"max : {MAX_HOPS}")
    num_cores = int(mp.cpu_count())
    if ENABLE_MULTIPROCESSING:
        print("This PC has: " + str(num_cores) + " cores")
        numProcess = input("Enter number of process, or 'Enter' to use default core value:")
        if numProcess != "":
            if int(numProcess) > 0 and int(numProcess) <99:
                num_cores = int(numProcess)
    
    csv_reader = csv.reader(open(path))
    seeds = [line for line in csv_reader]
    if 'http' not in seeds[0]:seeds.pop(0) #remove head
    
    
    start_t=datetime.datetime.now()
    totalPages = Value('i', 0)
    if ENABLE_MULTIPROCESSING:
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
    else:
        for seed in seeds:
            eduCrawler(seed,MAX_PAGE,MAX_HOPS)
        
    end_t = datetime.datetime.now()
    elapsed_sec = (end_t - start_t).total_seconds()
    elapsed_min = elapsed_sec // 60
    elapsed_sec = elapsed_sec % 60
    print("Total Time :" "{:.0f}".format(elapsed_min) + " Minutes " + "{:.2f}".format(elapsed_sec) + "sec")
    exit = input("program finished, enter 'y' to exit\n")