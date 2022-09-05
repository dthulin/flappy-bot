from turtle import width
from pyautogui import *
import pyautogui
import time
import keyboard
import random
import win32api, win32con
import cv2
import neat

# from bot import bot
# bot = Bot()


def pressSpace():
    '''
    one press, one release.
    accepts as many arguments as you want. e.g. press('left_arrow', 'a','b').
    '''
    win32api.keybd_event(0x20, 0,0,0)
    time.sleep(.02)
    win32api.keybd_event(0x20,0 ,win32con.KEYEVENTF_KEYUP ,0)

floor = int(200)
birdPositionY = int(500)
birdPositionX = int(0)
count = 1
vel = 0
lastVel = 0
running = True
afterSpaceCount = 1
time.sleep(3)  
pressSpace()
while keyboard.is_pressed('q') == False and running:
    pic = pyautogui.screenshot(region=(915,400,265,450))
    width, height = pic.size
    pipeLocate = pyautogui.locate('PipeBottom.png',pic)
    prevBirdPosY = birdPositionY
    birdfound = False
    for y in range(height):
        r,g,b =pic.getpixel((32,y))
        if((r == 250 and g == 250 and b == 250) or (r == 221 and g == 221 and b == 221)):
            birdPositionY = y + 80
            birdfound = True
            break
    lastVel = vel
    vel = birdPositionY-prevBirdPosY
    prevFloor = floor
    if pipeLocate != None:
        floor = pipeLocate[1]
    #     print('pipeLocate')
    #     print(pipeLocate)

    # if birdLocate != None:
    #     print('I CAN SEES ITS!')
        # birdPositionY = birdLocate[1]
    #     print('Yup')
    # print(birdLocate)
    # print (birdPositionY, floor, birdPositionY + vel + (vel-lastVel))
    if (floor != prevFloor):
        print('Floor Change from %s to %s'%(prevFloor,floor))
    # bot.act(playerx, playery, playerVelY, lowerPipes)
    if (birdPositionY + vel + (vel-lastVel) > floor and (afterSpaceCount > 3 or birdPositionY+300>floor)):    
    #     print('Indeed!')
        # print('YES',birdPositionY,floor)
        afterSpaceCount = 1
        pressSpace()
    # print(birdPositionY,floor)
    else: 
        afterSpaceCount = 1 + afterSpaceCount
        time.sleep(.02)
        # print('NO',birdPositionY,floor)





# while 1:
#     time.sleep(.05)
#     # if pyautogui.locateOnScreen('PipeBottom.png') != None:
#     if pyautogui.locateOnScreen('BirdEye.png',confidence=0.7) != None:
#         print('I CAN SEES ITS!')
#     else:
#         print('Where is it...')


# next pipe
# x 1150
# y 240 800
# rgb 84,56,71 201,227,125


# bird
# x 950
# y 380 800
# rgb 250, 250, 250
# floor = int(800)

        #    'spacebar':0x20,
# while keyboard.is_pressed('q') == False:
#     # Find next pipe
#     for y in range(560):
#         if pyautogui.pixel(1150, 800-y)[0] == 84 and pyautogui.pixel(1150, 801-y)[0] == 201:
#             print('next pipe at '+str(800-y))
#             break
    # Find birdy

def run(config_file):
    """
    runs the NEAT algorithm to train a neural network to play flappy bird.
    :param config_file: location of config file
    :return: None
    """
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    #p.add_reporter(neat.Checkpointer(5))

    # Run for up to 50 generations.
    winner = p.run(eval_genomes, 50)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))

if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)