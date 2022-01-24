import urllib.request
from urllib.request import Request, urlopen
import sys
import re
import os, os.path
from os import path
import fnmatch
import time
import datetime

header = '                    \n\
<html lang="en-us">           \n\
<style>                       \n\
.positive {                   \n\
  color: green;               \n\
  margin: 10px;               \n\
}                             \n\
.negative {                   \n\
  color: red;                 \n\
}                             \n\
.numeric {                    \n\
  margin: 20px;               \n\
}                             \n\
.text-left {                  \n\
  text-align: left;           \n\
}                             \n\
.text-right {                 \n\
  text-align: left;           \n\
}                             \n\
.hidden-lg {                  \n\
  /*margin: 20px; */          \n\
}                             \n\
.table {                      \n\
  border: 1px solid black;    \n\
}                             \n\
</style>                      \n\
<head>                        \n\
<body>                        \n\
'

#https://www.slickcharts.com/sp500
tr = r'.*<(/?)tr>'
TR = re.compile(tr)
td1 = r'.*<td>(?P<index>\d+)</td>'
TD1 = re.compile(td1)

#   <a href="/Research/Quotes/Snapshot?symbol=BSFC">
ahref = r'(?P<indent>.*)<a href="/Research/Quotes/Snapshot\?symbol=(?P<symbol>\S+)">.*'
AHREF = re.compile(ahref)

#Peloton Interactive Inc has been mentioned in the news 2 times today
news = r'.*<span class="sr-only">(?P<prefix>.*) has been mentioned in the news (?P<suffix>.*)'
NEWS =  re.compile(news)

LOG_DIR = "./files"

#href:
#https://www.google.com/search?q=hillstream+biopharma+inc+stock

def get_timestamp():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d_%H-%M")

def GetPage(url, name, file):
    print(name + ':')
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    output_on = False
    in_unwanted_span = False
    matched_items = 0
    counter = 0
    for line in webpage.splitlines():
        line = line.decode('utf-8')
        line = str(line).replace(',', '')
        if line.find('<span class="sr-only">Link to symbol </span>') != -1:
            continue
        if line.find('<span class="visible-lg-inline">') != -1:
            in_unwanted_span = True
            output_on = False
            continue
        if in_unwanted_span and line.find('</span>') != -1:
            in_unwanted_span = False
            output_on = True
            continue
        if line.find('<table') != -1:
            output_on = True
        if line.find('</table>') != -1:
            file.write(line + "\n")
            return
        if output_on:
            m = AHREF.match(line)
            if m:
                counter = counter + 1
                line = m.group('indent') + '<a href="https://www.google.com/search?q=' + m.group('symbol') + '+stock' + '">'
                print("%2d: %4s - %s" %(counter, m.group('symbol'), get_timestamp()))
            m = NEWS.match(line)
            if m:
                print(m.group("prefix"))
                line = line.replace(m.group("prefix"), "")
                line = line.replace(" has been mentioned in the news ", "" )
            line = line.replace("No news today", "")
            line = line.replace('<th>Company</th>', '<th class="text-right" >Company</th>')
            line = line.replace('<th>Symbol</th>',  '<th class="text-right" width="7%">Symbol</th>')
            line = line.replace('<th class="text-right">Last</th>', '<th class="text-right" width="7%">Last</th>')
            line = line.replace('<th class="text-right">Today\'s Change</th>', '<th class="text-right" width="17%">Today\'s Change</th>')
            line = line.replace('<th class="text-right">Volume</th>', '<th class="text-left"  width="10%">Volume</th>')
            line = line.replace('<th class="text-right">High</th>', '<th class="text-right" width="7%">High</th>')
            line = line.replace('<th class="text-right">Low</th>', '<th class="text-right" width="7%">Low</th>')
            line = line.replace('<th class="text-left">In the News</th>', '<th class="text-left"  width="17%">In the News</th>')
            file.write(line + "\n")
    return

def get_movers():
    out_file = open('US_Market_Movers_' + get_timestamp() + '.html', 'w')
    if out_file:
        out_file.write(header)
        out_file.write('<h2> US Market Gainers: </h2>\n')
        GetPage('https://www.etrade.wallst.com/Research/Markets/Movers?index=US&type=percentGainers', 'Gainers', out_file)
        out_file.write('<h2> US Market Losers: </h2>\n')
        GetPage('https://www.etrade.wallst.com/Research/Markets/Movers?index=US&type=percentLosers', 'Losers', out_file)
        out_file.write("</body>\n</html>\n")
        out_file.close()

def main():
    get_movers()

if __name__ == "__main__":
    main()

