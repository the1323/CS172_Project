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
import json
import unicodedata
import urllib3


csv_reader = csv.reader(open("DataFiles/University of California, Berkeley.csv"))
seeds = [line for line in csv_reader]
print(seeds[7][3])