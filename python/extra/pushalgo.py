from gridlib import *
import os

class Scene:
    def __init__(self,numGrid):
        self.numGrid = Grid(numGrid,(7,0),"xy","right","up")

    def applyVector(self,pos,vec):
        newPos = (pos[0]+vec[0],pos[1]+vec[1])
        self.numGrid.setElem(newPos,self.numGrid.getElem(pos)+self.numGrid.getElem(newPos))
        self.numGrid.setElem(pos,0)

    def push(self,pos,pushDir):
        curSpace = pos
        amount = 0
        prevNum = 0
        while True:
            curNum = self.numGrid.getElem(curSpace)
            # if wall then stop and return false
            if (amount != 0 and (prevNum == curNum or curNum == 0)):
                break

            amount = amount + 1
            curSpace = (curSpace[0]+pushDir[0],curSpace[1]+pushDir[1])
            prevNum = curNum
        
        for i in range(amount):
            print(curSpace)
            curSpace = (curSpace[0]-pushDir[0],curSpace[1]-pushDir[1])
            self.applyVector(curSpace,pushDir)



defaultNums = [[0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,8,0],
               [0,0,0,0,0,0,8,0],
               [0,0,2,4,0,0,2,0],
               [0,0,0,0,0,0,4,0],
               [0,0,0,0,0,0,2,0],
               [0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0]]

def cout(var):
    print(var,end='')

s = Scene(defaultNums)

while True:
    os.system("clear")
    display = s.numGrid.getDisplayArray()

    for i in display:
        for j in i:
            cout(str(j) + " ")
        cout('\n')

    cout('\n')
    position = (int(input("Position x: ")),int(input("Position y: ")))
    vector = (int(input("Vector x: ")),int(input("Vector y: ")))

    s.push(position,vector)
    input()