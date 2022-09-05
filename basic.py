from turtle import width
from pyautogui import *
import pyautogui
import time
import keyboard
import random
import win32api, win32con
# import cv2
import mss
# import mss.tools
from PIL import Image
import time
import math

sleepTime = .005
def pressSpace():
    '''
    one press, one release.
    accepts as many arguments as you want. e.g. press('left_arrow', 'a','b').
    '''
    win32api.keybd_event(0x20,0,0,0)
    time.sleep(sleepTime)
    win32api.keybd_event(0x20,0,win32con.KEYEVENTF_KEYUP,0)
birdPrintCount = 0
floorY = int(200)
floorX = int(245)
birdY = int(160)
birdX = int(32)
birdYOffset = 80
iml = []
count = 1
vel = 0
lastVel = 0
vel2 = 0
lastVel2 = 0
running = True
tryCounter = 0
afterSpaceCount = 1
time.sleep(2)
# pyautogui.click(950, 750)
# pyautogui.moveTo(50, 50)
# time.sleep(.5)
start = time.time()
lastPressed = time.time()
end = time.time()
# pressSpace()
pipeCounter = 0
reg1=915
reg2=400
reg3=245
reg4=450
now = time.time()
lastNow = time.time()
pipeBottomImage = Image.open('assets/PipeBottom.png')
reg={'left':reg1,'top':reg2,'width':245,'height':reg4}
pic = pyautogui.screenshot(region=(reg1,reg2,reg3,reg4))
with mss.mss() as sct:
    while keyboard.is_pressed('q') == False and running:
        # end = time.time()
        # print(end - start)
        # start = time.time()
        pic = pyautogui.screenshot(region=(reg1,reg2,reg3,reg4))
        width, height = pic.size
        r,g,b=pic.getpixel((25,350))
        # grab = sct.grab(reg)
        # pic = Image.frombytes("RGB", grab.size, grab.bgra, "raw", "BGRX")
        # width = reg3
        # height = reg4
        # r,g,b=grab.pixel(25,350)
        if((r == 23 and g == 166 and b == 76)or(r == 22 and g == 159 and b == 73)):
            tryCounter = tryCounter + 1
            print('Begining Attempt #%s:'%(tryCounter))
            time.sleep(.5)
            pyautogui.click(950, 750)
            # pyautogui.moveTo(50, 50)
            time.sleep(1)
            end = time.time()
            start = time.time()
            lastPressed = time.time()
            pressSpace()
            floorY = int(200)
            floorX = int(245)
            birdY = int(160)
            birdX = int(32)
            pipeCounter = 0
            count = 1
            vel = 0
            lastVel = 0
            running = True
            afterSpaceCount = 1
            r=1
            b=1
            g=1
        # else:
        #     print(r,g,b)

        
        # birdLocate = pyautogui.locateOnScreen('assets/Beak.png',confidence=0.8)
        # pipeLocate = pyautogui.locateOnScreen('assets/PipeBottom.png')
        # birdLocate = pyautogui.locate('assets/Beak.png',pic)
        pipeLocate = pyautogui.locate(pipeBottomImage,pic,grayscale=True)
        # if birdLocate != None:
        #     print('birdLocate')
        #     print(birdLocate)
        prevBirdPos = birdY
        birdfound = False
        for y in range(height):
            r,g,b=pic.getpixel((birdX,y))
            # r,g,b =grab.pixel(birdX,y)
            if((r == 250 and g == 250 and b == 250) or (r == 221 and g == 221 and b == 221)):
                birdY = y + birdYOffset
                birdfound = True
                # birdPrintCount=birdPrintCount+1
                # iml[birdPrintCount] = pyautogui.screenshot(region=(915-50+birdX,400-50+birdY-birdYOffset,100,100))
                break
        # if (not birdfound):
        #     print('Bird not found!!!')
        lastNow = now
        now = time.time()
        lastVel2=vel2
        lastVel = vel
        vel = math.dist([birdY],[prevBirdPos])
        vel2 = math.dist([birdY],[prevBirdPos])/math.dist([now],[lastNow])
        # if(prevBirdPos == birdY and count < 5):
        #     iml = pyautogui.screenshot(region=(925,400,275,450))
        #     iml.save(r"C:\Users\wdona\OneDrive\Documents\Code\Python\FlappyBot\screenshots\Investigate-%s.png"%(count))
        #     count+=1
        prevFloorY = floorY
        if pipeLocate != None:
            floorX = pipeLocate[0]
            floorY = pipeLocate[1]
        #     print('pipeLocate')
        #     print(pipeLocate)

        # if birdLocate != None:
        #     print('I CAN SEES ITS!')
        midYWithOffset = floorY-70+30
        distanceFromOptimalY = abs(midYWithOffset-birdY)
        print('BIRD Y:',birdY,(time.time()-start)*10,distanceFromOptimalY)
        if (floorY != prevFloorY):
            pipeCounter = pipeCounter + 1
            print('Floor Change %s from %s to %s'%(pipeCounter, prevFloorY,floorY))
        print('VEL 1 Now: %s Was: %s Acc: %s'%(vel, lastVel, math.dist([vel], [lastVel])))
        print('VEL 2 Now: %s Was: %s Acc: %s'%(vel2, lastVel2, math.dist([vel2], [lastVel2])/math.dist([now],[lastNow])))
        # pyautogui.moveTo(birdX+reg1, ((birdY + vel + (0,vel-lastVel)[vel > lastVel], birdY)[vel > 0 and lastVel > 0] +reg2),_pause=False)
        if ((birdY > floorY or (vel > 0 and lastVel > 0 and vel > lastVel and (birdY + vel + (vel-lastVel) > floorY))) and (afterSpaceCount > 4 or (birdY>floorY+100 and floorX > 55))):
        # if ((birdY > floorY ) and (afterSpaceCount > 4 or (birdY>floorY+100 and floorX > 55))):
            # birdPrintCount=birdPrintCount+1
            # iml.append({'image':pic,'y':birdY,'screenshot':pyautogui.screenshot(region=(915-50+birdX,400-50+birdY-birdYOffset,100,100))})
            afterSpaceCount = 1
            # print('JUMP!',birdY,floorY,vel,lastVel,afterSpaceCount)
            # pyautogui.moveTo(birdX+reg1, birdY+reg2,_pause=False)
            lastPressed = time.time()
            pressSpace()
        # print(birdY,floorY)
        else: 
            afterSpaceCount = 1 + afterSpaceCount
            time.sleep(sleepTime)
            # print('NO',birdY,floorY)

    for index, image in enumerate(iml):
        if image:
            im = image['image'].crop( (0, image['y']-50-birdYOffset, 100, image['y']+50-birdYOffset) )
            im.save(r"C:\Users\wdona\OneDrive\Documents\Code\Python\FlappyBot\screenshots\Investigate-%s-%s-crop.png"%(index,image['y']))
            image['screenshot'].save(r"C:\Users\wdona\OneDrive\Documents\Code\Python\FlappyBot\screenshots\Investigate-%s-%s-ss.png"%(index,image['y']))

