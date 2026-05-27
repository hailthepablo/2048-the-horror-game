# IMPORT LIBRARIES
# Imports the freakin' libraries

import random
from math import *
import platform
import os

# FILESYSTEM FUNCTIONS
# Only here because Windows is stupid and uses backslashes instead of forward slashes.
# I don't care about how DOS was back in the day. Fix ur files Bill Gates (this is a threat).

if platform.system() == "Windows":
    OS = False # Set to false since this garbage is not an acceptable operating system
else:
    OS = True # Congratulations your OS is made by sane people

def systemClear():
    if OS:
        os.system("clear")
    else:
        os.system("cls")

def charAssemble(pathList,char):
    finalPath = ""
    for i in pathList:
        finalPath = finalPath + i + char
    finalPath = finalPath[:-1]
    return finalPath

def pathAssemble(pathList):
    char = {True:"/",False:"\\"}[OS]
    return charAssemble(__file__.split(char)[:-2],char) + char + charAssemble(pathList,char)

# HANDY FUNCTIONS
# Functions that are useful to have but don't have one specific place they are supposed to be used in

def listSubtract(list1,list2):
    returnList = []
    for i in list1:
        if not i in list2:
            returnList = returnList + [i]
    return returnList

def stringToTuple(string):
    string = string.replace("(","")
    string = string.replace(")","")
    string = string.split(",")
    return tuple([int(i) for i in string])

def addDegrees(angle,amount):
    return (angle + amount) % 360
    
def ungrid(grid):
    returnList = []

    for i in grid:
        for j in i:
            returnList = returnList + [j]

    return returnList

def getBetweens(inpList,start,stop):
    if not ((start in inpList) and (stop in inpList)):
        return
    for i in range(len(inpList)):
        if inpList[i] == start:
            startingIndex = i
            break

    for i in range(len(inpList)):
        if inpList[i] == stop:
            stoppingIndex = i
            break

    return inpList[startingIndex+1:stoppingIndex]

def listify(string):
    returnList = []
    for i in string.split("\n"):
        if i != "":
            returnList = returnList + [i]
    return returnList

def correctLength(inpString,length):
    inpList = inpString.split()
    
    returnList = []
    for i in inpList:
        currentItem = i
        while len(currentItem) != length:
            currentItem = currentItem + "a"
        returnList = returnList + [currentItem]

    returnString = ""

    for i in returnList:
        returnString = returnString + i + "\n"

    returnString = returnString[0:-1]
    
    return returnString

def ref(referenceName,lineList):
    referenceName = "_REF " + referenceName + "\n"
    for i in range(len(lineList)):
        if lineList[i] == referenceName:
            currentIndex = i
            break
    finalText = ""
    while True:
        currentIndex = currentIndex + 1
        if (lineList[currentIndex] == "_END") or (lineList[currentIndex] == "_END\n"):
            return finalText.replace(">\n<","")[:len(finalText.replace(">\n<",""))-1]
        else:
            finalText = finalText + lineList[currentIndex]

# CONVERTER FUNCTIONS
# Converts between the backend side of the program and what's actually displayed on screen

def vectorize(rotation):
    rotation = rotation % 360
    if rotation == 0:
        return RIGHT
    elif rotation == 90:
        return UP
    elif rotation == 180:
        return LEFT
    elif rotation == 270:
        return DOWN
    
def angulize(dir):
    if dir == RIGHT:
        return 0
    elif dir == UP:
        return 90
    elif dir == LEFT:
        return 180
    elif dir == DOWN:
        return 270
    
def emojilize(rotation):
    if rotation == 0:
        return ">"
    elif rotation == 90:
        return "^"
    elif rotation == 180:
        return "<"
    elif rotation == 270:
        return "v"

def ableToMove(row):
    prevI = ""
    for i in row:
        if i == 0 or prevI == i:
            return True
        if i == "+":
            return False
        prevI = i
    return False

# DEFINE SPACE DICTIONARY
# Defines a dictionary so different types of spaces can correspond to different letters

spaceDict = {"a":[],"b":[0],"c":[90],"d":[180],"e":[270],"f":[180,270],"g":[90,180],"h":[0,90],"i":[0,270],"j":[0,180],"k":[90,270],"l":[0,90,180,270],"m":[90, 180, 270],"n":[0, 180, 270],"o":[0, 90, 270],"p":[0, 90, 180]}

# COMBINATION FORMULA AND NUMBER SPAWN PERCENTAGES
# Determines how numbers will be combined and what numbers can spawn

def combinationFormula(x):
    return x*2

percent90 = 2
percent10 = 4

# DISPLAY DATA CLASS
# Class for holding all graphical data about the current frame (i could've just used a list but no)

class DisplayData:
    def __init__(self,gridDisplay,hydra,door,roomType,frontBoxNum,gridHeight):
        self.gridDisplay = gridDisplay
        self.hydra = hydra
        self.door = door
        self.roomType = roomType
        self.frontBoxNum = frontBoxNum
        self.gridHeight = gridHeight

# BROCK'S CODE (Slightly altered to work with the display side)
# I (Logan) can't comment this out because only Brock knows what Brock codes

# ^^ The above comment is now innaccurate since the code is so intermixed now

"""remember who you are""" # But what if I can't
UP =    (0,1)
DOWN =  (0,-1)
LEFT =  (-1,0)
RIGHT = (1,0)

class Into2048:
    def resetVars(self):
        self.hydraOn = self.hydraOn_R
        self.playerPos = self.playerPos_R
        self.hydraPos = self.hydraPos_R
        self.game_over = self.game_over_R
        self.step = self.step_R

    def __init__(self, levelName, width=4, height=4, hydraOn=True, startingNumsOn=True, walls=[], doors=[]):
        self.hydraOn_R = hydraOn
        self.playerPos_R = "NO PLAYER POSITION"
        self.hydraPos_R = "NO HYDRA POSITION"
        self.game_over_R = False
        self.step_R = -1
        self.startingNumsOn = startingNumsOn
        self.width = width
        self.height = height
        self.walls = []
        self.doors = []

        #Possible temporary code, replace with better build2048 in the future 
        for i in range(self.width):
            for j in range(self.height):
                if (i == 0) and not ([(i,j,180)] in walls):
                    self.walls = self.walls + [(i,j,180)]
                
                if (i == width-1) and not ([(i,j,0)] in walls):
                    self.walls = self.walls + [(i,j,0)]
                
                if (j == 0) and not ([(i,j,270)] in walls):
                    self.walls = self.walls + [(i,j,270)]
                
                if (j == height-1) and not ([(i,j,90)] in walls):
                    self.walls = self.walls + [(i,j,90)]

        for i in walls:
            self.walls = self.walls + [i]
        #End of temporary code

        self.resetVars()
        
    #Generate a random 2048 number. Can only be 2 or 4
    def _generate_num(self):
        highestNum = self.getStats()[1]
        
        return random.choices([percent90,percent10], weights=(90,10))[0]
    
    #Generate and place 2 new tiles (1 if only 1 space is available)
    def generate_tiles(self,amount,number):
        if len(self.getEmptySlots()) < amount:
            self.game_over = "HydraJumpscare"
            return
        for i in random.sample(self.getEmptySlots(), k=amount):
            if number == "random":
                self.num_grid[i[0]][i[1]] = self._generate_num()
            else:
                self.num_grid[i[0]][i[1]] = number

    def spawn_player(self):
        self.playerPos = tuple(random.choice(self.getEmptySlots())) #This variable is used to find player position
        self.playerRot = [0,90,180,270][random.randint(0,3)]
        self.justMoved = False

    def spawn_hydra(self):
        spawnPosList = []
        for i in range(self.width):
            for j in range(self.height):
                if dist((i,j),self.playerPos) > 1.5:
                    spawnPosList = spawnPosList + [(i,j)]
        
        if self.hydraOn:
            self.hydraPos = tuple(random.choice(spawnPosList))
        else:
            self.hydraPos = (-1,-1)

    def move_player(self, dir):
        new_pos = tuple(self.playerPos[i] + dir[i] for i in range(2))
        
        if (self.playerPos[0],self.playerPos[1],angulize(dir)) in self.walls:
            return
        if new_pos == self.hydraPos:
            self.game_over = "HydraJumpscare"
        new_pos_value = self.num_grid[new_pos[0]][new_pos[1]]
        if new_pos_value != 0:
            if not self._push(new_pos, dir):
                return
            
        if new_pos == (self.playerPos[0]+vectorize(self.playerRot+180)[0],self.playerPos[1]+vectorize(self.playerRot+180)[1]):
            if not (self.playerPos[0],self.playerPos[1],self.playerRot) in self.walls:
                if not (self.playerPos[0],self.playerPos[1],self.playerRot+180) in self.walls:
                    # Really bad code, will improve later
                    self.pull()

        self.playerPos = new_pos
        
    def getEmptySlots(self):
        usingGrid = self.replaceSpaces(True,False)
        newEmpties = []
        
        for i in range(self.width):
            for j in range(self.height):
                if usingGrid[i][j] == 0:
                    newEmpties = newEmpties + [(i,j)]

        return newEmpties

    def rotate_player(self, amount):
        self.playerRot = addDegrees(self.playerRot,amount)

    def correctDirList(self,dirs):
        returnList = []

        for i in dirs:
            if not ((self.hydraPos[0],self.hydraPos[1],angulize(i)) in self.walls):
                returnList = returnList + [i]

        if returnList == []:
            returnList = [(0,0)]

        return returnList

    def enableHydra(self):
        if not self.hydraOn:
            self.hydraOn = True

            spawnPosList = []
            for i in range(self.width):
                for j in range(self.height):
                    if dist((i,j),self.playerPos) > 1.5:
                        spawnPosList = spawnPosList + [(i,j)]

            self.hydraPos = tuple(random.choice(spawnPosList))

    def move_hydra(self, approach_probability=50):
        if self.hydraOn:
            
            if random.choices((True, False), weights=(approach_probability, 100-approach_probability)): #Random movement
                dirs = []
                if self.hydraPos[0] < self.playerPos[0]:
                    dirs.append(DOWN)
                else:
                    dirs.append(UP)
                if self.hydraPos[1] < self.playerPos[1]:
                    dirs.append(RIGHT)
                else:
                    dirs.append(LEFT)
                dir = random.choice(self.correctDirList(dirs))
            else:
                dir = random.choice(self.correctDirList([UP,DOWN,LEFT,RIGHT]))
            
            new_pos = tuple(self.hydraPos[i] + dir[i] for i in range(2))
            if self.playerPos == new_pos:
                if self.justMoved:
                    return
                else:
                    self.game_over = "HydraJumpscare"
            if new_pos[0] < 0 or new_pos[0] >= len(self.num_grid) or new_pos[1] < 0 or new_pos[1] >= len(self.num_grid[0]):
                return
            self.hydraPos = new_pos

    def _push(self, pos, dir):
        #If pushing into wall
        if (pos[0],pos[1],angulize(dir)) in self.walls:
            return False
        #If pushing into block of equal value (merge)
        if self.num_grid[pos[0]][pos[1]] == self.num_grid[pos[0]+dir[0]][pos[1]+dir[1]]:
            self.num_grid[pos[0]][pos[1]] = 0
            
            self.num_grid[pos[0]+dir[0]][pos[1]+dir[1]] = combinationFormula(self.num_grid[pos[0]+dir[0]][pos[1]+dir[1]])

            return True
        #If pushing into nothing
        if self.num_grid[pos[0]+dir[0]][pos[1]+dir[1]] == 0:
            self.num_grid[pos[0]+dir[0]][pos[1]+dir[1]] = self.num_grid[pos[0]][pos[1]]
            self.num_grid[pos[0]][pos[1]] = 0
            return True
        #If pushing into block pushing into nothing
        elif self._push((pos[0]+dir[0], pos[1]+dir[1]), dir):
            self.num_grid[pos[0]+dir[0]][pos[1]+dir[1]] = self.num_grid[pos[0]][pos[1]]
            self.num_grid[pos[0]][pos[1]] = 0
            return True

        return False
    
    def pull(self):
        pulledNum = self.get_facing(self.num_grid,1,vectorize(self.playerRot))
        self.num_grid[self.playerPos[0]][self.playerPos[1]] = pulledNum
        self.num_grid[self.playerPos[0]+vectorize(self.playerRot)[0]][self.playerPos[1]+vectorize(self.playerRot)[1]] = 0

    def posInDirection(self, distance, dir):
        return tuple(self.playerPos[i] + dir[i]*distance for i in range(2))

    def get_facing(self, grid, distance, dir):
        frontPos = tuple(self.playerPos[i] + dir[i]*distance for i in range(2))
        if frontPos[0] < 0 or frontPos[0] >= len(grid) or frontPos[1] < 0 or frontPos[1] >= len(grid[0]):
            return
        return grid[frontPos[0]][frontPos[1]]

    def getRow(self, grid, dir):
        if dir == UP:
            blocker = self.height-1
            referenceCoord = self.playerPos[1]
        elif dir == DOWN:
            blocker = 0
            referenceCoord = self.playerPos[1]
        elif dir == RIGHT:
            blocker = self.width-1
            referenceCoord = self.playerPos[0]
        elif dir == LEFT:
            blocker = 0
            referenceCoord = self.playerPos[0]

        returnRow = []
        
        for i in range(abs(blocker-referenceCoord)):
            returnRow = returnRow + [self.get_facing(grid,i+1,dir)]

        return returnRow
    
    def replaceSpaces(self,enablePlayer=True,enableHydra=True):
        replacedGrid = [[self.num_grid[i][j] for j in range(self.height)] for i in range(self.width)]
        for i in range(self.width):
            for j in range(self.height):
                if self.playerPos == (i,j) and enablePlayer:
                    replacedGrid[i][j] = emojilize(self.playerRot)
                if self.hydraPos == (i,j) and enableHydra:
                    replacedGrid[i][j] = "+"
        
        return replacedGrid
    
    def alterNum(self,dir,num,wallRestrict):
        numberPos = self.posInDirection(1,dir)

        exeptionStatements = [(numberPos[0] < 0),(numberPos[1] < 0),(numberPos[0] > self.width-1),(numberPos[1] > self.height-1)]

        if True in exeptionStatements:
            return

        wallRestrict = [True,not ((self.playerPos[0],self.playerPos[1],angulize(dir)) in self.walls)][int(wallRestrict)]

        if wallRestrict:
            self.num_grid[numberPos[0]][numberPos[1]] = num

    def checkWin(self):
        numberList = ungrid(self.num_grid)
        if 2048 in numberList:
            self.game_over = "WinScreen"

    def getStats(self):
        allNums = []

        for i in range(self.width):
            for j in range(self.height):
                allNums = allNums + [self.num_grid[i][j]]

        totalScore = 0

        for i in allNums:
            totalScore = totalScore + i

        highestNum = 0

        for i in allNums:
            if i > highestNum:
                highestNum = i

        return (totalScore,highestNum)

    # DISPLAY
    # This function actually displays the things that are returned by the get display functions.

    def getGridDisplay(self,enablePlayer,enableHydra):
        grid = self.replaceSpaces(enablePlayer,False)

        stringGrid = ""
        for j in range(self.height):
            for i in range(self.width):
                if ((i,self.height-j-1) == self.hydraPos) and enableHydra:
                    hydraIndicator = "+"
                else:
                    hydraIndicator = int(enableHydra)*" "
                currentNumber = str(grid[i][self.height-j-1])
                currentNumber = hydraIndicator + currentNumber + " "*(4-len(currentNumber))
                stringGrid = stringGrid + currentNumber + " "
            stringGrid = stringGrid + "\n"
        return stringGrid
    
    def getRoomDisplay(self):
        wallChecks = []

        wallChecks = wallChecks + [(self.playerPos[0],self.playerPos[1],addDegrees(self.playerRot,90))]
        wallChecks = wallChecks + [(self.playerPos[0],self.playerPos[1],self.playerRot)]
        wallChecks = wallChecks + [(self.playerPos[0],self.playerPos[1],addDegrees(self.playerRot,270))]
        wallChecks = wallChecks + [(self.playerPos[0],self.playerPos[1],addDegrees(self.playerRot,180))]

        wallData = ""
        for i in wallChecks:
            if i in self.walls:
                wallData = wallData + "t"
            else: 
                wallData = wallData + "f"
        
        return wallData

    # START GAME
    # Starts the game by initializing variables and spawning the player and hydra

    def start(self):
        self.hydraMode = 0
        self.gridPlayback = []
        self.actionPlayback = ["Started game"]
        self.spawnee = "2"
        self.heldNumber = 0
        
        self.disableHydraMovement = False
        self.dadJumpscare = False
        self.step = 0

        self.resetVars()

        self.num_grid = [[0 for j in range(self.height)] for i in range(self.width)]

        if self.startingNumsOn:
            self.generate_tiles(2,"random")

        self.spawn_player()
        self.spawn_hydra()

    # UPDATE GAME
    # Computes the next frame of the game based on the player's input

    def update(self,action,timer):
        if len(self.actionPlayback)-1 == 0.00: # 0.00 should be Hydra spawn time
            self.enableHydra()

        hydraNear = False
        playerPosCheck = self.playerPos
        for i in [0,90,180,270]:
            if self.posInDirection(1,vectorize(addDegrees(self.playerRot,i))) == self.hydraPos:
                hydraNear = True
            
        if (not ableToMove(self.getRow(self.replaceSpaces(),vectorize(self.playerRot)))) and (not ableToMove(self.getRow(self.replaceSpaces(),vectorize(addDegrees(self.playerRot,180))))):
            blocked = True
        else:
            blocked = False

        if hydraNear and blocked:
            self.disableHydraMovement = True

        doorRandomizer = random.randint(1,10)

        self.gridPlayback = self.gridPlayback + [self.getGridDisplay(True,True)]

        if action == "forward":
            self.actionPlayback = self.actionPlayback + ["Moved forward"]
            self.move_player(vectorize(self.playerRot))
        if action == "left":
            self.actionPlayback = self.actionPlayback + ["Turned left"]
            self.rotate_player(90)
        if action == "backward":
            self.actionPlayback = self.actionPlayback + ["Moved backward"]
            self.move_player(vectorize(addDegrees(self.playerRot,180)))
        if action == "right":
            self.actionPlayback = self.actionPlayback + ["Turned right"]
            self.rotate_player(-90)
        
        if (action != None and self.hydraMode == 0) or (timer == 0 and self.hydraMode == 1):
            if playerPosCheck != self.playerPos:
                self.justMoved = True
            else:
                self.justMoved = False

            if self.disableHydraMovement:
                self.disableHydraMovement = False
            else:
                self.move_hydra(50)
        
        if action == "spawn":
            self.actionPlayback = self.actionPlayback + ["Spawned numbers"]
            self.generate_tiles(2,"random")
        
        if action == "destroy":
            self.actionPlayback = self.actionPlayback + ["Destroyed number"]
            self.alterNum(vectorize(self.playerRot),0,True)

    def getDisplayData(self):
        gridDisplay = self.getGridDisplay(True,False)
        roomType = self.getRoomDisplay()
        frontBoxNum = self.get_facing(self.num_grid,1,vectorize(self.playerRot))
        if frontBoxNum == None:
            frontBoxNum = 0
        frontBoxNum = str(frontBoxNum)
        
        if (self.playerPos[0],self.playerPos[1],self.playerRot) in [i[0] for i in self.doors]:
            door = "Front"
        elif (self.playerPos[0],self.playerPos[1],self.playerRot+90) in [i[0] for i in self.doors]:
            door = "Left"
        elif (self.playerPos[0],self.playerPos[1],self.playerRot-90) in [i[0] for i in self.doors]:
            door = "Right"
        else:
            door = "None"

        hydra = "None"
        if self.posInDirection(1,vectorize(addDegrees(self.playerRot,0))) == self.hydraPos:
            if roomType[1] == "f":
                hydra = "Front"
        elif self.posInDirection(1,vectorize(addDegrees(self.playerRot,90))) == self.hydraPos:
            if roomType[0] == "f":
                hydra = "Left"
        elif self.posInDirection(1,vectorize(addDegrees(self.playerRot,180))) == self.hydraPos:
            if roomType[3] == "f":
                hydra = "Back"
        elif self.posInDirection(1,vectorize(addDegrees(self.playerRot,270))) == self.hydraPos:
            if roomType[2] == "f":
                hydra = "Right"
        
        gridHeight = self.height

        return DisplayData(gridDisplay,hydra,door,roomType,frontBoxNum,gridHeight)

# CONTROL CONVERTER
# Defines the ControlConverter class so the controls can get converted to something Into2048 can understand

class ControlConverter:
    def __init__(self):
        self.controlDict = {}

    def listControls(self):
        returnList = []
        for i in self.controlDict:
            for j in self.controlDict[i]:
                returnList = returnList + [j]
        return returnList
            

    def set(self,action,controls):
        self.controlDict[action] = controls

    def getAction(self,control):
        for i in self.controlDict:
            if control in self.controlDict[i]:
                return i
            