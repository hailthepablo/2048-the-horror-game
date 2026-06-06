from gridlib import *
import os

def cout(var):
    print(var,end='')

def pauseExec():
    input()

def vectorize(rot):
    return [(1,0),(0,1),(-1,0),(0,-1)][rot]

class Walls:
    def __init__(self,wallTuple):
        self.wallTuple = wallTuple
    
    def getFacing(self,rot):
        if rot == 0:
            return (self.wallTuple[0],self.wallTuple[1],self.wallTuple[2],self.wallTuple[3])
        if rot == 1:
            return (self.wallTuple[1],self.wallTuple[2],self.wallTuple[3],self.wallTuple[0])
        if rot == 2:
            return (self.wallTuple[2],self.wallTuple[3],self.wallTuple[0],self.wallTuple[1])
        if rot == 3:
            return (self.wallTuple[3],self.wallTuple[0],self.wallTuple[1],self.wallTuple[2])

class Scene:
    def __init__(self,numArray,wallArray):
        self.numGrid = Grid(numArray,(7,0),"xy","right","up")
        self.wallGrid = Grid(wallArray,(7,0),"xy","right","up")

    def push(self,pos,rot):
        pushDir = vectorize(rot)
        curSpace = pos
        amount = 0
        prevNum = 0
        while True:
            curNum = self.numGrid.getElem(curSpace)
            
            if (amount != 0 and (prevNum == curNum or curNum == 0)):
                break
            
            if (self.wallGrid.getElem(curSpace)).getFacing(rot)[0]:
                return False

            amount += 1
            curSpace = (curSpace[0]+pushDir[0],curSpace[1]+pushDir[1])
            prevNum = curNum
        
        for i in range(amount):
            curSpace = (curSpace[0]-pushDir[0],curSpace[1]-pushDir[1])
            newPos = (curSpace[0]+pushDir[0],curSpace[1]+pushDir[1])
            self.numGrid.setElem(newPos,self.numGrid.getElem(curSpace)+self.numGrid.getElem(newPos))
            self.numGrid.setElem(curSpace,0)

        return True

defaultNums = [[0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,8,0],
               [0,0,0,0,0,0,8,0],
               [0,0,0,0,0,0,2,0],
               [0,0,0,4,0,0,4,0],
               [0,0,0,0,0,0,2,0],
               [0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0]]

defaultWalls = [[Walls((False,False,False,False)) for j in range(8)] for i in range(8)]

s = Scene(defaultNums,defaultWalls)
s.wallGrid.setElem((3,4),Walls((True,True,True,True)))
playerPos = (0,0)

while True:
    os.system("clear")
    displayGrid = s.numGrid.getStringGrid()
    displayGrid.setElem(playerPos,"@")

    for i in getDisplayArray(displayGrid,"left"):
        for j in i:
            cout(str(j) + " ")
        cout('\n')

    cout('\n')
    
    action = input("Action: ")
    if action == "w":
        rot = 1
    elif action == "a":
        rot = 2
    elif action == "s":
        rot = 3
    elif action == "d":
        rot = 0
    else:
        continue

    if s.push(playerPos,rot):
        playerPos = (playerPos[0]+vectorize(rot)[0],playerPos[1]+vectorize(rot)[1])