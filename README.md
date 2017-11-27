# Tic Tac Toe


## Introduction

This small program demonstrates the use of [Minimax Algorithm](https://en.wikipedia.org/wiki/Minimax) for playing the game of [Tic Tac Toe](https://en.wikipedia.org/wiki/Tic-tac-toe).


## Notes
The game requires the library pygame and runs on Python 2.7. I tried installing and running the game using pygame installed on Python 3.6 but faced issues related to mouse events. Since the objective was not to have a beautiful looking GUI but just to demonstrate the usage of Minimax Algorithm for playing Tic Tac Toe, i went ahead using Python 2.7. Also, the GUI implemented isnt incredible, but works. The requirements.txt files gives the details of the environment I executed the code in and contains lot more libraries than we require for the game.


## TODO

- The startup for the game is slow, the first time minimax is called. This is something to work on next. Try implementing Alpha Beta pruning.
- GUI isnt clean, especially the text message shown towards the bottom. To have a hacky solution in place to get working around the problem of overwritten text in the status bar.
- To start a new game, we need to close the window and restart the game. Restarting the game without restarting the program would de desirable.
- As we need to restart the game each time it is complete, we cannot keep a track of the number of ties, loses and wins.  
- No option to let computer start, the human always plays the first move 