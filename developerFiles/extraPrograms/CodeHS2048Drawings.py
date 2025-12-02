from math import *
import turtle as trtl
import os

def arrayToString(array):
    returnString = ""
    for i in array:
        returnString = returnString + str(i)
    return returnString

def cut(inputList,index):
    returnList = []
    
    for i in range(len(inputList)):
        if i != index:
            returnList = returnList + [inputList[i]]
    
    if (type(inputList) == type([1,2])):
        return returnList
    elif (type(inputList) == type((1,2))):
        return tuple(returnList)
    elif (type(inputList) == type("O")):
        return arrayToString(returnList)

def noString(inputList):
    returnList = []
    for i in inputList:
        if type(i) != type("O"):
            returnList = returnList + [i]
    return returnList

def cosd(angle):
    return cos(radians(angle))

def sind(angle):
    return sin(radians(angle))

def perspectiveMap(cornerList,inputPoint):
    p1 = cornerList[0]
    p2 = cornerList[1]
    p3 = cornerList[2]
    p4 = cornerList[3]
    
    x1 = p1[0]
    y1 = p1[1]
    x2 = p2[0]
    y2 = p2[1]
    x3 = p3[0]
    y3 = p3[1]
    x4 = p4[0]
    y4 = p4[1]
    a = inputPoint[0]
    b = inputPoint[1]

    returnX = (1-a)*b*x4 + b*a*x3 + (1-b)*a*x2 + (1-a)*(1-b)*x1
    returnY = (1-a)*b*y4 + b*a*y3 + (1-b)*a*y2 + (1-a)*(1-b)*y1

    return (returnX,returnY)

def commandDetect(element):
    return (type(element) == type("O")) and (element[0] == "_")

def commandSplit(command):
    command = str(cut(command,0))
    if "=" in command:
        command = command.replace("="," ")
        command = command.split()
        return (command[0],command[1])
    else:
        return (command,None)

def fracLine(p1,p2,fraction):
    x1 = p1[0]
    y1 = p1[1]
    x2 = p2[0]
    y2 = p2[1]
    
    return (fraction*(x2-x1)+x1,fraction*(y2-y1)+y1)

class PointList:
    def __init__(self,points):
        self.points = points

    def __str__(self):
        return str(self.points)
    
    def dilate(self,x,y):
        newList = []
        for i in self.points:
            if commandDetect(i):
                newList = newList + [i]
            else:
                newList = newList + [(i[0]*x,i[1]*y)]
        self.points = newList

    def rotate(self,angle):
        newList = []
        for i in self.points:
            if commandDetect(i):
                newList = newList + [i]
            else:
                newList = newList + [(i[0]*cosd(angle)-i[1]*sind(angle),i[0]*sind(angle)+i[1]*cosd(angle))]
        self.points = newList
    
    def translate(self,x,y):
        newList = []
        for i in self.points:
            if commandDetect(i):
                newList = newList + [i]
            else:
                newList = newList + [(i[0]+x,i[1]+y)]
        self.points = newList

    def apply(self,x,y):
        newList = []
        for i in self.points:
            outputX = x.replace("x",str(i[0]))
            outputX = outputX.replace("y",str(i[1]))
            outputY = y.replace("x",str(i[0]))
            outputY = outputY.replace("y",str(i[1]))
            newList = newList + [(eval(outputX),eval(outputY))]
        self.points = newList

    def project(self,corners):
        newList = []
        for i in self.points:
            if commandDetect(i):
                newList = newList + [i]
            else:
                newList = newList + [perspectiveMap(corners,(i[0],i[1]))]
        self.points = newList

    def draw(self,turtle):
        turtle.goto(noString(self.points)[0])
        turtle.pendown()

        jump = False

        for i in self.points:
            if commandDetect(i):
                action = commandSplit(i)[0]
                parameter = commandSplit(i)[1]

                if action == "JUMP":
                    jump = True
                elif action == "COLOR":
                    turtle.pencolor(parameter.lower())
                elif action == "SIZE":
                    turtle.pensize(int(parameter))
                elif action == "SFILL":
                    turtle.begin_fill()
                elif action == "EFILL":
                    turtle.fillcolor(parameter.lower())
                    turtle.end_fill()
            else:
                if jump:
                    turtle.penup()
                    turtle.goto(i)
                    turtle.pendown()
                    jump = False
                else:
                    turtle.goto(i)
            
        turtle.penup()

def arcPosList(start=0,end=360,radius=100,sides=100):
    returnList = []
    for i in range(sides+1):
        returnList = returnList + [(radius*cosd(start+i*(end-start)/sides),radius*sind(start+i*(end-start)/sides))]
    return PointList(returnList)

# SETUP ROOM DIMENSIONS

scale = 1/2
bw = 200
bh = 400/3
sw = bw * scale
sh = bh * scale

# MAKE WINDOW AND TURTLE

wn = trtl.Screen()

painter = trtl.Turtle()
painter.penup()
painter.speed(0)

painter.goto(-200,-200)

painter.pendown()
painter.begin_fill()
for i in range(4):
    painter.forward(400)
    painter.left(90)
painter.penup()
painter.end_fill()

# SET WALL LISTS

backCoords = ((-sw,-sh),(sw,-sh),(sw,sh),(-sw,sh))

leftCoords = ((-bw,-bh),(-sw,-sh),(-sw,sh),(-bw,bh))

rightCoords = ((sw,-sh),(bw,-bh),(bw,bh),(sw,sh))

bottomCoords = ((-bw,-bh),(bw,-bh),(sw,-sh),(-sw,-sh))

topCoords = ((-sw,sh),(sw,sh),(bw,bh),(-bw,bh))

deskCoords = (fracLine((-bw,-bh),(-sw,-sh),2/5),fracLine((bw,-bh),(sw,-sh),2/5),fracLine((bw,bh),(sw,sh),2/5),fracLine((-bw,bh),(-sw,sh),2/5))

# CREATE TEXTURES

textures = []

# floor

floorTexture = ["_SFILL",(0,0),(5,0),(5,5),(0,5),(0,0),"_EFILL=GREEN","_JUMP"]

floorTexture = PointList(floorTexture)
floorTexture.dilate(1/5,1/5)
floorTexture.project(bottomCoords)
textures = textures + [floorTexture]

# left

current = ["_SFILL",(0,0),(5,0),(5,5),(0,5),(0,0),"_EFILL=GRAY"]
current = current + ["_SFILL",(1,0),(1,5),(4,5),(4,0),(2,0),"_EFILL=BLACK"]

current = PointList(current)
current.dilate(1/5,1/5)
current.project(leftCoords)
textures = textures + [current]

# right

current = ["_SFILL",(0,0),(5,0),(5,5),(0,5),(0,0),"_EFILL=GRAY"]
current = current + ["_SFILL",(1,0),(1,5),(4,5),(4,0),(1,0),"_EFILL=BLACK"]

current = PointList(current)
current.dilate(1/5,1/5)
current.project(rightCoords)
textures = textures + [current]

# back

current = ["_SFILL",(0,0),(5,0),(5,5),(0,5),(0,0),"_EFILL=GRAY"]

current = current + ["_JUMP","_SFILL",(1,0),(4,0),(4,5),(1,5),(1,0),"_EFILL=BLACK"]

current = PointList(current)
current.dilate(1/5,1/5)
current.project(backCoords)
textures = textures + [current]

# DRAW

for i in textures:
    os.system("clear")
    input(i)
    i.draw(painter)

painter.hideturtle()

wn.mainloop()