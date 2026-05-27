import pygame
import pygame.freetype
from game import *
from showinfm import show_in_file_manager

# BUILD GAME
# Builds a new Into2048 object containing all settings for running the game

def build2048(fileLineList):
    walls = []

    mapData = listify(ref("Map",fileLineList))
    mapData.reverse()

    width = len(mapData[0])
    height = len(mapData)

    grid = []
    for i in range(width):
        column = []
        for j in range(height):
            column = column + [mapData[j][i]]
        grid = grid + [column]

    for i in range(width):
        for j in range(height):
            for angle in spaceDict[grid[i][j]]:
                walls = walls + [(i,j,angle)]

    for i in range(width):
        for j in range(height):
            if (i == 0) and not ([(i,j,180)] in walls):
                walls = walls + [(i,j,180)]
            
            if (i == width-1) and not ([(i,j,0)] in walls):
                walls = walls + [(i,j,0)]
            
            if (j == 0) and not ([(i,j,270)] in walls):
                walls = walls + [(i,j,270)]
            
            if (j == height-1) and not ([(i,j,90)] in walls):
                walls = walls + [(i,j,90)]

    doorData = listify(ref("Doors",fileLineList))

    doors = []

    name = listify(ref("Name",fileLineList))[0]

    for i in doorData:
        currentDoor = i.split()
        doors = doors + [[stringToTuple(currentDoor[0]),currentDoor[1],stringToTuple(currentDoor[2])]]

    return Into2048(name,width,height,False,True,walls,doors)

level = Into2048("Classic?",4,4,True,True,[],[])

# PYGAME INITIALIZATION
# Initializes Pygame and sets up the game window

pygame.init()
pygame.joystick.init()
systemClear()

red = (255,0,0)

WN_WIDTH = 1440
WN_HEIGHT = 776

wn = pygame.display.set_mode((WN_WIDTH,WN_HEIGHT),pygame.RESIZABLE)
systemClear()

pygame.display.set_caption("2048: THE HORROR GAME")

# PYGAME FUNCTIONS
# Functions for automatically displaying things on the Pygame window so I don't lose my sanity

def stampImage(path,pos,scale=True):
    blitImage = pygame.image.load(path)
    blitImage = blitImage.convert_alpha()
    if scale:
        blitImage = pygame.transform.scale(blitImage, wn.get_size())
    wn.blit(blitImage,pos)

def writeText(string,font,color,pos,align="left",offset=(0,0)):
    align = align.lower()
    string = str(string)
    lines = string.split("\n")
    size = font.size
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            if align=="left":
                font.render_to(wn, (pos[0]+size*(j+offset[0])*0.65,pos[1]+size*(i-offset[1])), lines[i][j], color)
            elif align == "center":  
                font.render_to(wn, (pos[0]+size*(j-len(lines[i])/2+offset[0])*0.65,pos[1]+size*(i-offset[1])), lines[i][j], color)
            elif align == "right":
                font.render_to(wn, (pos[0]+size*(j-len(lines[i]+offset[0]))*0.65,pos[1]+size*(-offset[1])), lines[i][j], color)
            else:
                raise ValueError("'" + str(align) + "' is not an appropriate value for 'align'.")

def middle(offset=(0,0)):
    return (wn.get_size()[0]/2+offset[0],wn.get_size()[1]/2-offset[1])

def cursorDisplay(string,position,typing=False):
    if cursorPos == position:
        if typing:
            return "~ "+string
        else:
            return "> "+string
    else:
        return "  "+string

def unicodeType(string,char):
    if char in ["\x08"]:
        return string[0:-1]
    elif char in ["\t","\n"]:
        pass
    else:
        return string+char

running = True
keyQuit = False
screen = "SetupMenu"
cursorPos = 0
jumpscareCounter = 0
prevStickX = 0
prevStickY = 0

currentPos = (0,0)
width = 4
height = 4

outerWalls = []
walls = []

timer = 1

startData = list(open(pathAssemble(["textData","2048StartData.txt"])))
tempDict = {}
for i in startData:
    current = i.replace("\n","")
    current = current.split(":")
    tempDict[current[0]] = current[1]

startData = tempDict

levelName = startData["levelName"]
levelData = startData["levelData"]
displayMode = int(startData["displayMode"])
startMode = int(startData["startMode"])

hydraImage = ""

startingGame = ((startMode == 2) or (startMode == 3))

startingEditor = False

controls = ControlConverter()

controls.set("forward",["w","LeftstickUp"])
controls.set("backward",["s","LeftstickDown"])
controls.set("right",["d","LeftstickRight"])
controls.set("left",["a","LeftstickLeft"])
controls.set("spawn",["z","ButtonA"])
controls.set("destroy",["x","ButtonX"])

def updateStartData():
    startData = open(pathAssemble(["textData","2048StartData.txt"]),"w")
    startData.write("levelName:"+levelName+"\nlevelData:"+levelData+"\ndisplayMode:"+str(displayMode)+"\nstartMode:"+str(startMode))
    startData.close()

while running:
    timer = (timer + 1)%10

    if startingGame:
        startData = open(pathAssemble(["textData","2048StartData.txt"]),"w")
        startData.write("levelName:"+levelName+"\nlevelData:"+levelData+"\ndisplayMode:"+str(displayMode)+"\nstartMode:"+str(startMode))
        startData.close()
        level = build2048(list(open(pathAssemble(["assets","LevelFiles",levelName+".txt"]))))
        level.start()
        screen = "GamePlay"
        startingGame = False

    if startingEditor:
        screen = "MapEditor"
        startingEditor = False
    
    if pygame.joystick.get_count() == 1:
        controller = pygame.joystick.Joystick(0)
    else:
        controller = "I do not exist"

    controlList = []
    unicodeKeys = []

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.KEYUP:

            unicodeKeys = unicodeKeys + [event.unicode]

            if (screen == "GamePlay" or screen == "MapEditor") and event.unicode in controls.listControls():
                controlList = controlList + [controls.getAction(event.unicode)]
            
            if screen == "SetupMenu":
                if event.key == pygame.K_UP:
                    controlList = controlList + ["LeftstickUp"]
                if event.key == pygame.K_DOWN:
                    controlList = controlList + ["LeftstickDown"]
                if event.key == pygame.K_RIGHT:
                    controlList = controlList + ["ButtonA"]

            if event.key == pygame.K_LEFT:
                controlList = controlList + ["ButtonL"]
            
        elif event.type == pygame.JOYBUTTONUP:
            if event.dict["button"] == 1:
                controlList = controlList + [controls.getAction("ButtonA")]
            if event.dict["button"] == 2:
                controlList = controlList + [controls.getAction("ButtonX")]

    if controller != "I do not exist":
        stickX = round(controller.get_axis(0))
        if prevStickX == 1 and stickX == 0 and screen == "GamePlay":
            controlList = controlList + [controls.getAction("LeftstickRight")]
        if prevStickX == -1 and stickX == 0:
            controlList = controlList + [controls.getAction("LeftstickLeft")]
        prevStickX = stickX

        stickY = round(controller.get_axis(1))
        if prevStickY == -1 and stickY == 0:
            controlList = controlList + [controls.getAction("LeftstickUp")]
        if prevStickY == 1 and stickY == 0:
            controlList = controlList + [controls.getAction("LeftstickDown")]
        prevStickY = stickY

    if controlList == []:
        key = None
    else:
        key = controlList[0]

    if key == "ButtonL":
        running = False
        keyQuit = True
        wn.fill((0,0,0))
        writeText("Please check the Python terminal.",gameFont,red,middle(),"center",(0,0))
        pygame.display.update()

    if not running:
        break

    # SETUP MENU LOGIC
    # Computes the next frame of the setup menu.

    if screen == "SetupMenu":
        if key == "LeftstickUp":
            cursorPos = (cursorPos-1)%7
        if key == "LeftstickDown":
            cursorPos = (cursorPos+1)%7
        
        if len(unicodeKeys)>0 and cursorPos == 0:
            levelName = unicodeType(levelName,unicodeKeys[0])
        if len(unicodeKeys)>0 and cursorPos == 1:
            levelData = unicodeType(levelData,unicodeKeys[0])
        if key == "ButtonA" and cursorPos == 2:
            displayMode = 1-displayMode
        if key == "ButtonA" and cursorPos == 3:
            startMode = (startMode + 1)%4
        if key == "ButtonA" and cursorPos == 4:
            startingEditor = True
        if key == "ButtonA" and cursorPos == 5:
            show_in_file_manager(pathAssemble([]))
        if key == "ButtonA" and cursorPos == 6:
            startingGame = True

    # EDITOR LOGIC
    # Handles the map editor

    if screen == "MapEditor":
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

        if key == "LeftstickUp":
            currentPos = (currentPos[0],currentPos[1] + 1)
        if key == "LeftstickLeft":
            currentPos = (currentPos[0] - 1,currentPos[1])
        if key == "LeftstickDown":
            currentPos = (currentPos[0],currentPos[1] - 1)
        if key == "LeftstickRight":
            currentPos = (currentPos[0] + 1,currentPos[1])

        if (key == "t") and not ([(currentPos[0],currentPos[1],90)] in walls) and not ([(currentPos[0],currentPos[1],90)] in outerWalls):
            walls = walls + [(currentPos[0],currentPos[1],90)]
            walls = walls + [(currentPos[0],currentPos[1],270)]
        if (key == "f") and not ([(currentPos[0],currentPos[1],180)] in walls) and not ([(currentPos[0],currentPos[1],180)] in outerWalls):
            walls = walls + [(currentPos[0],currentPos[1],0)]
            walls = walls + [(currentPos[0],currentPos[1],180)]
        if (key == "g") and not ([(currentPos[0],currentPos[1],270)] in walls) and not ([(currentPos[0],currentPos[1],270)] in outerWalls):
            walls = walls + [(currentPos[0],currentPos[1],90)]
            walls = walls + [(currentPos[0],currentPos[1],270)]
        if (key == "h") and not ([(currentPos[0],currentPos[1],0)] in walls) and not ([(currentPos[0],currentPos[1],0)] in outerWalls):
            walls = walls + [(currentPos[0],currentPos[1],0)]
            walls = walls + [(currentPos[0],currentPos[1],180)]

        if (key == "i") and not ([(currentPos[0],currentPos[1],90)] in walls) and not ([(currentPos[0],currentPos[1],90)] in outerWalls):
            walls = walls + [(currentPos[0],currentPos[1],90)]
        if (key == "j") and not ([(currentPos[0],currentPos[1],180)] in walls) and not ([(currentPos[0],currentPos[1],180)] in outerWalls):
            walls = walls + [(currentPos[0],currentPos[1],180)]
        if (key == "k") and not ([(currentPos[0],currentPos[1],270)] in walls) and not ([(currentPos[0],currentPos[1],270)] in outerWalls):
            walls = walls + [(currentPos[0],currentPos[1],270)]
        if (key == "l") and not ([(currentPos[0],currentPos[1],0)] in walls) and not ([(currentPos[0],currentPos[1],0)] in outerWalls):
            walls = walls + [(currentPos[0],currentPos[1],0)]

        if key == "ButtonA":
            width = currentPos[0] + 1
            height = currentPos[1] + 1

    # GAME LOGIC
    # Computes the next frame of gameplay and returns display data. Everything is handled by the level's update method.

    if screen == "GamePlay":
        
        level.update(key,timer)
        currentDisplayData = level.getDisplayData()

    # JUMPSCARE LOGIC
    # Changes the current screen to the jumpscare and wdisplays it for 60 frames

    if level.game_over != False:
        screen = level.game_over
        jumpscareCounter = jumpscareCounter + 1
        if jumpscareCounter == 60:
            jumpscareCounter = 0
            startingGame = True
            if (startMode == 0) or (startMode == 3):
                break
    
    # RESET SCREEN
    # Covers up the previous frame with a black screen so new stuff can be drawn on it and not look weird
    
    wn.fill((0,0,0))

    if displayMode:
        fontSize = 50
        titleScreenY = 150
        fontOffset = 1.6
    else:
        fontSize = 30
        titleScreenY = 75
        fontOffset = 1

    gameFont = pygame.freetype.SysFont("Menlo",fontSize,True)
    gameFont.pad = True

    titleFont = pygame.freetype.SysFont("Menlo",fontSize*2,True)
    titleFont.pad = True

    smallFont = pygame.freetype.SysFont("Menlo",fontSize*0.5,True)
    smallFont.pad = True

    # SETUP MENU DISPLAY
    # Displays text on the setup menu

    if screen == "SetupMenu":
        writeText("2048 Setup Menu",titleFont,red,middle((0,titleScreenY)),"center",(0,2))

        writeText(cursorDisplay("Level name: "+levelName,0,True),gameFont,red,middle((0,titleScreenY)),"left",(-12,0))

        writeText(cursorDisplay("Level data: "+levelData,1,True),gameFont,red,middle((0,titleScreenY)),"left",(-12,-1))

        writeText(cursorDisplay("Display mode: "+{0:"Laptop",1:"TV"}[displayMode],2,False),gameFont,red,middle((0,titleScreenY)),"left",(-12,-3))

        writeText(cursorDisplay("Start mode: "+{0:"Setup menu, no retry",1:"Setup menu, retry",2:"QuickStart, retry",3:"QuickStart, no retry"}[startMode],3,False),gameFont,red,middle((0,titleScreenY)),"left",(-12,-4))

        writeText(cursorDisplay("Open map editor",4,False),gameFont,red,middle((0,titleScreenY)),"left",(-12,-6))

        writeText(cursorDisplay("Open game files folder",5,False),gameFont,red,middle((0,titleScreenY)),"left",(-12,-7))

        writeText(cursorDisplay("START GAME",6,False),gameFont,red,middle((0,titleScreenY)),"center",(0,-10))

        writeText("All updated settings are saved once the game starts.",smallFont,red,(0,0),"left",(0,0))

    # EDITOR DISPLAY
    # Displays the map editor

    if screen == "MapEditor":
        wn.fill((255,255,255))
        
        for i in range(width):
            for j in range(height):
                stampImage(pathAssemble(["assets","MapMakerImages","mapSquare.gif"]),middle((30*(i-currentPos[0]),30*(j-currentPos[1]))),False)

        for i in walls+outerWalls:
            stampImage(pathAssemble(["assets","MapMakerImages",str(i[2])+"DegreeWall.gif"]),middle((30*(i[0]-currentPos[0]),30*(i[1]-currentPos[1]))),False)
        
        stampImage(pathAssemble(["assets","MapMakerImages","painterSquare.gif"]),middle((0,0)),False)

    # GAME DISPLAY
    # Displays the graphics of the game

    if screen == "GamePlay":

        stampImage(pathAssemble(["assets","Chambers",currentDisplayData.roomType[0:-1] + "Chamber.gif"]),(0,0))
        stampImage(pathAssemble(["assets","Boxes",currentDisplayData.frontBoxNum + "Box.gif"]),(0,0))
        stampImage(pathAssemble(["assets","HydraRenders","Hydra" + currentDisplayData.hydra + ".gif"]),(0,0))
        stampImage(pathAssemble(["assets","Doors","Door" + currentDisplayData.door + ".gif"]),(0,0))

        writeText(currentDisplayData.gridDisplay,gameFont,(255,0,0),(0,0),"left",(fontOffset,-0.5))

    # JUMPSCARE DISPLAY
    # You know what this does.

    if "HydraJumpscare" in screen:
        stampImage(pathAssemble(["assets","EndScreens",level.game_over+".gif"]),(0,0))

    pygame.display.update()

if keyQuit:
    startMode = 0
    print("Type the debug password below to enable the setup menu the next time the game is run.")
    if input("~ ") == "debugger666":
        updateStartData()

pygame.quit()