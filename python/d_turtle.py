# I decided to make a turtle version of the game because Pygame would not work on the Mill.
# Why am I running this on the Mill? Because it's freaking awesome thats why.

# IMPORT LIBRARIES
# Imports the freakin' libraries

import turtle
from game import *
from functools import partial
from time import sleep

FONT = ("Menlo",20,"bold")

def overlap(list1,list2):
    for i in list1:
        if i in list2:
            return True
    return False

# KEYBOARD MANAGER
# This section of the code implements a new keypress system, as the one that came with turtle kinda sucks.

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

# WINDOW SETUP
# You can probably guess what this does.

wn = turtle.Screen()
wn.title("2048: THE HORROR GAME")
wn.setup(1481,856,0,0)

# ADD IMAGES
# This section of the code collects and adds all required images to the program.

roomTypes = ["ttf","ftf","ftt","tff","fff","fft","ttt","tft","fftDoor"]
boxTypes = ["0","2","4","8","16","32","64","128","256","512","1024","2048"]
hydraStates = ["Front","Back","Left","Right","FrontLD","None"]
endScreens = ["HydraJumpscare","DadJumpscare","WinScreen","HydraJumpscareLD"]
doorImages = ["Left","Front","Right","None"]

imageDict = {}

for i in roomTypes:
    imageDict[pathAssemble(["assets","Chambers",i+"Chamber.gif"])] = pathAssemble(["assets","Chambers",i+"Chamber.gif"])

for i in boxTypes:
    imageDict[pathAssemble(["assets","Boxes",i+"Box.gif"])] = pathAssemble(["assets","Boxes",i+"Box.gif"])

for i in hydraStates:
    imageDict[pathAssemble(["assets","HydraRenders","Hydra"+i+".gif"])] = pathAssemble(["assets","HydraRenders","Hydra"+i+".gif"])

for i in endScreens:
    imageDict[pathAssemble(["assets","EndScreens",i+".gif"])] = pathAssemble(["assets","EndScreens",i+".gif"])

for i in doorImages:
    imageDict[pathAssemble(["assets","Doors","Door"+i+".gif"])] = pathAssemble(["assets","Doors","Door"+i+".gif"])

for i in imageDict:
    wn.addshape(imageDict[i])

# DEFINE PAINTER
# Defines the painter turtle that's more of a stamper rather than a painter.

painter = turtle.Turtle()
painter.speed(0)
painter.penup()
painter.hideturtle()
wn.tracer(0,0)

# KEY LISTENER
# Listens for keypresses and sends them out to the new keypress system.

wn.listen()
for i in keyList:
    wn.onkeypress(partial(updateKeyLists,i,True),i)
    wn.onkeyrelease(partial(updateKeyLists,i,False),i)

# GAMELOOP
# This is the main loop where the game runs.

game = Into2048("Classic?",4,4,True,True,[],[])
controls = ControlConverter()

controls.set("forward",["w"])
controls.set("backward",["s"])
controls.set("right",["d"])
controls.set("left",["a"])
controls.set("spawn",["z"])
controls.set("destroy",["x"])

actionKeys = ["w","a","s","d","z","x","c","m"]

systemClear()
print("2048: The Horror Game (turtle edition)")
print("Game currently running...")

while True:
    game.start()
    timer = 0
    while not game.game_over:
        painter.clear()
        
        currentDisplayData = game.getDisplayData()

        painter.clear()
        painter.goto(0,0)

        painter.shape(imageDict[pathAssemble(["assets","Chambers",currentDisplayData.roomType[0:-1] + "Chamber.gif"])])
        painter.stamp()
        painter.shape(imageDict[pathAssemble(["assets","Boxes",currentDisplayData.frontBoxNum + "Box.gif"])])
        painter.stamp()
        painter.shape(imageDict[pathAssemble(["assets","HydraRenders","Hydra" + currentDisplayData.hydra + ".gif"])])
        painter.stamp()
        painter.shape(imageDict[pathAssemble(["assets","Doors","Door" + currentDisplayData.door + ".gif"])])
        painter.stamp()

        painter.goto(-730,200-15*game.height)
        painter.color("red")
        painter.write(currentDisplayData.gridDisplay,font=FONT)
        painter.color("black")
        painter.goto(0,0)
        
        while not overlap(keysDown,actionKeys):
            wn.update()

        while overlap(keysDown,actionKeys):
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
            if keyPressed("m"):
                wn.bye()
                systemClear()
                print("You quit the game.")
                exit()
            wn.update()
        
        game.update(controls.getAction(action),timer)

    painter.clear()
    painter.shape(imageDict[pathAssemble(["assets","EndScreens",game.game_over+".gif"])])
    painter.stamp()
    wn.update()
    sleep(1)