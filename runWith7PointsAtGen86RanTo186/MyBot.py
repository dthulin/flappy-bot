from turtle import width
from pyautogui import *
import pyautogui
import time
import keyboard
import win32api, win32con
from PIL import Image
import time
import neat
import pickle as pickle
import os
from pathlib import Path
import math

pyautogui.FAILSAFE = False
# ^^^^ Careful with this one ^^^^
# FAILSAFE kills the program if you jam your mouse into the corner of the screen or something like that.
# This turns off that feature, making it possible if you don't have something like the press Q to terminate
# This code is unsafe, because there is no q failsafe in "for genome_id, genome in genomes:" and I rely
# on being able to grab control of the mouse long enough to click on the terminal and kill it with CTRL+C

SCORE = 0
HIGHESTSCORTHISROUND = 0
HIGHESTSCORE = 0
GENERATION = 0
MAX_FITNESS = float('-inf')
GEN_WITH_MAX_F = 0
GENOME_WITH_MAX_F = 0
MAX_FITNESS_THIS_GEN = float('-inf')
MAX_FITNESS_LAST_GEN = float('-inf')
BEST_GENOME = 0
sleepTime = .005
normalizePassTo = .1
GAMESPLAYED = 0
GAMESPLAYED = 0
pipeBottomImage = Image.open('assets/PipeBottom.png')


def pressSpace():
    '''
    one press, one release.
    accepts as many arguments as you want. e.g. press('left_arrow', 'a','b').
    '''
    pyautogui.press('space')
    # win32api.keybd_event(0x20,0,0,0)
    time.sleep(sleepTime)
    # win32api.keybd_event(0x20,0,win32con.KEYEVENTF_KEYUP,0)

def game(genome, config):
    net = neat.nn.FeedForwardNetwork.create(genome, config)

    global SCORE
    global HIGHESTSCORTHISROUND
    global HIGHESTSCORE
    global GAMESPLAYED

    reg1=915
    reg2=400
    reg3=245
    reg4=450
    running = True
    pipeSeenCounter = 0
    pipeScoreCounter = 0
    autoPilot = True
    floorX = int(reg3)
    prevFloorX = floorX
    floorY = int(200)
    prevFloorY = floorY
    floorYDebounce = [floorY,floorY]
    birdY = int(160)
    birdX = int(32)
    tryCounter = 0
    afterSpaceCount = 0
    time.sleep(2)
    start = time.time()
    birdFound = False
    # birdLastSeen = time.time()
    # birdFlewAway = False
    lastPressed = time.time()
    end = time.time()
    pic = pyautogui.screenshot(region=(reg1,reg2,reg3,reg4))
    pipeScored = True
    totalJumpedPerRound = 0
    fitness = 0
    gameOver = False
    passCounter = 0
    passLogStart = time.time()
    passLogEnd = time.time()

    while keyboard.is_pressed('q') == False and running:
        passLogEnd = time.time()
        if(passLogEnd-passLogStart < normalizePassTo):
            sleep(normalizePassTo-(passLogEnd-passLogStart))
            passLogEnd = time.time()
        # print('Pass was:', passLogEnd-passLogStart)
        passLogStart = passLogEnd
        if not autoPilot and not gameOver:
            passCounter += 1
        # if tryCounter > 0 and time.time()-birdLastSeen>1.25:
        #     end = time.time()
        #     birdFlewAway = True
        #     sleep(2)
        pic = pyautogui.screenshot(region=(reg1,reg2,reg3,reg4))
        width, height = pic.size
        r,g,b=pic.getpixel((25,350))
        if((r == 23 and g == 166 and b == 76)or(r == 22 and g == 159 and b == 73)):
            # if not birdFlewAway:
            #     end = time.time()
            if pipeScoreCounter>HIGHESTSCORTHISROUND:
                HIGHESTSCORTHISROUND = pipeScoreCounter
            if pipeScoreCounter>HIGHESTSCORE:
                HIGHESTSCORE = pipeScoreCounter
            if tryCounter > 0:
                if not autoPilot:
                    GAMESPLAYED += 1
                    print('GAME %s OVER! | Score: %s | Highest This Gen: %s | Highest Overall: %s'%(GAMESPLAYED,pipeScoreCounter,HIGHESTSCORTHISROUND,HIGHESTSCORE))
                # if(birdFlewAway):
                #     print('After %s jumps the bird flew away...'%(totalJumpedPerRound))
                #     fitness = float('-inf')
                #     birdFlewAway = False
                # if(totalJumpedPerRound<1):
                #     print('After not even trying bird went splat...')
                #     fitness = float('-inf')
            if tryCounter < 1:
                gameOver = False
                running = True
                tryCounter += 1
                time.sleep(.5)
                pyautogui.moveTo(50, 50)
                pyautogui.click(950, 750)
                pyautogui.moveTo(50, 50)
                time.sleep(1)
                # birdLastSeen = time.time()
                # birdFlewAway = False
                start = time.time()
                lastPressed = time.time()
                pressSpace()
                totalJumpedPerRound = 0
            else:
                tryCounter = 0
                gameOver = True
                if not autoPilot:
                    running = False
            autoPilot = True
            pipeScoreCounter = 0
            pipeSeenCounter = 0
            floorX = int(reg3)
            prevFloorX = floorX
            floorY = int(200)
            prevFloorY = floorY
            floorYDebounce = [floorY,floorY]
            birdY = int(160)
            birdX = int(32)
            pipeScored = True
            afterSpaceCount = 0
        if (not gameOver):
            gameOver = True
            birdFound = False
            for y in range(height):
                r,g,b=pic.getpixel((birdX,y))
                if r<180:
                    gameOver = False
                if((r == 250 and g == 250 and b == 250) or (r == 221 and g == 221 and b == 221)):
                    birdY = y
                    gameOver = False
                    birdFound = True
                    # birdLastSeen = time.time()
                    break
            if not gameOver:
                # print('Looking for pipe...')
                pipeLocate = pyautogui.locate(pipeBottomImage,pic)
                prevFloorX = floorX
                prevFloorY = floorY
                if pipeLocate != None:
                    floorYDebounce[1] = floorYDebounce[0]
                    floorYDebounce[0] = pipeLocate[1]
                    if pipeLocate[1] == prevFloorY:
                        floorX = pipeLocate[0]
                    else:
                        # print('Pipe X found: ',floorX,math.dist([prevFloorX],[floorX]))
                        if (floorYDebounce[0] == floorYDebounce[1]):
                            if not pipeScored:
                                pipeScoreCounter += 1
                                SCORE = pipeScoreCounter * 1000
                            floorX = pipeLocate[0]
                            floorY = pipeLocate[1]
                            autoPilot = False
                            pipeSeenCounter += 1
                            pipeScored = False
                            print('Floor Change %s from %s to %s'%(pipeSeenCounter, prevFloorY, floorY))
                        else:
                            floorX-=25
                else:
                    if not autoPilot:
                        floorX-=25
                if(not pipeScored and floorX < birdX and birdFound and birdY < floorY and birdY > floorY-140):
                    pipeScored = True
                    pipeScoreCounter += 1
                    SCORE = pipeScoreCounter * 100
                if autoPilot:
                    if floorY < birdY+80 and afterSpaceCount > 3:
                        afterSpaceCount = 0
                        lastPressed = time.time()
                        pressSpace()
                    else: 
                        afterSpaceCount += 1
                        time.sleep(sleepTime)
                else:
                    # Mid is technically 70 since it's 140 high, but in the interest of illiciting a higher arc, hoping 100 will be better
                    midYWithOffset = floorY-100
                    # pyautogui.moveTo(floorX+reg1, midYWithOffset+reg2,_pause=False)
                    distanceFromOptimalY = math.dist([midYWithOffset],[birdY])

                    bonusPoints = 0
                    penalties = 0
                    bonusPoints += pipeSeenCounter * 50
                    bonusPoints += passCounter * 10

                    # More for deeper into pipe, 75 pixels deep = roughly the same as 500 for next pipe seen, no double dipping this with pipe seen though
                    if birdX > floorX and pipeSeenCounter == pipeScoreCounter:
                        bonus = ((birdX-floorX)**2)/100
                        if bonus > 50:
                            bonus = 50
                        bonusPoints += bonus

                    # Less points for further away, from optimal Y, power of two makes non linear, /1000 makes it so it doesn't eliminate last pipe seen score all the way
                    offTargetPenalty = (distanceFromOptimalY**2)/1000
                    if offTargetPenalty > 90:
                        offTargetPenalty = 90
                    penalties += offTargetPenalty

                    # Flew away penalty
                    if not birdFound:
                        penalties += 50

                    # Didn't even try penalty
                    if totalJumpedPerRound < 1:
                        penalties += 50
                    
                    # If bird flew in opposite direction of pipe, that's a big no-no. 50 points from Slytherine! (But only if floors are far enough apart)
                    if math.dist([prevFloorY],[floorY]) > 150 and math.dist([birdY],[floorY]) > math.dist([birdY],[prevFloorY]):
                        penalties += 50
                    # The above was in lue of higher score for further distance from this pipe to last which would be implemented as pipeScoreCounter multiplier in the SCORE adjustment
                    
                    fitness = SCORE - penalties + bonusPoints
                    # inp = (birdX,birdY,floorY,floorX,afterSpaceCount,time.time()-lastPressed)
                    inp = (distanceFromOptimalY, birdY-floorY, floorX,afterSpaceCount)
                    output = net.activate(inp)
                    if (output[0]>0.5):
                        afterSpaceCount = 0
                        lastPressed = time.time()
                        pressSpace()
                        totalJumpedPerRound += 1
                    else: 
                        afterSpaceCount += 1
                        time.sleep(sleepTime)
    return(fitness)


config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         'config')

outputDir = os.getcwd() + '/bestGenomes'
Path(outputDir).mkdir(parents =True, exist_ok=True)
os.chdir(outputDir)

def eval_genomes(genomes, config):
    global SCORE
    global HIGHESTSCORTHISROUND
    global GENERATION, MAX_FITNESS, GEN_WITH_MAX_F, GENOME_WITH_MAX_F, BEST_GENOME, MAX_FITNESS_THIS_GEN, MAX_FITNESS_LAST_GEN

    MAX_FITNESS_LAST_GEN = MAX_FITNESS_THIS_GEN
    MAX_FITNESS_THIS_GEN = float('-inf')
    GENERATION += 1
    i = 0
    for genome_id, genome in genomes:
        i+=1
        genome.fitness = game(genome, config)
        if genome.fitness is None:
            genome.fitness = float('-inf') #fixes errors on early termination
        print("Gen: {} | Genome#: {} | Fitness: {} | Max Gen Fitness: {} | Max Overall Fitness: {} | Max Gen/Genome#: {}:{}".format(GENERATION,i,genome.fitness,MAX_FITNESS_THIS_GEN,MAX_FITNESS,GEN_WITH_MAX_F,GENOME_WITH_MAX_F))
        if (genome.fitness):
            if genome.fitness >= MAX_FITNESS:
                GEN_WITH_MAX_F = GENERATION
                GENOME_WITH_MAX_F = i
                MAX_FITNESS = genome.fitness
                BEST_GENOME = genome
                if GENERATION > 5:
                    serialNo = len(os.listdir(outputDir))+1
                    outputFile = open(str(serialNo)+'_'+str(int(MAX_FITNESS))+'.p','wb' )
                    pickle.dump(genome, outputFile)
            if genome.fitness >= MAX_FITNESS_THIS_GEN:
                MAX_FITNESS_THIS_GEN = genome.fitness
        SCORE = 0
    HIGHESTSCORTHISROUND = 0
    print('**********')
    print("GEN COMPLETE: {} | Best Fitness: {} | Improvement Over Last: {}".format(GENERATION, MAX_FITNESS_THIS_GEN, MAX_FITNESS_THIS_GEN - MAX_FITNESS_LAST_GEN))
    print('**********')

pop = neat.Population(config)
stats = neat.StatisticsReporter()
pop.add_reporter(stats)

winner = pop.run(eval_genomes, 1000)

print(winner)

serialNo = len(os.listdir(outputDir))+1
outputFile = open(str(serialNo)+'_'+str(int(MAX_FITNESS))+'.p','wb' )

pickle.dump(winner, outputFile)