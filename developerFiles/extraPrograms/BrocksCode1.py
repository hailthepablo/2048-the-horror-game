import random
import os
"""remember who you are"""
UP =    (-1,0)
DOWN =  (1,0)
LEFT =  (0,-1)
RIGHT = (0,1)


#This class creates a 2d list representing the 2048 game board when
#called, and handles all the interactions that can happen in the game
class Into2048:
    def __init__(self, length=4, height=4, grid="default"):
        if grid == "default":
            self.num_grid = [[0 for i in range(height)] for j in range(length)]
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
        self.playerpos = tuple(random.choice(empty_slot_indexes))
        self.num_grid[self.playerpos[0]][self.playerpos[1]] = "x"
    
    def move_player(self, dir):
        new_pos = tuple(self.playerpos[i] + dir[i] for i in range(2))
        print(new_pos)
        if new_pos[0] < 0 or new_pos[0] >= len(self.num_grid) or new_pos[1] < 0 or new_pos[1] >= len(self.num_grid[0]):
            return
        new_pos_value = self.num_grid[new_pos[0]][new_pos[1]]
        if new_pos_value != 0:
            if not self._push(new_pos, dir):
                return
        self.num_grid[self.playerpos[0]][self.playerpos[1]] = 0
        self.playerpos = new_pos
        self.num_grid[self.playerpos[0]][self.playerpos[1]] = "x"

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

#main
grid = [
    [0,0,0,0],
    [0,4,4,8],
    [0,8,8,16],
    [0,0,0,0]
]
N = Into2048()

while True:
    for y in range(4):
        for x in range(4):
            print(N.num_grid[y][x], end = "\t")
        print()
    print()

    print(N.playerpos)
    
    dir = input("move: ")
    if dir == "w":
        N.move_player(UP)
    elif dir == "a":
        N.move_player(LEFT)
    elif dir == "s":
        N.move_player(DOWN)
    elif dir == "d":
        N.move_player(RIGHT)
    elif dir == "1":
        N.generate_tiles()
    os.system("clear")