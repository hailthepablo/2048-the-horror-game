# 2048: The Horror Game

This repository is for both the original Python and the eventual C++ versions of 2048: The Horror Game.

## Setup instructions

If you want to play the terminal only version of the game, the setup is pretty simple. Just clone the repository onto your computer, then navigate to the Python folder and run *terminal.py*. For the windowed version, you will have to download Pygame by running
```bash
pip install pygame
```
and then run *windowed.py*.

## Gameplay instructions

In the top-left of the screen, you will see a minimap that looks similar to this:
```
0    0    0    2  
0    0    0    0  
0    <    0    2  
0    0    0    0  
```
If you are playing the terminal only version, this will be shown directly in your terminal.

The arrow (<) is your character, and points in the direction you are facing. There are also numbers on the grid that you can push if you move into them. If you push two of the same number into each other, they will add together.

For example, if you have a setup like this:
```
0    0    0    0  
0    2    2    <  
0    0    0    0  
0    0    0    0  
```
Then if you push the 2s into each other, you get:
```
0    0    0    0  
0    4    <    0  
0    0    0    0  
0    0    0    0  
```
This means that the only numbers that you can get (besides 0) are powers of 2, such as 2, 4, 8, 16, 32, and so on up to 2048. You cannot combine different numbers, but you can push rows of them.

## Controls

The controls here are pretty simple, being a variation on standard **WASD** controls.

**W** to move forward  
**A** to turn left  
**S** to move backward  
**D** to turn right  

There are two other useful controls in this game:

**Z** to spawn 2 new numbers in random locations on the grid (can either be a 2 or a 4, but 4 is more rare)  
**X** to destroy the number in front of you

In the terminal version, you will have to press **Enter** after each keypress.

## Why is it a horror game?

Based on what I've described so far, it doesn't really seem like this is a horror game. However, once you play the game, you will see that there is much more than the minimap. You will be traversing a dark grid of chambers where you push these numbers around. Though I won't tell you why, as it would spoil the fun, be sure to look at the main screen. It's easy to get distracted by the minimap, but the main screen may tell you if you're in danger. As for the terminal version, you might want to look at the text right below the minimap. You'll need it if you want to survive.

Something is lurking in the shadows...



