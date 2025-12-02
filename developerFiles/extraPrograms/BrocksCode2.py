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
        self.game_over = False
        if grid == "default":
            self.num_grid = [[0 for j in range(height)] for i in range(length)]
            #Stores a list of tuples that act as coordinates for the empty slots in self.num_grid
            self.empty_slot_indexes = [(i, j) for i in range(len(self.num_grid))
                                       for j in range(len(self.num_grid[i]))
                                       if self.num_grid[i][j] == 0]
            self.generate_tiles()
        else:
            self.num_grid = grid
            #Stores a list of tuples that act as coordinates for the empty slots in self.num_grid
            self.empty_slot_indexes = [(i, j) for i in range(len(self.num_grid))
                                       for j in range(len(self.num_grid[i]))
                                       if self.num_grid[i][j] == 0]

        self.spawn_player()
        self.spawn_hydra()
        
    #Generate a random 2048 number. Can only be 2 or 4
    def _generate_num(self):
        return random.choices([2,4], weights=(90,10))[0]
    
    #Generate and place 2 new tiles (1 if only 1 space is available)
    def generate_tiles(self):
        if len(self.empty_slot_indexes) == 1:
            self.num_grid[self.empty_slot_indexes[0][0]][self.empty_slot_index[0][1]] = self._generate_num()
            self.empty_slot_indexes = [] #After filling the last empty square on num_grid, there are no more empty slots
            return
        for i in random.sample(self.empty_slot_indexes, k=2):
            self.num_grid[i[0]][i[1]] = self._generate_num()
            self.empty_slot_indexes.remove(i)


    def spawn_player(self):
        self.player_pos = tuple(random.choice(self.empty_slot_indexes)) #This variable is used to find player position
        self.empty_slot_indexes.remove(self.player_pos)

    def spawn_hydra(self):
        self.hydra_pos = tuple(random.choice(self.empty_slot_indexes))

    def move_player(self, dir):
        new_pos = tuple(self.player_pos[i] + dir[i] for i in range(2))
        if new_pos == self.hydra_pos:
            self.game_over = True
        if new_pos[0] < 0 or new_pos[0] >= len(self.num_grid) or new_pos[1] < 0 or new_pos[1] >= len(self.num_grid[0]):
            return
        new_pos_value = self.num_grid[new_pos[0]][new_pos[1]]
        if new_pos_value != 0:
            if not self._push(new_pos, dir):
                return
        self.empty_slot_indexes.append(self.player_pos)
        if new_pos in self.empty_slot_indexes:
            self.empty_slot_indexes.remove(new_pos)
        self.player_pos = new_pos

    def move_hydra(self, approach_probability=50):
        if random.choices((True, False), weights=(approach_probability, 100-approach_probability)): #Random movement
            dirs = []
            if self.hydra_pos[0] < self.player_pos[0]:
                dirs.append(DOWN)
            else:
                dirs.append(UP)
            if self.hydra_pos[1] < self.player_pos[1]:
                dirs.append(RIGHT)
            else:
                dirs.append(LEFT)
            dir = random.choice(dirs)
        else:
            dir = random.choice((UP,DOWN,LEFT,RIGHT))
        
        new_pos = tuple(self.hydra_pos[i] + dir[i] for i in range(2))
        if self.player_pos == new_pos:
            self.game_over = True
        if new_pos[0] < 0 or new_pos[0] >= len(self.num_grid) or new_pos[1] < 0 or new_pos[1] >= len(self.num_grid[0]):
            return
        self.hydra_pos = new_pos
            


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

while not N.game_over:
    os.system("clear")
    print(N.player_pos)
    print(N.hydra_pos)
    print(N.game_over)
    for y in range(4):
        for x in range(4):
            if N.player_pos == (y, x):
                print("x", end = "\t")
                continue
            if N.hydra_pos == (y, x):
                if N.num_grid[y][x] == 0:
                    print("+", end = "\t")
                else:
                    print("+" + str(N.num_grid[y][x]), end = "\t")
                continue
            print(N.num_grid[y][x], end = "\t")
        print()
    print()
    
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
    else:
        print("invalid, use WASD")
    N.move_hydra(50) #The number represents the % chance of the hydra 
                     # approaching the player vs moving randomly. 50% chance if unspecified