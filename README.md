# **2048_solver**
---
Solving my 2048 clone using PyGame using artificial intelligence. Specifically using Alpha-Beta pruning and Expectimax.

![gif_for_final](https://user-images.githubusercontent.com/70533514/235511499-ed6f0a52-f4f7-40e5-89be-3e85d71477a7.gif)

<br>

# **Installation**
---
1. Make sure you have the following packages installed: 
PyGame, NumPy
  
2. Clone the repo:

`git clone https://github.com/noahnisbet/2048_solver.git`

3. From inside the 2048_solver directory execute:

`python3 2048_solver.py`

After that simply interact with the PyGame UI. Additional intructions appear
in the terminal once the game is runnning.

<br>

# **More Info**
---
This is a Simulation that uses adversarial search algorithms to solve the game 2048. 2048 is a popular single-player game where players slide tiles in a four-by-four grid, combining like-valued tiles until they reach the 2048 tile. Although you do not have to stop there, you can continue after the 2048 tile has been reached. I implement the expectimax and alpha-beta pruning algorithms to solve 2048. To do this, I created the game from scratch using PyGame, which involved building the moving mechanism, random spawning of tiles, a user interface, and other game functionalities. Then, I implemented the adversarial search algorithms. For the adversarial search algorithms to work, I developed my own evaluation function to determine the current value of the board and the algorithms themselves.


