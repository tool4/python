import numpy as np
import os
import fnmatch
import sys
import keyboard

arguments = len(sys.argv) - 1
direction = 0
position = 1
print('numargs: ', arguments)
while (arguments >= position):
    if(sys.argv[position] == "-c"):
        direction = 1
    if(sys.argv[position] == "-d"):
        direction = -1
    position = position + 1

pattern = "*.*"

print('direction: ', direction)

if(direction != 0):
  confirmation = input('All files here will be renamed, are you sure? [y/n] ')

if(confirmation == 'y'):
  for root, dirs, files in os.walk("."):
    for filename in files:
        if fnmatch.fnmatch(filename, pattern):
            newname = ''
            for i in filename:
              if ('A' < i < 'Z') or ('a' < i < 'z') or ('0' < i < '9'):
                newname += chr(ord(i)+direction)
              else:
                newname += i
            print(filename, ' --> ', newname)
            file = os.path.join(root, filename)
            newfile = os.path.join(root, newname)
            os.rename(file, newfile)
            if keyboard.is_pressed('q'):
                print('QUIT!')
                sys.exit()
            if keyboard.is_pressed('a'):
                delay = float(delay) * 2.0
                print('delay: ', delay)
            if keyboard.is_pressed('s'):
                delay = float(delay) / 2.0
                print('delay: ', delay)
