# -*- coding: Windows-1250 -*-

from __future__ import unicode_literals
import urllib.request
import sys
import re
import os
import fnmatch
#help (re)
# ----

program_name = sys.argv[0]
arguments = sys.argv[1:]
dry_run = False

if len(arguments) > 0 and arguments[0] == '--dry-run':
    dry_run = True

to_retrieve = ['Minimax', 'Czarna noc', '3 wymiary gitary', 'Ciemna Strona Mocy',
               'Atelier', 'Aksamit', 'Nocna Polska', 'Offensywa', 'Trzy kwadranse jazzu',
               'Radio młodych bandytów', 'Strefa rokendrola wolna od angola',
               'Koncert w Trójce', 'Manniak po ciemku', 'Potrójne Pasmo Przenoszenia']

# 'Koncert w trójce', 'Radio młodych bandytów', 'Nocna Polska', 'Teraz polskie'
# , 'Trójka pod Księżycem',
# ' Trójkowy Ossobowy', 'Trzy kwadranse jazzu', 'MO czyli Mało Obiektywnie',
# 'MO czyli Ma\xb3o Obiektywnie', 'Atelier'
#

#b"<a href=http://28storage.dktr.pl:8888/dl.php?fl=08_09_2019/rec-23-00-01.ogg>
regex1 = r'b"<a href=\s?(?P<ogg_url>[A-z0-9\:\/\.\:\?\=\_\-]+)>'
REGEX1 = re.compile(regex1)

#&#243;w
#... <te class=te><font color=#440> | </font>Minimax</te>
#regex2 = r'(?P<rec_name>[A-z0-9\:\/\.\:\?\=\_\-]+)<\/te>'
regex2 = r'b"(.*)font>(?P<rec_name>[A-z0-9\s\/\.\?\=\_\-\,\\\&\#\;]+)<'
REGEX2 = re.compile(regex2)

#http://28storage.dktr.pl:8888/dl.php?fl=08_09_2019/rec-22-00-01.ogg
#regex3 = r'(.*)fl\=(?P<rec_date>[0-9\_]+)\/rec\-(?P<rec_time>[0-9\_]+)\.ogg'
regex3 = r'(.*)fl\=(?P<rec_date>(.*))\/rec\-(?P<rec_time>(.*))\.ogg'
REGEX3 = re.compile(regex3)

#08_09_2019
regex4 = r'(?P<dd>\d\d)_(?P<mm>\d\d)_(?P<yyyy>\d\d\d\d)'
REGEX4 = re.compile(regex4)

#page = urllib.request.urlopen('http://3.dktr.pl/?sel=08_09_2019#')

import datetime
now = datetime.datetime.now()
print ("Script started at: " + now.strftime("%Y-%m-%d %H:%M:%S"))

this_yr = int(now.strftime("%Y"))
this_mm = int(now.strftime("%m"))
now = datetime.datetime.now()
this_dd = int(now.strftime("%d"))
#this_mon=12
#this_day=30

def parse_url(url):
    if dry_run:
        print(url)
        return
    now = datetime.datetime.now()
    print ("\n%s: %s" %(now.strftime("%H:%M:%S"), url), flush=True)
    page = urllib.request.urlopen(url)
    #html = page.read().decode('Windows-1250')
    #html = page.read().decode('iso-8859-2')
    html = page.read()
    ogg_file = ""
    for line in html.splitlines():
        title = "unknown"
        line2 = str(line)
        m1 = REGEX1.match(line2)
        if m1:
            ogg_file = m1.group('ogg_url')
        m2 = REGEX2.match(line2)
        if m2:
            title = m2.group('rec_name')
            m3 = REGEX3.match(ogg_file)
            date_str = "unknown"
            time_str = "unknown"
            if m3:
                date_str = m3.group('rec_date')
                time_str = m3.group('rec_time')
                m4 = REGEX4.match(date_str)
                if m4:
                    date_str = m4.group('yyyy') + "_" + m4.group('mm') + "_" + m4.group('dd')
            title = title.replace("\\xb3", "ł")
            title = title.replace("&#243;", "ó")
            title = title.replace("\xbf", "ż")
            title = title.replace("\\xb1", "ą")
            title = title.replace("\\xb6", "ś")
            title = title.replace("\x9c\\xe6", "ść")
            title = title.replace("\\xbf", "z")
            title = title.replace("\xc5\x82", "ł")
            title = title.replace("\\xf1", "ń")
            title = title.replace("&quot;", "")
            title = title.replace("\\xea", "ę")
            title = title.replace("\\xe6", "ć")
            title = title.replace("3/5/7", "3.5.7")
            title = title.replace("\\xbc", "ź")
            if title[0] == '&' or title[0] == ' ':
                continue;
            directory = title
            title1 = title.replace(" ", "_")
            dir_path = "Nagrania\\" + directory
            if os.path.isdir(dir_path) == False:
                print("Creating directory: " + dir_path)
                os.mkdir(dir_path)
            filename1 = "Nagrania\\" + date_str + "_" + time_str + "_" + title + ".ogg"
            filename2 = "Nagrania\\" + title + "_" + date_str + "_" + time_str + ".ogg"
            filename3 = "Nagrania\\" + title1 + "_" + date_str + "_" + time_str + ".ogg"
            filename4 = "Nagrania\\" + directory + "\\" + title1 + "_" + date_str + "_" + time_str + ".ogg"

            if title in to_retrieve:
                if os.path.isfile(filename1) or os.path.isfile(filename2) or os.path.isfile(filename3) or os.path.isfile(filename4):
                    print("file [%s] already exists." %(filename4), flush=True)
                else:
                    print("file1 [%s] not found." %(filename1), flush=True)
                    print("file2 [%s] not found." %(filename2), flush=True)
                    print("file3 [%s] not found." %(filename3), flush=True)
                    print("file4 [%s] not found." %(filename4), flush=True)
                    if ogg_file != "":
                        now = datetime.datetime.now()
                        #filename2 = filename2.replace(" ", "_")
                        print(title + " - downloading to: " + filename4 + " ...")
                        print ("started at: " + now.strftime("%H:%M:%S"), flush=True)
                        urllib.request.urlretrieve(ogg_file, filename4)
                        now = datetime.datetime.now()
                        print ("done at: " + now.strftime("%H:%M:%S"), flush=True)
                    else:
                        print("Invalid url: [%s]" %(ogg_file), flush=True)
            else:
                if title[:8] != "pozosta\\" and title != " -" :
                    print("\t[" + title + "]", flush=True)


#Trzy_kwadranse_jazzu_2020_03_28_23-00-01.ogg
regex5 = r'.*_(?P<yyyy>\d\d\d\d)_(?P<mm>\d\d)_(?P<dd>\d\d)_\d\d\-\d\d\-\d\d\.ogg'
REGEX5 = re.compile(regex5)

def find_last_file(folder):
    files_found = 0
    max_date = 0
    last_date_str = "unknown"
    last_file_str = "unknown"
    pattern = "*.ogg"
    for root, dirs, files in os.walk(folder):
        for filename in files:
            if fnmatch.fnmatch(filename, pattern):
                full_path = os.path.join(root, filename)
                files_found = files_found + 1
                m5 = REGEX5.match(filename)
                if m5:
                    date = int(m5.group('yyyy')) * 365 + int(m5.group('mm')) * 31 + int(m5.group('dd'))
                    #print("%d - %s: %d" %(files_found, filename, max_date))
                    if date > max_date:
                        max_date = date
                        last_date_str = m5.group('yyyy') + "_" + m5.group('mm') + "_" + m5.group('dd')
                        last_file_str = full_path
                        last_yr = int(m5.group('yyyy'))
                        last_mm = int(m5.group('mm'))
                        last_dd = int(m5.group('dd'))
    print("%d files found - last one: %s: %s %d_%d_%d" %(files_found, last_file_str, last_date_str, last_yr, last_mm, last_dd))
    return (last_yr, last_mm, last_dd)

def scan_whole_year():
    for y in range(this_yr - 1, this_yr + 1):
        for m in range(1, 13):
            if (y < this_yr and m < this_mm) or (y >= this_yr and m > this_mm) :
                pass
            else:
                for d in range(1, 32):
                    if (y < this_yr and m <= this_mm and d < this_dd) or (y >= this_yr and m >= this_mm and d > this_dd) :
                        pass
                    else:
                        url = "http://3.dktr.pl/?sel=" + str(d).zfill(2) + "_" + str(m).zfill(2) + "_" + str(y)
                        #print(" date: %02d-%02d-%04d" %(d, m, y))
                        parse_url(url)

def scan_range(from_yr, from_mm, from_dd):
    now = datetime.datetime.now()
    this_dd = int(now.strftime("%d"))
    if this_yr > from_yr:
        print("Year overlapping not implemented! watch out...")
    if this_mm > from_mm:
        print("Month overlapping not implemented! watch out...")
    for y in range(from_yr, this_yr + 1):
        print("scanning range: %d_%d_%d - %d_%d_%d " %(from_yr, from_mm, from_dd, this_yr, this_mm, this_dd))
        for m in range(from_mm, this_mm + 1): #no overlapping here...
            print("from day: %d to_day: %d " %(from_dd, this_dd))
            if this_mm > from_mm:
                for d in range(from_dd, 32):
                    url = "http://3.dktr.pl/?sel=" + str(d).zfill(2) + "_" + str(m).zfill(2) + "_" + str(y)
                    print(" date: %02d-%02d-%04d" %(d, m, y))
                    parse_url(url)
                from_mm = from_mm + 1
                from_dd = 1
                continue
            for d in range(from_dd, this_dd + 1):
                url = "http://3.dktr.pl/?sel=" + str(d).zfill(2) + "_" + str(m).zfill(2) + "_" + str(y)
                print(" date: %02d-%02d-%04d" %(d, m, y))
                parse_url(url)

(last_yr, last_mm, last_dd) = find_last_file("Nagrania")
scan_range(last_yr, last_mm, last_dd)
os.sys.exit(0)
