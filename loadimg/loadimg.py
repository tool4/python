import numpy as np
import cv2
import os
import fnmatch
import sys

arguments = len(sys.argv) - 1

fullscreen = 0
delay = 1       # second
position = 1
while (arguments >= position):
    if(sys.argv[position] == "-f"):
        fullscreen = 1
    if(sys.argv[position] == "-t"):
        if(position < arguments):
            delay = sys.argv[position+1]
    position = position + 1

pattern = "*.jpg"

cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)

if( fullscreen == 1):
    cv2.setWindowProperty("window", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

for root, dirs, files in os.walk("."):
    for filename in files:
        if fnmatch.fnmatch(filename, pattern):
            jpgfile = os.path.join(root, filename)
            print(jpgfile)
            img = cv2.imread(jpgfile)
            if (type(img) is np.ndarray):
                wx, wy, ww, wh = cv2.getWindowImageRect('window')
                img_height, img_width, img_depth = img.shape
                windowaspect = ww/wh
                imgaspect=img_width/img_height
                if(imgaspect < windowaspect):
                    #adjust to height
                    ratio = wh/img_height
                    img_height = img_height*ratio
                    img_width = img_width*ratio
                else:
                    #adjust to width
                    ratio = ww/img_width
                    img_height = img_height*ratio
                    img_width = img_width*ratio
                cv2.setWindowTitle("window", jpgfile)
                top = bottom = int((wh - img_height)/2)
                left = int((ww - img_width)/2)
                right = int((ww - img_width)/2)
                padColor = (55,55,55)
                newimg = cv2.resize(img,(int(img_width),int(img_height)))
                scaled_img = cv2.copyMakeBorder(newimg, top, bottom, left, right, borderType=cv2.BORDER_CONSTANT, value=padColor)
                cv2.imshow("window", scaled_img)
                cv2.waitKey(int(float(delay) * 1000))
cv2.destroyAllWindows()