from RPLCD.gpio import CharLCD
import socket
import fcntl
import struct
import time
import datetime
import RPi.GPIO as GPIO
import subprocess

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,
        struct.pack('256s', ifname[:15])
    )[20:24])

lcd = CharLCD(
    numbering_mode=GPIO.BCM,
    cols=16,
    rows=2,
    pin_rs=26,
    pin_e=19,
    pins_data=[13, 6, 5, 11],
    compat_mode = True)

def get_line( prefix, filename, suffix ):
    try:
        fp = open(filename, 'r')
        str = fp.readline()
        fp.close()
        s_len = len(str)
        if (s_len > 2):
            str = str[:-1]
            str.ljust(7)[:7]
            line = (prefix + str + suffix + 15*" ")[:15]
            print(line)
            return line
    except:
        return "Invalid file" + filename

true = 1
counter = 0
while true == 1:
    #per every 5 min:
    if( (counter % 300) == 0 ):
        lcd.cursor_pos = (0, 0)
        lcd.write_string("My IP address:")
        lcd.cursor_pos = (1, 0)
        lcd.write_string(get_ip_address('wlan0'))
        rc = subprocess.call("/home/pi/git/python/weather/get_folsom.sh")
        substr_c = get_line("Folsom: ", 'folsom_c.txt', " C")
        substr_f = get_line("Folsom: ", 'folsom_f.txt', " F")
        substr_hc = get_line("Today:  ", 'folsom_hc.txt', " C")
        substr_hf = get_line("Today:  ", 'folsom_hf.txt', " F")
        substr_desc = get_line("", 'folsom_desc.txt', "")
        time.sleep(1)
        
    counter = counter + 1    
    x = datetime.datetime.now()
    lcd.cursor_pos = (0, 0)
    lcd.write_string(x.strftime("%d %b  %H:%M:%S"))
    lcd.cursor_pos = (1, 0)
    len = 11
    if( (counter % len) < 2):
        lcd.write_string(substr_c)
    elif( (counter % len) <= 4):
        lcd.write_string(substr_f)
    elif( (counter % len) <= 6):
        lcd.write_string(substr_hc)
    elif( (counter % len) <= 8):
        lcd.write_string(substr_hf)
    elif( (counter % len) <= 10):
        lcd.write_string(substr_desc)
#    else:
#        lcd.write_string(u"playing: trojka")
    time.sleep(1)
