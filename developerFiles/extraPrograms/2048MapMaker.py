import turtle
import os

folderDirectory = __file__.replace("ExtraPrograms/2048MapMaker.py","2048EssentialFiles")

wn = turtle.Screen()
wn.title("2048 Map Maker")

imageDict = {}
imageNames = ["mapSquare","PainterSquare","0DegreeWall","90DegreeWall","180DegreeWall","270DegreeWall"]

wallDict = {"[]":"a","[0]":"b","[90]":"c","[180]":"d","[270]":"e","[180, 270]":"f","[90, 180]":"g","[0, 90]":"h","[0, 270]":"i","[0, 180]":"j","[90, 270]":"k","[0, 90, 180, 270]":"l","[90, 180, 270]":"m","[0, 180, 270]":"n","[0, 90, 270]":"o","[0, 90, 180]":"p"}

def getWallsAt(wallList,space):
    returnList = []

    for i in wallList:
        if (i[0],i[1]) == space:
            returnList = returnList + [i[2]]

    return returnList

for i in imageNames:
    imageDict[i] = folderDirectory + "/MapMakerImages/" + i + ".gif"

for i in imageDict:
    wn.addshape(imageDict[i])

currentPos = (0,0)
width = 4
height = 4

outerWalls = []
walls = []

wn.tracer(0,0)
painter = turtle.Turtle()
painter.speed(0)
painter.penup()
painter.hideturtle()

running = True

while running:
    painter.clear()
    os.system("clear")

    outerWalls = []

    for i in range(width):
        for j in range(height):
            if (i == 0):
                outerWalls = outerWalls + [(i,j,180)]
            
            if (i == width-1):
                outerWalls = outerWalls + [(i,j,0)]
            
            if (j == 0):
                outerWalls = outerWalls + [(i,j,270)]
            
            if (j == height-1):
                outerWalls = outerWalls + [(i,j,90)]

    painter.goto(30*(-0.5-currentPos[0]),30*(-0.5-currentPos[1]))
    painter.pendown()
    painter.goto(30*(-0.5-currentPos[0]),30*(100-currentPos[1]))
    painter.penup()

    painter.goto(30*(-0.5-currentPos[0]),30*(-0.5-currentPos[1]))
    painter.pendown()
    painter.goto(30*(100-currentPos[0]),30*(-0.5-currentPos[1]))
    painter.penup()

    for i in range(width):
        for j in range(height):
            painter.goto(30*(i-currentPos[0]),30*(j-currentPos[1]))
            painter.shape(imageDict["mapSquare"])
            painter.stamp()

    for i in walls:
        painter.goto(30*(i[0]-currentPos[0]),30*(i[1]-currentPos[1]))
        painter.shape(imageDict[str(i[2]) + "DegreeWall"])
        painter.stamp()

    for i in outerWalls:
        painter.goto(30*(i[0]-currentPos[0]),30*(i[1]-currentPos[1]))
        painter.shape(imageDict[str(i[2]) + "DegreeWall"])
        painter.stamp()

    painter.goto(0,0)

    painter.shape(imageDict["PainterSquare"])
    painter.stamp()
    
    wn.update()

    print(currentPos)
    action = input()
    
    if action == "w":
        currentPos = (currentPos[0],currentPos[1] + 1)
    if action == "a":
        currentPos = (currentPos[0] - 1,currentPos[1])
    if action == "s":
        currentPos = (currentPos[0],currentPos[1] - 1)
    if action == "d":
        currentPos = (currentPos[0] + 1,currentPos[1])

    if (action == "t") and not ([(currentPos[0],currentPos[1],90)] in walls) and not ([(currentPos[0],currentPos[1],90)] in outerWalls):
        walls = walls + [(currentPos[0],currentPos[1],90)]
        walls = walls + [(currentPos[0],currentPos[1],270)]
    if (action == "f") and not ([(currentPos[0],currentPos[1],180)] in walls) and not ([(currentPos[0],currentPos[1],180)] in outerWalls):
        walls = walls + [(currentPos[0],currentPos[1],0)]
        walls = walls + [(currentPos[0],currentPos[1],180)]
    if (action == "g") and not ([(currentPos[0],currentPos[1],270)] in walls) and not ([(currentPos[0],currentPos[1],270)] in outerWalls):
        walls = walls + [(currentPos[0],currentPos[1],90)]
        walls = walls + [(currentPos[0],currentPos[1],270)]
    if (action == "h") and not ([(currentPos[0],currentPos[1],0)] in walls) and not ([(currentPos[0],currentPos[1],0)] in outerWalls):
        walls = walls + [(currentPos[0],currentPos[1],0)]
        walls = walls + [(currentPos[0],currentPos[1],180)]

    if (action == "i") and not ([(currentPos[0],currentPos[1],90)] in walls) and not ([(currentPos[0],currentPos[1],90)] in outerWalls):
        walls = walls + [(currentPos[0],currentPos[1],90)]
    if (action == "j") and not ([(currentPos[0],currentPos[1],180)] in walls) and not ([(currentPos[0],currentPos[1],180)] in outerWalls):
        walls = walls + [(currentPos[0],currentPos[1],180)]
    if (action == "k") and not ([(currentPos[0],currentPos[1],270)] in walls) and not ([(currentPos[0],currentPos[1],270)] in outerWalls):
        walls = walls + [(currentPos[0],currentPos[1],270)]
    if (action == "l") and not ([(currentPos[0],currentPos[1],0)] in walls) and not ([(currentPos[0],currentPos[1],0)] in outerWalls):
        walls = walls + [(currentPos[0],currentPos[1],0)]

    if action == "z":
        width = currentPos[0] + 1
        height = currentPos[1] + 1

    if action == "x":
        running = False

wn.bye()

walls = walls + outerWalls

lineList = []

for j in range(height):
    rowString = ""
    for i in range(width):
        currentWallAngles = getWallsAt(walls,(i,j))
        currentWallAngles.sort()
        rowString = rowString + wallDict[str(currentWallAngles)]
    
    lineList = lineList + [rowString]

lineList.reverse()

os.system("clear")

mapName = input("Name your map: ")

mapContent = "_REF " + mapName + "\n"
for i in lineList:
    mapContent = mapContent + i + "\n"

mapContent = mapContent + "_END " + mapName + "\n\n"

mapsFile = open(folderDirectory+"/TextData/2048Maps.txt","a")

mapsFile.write(mapContent)

mapsFile.close()

os.system("clear")
print("Done!")