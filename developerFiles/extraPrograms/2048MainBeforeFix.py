# IMPORTS

import turtle
import os
from math import *
import random
import time
from functools import partial

# GET FOLDER DIRECTORY

folderDirectory = __file__.replace("/2048Main.py","")
folderDirectory = folderDirectory + "/2048Images"

# HANDY FUNCTIONS

def overlap(list1,list2):
    for i in list1:
        if i in list2:
            return True
    return False

# CONVERTER FUNCTIONS

def vectorize(rotation):
    if rotation == 0:
        return RIGHT
    elif rotation == 90:
        return UP
    elif rotation == 180:
        return LEFT
    elif rotation == 270:
        return DOWN
    
def emojilize(rotation):
    if rotation == 0:
        return "▶"
    elif rotation == 90:
        return "▲"
    elif rotation == 180:
        return "◀"
    elif rotation == 270:
        return "▼"
    
def addDegrees(angle,amount):
    return (angle + amount) % 360

def ableToMove(row):
    prevI = ""
    for i in row:
        if i == 0 or prevI == i:
            return True
        if i == "+":
            return False
        prevI = i
    return False

# BROCK'S CODE

"""remember who you are"""
UP =    (0,1)
DOWN =  (0,-1)
LEFT =  (-1,0)
RIGHT = (1,0)
    
#This class creates a 2d list representing the 2048 game board when
#called, and handles all the interactions that can happen in the game
class Into2048:
    def __init__(self, width=4, height=4, grid="default"):
        self.width = width
        self.height = height
        
        self.game_over = False
        if grid == "default":
            self.num_grid = [[0 for j in range(self.height)] for i in range(self.width)]
            #Stores a list of tuples that act as coordinates for the empty slots in self.num_grid
            self.empty_slot_indexes = [(i, j) for i in range(len(self.num_grid))
                                       for j in range(len(self.num_grid[i]))
                                       if self.num_grid[i][j] == 0]
            self.generate_tiles()
        else:
            self.num_grid = grid
            #Stores a list of tuples that act as coordinates for the empty slots in self.num_grid
            self.empty_slot_indexes = [(i, j) for i in range(len(self.num_grid))
                                       for j in range(len(self.num_grid[i]))
                                       if self.num_grid[i][j] == 0]

        self.spawn_player()
        self.spawn_hydra()
        
    #Generate a random 2048 number. Can only be 2 or 4
    def _generate_num(self):
        return random.choices([2,4], weights=(90,10))[0]
    
    #Generate and place 2 new tiles (1 if only 1 space is available)
    def generate_tiles(self):
        if len(self.empty_slot_indexes) == 1:
            self.num_grid[self.empty_slot_indexes[0][0]][self.empty_slot_index[0][1]] = self._generate_num()
            self.empty_slot_indexes = [] #After filling the last empty square on num_grid, there are no more empty slots
            return
        for i in random.sample(self.empty_slot_indexes, k=2):
            self.num_grid[i[0]][i[1]] = self._generate_num()
            self.empty_slot_indexes.remove(i)


    def spawn_player(self):
        self.playerPos = tuple(random.choice(self.empty_slot_indexes)) #This variable is used to find player position
        self.playerRot = [0,90,180,270][random.randint(0,3)]
        self.justMoved = False
        self.empty_slot_indexes.remove(self.playerPos)

    def spawn_hydra(self):
        self.hydraPos = tuple(random.choice(self.empty_slot_indexes))

    def move_player(self, dir):
        new_pos = tuple(self.playerPos[i] + dir[i] for i in range(2))
        
        if new_pos == self.hydraPos:
            self.game_over = True
        if new_pos[0] < 0 or new_pos[0] >= len(self.num_grid) or new_pos[1] < 0 or new_pos[1] >= len(self.num_grid[0]):
            return
        new_pos_value = self.num_grid[new_pos[0]][new_pos[1]]
        if new_pos_value != 0:
            if not self._push(new_pos, dir):
                return
        self.empty_slot_indexes.append(self.playerPos)
        if new_pos in self.empty_slot_indexes:
            self.empty_slot_indexes.remove(new_pos)
        self.playerPos = new_pos

    def rotate_player(self, amount):
        self.playerRot = addDegrees(self.playerRot,amount)

    def move_hydra(self, approach_probability=50):
        
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
            dir = random.choice(dirs)
        else:
            dir = random.choice((UP,DOWN,LEFT,RIGHT))
        
        new_pos = tuple(self.hydraPos[i] + dir[i] for i in range(2))
        if self.playerPos == new_pos:
            if self.justMoved:
                return
            else:
                self.game_over = True
        if new_pos[0] < 0 or new_pos[0] >= len(self.num_grid) or new_pos[1] < 0 or new_pos[1] >= len(self.num_grid[0]):
            return
        self.hydraPos = new_pos

    def _push(self, pos, dir):
        #If pushing into wall
        if pos[0]+dir[0] < 0 or pos[0]+dir[0] >= len(self.num_grid) or pos[1]+dir[1] < 0 or pos[1]+dir[1] >= len(self.num_grid[0]):
            return False
        #If pushing into block of equal value (merge)
        if self.num_grid[pos[0]][pos[1]] == self.num_grid[pos[0]+dir[0]][pos[1]+dir[1]]:
            self.num_grid[pos[0]][pos[1]] = 0
            self.num_grid[pos[0]+dir[0]][pos[1]+dir[1]] *= 2
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
    
    def posInDirection(self, dist, dir):
        return tuple(self.playerPos[i] + dir[i]*dist for i in range(2))

    def get_facing(self, grid, dist, dir):
        frontPos = tuple(self.playerPos[i] + dir[i]*dist for i in range(2))
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
        for i in range(width):
            for j in range(height):
                if self.playerPos == (i,j) and enablePlayer:
                    replacedGrid[i][j] = emojilize(self.playerRot)
                if self.hydraPos == (i,j) and enableHydra:
                    replacedGrid[i][j] = "+"
        
        return replacedGrid
    
    def destroyNum(self,dir):
        numberPos = self.posInDirection(1,dir)
        if (numberPos[0] < 0) or (numberPos[1] < 0):
            return

        if (numberPos[0] == 0) or (numberPos[1] == 0) or (numberPos[0] == self.width-1) or (numberPos[1] == self.height-1):
            N.num_grid[numberPos[0]][numberPos[1]] = 0
            self.empty_slot_indexes.append(numberPos)




#main
grid = [
    [0,0,0,0],
    [0,4,4,8],
    [0,8,8,16],
    [0,0,0,0]
]
N = Into2048()

# LOGAN'S CODE

# DEFINE SPACEDATA CLASS
# This class assigns walls to spaces.

class spaceData:
    def __init__(self,position):
        self.position = position
        self.wallDict = {"north":False,"east":False,"south":False,"west":False}
    
    def toggleWall(self,direction):
        if direction in self.wallDict:
            self.wallDict[direction] = not self.wallDict[direction]
        else:
            errorMessage = "'" + direction + "' isn't a direction, dummy"
            raise ValueError(errorMessage)
    
    def isWall(self,direction):
        if direction in self.wallDict:
            return self.wallDict[direction]
        else:
            errorMessage = "'" + direction + "' isn't a direction, dummy"
            raise ValueError(errorMessage)

# GET DISPLAYS
# These functions get the displays for each chamber and for the grid.

displayPlayer = True
displayHydra = True

def getGridDisplay(into2048obj,width,height):
    grid = into2048obj.replaceSpaces(True,False)

    stringGrid = ""
    for j in range(height):
        for i in range(width):
            currentNumber = str(grid[i][height-j-1])
            currentNumber = currentNumber + " "*(4-len(currentNumber))
            stringGrid = stringGrid + currentNumber + " "
        stringGrid = stringGrid + "\n"
    return stringGrid

def getRoomDisplay(spaces,position,rotation):
    directionalRanges = {0:["north","east","south"],90:["west","north","east"],180:["south","west","north"],270:["east","south","west"]}
    currentSpace = [i for i in spaces if i.position == position][0]
    currentDirectionalRange = directionalRanges[int(rotation)]
    wallDisplay = ""
    for i in currentDirectionalRange:
        if currentSpace.isWall(i):
            wallDisplay = wallDisplay + "t"
        else: 
            wallDisplay = wallDisplay + "f"

    if wallDisplay == "fft" and random.randint(1,10) == 10:
        wallDisplay = "fftDoor"
    
    return wallDisplay

# DEFINE SPACE LIST


spaceList = []

width = 4
height = 4
scaleFactor = 50

for i in range(width):
    for j in range(height):
        spaceList = spaceList + [spaceData((i,j))]
        if i == 0:
            spaceList[-1].toggleWall("west")
        if i == width-1:
            spaceList[-1].toggleWall("east")
        if j == 0:
            spaceList[-1].toggleWall("south")
        if j == height-1:
            spaceList[-1].toggleWall("north")

roomTypes = ["ttf","ftf","ftt","tff","fff","fft","fftDoor"]
boxTypes = ["2","4","8","16","32","64","128","256","512","1024","2048"]
hydraStates = ["Front","Back","Left","Right"]
jumpscares = ["Hydra","Dad"]

imageDict = {}

# KEYBOARD MANAGER

keyList = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","Left","Right","Up","Down","space"]
isPressedList = [False for i in range(len(keyList))]
keysDown = []

def updateKeyLists(key,isPressed):
    global isPressedList
    global keysDown

    replacementIndex = keyList.index(key)
    
    newList = []
    for i in range(len(isPressedList)):
        if i == replacementIndex:
            newList = newList + [isPressed]
        else:
            newList = newList + [isPressedList[i]]
    
    isPressedList = newList

    keysDown = []

    for i in range(len(keyList)):
        if isPressedList[i]:
            keysDown = keysDown + [keyList[i]]

def keyPressed(key):
    return key in keysDown

wn = turtle.Screen()
wn.title("2048: THE HORROR GAME")
wn.setup(1481,856,0,0)

for i in roomTypes:
    imageDict[i] = folderDirectory + "/Chambers/" + i + "Chamber.gif"

for i in boxTypes:
    imageDict[i] = folderDirectory + "/Boxes/" + i + "Box.gif"

for i in hydraStates:
    imageDict[i] = folderDirectory + "/HydraRenders/Hydra" + i + ".gif"

for i in jumpscares:
    imageDict[i] = folderDirectory + "/Jumpscares/" + i + "Jumpscare.gif"

for i in imageDict:
    wn.addshape(imageDict[i])

painter = turtle.Turtle()
painter.speed(0)
painter.penup()
painter.hideturtle()
wn.tracer(0,0)

wn.listen()
for i in keyList:
    wn.onkeypress(partial(updateKeyLists,i,True),i)
    wn.onkeyrelease(partial(updateKeyLists,i,False),i)

# GAMELOOP

def display():
    global currentRoomType
    global frontBoxNum

    os.system("clear")
    painter.clear()

    currentRoomType = getRoomDisplay(spaceList,N.playerPos,N.playerRot)
    frontBoxNum = N.get_facing(N.num_grid,1,vectorize(N.playerRot))
    gridDisplay = getGridDisplay(N,N.width,N.height)

    painter.shape(imageDict[currentRoomType])
    painter.stamp()
    if frontBoxNum != 0 and frontBoxNum != None:
        painter.shape(imageDict[str(frontBoxNum)])
        painter.stamp()
    
    if N.posInDirection(1,vectorize(addDegrees(N.playerRot,0))) == N.hydraPos:
        painter.shape(imageDict["Front"])
        painter.stamp()
    elif N.posInDirection(1,vectorize(addDegrees(N.playerRot,90))) == N.hydraPos:
        painter.shape(imageDict["Left"])
        painter.stamp()
    elif N.posInDirection(1,vectorize(addDegrees(N.playerRot,180))) == N.hydraPos:
        painter.shape(imageDict["Back"])
        painter.stamp()
    elif N.posInDirection(1,vectorize(addDegrees(N.playerRot,270))) == N.hydraPos:
        painter.shape(imageDict["Right"])
        painter.stamp()
    
    painter.goto(-700,200)
    painter.color("red")
    painter.write(gridDisplay,font=("Menlo", 30, "bold"))
    painter.color("black")
    painter.goto(0,0)

    print("PLAYER POSITION: " + str(N.playerPos))
    print("PLAYER ROTATION: " + str(N.playerRot))
    print("ROOM TYPE: " + str(currentRoomType))
    print("JUST MOVED: " + str(N.justMoved))
    print()
    print(N.getRow(N.replaceSpaces(),vectorize(N.playerRot)))
    print(N.getRow(N.replaceSpaces(),vectorize(addDegrees(N.playerRot,180))))
    print()
    print("BLOCKED: " + str(blocked))
    print("HYDRA NEAR: " + str(hydraNear))
    print()
    print("HYDRA DISABLED: " + str(disableHydraMovement))

disableHydraMovement = False
dad = False

while not N.game_over:
    
    playerPosCheck = N.playerPos
    if N.posInDirection(1,vectorize(addDegrees(N.playerRot,0))) == N.hydraPos:
        hydraNear = True
    elif N.posInDirection(1,vectorize(addDegrees(N.playerRot,90))) == N.hydraPos:
        hydraNear = True
    elif N.posInDirection(1,vectorize(addDegrees(N.playerRot,180))) == N.hydraPos:
        hydraNear = True
    elif N.posInDirection(1,vectorize(addDegrees(N.playerRot,270))) == N.hydraPos:
        hydraNear = True
    else:
        hydraNear = False
        
    if (not ableToMove(N.getRow(N.replaceSpaces(),vectorize(N.playerRot)))) and (not ableToMove(N.getRow(N.replaceSpaces(),vectorize(addDegrees(N.playerRot,180))))):
        blocked = True
    else:
        blocked = False
        
    if hydraNear and blocked:
        disableHydraMovement = True

    os.system("clear")
    painter.clear()
    display()
    while not overlap(keysDown,["w","a","s","d","z","x"]):
        wn.update()

    while overlap(keysDown,["w","a","s","d","z","x"]):
        if keyPressed("w"):
            action = "w"
        if keyPressed("a"):
            action = "a"
        if keyPressed("s"):
            action = "s"
        if keyPressed("d"):
            action = "d"
        if keyPressed("z"):
            action = "z"
        if keyPressed("x"):
            action = "x"

        wn.update()

    if action == "w":
        N.move_player(vectorize(N.playerRot))
    if action == "a":
        N.rotate_player(90)
    if action == "s":
        N.move_player(vectorize(addDegrees(N.playerRot,180)))
    if action == "d":
        N.rotate_player(-90)
    
    if playerPosCheck != N.playerPos:
        N.justMoved = True
    else:
        N.justMoved = False

    if disableHydraMovement:
        disableHydraMovement = False
    else:
        N.move_hydra(50)
    
    if action == "z":
        if currentRoomType == "fftDoor":
            N.game_over = True
            dad = True
        N.generate_tiles()
    elif action == "x":
        N.destroyNum(vectorize(N.playerRot))

    wn.update()

os.system("clear")
painter.clear()
if dad:
    painter.shape(imageDict["Dad"])
else:
    painter.shape(imageDict["Hydra"])

painter.stamp()

wn.update()

time.sleep(1)

wn.bye()
os.system("clear")

print("---------------------")
print("      GAME OVER")
print("---------------------")
print()