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


#https://www.marketwatch.com/investing/stock/intc
#<meta name="price" content="$58.67" />
regex1 = r'.*<meta name=\"price\" content=\"\$(?P<price>.*)\"\s+/>'
REGEX1 = re.compile(regex1)

#https://www.slickcharts.com/sp500
tr = r'.*<(/?)tr>'
TR = re.compile(tr)

td1 = r'.*<td>(?P<index>\d+)</td>'
TD1 = re.compile(td1)

#<td><a href="/symbol/HES">HES</a></td>
td2 = r'.*<td><a href="/symbol/\S+">(?P<symbol>\S+)</a></td>'
TD2 = re.compile(td2)
td3 = r'.*<td><a href="/symbol/\S+">(?P<name>.*)</a></td>'
TD3 = re.compile(td3)
td4 = r'.*<td>(?P<weight>\d\.\d+)</td>'
TD4 = re.compile(td4)
td5 = r'.*<td class="text-nowrap"><img src=".*" alt=""> &nbsp;&nbsp;(?P<price>\d+\.\d+)</td>'
TD5 = re.compile(td5)
#<td class="text-nowrap" style="color: green">0.00</td>
td6 = r'.*<td class="text-nowrap" style="color:.*">(?P<change>-?\d+\.\d+)</td>'
TD6 = re.compile(td6)
td7 = r'.*<td class="text-nowrap" style="color:.*">\((?P<change_percent>-?\d+\.\d+)\%\)</td>'
TD7 = re.compile(td7)

LOG_DIR = "./files"

def log_single_stock(name, stock_data):
    x = datetime.datetime.now()
    timestamp = x.strftime("%H:%M")
    YEAR = x.strftime("%Y")
    MONTH = x.strftime("%m_%B")
    DAY = x.strftime("%Y_%m_%d_%A")
    if not os.path.isdir(LOG_DIR):
        os.mkdir(LOG_DIR)
    if not os.path.isdir(LOG_DIR + "/" + name):
        os.mkdir(LOG_DIR + "/" + name)
    if not os.path.isdir(LOG_DIR + "/" + name + "/" + YEAR):
        os.mkdir(LOG_DIR +  "/" + name + "/" + YEAR)
    if not os.path.isdir(LOG_DIR + "/" + name + "/" +  YEAR + "/" + MONTH):
        os.mkdir(LOG_DIR + "/" + name + "/" + YEAR + "/" + MONTH)
        os.system('ln -s ../index.php ' + LOG_DIR + "/" + name + "/" + YEAR + "/" + MONTH + '/index.php')
        os.system('ln -s ../readcsv.php ' + LOG_DIR + "/" + name + "/" + YEAR + "/" + MONTH + '/readcsv.php')

    index = int(stock_data[0])
    stock_data[0] = "%03d" %(index)
    stock_data[2] = stock_data[2].replace("\'", "")
    stock_data[2] = stock_data[2].replace("\"", "")
    stock_data[2] = stock_data[2].replace('&', 'and')
    csv_filename = LOG_DIR + "/" + name + "/" + YEAR + "/" + MONTH + "/";
    csv_filename = csv_filename + stock_data[0] + "_" + stock_data[1] + "_";
    csv_filename = csv_filename + stock_data[2].replace(" ", "_") + "_" +  DAY + ".csv"
    LOG(csv_filename + ':')
    if not os.path.isfile(csv_filename):
        csv_file = open(csv_filename, 'w')
        csv_file.write('TIME, PRICE, CHANGE, CHANGE_PERCENT,\n')
        csv_file.close()
    print(csv_filename)
    csv_file = open(csv_filename, 'a')
    csv_file.write(timestamp + ', ')
    csv_file.write(stock_data[4] + ', ')
    csv_file.write(stock_data[5] + ', ')
    csv_file.write(stock_data[6] + ', ')
    csv_file.write('\n')
    csv_file.close()
    LOG(stock_data)

def GetSP500():
    url = 'https://www.slickcharts.com/sp500'
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    csv_file = open('sp500.csv', 'w')
    csv_file.write('INDEX, SYMBOL, NAME, WEIGHT, PRICE, CHANGE, CHANGE_PERCENT')
    matched_items = 0
    stock_data = ["", "", "", "", "", "", ""]
    for line in webpage.splitlines():
        line = str(line).replace(',', '')
        line = line.replace('&amp;', 'and').replace('&#39;', '\'')
        td1 = TD1.match(line)
        td2 = TD2.match(line)
        td3 = TD3.match(line)
        td4 = TD4.match(line)
        td5 = TD5.match(line)
        td6 = TD6.match(line)
        td7 = TD7.match(line)
        if TR.match(line):
            if matched_items > 0 and matched_items != 7:
                print("ERROR - found %d items instead of 7..." %(matched_items))
            matched_items = 0
            stock_data = ["", "", "", "", "", "", ""]
            LOG("\n")
        elif td1:
            LOG("INDEX: %d"  %(int(td1.group('index'))))
            csv_file.write('\n' + td1.group('index') + ', ')
            stock_data[0] = td1.group('index')
            matched_items = matched_items + 1
        elif td2:
            LOG("SYMBOL: %s" %(td2.group('symbol')))
            csv_file.write(td2.group('symbol') + ', ')
            stock_data[1] = td2.group('symbol')
            matched_items = matched_items + 1
        elif td3:
            LOG("NAME: %s"   %(td3.group('name')))
            csv_file.write(td3.group('name') + ', ')
            stock_data[2] = td3.group('name')
            matched_items = matched_items + 1
        elif td4:
            LOG("WEIGHT: %s" %(td4.group('weight')))
            csv_file.write(td4.group('weight') + ', ')
            stock_data[3] = td4.group('weight')
            matched_items = matched_items + 1
        elif td5:
            LOG("PRICE: %s"  %(td5.group('price')))
            csv_file.write(td5.group('price') + ', ')
            stock_data[4] = td5.group('price')
            matched_items = matched_items + 1
        elif td6:
            LOG("CHANGE: %s" %(td6.group('change')))
            csv_file.write(td6.group('change') + ', ')
            stock_data[5] = td6.group('change')
            matched_items = matched_items + 1
        elif td7:
            matched_items = matched_items + 1
            LOG("CHANGE: %s %% (%d th matched item)" %(td7.group('change_percent'), matched_items))
            csv_file.write(td7.group('change_percent'))
            stock_data[6] = td7.group('change_percent')
            log_single_stock('sp500', stock_data)
        else:
            if len(line) > 1 and DEBUG:
                LOG(line)
        #if td1 and int(td1.group('index')) == 505:
        #    break
    csv_file.close()
    return

while True:
    force = False
    if len(sys.argv) > 1:
        if sys.argv[1] == "-f":
            force = True
    x = datetime.datetime.now()
    timestamp = x.strftime("%H:%M")
    hour = int(x.strftime("%H"))
    minute = int(x.strftime("%M"))
    minutes = hour * 60 + minute
    day = int(x.strftime("%w"))
    #stock market is open Mon-Fri between 6:30 and 13:30 PST:
    if force or (day > 0 and day < 6 and minutes >= 6 * 60 + 20 and minutes <= 14 * 60 + 0):
        GetSP500()
        time.sleep(60)
    else:
        print(timestamp + " market closed, sleeping for 10 min\n")
        time.sleep(600)
