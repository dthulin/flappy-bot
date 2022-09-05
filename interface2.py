from turtle import width
from pyautogui import *
import pyautogui
import time
import keyboard
import win32api, win32con
import mss
from PIL import Image
import time
import neat
import pickle as pickle
import os
from pathlib import Path

SCORE = 0
GENERATION = 0
MAX_FITNESS = float('-inf')
BEST_GENOME = 0
sleepTime = .005


def pressSpace():
    '''
    one press, one release.
    accepts as many arguments as you want. e.g. press('left_arrow', 'a','b').
    '''
    win32api.keybd_event(0x20,0,0,0)
    time.sleep(sleepTime)
    win32api.keybd_event(0x20,0,win32con.KEYEVENTF_KEYUP,0)

def game(genome, config):
    net = neat.nn.FeedForwardNetwork.create(genome, config)

    global SCORE


    running = True
    pipeSeenCounter = 0
    pipeScoreCounter = 0
    floorY = int(200)
    floorX = int(0)
    birdY = int(160)
    birdX = int(32)
    vel = 0
    lastVel = 0
    tryCounter = 0
    afterSpaceCount = 0
    time.sleep(2)
    start = time.time()
    lastPressed = time.time()
    end = time.time()
    pipeBottomImage = Image.open('assets/PipeBottom.png')
    reg1=915
    reg2=400
    reg3=245
    reg4=450
    pic = pyautogui.screenshot(region=(reg1,reg2,reg3,reg4))
    highestScore = 0
    pipeScored = False

    while keyboard.is_pressed('q') == False and running:
        pic = pyautogui.screenshot(region=(reg1,reg2,reg3,reg4))
        width, height = pic.size
        r,g,b=pic.getpixel((25,350))
        if((r == 23 and g == 166 and b == 76)or(r == 22 and g == 159 and b == 73)):
            highestScore = (pipeScoreCounter,highestScore)[highestScore>pipeScoreCounter]
            pipeScoreCounter = 0
            pipeSeenCounter = 0
            if tryCounter > 0:
                print('GAME OVER! Attempt %s Score: %s Highest: %s'%(tryCounter,pipeScoreCounter,highestScore))
            if tryCounter < 5:
                tryCounter = tryCounter + 1
                print('Begining Attempt #%s:'%(tryCounter))
                time.sleep(.5)
                pyautogui.click(950, 750)
                time.sleep(1)
                floorY = int(200)
                floorX = int(0)
                birdY = int(160)
                birdX = int(32)
                pipeScored = False
                vel = 0
                lastVel = 0
                running = True
                afterSpaceCount = 0
                r=1
                b=1
                g=1
                end = time.time()
                start = time.time()
                lastPressed = time.time()
                pressSpace()
            else:
                end = time.time()
                print('NO MORE ATTEMPTS!')
                running = False
        if (running):
            pipeLocate = pyautogui.locate(pipeBottomImage,pic,grayscale=True)
            for y in range(height):
                r,g,b=pic.getpixel((birdX,y))
                if((r == 250 and g == 250 and b == 250) or (r == 221 and g == 221 and b == 221)):
                    birdY = y
                    break
            prevFloorY = floorY
            if pipeLocate != None:
                floorX = pipeLocate[0]
                floorY = pipeLocate[1]
            if (floorY != prevFloorY):
                pipeSeenCounter = pipeSeenCounter + 1
                print('Floor Change %s from %s to %s'%(pipeSeenCounter, prevFloorY,floorY))
            else:
                if(not pipeScored and floorX < birdX):
                    pipeScored = True
                    pipeScoreCounter = pipeScoreCounter + 1
                    SCORE = SCORE + pipeScoreCounter * 100
            midYWithOffset = floorY-70+30
            distanceFromOptimalY = abs(midYWithOffset-birdY)
            fitness = SCORE - (distanceFromOptimalY,500)[birdY<85] + (time.time()-start)
            inp = (birdY,floorY,floorX,afterSpaceCount,time.time()-lastPressed)
            output = net.activate(inp)
            if (output[0]>=0.5):
                afterSpaceCount = 0
                lastPressed = time.time()
                pressSpace()
            else: 
                afterSpaceCount = 1 + afterSpaceCount
                time.sleep(sleepTime)
    return(fitness)

def eval_genomes(genomes, config):
	global SCORE
	global GENERATION, MAX_FITNESS, BEST_GENOME

	GENERATION += 1
	i = 0
	for genome_id, genome in genomes:
		i+=1
		genome.fitness = game(genome, config)
		if genome.fitness is None:
			genome.fitness = float('-inf') #fixes errors on early termination
		print("Gen : {} Genome # : {}  Fitness : {} Max Fitness : {}".format(GENERATION,i,genome.fitness, MAX_FITNESS))
		if (genome.fitness):
			if genome.fitness >= MAX_FITNESS:
				MAX_FITNESS = genome.fitness
				BEST_GENOME = genome
		SCORE = 0

config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         'config')

pop = neat.Population(config)
stats = neat.StatisticsReporter()
pop.add_reporter(stats)

winner = pop.run(eval_genomes, 30)

print(winner)

outputDir = os.getcwd() + '/bestGenomes'
Path(outputDir).mkdir(parents =True, exist_ok=True)
os.chdir(outputDir)
serialNo = len(os.listdir(outputDir))+1
outputFile = open(str(serialNo)+'_'+str(int(MAX_FITNESS))+'.p','wb' )

pickle.dump(winner, outputFile)