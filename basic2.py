from turtle import width
from pyautogui import *
import pyautogui
import time
import keyboard
import random
import win32api, win32con
import cv2
import mss
import mss.tools
from PIL import Image
from PIL import ImageGrab
import numpy as np
import cv2 as cv

import time

sleepTime = .005
def pressSpace():
    '''
    one press, one release.
    accepts as many arguments as you want. e.g. press('left_arrow', 'a','b').
    '''
    win32api.keybd_event(0x20, 0,0,0)
    time.sleep(sleepTime)
    win32api.keybd_event(0x20,0 ,win32con.KEYEVENTF_KEYUP ,0)
birdFoundCount = 0
floorY = int(200)
floorX = int(245)
birdY = int(160)
birdX = int(32)
birdYOffset = 80
iml = [None]*100
count = 1
vel = 0
lastVel = 0
running = True
afterSpaceCount = 1
time.sleep(1)
pyautogui.click(950, 750)
pyautogui.moveTo(50, 50)
time.sleep(.5)
# start = time.time()
pressSpace()
reg1=915
reg2=400
reg3=245
reg4=450
REGION = (reg1,reg2,reg1+reg3,reg2+reg4)
pipeBottomImage = cv.imread('assets/PipeBottom.png')
with mss.mss() as sct:
    while keyboard.is_pressed('q') == False and running:
        # end = time.time()
        # print(end - start)
        # start = time.time()
        img = np.array(ImageGrab.grab(bbox=REGION))
        img_cv = cv.cvtColor(np.array(img), cv.COLOR_RGB2BGR)
        width=reg3
        height=reg4
        r,g,b=img[350,25]
        if((r == 23 and g == 166 and b == 76)or(r == 22 and g == 159 and b == 73)):
            pyautogui.click(950, 750)
            pyautogui.moveTo(50, 50)
            time.sleep(.5)
            pressSpace()
            floorY = int(200)
            floorX = int(245)
            birdY = int(160)
            birdX = int(32)
            count = 1
            vel = 0
            lastVel = 0
            running = True
            afterSpaceCount = 1
            r=1
            b=1
            g=1
        
        pipeLocate = pyautogui.locate(pipeBottomImage,img_cv,grayscale=True)
        # pipeLocate = cv.matchTemplate(img_cv, pipeBottomImage,eval('cv.TM_CCORR'))
        
        prevBirdPos = birdY
        birdfound = False
        for y in range(height):
            r,g,b=img[y,birdX]
            # r,g,b =grab.pixel(birdX,y)
            if((r == 250 and g == 250 and b == 250) or (r == 221 and g == 221 and b == 221)):
                birdY = y + birdYOffset
                birdfound = True
                break
        lastVel = vel
        vel = birdY-prevBirdPos
        prevFloorY = floorY
        # print(min_val,max_val,min_loc,max_Pipeloc)
        # if (pipeLocate >= 1).any():
        #     min_val,max_val,min_loc,max_Pipeloc = cv.minMaxLoc(pipeLocate)
        #     floorX = max_Pipeloc[0]
        #     floorY = max_Pipeloc[1]
        if pipeLocate != None:
            floorX = pipeLocate[0]
            floorY = pipeLocate[1]
        if (floorY != prevFloorY):
            print('Floor Change from %s to %s'%(prevFloorY,floorY))
        if ((birdY > floorY or (vel > 0 and lastVel > 0 and vel > lastVel and (birdY + vel + (vel-lastVel) > floorY))) and (afterSpaceCount > 4 or (birdY>floorY+100 and floorX > 55))):
            afterSpaceCount = 1
            pressSpace()
        else: 
            afterSpaceCount = 1 + afterSpaceCount
            time.sleep(sleepTime)