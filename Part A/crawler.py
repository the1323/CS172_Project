
from random import seed
from time import sleep
import requests 
from bs4 import BeautifulSoup 
import csv
import multiprocessing as mp

MAX_PAGE = 1000
MAX_HOPS = 3



def collect_result(result):
    global results
    results.append(result)

def saveFile(fname,data,mode):
    f = open(fname, mode)
    f.write(data)
    f.close()


def LogFile(school,url,fileCounter):
    with open("log.csv", 'a',newline='',encoding='utf-8') as csvfile: 
    # creating a csv writer object 
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([school, fileCounter,url ])
    #saveFile("log.txt",f"{school},{fileCounter},{url}\n",'a')

def ParseHTML(url,hops,childrenPages, fileCounter,logUrl,school):
    try:
        
        if hops > MAX_HOPS:
            return
        response = requests.get(url)

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
                    

    except:
        print("error at this url: " + url)
        #print("skipping to next url")
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
        #print(f"working on url: {childrenPages[0]}")
        ParseHTML(childrenPages[0],0,childrenPages, fileCounter,logUrl,school)
        fileCounter +=1
        childrenPages.pop(0)
        sleep(0.1)


    

if __name__ == '__main__':
    path = input("Enter Seeds file path:")
    MAX_PAGE = input("Enter Max Page:")
    MAX_HOPS = input("Enter Max Hops:")
    num_cores = int(mp.cpu_count())
    mp.freeze_support()
    print("This PC has: " + str(num_cores) + " cores")
    numProcess = input("Enter number of process, or 'Enter' to use default value:")
    if numProcess != "":
       num_cores=numProcess 
    #path =  r'C:\Users\tongy\Desktop\CS172\project\CS172_Project\Part A\us_universities.csv'
    csv_reader = csv.reader(open(path))
    seeds = [line for line in csv_reader]
  
    
    

    
    
    pool = mp.Pool(num_cores)
    for seed in seeds:
        pool.apply_async(eduCrawler, args = (seed, ), callback = None)

    pool.close()
    pool.join()


    
    
    


