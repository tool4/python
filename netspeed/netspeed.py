# To install add the following line to /etc/crontab (hourly execution):
#
#    0 *    * * *   pi      python /home/pi/git/python/netspeed/netspeed.py > /dev/null 2>&1
#

import os
import re
import datetime
import sys

reg_download = r'Download: (?P<speed>\S+) Mbit/s'
REG_DOWNLOAD = re.compile(reg_download)
reg_upload = r'Upload: (?P<speed>\S+) Mbit/s'
REG_UPLOAD = re.compile(reg_upload)

def main():
    now = datetime.datetime.now()
    time = now.strftime('%H:%M:%S')
    date = now.strftime('%Y-%m-%d')
    #os.system('/home/pi/.local/bin/speedtest > /tmp/temp.txt')
    down = 'unknown'
    up = 'unknown'
    with open('/tmp/temp.txt') as file:
        for line in file:
            m1 = REG_DOWNLOAD.match(line)
            if m1:
                print("%s" %(m1.group('speed')))
                down = m1.group('speed')
            m2 = REG_UPLOAD.match(line)
            if m2:
                print("%s" %(m2.group('speed')))
                up = m2.group('speed')
    filename = "/var/www/html/netspeed/speed_%s.csv" %date
    if down != "unknown" and up != "unknown":
        out_file = open(filename, 'a')
        out_file.write("%s, %s, %s\n" %(time, down, up))
        out_file.close()

if __name__ == '__main__':
    sys.exit(main())
