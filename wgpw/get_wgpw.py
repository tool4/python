import sys
import urllib.request
from html.parser import HTMLParser


# PARSE:
class MyHTMLParser(HTMLParser):
    def __init__(self, tl):
        self.tl = int(tl)
        self.table_level = 0
        self.script_level = 0
        self.tr_level = 0
        self.td_level = 0
        self.a_level = 0
        self.column = 0
        self.td_stored = 0
        self.tr_stored = 0
        self.td_attr = ""
        self.num_td_attrs = 0
        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        if (tag == "table"):
            self.table_level = self.table_level + 1
        if (tag == "tr"):
            self.tr_level = self.tr_level + 1
        if (tag == "td"):
            self.td_level = self.td_level + 1
            self.num_td_attrs = 0
            for attribute in attrs:
                self.num_td_attrs = self.num_td_attrs + 1
                if attribute[0] == 'id':
                    self.td_attr = attribute[1]
        if (tag == "a"):
            self.a_level = self.a_level + 1
        if (tag == "script"):
            self.script_level = self.script_level + 1

    def handle_endtag(self, tag):
        if (tag == "table"):
            self.table_level = self.table_level - 1
        if (tag == "tr"):
            self.tr_level = self.tr_level - 1
            self.column = 0
            if(self.tr_stored == 1):
                print("")
            #if(self.td_attr =="c"):
            #print("  **** ", self.table_level, self.tr_level, self.td_level, self.td_attr, self.num_td_attrs);
            self.td_attr = ""
            self.tr_stored = 0
        if (tag == "td"):
            self.td_level = self.td_level - 1
            if(self.td_stored == 0):
                if(self.td_attr =="f13" and self.num_td_attrs == 1):
                    print("        ,", end='')
                #print(self.td_attr, end='')
            self.td_stored = 0
        if (tag == "a"):
            self.a_level = self.a_level - 1
        if (tag == "script"):
            self.script_level = self.script_level -1

    def handle_data(self, data):
        if (self.script_level <= 0):
            if (self.table_level == self.tl):
                if (self.tr_level == 6 and self.td_attr == "f13" and self.num_td_attrs == 1):
                    if (self.a_level > 0 or self.td_level > 0):
                        if(self.column == 1):
                            sys.stdout.write(" %10s" %(data));
                        else:
                            sys.stdout.write("%8s," %(data));
                        self.column = self.column + 1
                        self.td_stored = 1
                        self.tr_stored = 1

################ MAIN ##########################

local = 1

# get page
if(local):
    f=open("strona.html", "r")
    if f.mode == 'r':
        contents =f.read()

else:
    fp = urllib.request.urlopen("https://stooq.pl/t/?i=513&v=8")
    mybytes = fp.read()
    contents = mybytes.decode("utf8")
    fp.close()

level = 0
if (len(sys.argv) > 1):
    level = sys.argv[1]

parser = MyHTMLParser(level)
parser.feed(contents)

#https://stooq.pl/t/?i=513&v=8