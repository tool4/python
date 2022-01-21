import urllib.request
from urllib.request import Request, urlopen
import sys
import re
import os, os.path
from os import path
import fnmatch
import time
import datetime

DEBUG = 0

def LOG(str):
    if DEBUG:
        print(str)


#https://www.slickcharts.com/sp500
tr = r'.*<(/?)tr>'
TR = re.compile(tr)
td1 = r'.*<td>(?P<index>\d+)</td>'
TD1 = re.compile(td1)

LOG_DIR = "./files"


def GetSP500():
    #url = 'https://www.slickcharts.com/sp500'
    url = 'https://www.etrade.wallst.com/Research/Markets/Movers?index=US&type=percentGainers'
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    csv_file = open('gainers.csv', 'w')
    matched_items = 0
    for line in webpage.splitlines():
        line = str(line).replace(',', '')
        print(line)
        csv_file.write(line)
        #line = line.replace('&amp;', 'and').replace('&#39;', '\'')
    csv_file.close()
    return


GetSP500()
