from game import *
from time import sleep

game = Into2048("Classic?",4,4,True,True,[],[])
controls = ControlConverter()

controls.set("forward",["w"])
controls.set("backward",["s"])
controls.set("right",["d"])
controls.set("left",["a"])
controls.set("spawn",["z"])
controls.set("destroy",["x"])

while True:
    game.start()
    timer = 0

    while not game.game_over:
        systemClear()
        display = game.getDisplayData()
        print(display.gridDisplay)
        print("Hydra at: " + display.hydra)
        print()
        control = input("Act: ")
        if control == "m":
            systemClear()
            print("You quit the game.")
            exit()
        game.update(controls.getAction(control),timer)

    systemClear()
    print("You died ):")
    sleep(1)