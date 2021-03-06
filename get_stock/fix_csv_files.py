#import plotly
import plotly.graph_objects as go
import pandas as pd
import sys
import re
import os
import fnmatch

overwrite = False
if len(sys.argv) > 1:
    if sys.argv[1] == '-o':
        overwrite = True

pattern0 = "*.csv"
folder = '.'

for root, dirs, files in os.walk(folder):
    for filename in files:
        if fnmatch.fnmatch(filename, pattern0):
            full_path = os.path.join(root, filename)
            if filename != 'sp500.csv':
                filename = full_path
            if filename.find("&") != -1:
                print("&file: " + full_path)
                os.rename(full_path, full_path.replace("&", "and"))

                #f = open(filename, "r")
                #w = open(filename+'_temp', "w")
                #i = 0
                #for line in f:
                #    if i == 0:
                #        if line[len(line)-2] == ',':
                #            print(str(i) + ': ' + line[:-1])
                #        else:
                #            line = line[:-1]
                #            line = line + ',\n'
                #            print(str(i) + ': ' + line[:-1])
                #    else:
                #        print(str(i) + ': ' + line[:-1])
                #    w.write(line)
                #    i = i  + 1
                #f.close()
                #w.close()
                ## swap files:
                #f = open(filename+'_temp', "r")
                #w = open(filename, "w")
                #for line in f:
                #    w.write(line)
                #f.close()
                #w.close()
