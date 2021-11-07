import os
import re
import math

ext= '.csv'

#08:40, 709.40, -2.70, -0.38,
regex1 = r'\s*(?P<time>\d+\:\d+),\s*(?P<price>\d+\.\d+),\s*(?P<change>\-?\d+\.\d+),\s*(?P<change_perc>\-?\d+\.\d+),.*'
#regex1 = r'\s+(?P<time>.*),.*'
REGEX1 = re.compile(regex1)

#  1, Apple Inc., AAPL, 6.031608, 121.49, 1.36, 1.13
regex2 = r'\s*(?P<index>\d*),\s*(?P<name>.*),\s*(?P<symbol>.*),\s*(?P<price>\d+\.\d+),\s*\-?(?P<change>\d+\.\d+),\s*\-?(?P<change_perc>\d+\.\d+),.*'
REGEX2 = re.compile(regex2)

#001_AAPL_Apple_Inc._2021_02_23_Tuesday.csv
regex_filename = r'(?P<index>\d\d\d)_(?P<symbol>\w+)_(?P<name>.*)_(?P<date>\d\d\d\d_\d\d_\d\d)_(?P<day>\w+).csv'

regex_filename = r'(?P<index>\d\d\d)_(?P<symbol>[A-Za-z0-9\.]+)_(?P<name>.*)_(?P<date>\d\d\d\d_\d\d_\d\d)_(?P<day>\w+).csv'
REGEX_FILENAME=re.compile(regex_filename)

def process_file(filename):
    max_diff = 0.0
    min_diff = 1000.0
    changes = []
    sum = 0.0
    mean = 0.0
    std_dev = 0.0
    with open(filename) as file:
        for line in file:
            m = REGEX1.match(line)
            if m:
                #print("\t%s" %(m.group('change_perc')))
                diff = float(m.group('change_perc'))
                changes.append(diff)
                sum = sum + diff
                if diff > max_diff:
                    max_diff = diff
                if diff < min_diff:
                    min_diff = diff
            if not m and line[0] != '#' and line.find('PRICE') == -1:
                m2 = REGEX2.match(line)
                #if m2:
                #    print("M2:\t%s" %(m2.group('change_perc')))
                #else:
                print("NOT MATCHED!\t%s - %s" %(filename, line))
                quit()
    items = len(changes)
    if items:
        mean = sum / items
        std_dev_sum = 0.0
        for change in changes:
            dev         = change - mean
            std_dev_sum = std_dev_sum + (dev * dev)
        std_dev = math.sqrt(std_dev_sum / items)
    return (min_diff, max_diff, mean, std_dev)

max_diff = 0.0
min_diff = 0.0
merge_files = True

if merge_files:
    if not os.path.isdir('per_symbol'):
        os.mkdir('per_symbol')

counter = 0
with open('mean_devs.csv', 'w') as dev_file:
    for root, dirs, files in os.walk("D:/python/sp500/2021"):
        for file in files:
            if file.endswith(ext):
                counter = counter + 1
                if merge_files:
                    mf = REGEX_FILENAME.match(file)
                    name = os.path.join(root, file)
                    if mf:
                        print("[%s] [%s] [%s] [%s] [%s] " %(mf.group('index'), mf.group('symbol'), mf.group('name'), mf.group('date'), mf.group('day')))
                        #with open('per_symbol/' + mf.group("index") + '_' + mf.group("symbol") + '.csv', 'a') as outFile:
                        newFileName = 'per_symbol/' + mf.group("symbol") + '_' + mf.group('name') +'.csv'
                        startFrom = 0
                        newFile = 0
                        if os.path.isfile(newFileName):
                            startFrom = 1
                        else:
                            newFile = 1
                        lineCnt = 0
                        with open(newFileName, 'a') as outFile:
                            with open(name) as inFile:
                                for line in inFile:
                                    if newFile:
                                        outFile.write('DATE, ' + line)
                                        newFile = 0
                                    elif lineCnt >= startFrom:
                                        outFile.write(mf.group('date') + ', ' + line)
                                    lineCnt = lineCnt + 1
                                    pass
                    else:
                        print("%s - %s" %(file, "NOT MATCHED"))
                        exit(-1)

                else:
                    #print(name)
                    #(low, high, mean, std_dev) = process_file(name)
                    low = high = mean = std_dev = 0.0
                    if low < min_diff:
                        min_diff = low
                    if high > max_diff:
                        max_diff = high
                    print("LOW: %.2f, MEAN: %.2f, HIGH: %.2f, STDDEV: %.2f, MIN: %.2f, MAX: %.2f" %(low, mean, high, std_dev, min_diff, max_diff))
                    dev_file.write('%s, %.2f,\n' %(file, std_dev))

if not merge_files:
    print("OVERALL: MIN: %.2f, MAX: %.2f" %(min_diff, max_diff))

print("processed %d files" %(counter))

