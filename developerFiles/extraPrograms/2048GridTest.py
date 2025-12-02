import turtle
import os
from math import *
os.system("clear")
print("Building grid...")

# DEFINE SPACEDATA CLASS

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

# DEFINE GET WALL DISPLAY

def getWallDisplay(spaces,position,rotation):
    directionalRanges = {0:["north","east","south"],90:["west","north","east"],180:["south","west","north"],270:["east","south","west"]}
    currentSpace = [i for i in spaces if i.position == position][0]
    currentDirectionalRange = directionalRanges[int(rotation)]
    wallDisplay = ""
    for i in currentDirectionalRange:
        if currentSpace.isWall(i):
            wallDisplay = wallDisplay + "t"
        else: 
            wallDisplay = wallDisplay + "f"
    
    return wallDisplay

def getCurrentSpace(spaces,position):
    return [i for i in spaces if i.position == position][0]

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

drawAxes = True

roomTypes = ["ttf","ftf","ftt","tff","fff","fft"]
imageDict = {}

wn = turtle.Screen()

for i in roomTypes:
    imageDict[i] = "/Users/837795/Desktop/APCSP/2048 THE HORROR GAME/" + i + "RoomTest.gif"

for i in imageDict:
    wn.addshape(imageDict[i])

painter = turtle.Turtle(shape="circle")
roomDisplay = turtle.Turtle()
roomDisplay.speed(0)
roomDisplay.penup()
roomDisplay.goto(-200,0)
painter.speed(0)
if drawAxes:
    painter.goto(0,-400/2)
    painter.pendown()
    painter.goto(0,400/2)
    painter.penup()
    painter.goto(-400/2,0)
    painter.pendown()
    painter.goto(400/2,0)
    painter.penup()
painter.penup()
painter.pensize(10)

for i in spaceList:
    painter.goto(scaleFactor*(i.position[0]-0.5),scaleFactor*(i.position[1]-0.5))
    for j in ["south","east","north","west"]:
        if i.isWall(j):
            painter.pendown()
        painter.forward(scaleFactor)
        painter.penup()
        painter.stamp()
        painter.left(90)
    os.system("clear")

painter.shape("turtle")
painter.goto(0,0)
painter.speed(2)

while 1==1:
    os.system("clear")
    convertedPos = (round(painter.xcor()/scaleFactor),round(painter.ycor()/scaleFactor))
    print(getCurrentSpace(spaceList,convertedPos).position)
    currentRoomType = getWallDisplay(spaceList,convertedPos,painter.heading())
    roomDisplay.shape(imageDict[currentRoomType])
    print("Current picture type: " + currentRoomType)
    action = input("Type a key to move or rotate: ")
    if action == "w":
        painter.forward(scaleFactor)
    if action == "a":
        painter.left(90)
    if action == "d":
        painter.right(90) 

wn.mainloop()