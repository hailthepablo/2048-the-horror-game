import os
length = 4
height = 4

grid = [[(0,0),(0,1),(0,2),(0,3)],[(1,0),(1,1),(1,2),(1,3)],[(2,0),(2,1),(2,2),(2,3)],[(3,0),(3,1),(3,2),(3,3)]]
grid = [[0 for j in range(height)] for i in range(length)]

currentPos = (0,0)

while 1==1:
    os.system("clear")
    print(grid[currentPos[0]][currentPos[1]])
    action = input()
    if action == "w":
        currentPos = (currentPos[0],currentPos[1]+1)
    if action == "a":
        currentPos = (currentPos[0]-1,currentPos[1])
    if action == "s":
        currentPos = (currentPos[0],currentPos[1]-1)
    if action == "d":
        currentPos = (currentPos[0]+1,currentPos[1])