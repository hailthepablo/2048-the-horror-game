# IMPORTS

import turtle
import os
from math import *
import random
import time
from functools import partial

# GET FOLDER DIRECTORY

folderDirectory = __file__.replace("/2048MainBackup.py","")

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

# BROCK'S CODE

"""remember who you are"""
UP =    (0,1)
DOWN =  (0,-1)
LEFT =  (-1,0)
RIGHT = (1,0)
    
#This class creates a 2d list representing the 2048 game board when
#called, and handles all the interactions that can happen in the game
class Into2048:
    def __init__(self, length=4, height=4, grid="default"):
        if grid == "default":
            self.num_grid = [[0 for j in range(height)] for i in range(length)]
            self.generate_tiles()
        else:
            self.num_grid = grid
        self.spawn_player()
        
    #Generate a random 2048 number. Can only be 2 or 4
    def _generate_num(self):
        return random.choices([2,4], weights=(90,10))[0]
    
    #Generate and place 2 new tiles (1 if only 1 space is available)
    def generate_tiles(self):
        #Find coordinates for all empty slots
        empty_slot_indexes = [(i, j) for i in range(len(self.num_grid))
                              for j in range(len(self.num_grid[i]))
                              if self.num_grid[i][j] == 0]
        if empty_slot_indexes == 1:
            self.num_grid[empty_slot_indexes[0][0]][empty_slot_indexes[0][1]] = self._generate_num()
            return
        for i in random.sample(empty_slot_indexes, k=2):
            self.num_grid[i[0]][i[1]] = self._generate_num()
    
    def spawn_player(self):
        empty_slot_indexes = [(i, j) for i in range(len(self.num_grid))
                              for j in range(len(self.num_grid[i]))
                              if self.num_grid[i][j] == 0]
        self.playerPos = tuple(random.choice(empty_slot_indexes))
        self.playerRot = [0,90,180,270][random.randint(0,3)]
        self.num_grid[self.playerPos[0]][self.playerPos[1]] = emojilize(self.playerRot)
    
    def move_player(self, dir):
        new_pos = tuple(self.playerPos[i] + dir[i] for i in range(2))
        if new_pos[0] < 0 or new_pos[0] >= len(self.num_grid) or new_pos[1] < 0 or new_pos[1] >= len(self.num_grid[0]):
            return
        new_pos_value = self.num_grid[new_pos[0]][new_pos[1]]
        if new_pos_value != 0:
            if not self._push(new_pos, dir):
                return
        self.num_grid[self.playerPos[0]][self.playerPos[1]] = 0
        self.playerPos = new_pos
        self.num_grid[self.playerPos[0]][self.playerPos[1]] = emojilize(self.playerRot)

    def rotate_player(self,amount):
        self.playerRot = (self.playerRot + amount) % 360
        self.num_grid[self.playerPos[0]][self.playerPos[1]] = emojilize(self.playerRot)

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
    
    def get_facing(self, dir):
        frontPos = tuple(self.playerPos[i] + dir[i] for i in range(2))
        if frontPos[0] < 0 or frontPos[0] >= len(self.num_grid) or frontPos[1] < 0 or frontPos[1] >= len(self.num_grid[0]):
            return
        return self.num_grid[frontPos[0]][frontPos[1]]



#main
grid = [
    [0,0,0,0],
    [0,4,4,8],
    [0,8,8,16],
    [0,0,0,0]
]
N = Into2048()

# LOGAN'S CODE

def getGridDisplay(grid,width,height):
    stringGrid = ""
    for j in range(height):
        for i in range(width):
            currentNumber = str(grid[i][height-j-1])
            currentNumber = currentNumber + " "*(4-len(currentNumber))
            stringGrid = stringGrid + currentNumber + " "
        stringGrid = stringGrid + "\n"
    return stringGrid

# DEFINE SPACEDATA CLASS
# This class assigns walls to spaces

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

# DEFINE GET ROOM DISPLAY
# This function gets the display code for the current room.

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
imageDict = {}

# KEYBOARD MANAGER

keyList = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","Left","Right","Up","Down"]
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
    frontBoxNum = N.get_facing(vectorize(N.playerRot))
    gridDisplay = getGridDisplay(N.num_grid,4,4)

    painter.shape(imageDict[currentRoomType])
    painter.stamp()
    if frontBoxNum != 0 and frontBoxNum != None:
        painter.shape(imageDict[str(frontBoxNum)])
        painter.stamp()
    painter.goto(-700,200)
    painter.color("red")
    painter.write(gridDisplay,font=("Menlo", 30, "bold"))
    painter.color("black")
    painter.goto(0,0)

    print("PLAYER POSITION: " + str(N.playerPos))
    print("PLAYER ROTATION: " + str(N.playerRot))
    print("ROOM TYPE: " + str(currentRoomType))
    
while 1==1:
    os.system("clear")
    painter.clear()
    display()
    while not overlap(keysDown,["w","a","s","d"]):
        wn.update()

    while overlap(keysDown,["w","a","s","d"]):
        if keyPressed("w"):
            action = "w"
        if keyPressed("a"):
            action = "a"
        if keyPressed("s"):
            action = "s"
        if keyPressed("d"):
            action = "d"
        wn.update()

    if action == "w":
        N.move_player(vectorize(N.playerRot))
    if action == "a":
        N.rotate_player(90)
    if action == "s":
        N.move_player(vectorize((N.playerRot + 180) % 360))
    if action == "d":
        N.rotate_player(-90)
    wn.update()
    
wn.mainloop()