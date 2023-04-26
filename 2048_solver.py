# Noah Nisbet
# 2048 Clone using PyGame
# Solving using Alpha-Beta pruning & Expectimax Algorithms

# Import the pygame module
import pygame
import os
import random
from itertools import permutations
import time
import math
import copy

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_SPACE,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_e,
    K_a,
    K_r,
    K_b,
    KEYDOWN,
    QUIT,
)

# Print out the directions of the game to terminal
def print_directions():
    print()
    print("Artificial Intelligence Final Project")
    print()
    print("**CLICK ON PYTHON WINDOW \"AI HW1\" AND THEN PRESS KEYS TO USE.")
    print("**2048, try to combine tiles until you get 2048")
    print()
    print("BASIC COMMANDS:")
    print("\tUP to move blocks up")
    print("\tDOWN to move blocks down")
    print("\tLEFT to move blocks left")
    print("\tRIGHT to move blocks right")
    print("\tA to start Alpha-Beta Pruning Algorithm")
    print("\tE to start Expectimax Algorithm")
    print("\tB to use combination of both")
    print("\tR to move randomly")


##########################################################
# 2048 Game class
#
# Holds the 2048 implementation code with
# adversarial search algorithm implementations
##########################################################
class Game:
	# initialize the start of the game
	def __init__(self):
		# create the board
		self.board = []
		# board 2 is used to check if the board changes after a move
		self.board2 = []
		# score of the game, sum of all combinations of tiles
		self.score = 0

		# create both boards
		for i in range(4):
			self.board.append([])
			self.board2.append([])
			for _ in range(4):
				self.board[i].append(0)
				self.board2[i].append(-1)

		# spawn in first two tiles, always a four and a two.
		for k in range(2):
			i = random.randint(0,3)
			j = random.randint(0,3)
			if k == 1:
				self.board[i][j] = 2
			else:
				self.board[i][j] = 4

		# dictionary holding colors of tile values
		self.color_dict = {
			0:(202,192,180),
			2:(239,234,227),
			4:(237,230,214),
			8:(229,193,152),
			16:(225,171,132),
			32:(221,152,126),
			64:(217,128,94),
			128:(233,215,151),
			256:(232,209,127),
			512:(232,209,127),
			1024:(233,208,122),
			2048:(232,206,111),
			4096:(175,134,169)
		}

	##########################################################
	# get_boards returns both boards
	##########################################################
	def get_boards(self):
		return self.board, self.board2

	##########################################################
	# returns the score of the game
	##########################################################
	def get_score(self):
		return self.score
	
	##########################################################
	# spawn blocks randomly spawns tiles onto empty tiles
	# on the board
	##########################################################
	def spawn_blocks(self):
		# find empty cells, if the element in 2D array
		# is 0 append tuple of (x,y)
		empty_cells = []
		for i in range(4):
			for j in range(4):
				if self.board[i][j] == 0:
					empty_cells.append((i,j))

		# if there are no empty cells the game is over
		if len(empty_cells) == 0:
			self.game_over = True
		# otherwise spawn cells
		else:
			# spawn a two in a random open tile, but with a 10% chance
			# spawn a 4 instead.
			cell_num = empty_cells[random.randint(0,len(empty_cells)-1)]
			cell_value = 2
			if random.randint(0,9) == 0:
				cell_value = 4
			self.board[cell_num[0]][cell_num[1]] = cell_value

	##########################################################
	# print the 2D array representation of the board.
	##########################################################
	def print_board(self):
		print(self.board)

	##########################################################
	# print the pygame representation of the board.
	##########################################################
	def print_pygame(self):
		# set the font
		font = pygame.font.SysFont(None, 50)
		# sentinel value, this holds the value 1 if the board 
		# has changed
		sentinel = 0
		for i in range(4):
			for j in range(4):
				if self.board[i][j] != self.board2[i][j]:
					sentinel = 1

		# If the board has changed then print the board.
		if sentinel == 1:
			# start by filling background with a greyish color
			screen.fill((185,172,161))
			# loop over all tiles in the 2D array representation of the game
			for i in range(4):
				for j in range(4):
					# get the colors of the tiles using the color_dict in __init__
					if self.board[i][j] in self.color_dict:
						color = self.color_dict[self.board[i][j]]
					else:
						color = self.color_dict[4096]

					# draw the rectange of the tile using color and location in
					# 2D array
					rectangle = pygame.Rect(15+100*i, 65+100*j, 95, 95)
					pygame.draw.rect(screen,color,rectangle)

					# if the 2D array at i,j holds a value other than 0 (empty)
					# add text of the value of the tile.
					if self.board[i][j] != 0:
						# center the text depending on number of characters
						if self.board[i][j] in [2,4]:
							img = font.render(str(self.board[i][j]), True, (116,110,102))
						else:
							img = font.render(str(self.board[i][j]), True, (255,255,255))
						if self.board[i][j] < 10:
							screen.blit(img, (50+100*i, 100+100*j))
						elif self.board[i][j] < 100:
							screen.blit(img, (43+100*i, 100+100*j))
						elif self.board[i][j] < 1000:
							screen.blit(img, (36+100*i, 100+100*j))
						else:
							screen.blit(img, (23+100*i, 100+100*j))
			
			# print the score
			font = pygame.font.SysFont(None, 40)
			img = font.render(f"Score: {self.score}", True, (255,255,255))
			screen.blit(img, (30, 20))

			# update screen
			screen_display.update()
			
			# update board2 so that the screen will not be updated until another
			# change occurs in board
			for i in range(4):
				for j in range(4):
					self.board2[i][j] = self.board[i][j]


	##########################################################
	# move function, this move function changed the value in
	# self.board. There is another move function that does
	# the same steps but instead returns the resulting board
	#
	# dir map:
	# 1 = left
	# 2 = right
	# 3 = up
	# 4 = down
	##########################################################

	def move(self, dir):
		# if directions is 1 move tiles left
		if dir == 1:
			# loop over tiles on board
			for i in range(4):
				for j in range(4):
					# if tile j,i is zero loop over the row from that point
					if self.board[j][i] == 0:
						for k in range(j,4):
							# if a tile is found to the left of tile j,i replace
							# j,i with the new tile and the new tile becomes zero
							if self.board[k][i] != 0:
								self.board[j][i] = self.board[k][i]
								self.board[k][i] = 0
								break # after the tiles have been replaced break out of current loop
				
				#  handles combining tiles
				# since we are combining to the left loop over the rows and check for neighboring
				# tiles that are the same after being pushing together above
				
				# if the first column equals the second column in the current row
				if self.board[0][i] == self.board[1][i]:
					# the double value in current row, first column
					self.board[0][i] = 2*self.board[0][i]
					# add the new value of current row, first column to score
					self.score+=self.board[0][i]
					# current row, second column now equals zero
					self.board[1][i] = 0
				
				# same logic as above just working its way over
				if self.board[1][i] == self.board[2][i]:
					self.board[1][i] = 2*self.board[1][i]
					self.score+=self.board[1][i]
					self.board[2][i] = 0

				if self.board[2][i] == self.board[3][i]:
					self.board[2][i] = 2*self.board[2][i]
					self.score+=self.board[2][i]
					self.board[3][i] = 0

			# push the values over again, this is because combining tiles can unintentionally
			# leave spaces
			for i in range(4):
				for j in range(4):
					if self.board[j][i] == 0:
						for k in range(j,4):
							if self.board[k][i] != 0:
								self.board[j][i] = self.board[k][i]
								self.board[k][i] = 0
								break
		
		# moving right if dir = 2
		if dir == 2:
			# same logic as above just working from right to left
			# instead of left->right

			for i in range(4):
				for j in range(3,-1,-1):
					if self.board[j][i] == 0:
						for k in range(j,-1, -1):
							if self.board[k][i] != 0:
								self.board[j][i] = self.board[k][i]
								self.board[k][i] = 0
								break

				if self.board[2][i] == self.board[3][i]:
					self.board[2][i] = 2*self.board[2][i]
					self.score+=self.board[2][i]
					self.board[3][i] = 0

				if self.board[1][i] == self.board[2][i]:
					self.board[1][i] = 2*self.board[1][i]
					self.score+=self.board[1][i]
					self.board[2][i] = 0

				if self.board[0][i] == self.board[1][i]:
					self.board[0][i] = 2*self.board[0][i]
					self.score+=self.board[0][i]
					self.board[1][i] = 0

				

			for i in range(4):
				for j in range(3,-1,-1):
					if self.board[j][i] == 0:
						for k in range(j,-1, -1):
							if self.board[k][i] != 0:
								self.board[j][i] = self.board[k][i]
								self.board[k][i] = 0
								break
		
		# if directions is 3 move tiles up
		if dir == 3:
			# same logic as above just working from top to bottom
		
			for i in range(4):
				for j in range(4):
					if self.board[i][j] == 0:
						for k in range(j,4):
							if self.board[i][k] != 0:
								self.board[i][j] = self.board[i][k]
								self.board[i][k] = 0
								break

				if self.board[i][0] == self.board[i][1]:
					self.board[i][0] = 2*self.board[i][0]
					self.score+=self.board[i][0]
					self.board[i][1] = 0

				if self.board[i][1] == self.board[i][2]:
					self.board[i][1] = 2*self.board[i][1]
					self.score+=self.board[i][1]
					self.board[i][2] = 0

				if self.board[i][2] == self.board[i][3]:
					self.board[i][2] = 2*self.board[i][2]
					self.score+=self.board[i][2]
					self.board[i][3] = 0

			for i in range(4):
				for j in range(4):
					if self.board[i][j] == 0:
						for k in range(j,4):
							if self.board[i][k] != 0:
								self.board[i][j] = self.board[i][k]
								self.board[i][k] = 0
								break
				
		# if directions is 3 move tiles down
		if dir == 4:
			# same logic as above just working from bottom to top

			for i in range(4):
				for j in range(3,-1,-1):
					if self.board[i][j] == 0:
						for k in range(j,-1, -1):
							if self.board[i][k] != 0:
								self.board[i][j] = self.board[i][k]
								self.board[i][k] = 0
								break

				if self.board[i][2] == self.board[i][3]:
					self.board[i][2] = 2*self.board[i][3]
					self.score+=self.board[i][2]
					self.board[i][3] = 0

				if self.board[i][1] == self.board[i][2]:
					self.board[i][1] = 2*self.board[i][1]
					self.score+=self.board[i][1]
					self.board[i][2] = 0

				if self.board[i][0] == self.board[i][1]:
					self.board[i][0] = 2*self.board[i][0]
					self.score+=self.board[i][0]
					self.board[i][1] = 0

			for i in range(4):
				for j in range(3,-1,-1):
					if self.board[i][j] == 0:
						for k in range(j,-1, -1):
							if self.board[i][k] != 0:
								self.board[i][j] = self.board[i][k]
								self.board[i][k] = 0
								break

	##########################################################
	# this is important for the evaluation function
	# moves a board parameter based on dir and returns the new board and
	# score
	##########################################################
	def move2(self,board,dir):
		board = copy.deepcopy(board)
		score = self.score

		## Same logic as the orginal move function
		if dir == 1:
			for i in range(4):
				for j in range(4):
					if board[j][i] == 0:
						for k in range(j,4):
							if board[k][i] != 0:
								board[j][i] = board[k][i]
								board[k][i] = 0
								break

				if board[0][i] == board[1][i]:
					board[0][i] = 2*board[0][i]
					score+=board[0][i]
					board[1][i] = 0

				if board[1][i] == board[2][i]:
					board[1][i] = 2*board[1][i]
					score+=board[1][i]
					board[2][i] = 0

				if board[2][i] == board[3][i]:
					board[2][i] = 2*board[2][i]
					score+=board[2][i]
					board[3][i] = 0

			for i in range(4):
				for j in range(4):
					if board[j][i] == 0:
						for k in range(j,4):
							if board[k][i] != 0:
								board[j][i] = board[k][i]
								board[k][i] = 0
								break

		if dir == 2:
			for i in range(4):
				for j in range(3,-1,-1):
					if board[j][i] == 0:
						for k in range(j,-1, -1):
							if board[k][i] != 0:
								board[j][i] = board[k][i]
								board[k][i] = 0
								break

				if board[2][i] == board[3][i]:
					board[2][i] = 2*board[2][i]
					score+=board[2][i]
					board[3][i] = 0

				if board[1][i] == board[2][i]:
					board[1][i] = 2*board[1][i]
					score+=board[1][i]
					board[2][i] = 0

				if board[0][i] == board[1][i]:
					board[0][i] = 2*board[0][i]
					score+=board[0][i]
					board[1][i] = 0

				

			for i in range(4):
				for j in range(3,-1,-1):
					if board[j][i] == 0:
						for k in range(j,-1, -1):
							if board[k][i] != 0:
								board[j][i] = board[k][i]
								board[k][i] = 0
								break
		
		if dir == 3:
			for i in range(4):
				for j in range(4):
					if board[i][j] == 0:
						for k in range(j,4):
							if board[i][k] != 0:
								board[i][j] = board[i][k]
								board[i][k] = 0
								break

				if board[i][0] == board[i][1]:
					board[i][0] = 2*board[i][0]
					score+=board[i][0] 
					board[i][1] = 0

				if board[i][1] == board[i][2]:
					board[i][1] = 2*board[i][1]
					score+=board[i][1]
					board[i][2] = 0

				if board[i][2] == board[i][3]:
					board[i][2] = 2*board[i][2]
					score+=board[i][2] 
					board[i][3] = 0

			for i in range(4):
				for j in range(4):
					if board[i][j] == 0:
						for k in range(j,4):
							if board[i][k] != 0:
								board[i][j] = board[i][k]
								board[i][k] = 0
								break
				
		if dir == 4:

			for i in range(4):
				for j in range(3,-1,-1):
					if board[i][j] == 0:
						for k in range(j,-1, -1):
							if board[i][k] != 0:
								board[i][j] = board[i][k]
								board[i][k] = 0
								break

				if board[i][2] == board[i][3]:
					board[i][2] = 2*board[i][3]
					score+=board[i][2]
					board[i][3] = 0

				if board[i][1] == board[i][2]:
					board[i][1] = 2*board[i][1]
					score+=board[i][1]
					board[i][2] = 0

				if board[i][0] == board[i][1]:
					board[i][0] = 2*board[i][0]
					score+=board[i][0]
					board[i][1] = 0

			for i in range(4):
				for j in range(3,-1,-1):
					if board[i][j] == 0:
						for k in range(j,-1, -1):
							if board[i][k] != 0:
								board[i][j] = board[i][k]
								board[i][k] = 0
								break
	
		return board, score

	##########################################################
	# checks if a state is terminal 
	# uses move2 to see if any move you make will result in no zeros on the board
	#
	# this is important because sometimes there are no empty tiles, but
	# you can still combine tiles to continue.
	##########################################################
	def terminal(self, board: list):
		res = True
		for i in range(1,5):
			next, _ = self.move2(board,i)
			for i in range(4):
				for j in range(4):
					if next[i][j] == 0:
						res = False

		return res
	
	##########################################################
	# Evaluation function
	#
	# Basic Strategy:
	# Reward combining tiles.
	# Reward tiles on the sides and penalize tiles in middle. Extra reward to the corner with the greatest tile.
	# Reward tiles with similar values neighboring each other and penalize large differences in tile values neighboring.
	# Penalize tiles on the board less than 128.
	# Penalize moving tiles greater than 128 without combining them.
	#
	# inputs are parent_board (previous state), board (current board), score (displayed game score, this is manipulated to get
	# an evaluation score) 
	##########################################################
	def evaluate(self, parent_board: list, board: list, score):
		
		# if the current state is nerminal add a really large negative score
		if self.terminal(board):
			return -99999999999999999+score
		
		# multiply the current score by 5 to give it more weight
		score = score*5

		# sentinel value for checking if the greatest tile in the corner bonus has been used.
		sentinel = 0
		# loop over tiles on board
		for i in range(4):
			for j in range(4):
				# any tile less than or equal to 64 has a penalty for simply being on the board
				if board[i][j] <= 64:
					score = score - (board[i][j]*(70-board[i][j]))

				# decentivize moving large tiles
				# checking if the current tile has changed from the parent board
				# and that the new tile has not become 2 times its previous value
				if (parent_board[i][j] != board[i][j]) or (board[i][j] != 0) or (2*parent_board[i][j] != board[i][j]):
					# if condition is met subtract 12 * the moved tile
					score = score - 8*parent_board[i][j]

				# checking for all neighbors
				# if the values are close in tile value add to score
				if (i != 3 and (board[i][j] == board[i+1][j] or board[i][j] == 2*board[i+1][j] or 2*board[i][j] == board[i+1][j])):
					score = score + board[i][j]
				# if the are far from each other decrease from score scaling on the difference
				elif (i != 3 and (board[i][j] > 2*board[i+1][j] or 2*board[i][j] > board[i+1][j])):
					score = score - 2.2*abs(board[i+1][j] - board[i][j])

				# if the values are close in tile value add to score
				if (j != 3 and (board[i][j] == board[i][j+1] or board[i][j] == 2*board[i][j+1] or 2*board[i][j] == board[i][j+1])):
					score = score + board[i][j]
				# if the are far from each other decrease from score scaling on the difference
				elif (j != 3 and (board[i][j] > 2*board[i][j+1] or 2*board[i][j] > board[i][j+1])):
					score = score - 2.2*abs(board[i][j+1] - board[i][j])

				# if the values are close in tile value add to score
				if (i != 0 and (board[i][j] == board[i-1][j] or board[i][j] == 2*board[i-1][j] or 2*board[i][j] == board[i-1][j])):
					score = score + board[i][j]
				# if the are far from each other decrease from score scaling on the difference
				elif (i != 0 and (board[i][j] > 2*board[i-1][j] or 2*board[i][j] > board[i-1][j])):
					score = score - 2.2*abs(board[i-1][j] - board[i][j])

				# if the values are close in tile value add to score
				if (j != 0 and (board[i][j] == board[i][j-1] or board[i][j] == 2*board[i][j-1] or 2*board[i][j] == board[i][j-1])):
					score = score + board[i][j]
				# if the are far from each other decrease from score scaling on the difference
				elif (j != 0 and (board[i][j] > 2*board[i][j-1] or 2*board[i][j] > board[i][j-1])):
					score = score - 2.2*abs(board[i][j-1] - board[i][j])
				
				# if the tile is on the side enter
				if i == 0 or i == 3 or j == 0 or j == 3:
					value = board[i][j]
					# if the tile value is less than 16 decrease from score for being on the side
					if value < 16:
						value*=-4
					# if the tile value is greater than 500 add to score
					if value >= 500:
						value*=8	
					# if the tile value is greater than 100 add a lot to score
					if value >= 1000:
						value*=16

					# multiplier for tiles on sides
					multiplier = 0
					# if tile is on the side add one to multiplier
					if i == 0:
						multiplier+=1
					elif j == 0:
						multiplier+=1
					elif i == 3:
						multiplier+=1
					elif j == 3:
						multiplier+=1	
					# if the sentinel value is still zero (bonus is not claimed)
					# add is is in the corner add 4 to multiplier
					elif j == 3 and i == 3 and sentinel == 0:
						multiplier+=4	
						sentinel = 1
					elif j == 3 and i == 0 and sentinel == 0:
						multiplier+=4
						sentinel = 1
					elif j == 0 and i == 3 and sentinel == 0:
						multiplier+=4
						sentinel = 1
					elif j == 0 and i == 0 and sentinel == 0:
						multiplier+=4	
						sentinel = 1
					# add to score value * multiplier
					score = score + multiplier*value

				# decentivize large values in middle
				if i == 1 or i == 2 or j == 1 or j == 2:
					value = board[i][j]
					# if the value is large add an extra penalization for being in the middle 
					if value >= 128:
						value*=4
					# add a multipier for being in middle
					multiplier = 0
					if i == 1:
						multiplier+=1
					if j == 1:
						multiplier+=1
					if i == 2:
						multiplier+=1
					if j == 2:
						multiplier+=1
					score = score - multiplier*value

		return score

	##########################################################
	# gets all possible boards resulting from a state depending on current player
	##########################################################
	def get_child_boards(self, player, board: list):

		# if player equals one use move2 to find possible states
		if player == 1:
			res = []
			for i in range(1,5):
				toappend = []
				temp, score = self.move2(board,i)
				if temp != board:
					toappend.append(i)
					toappend.append(copy.deepcopy(temp))
					toappend.append(score)
					res.append(toappend)

			return res
		
		# otherwise find all empty tiles and add to res a version where that empty tile now
		# is 2 or 4.
		else:
			res = []
			for i in range(4):
				for j in range(4):
					if board[i][j] == 0:
						board[i][j] = 2
						res.append(copy.deepcopy(board))
						# board[i][j] = 4
						# res.append(copy.deepcopy(board))
						board[i][j] = 0
			return res

	
	##########################################################
	# Expectimax implementation using depth parameter
	##########################################################
	def expectimax(self, depth_limit: int):

		# the following functions recursively call eachother and decrement depth at each "move"

		# define the expected value for player function (expected score after environment move)
		def expected_value_for_max(parent_board: list, board: list, depth_limit: int, score2):
			# if the board is terminal or the depth is zero return the evaluation function's score
			if self.terminal(board) or depth_limit == 0:
				return None, self.evaluate(parent_board, board, score2)
			
			# loop over the child boards and average their scores from max_value
			scores = []
			for child_board in self.get_child_boards(2, board):
				_, score = max_value(board, child_board, depth_limit-1, score2)
				scores.append(score)

			expected_score = sum(scores) / len(scores)
			return None, expected_score
		
		# define the value function of players moves
		def max_value(parent_board:list, board: list, depth_limit: int, score2):
			if self.terminal(board) or depth_limit == 0:
				return None, self.evaluate(parent_board, board, score2)

			# loop over child boards and find the best score from the expected value function.
			best_score = -math.inf
			best_move = None
			for move, child_board, score2 in self.get_child_boards(1, board):
				_, score = expected_value_for_max(board, child_board, depth_limit - 1, score2)
				if score > best_score:
					best_score = score
					best_move = move

			return best_move, best_score

		# call max value first since it is "our move"
		best_move, _ = max_value(self.board,self.board,depth_limit,0)

		return best_move

	##########################################################
	# alphabeta implementation
	##########################################################
	def alphabeta(self, depth_limit):
		
		# max value function for player (you)
		# takes in the parent_board (previous board), board (current board),
		# a depth limit, beta, and score2 (score of child board / current board)
		def max_value(parent_board, board, depth_limit, alpha, beta, score2):
			# if the board is at a terminal state or the depth is at zero return
			# the evaluation score
			if self.terminal(board) or depth_limit == 0:
				return None, self.evaluate(parent_board, board, score2)
			
			# define best_score, best_move and alpha
			best_score = -math.inf
			best_move = None

			# get child boards and call min_value
			for move, child_board, score2 in self.get_child_boards(1, board):
				_, score = min_value(board, child_board, depth_limit - 1, alpha, beta, score2)
				# if the current score of the child board is better than best score make that the best move
				if score > best_score:
					best_score = score
					best_move = move
				# alpha is the greatest of best score and alpha
				alpha = max(alpha, best_score)
				# if alpha is ever greater than or equal to beta then break
				if beta <= alpha:
					break
			
			return best_move, best_score
	
		# min value function for environment
		# takes in the parent_board (previous board), board (current board),
		# a depth limit, beta, and score2 (score of child board / current board)
		def min_value(parent_board, board, depth_limit, alpha, beta, score2):
			# if the board is at a terminal state or the depth is at zero return
			# the evaluation score
			if self.terminal(board) or depth_limit == 0:
				return None, self.evaluate(parent_board, board, score2)

			# define best score and beta
			best_score = math.inf

			# get all the child boards resulting from an environment move and find the max value using
			# max value function
			for child_board in self.get_child_boards(2, board):
				_, score = max_value(board, child_board, depth_limit-1, alpha, beta, score2)
				# score is the worst possible state resulting from max_value
				if score < best_score:
					best_score = score

				# beta is the worst score so far
				beta = min(beta, best_score)
				# if beta is ever less than or equal to alpha break
				if beta <= alpha:
					break
			
			return None, best_score

		# call max_value since it always is "our move" 
		placement, _ = max_value(self.board,self.board,depth_limit,-math.inf,math.inf,0)

		# return resulting placement
		return placement

	# return a random number from 1-4	
	def random_move(self):
		return random.randint(1,5)
	
	##########################################################
	# after game has ended display score and then reset
	##########################################################
	def endGame(self):
		string = ""
		isWon = False
		for i in range(4):
			for j in range(4):
				if self.board[i][j] >= 2048:
					isWon = True

		if isWon:
			string = "Congratulations you won!"
			print(string)
		else:
			string = f"Game over! Final Score: {self.score}"
			print(string)

		screen.fill((185,172,161))
		font = pygame.font.SysFont(None, 40)
		img = font.render(string, True, (255,255,255))
		screen.blit(img, (10,200))
		if isWon:
			string = f"Final Score: {self.score}"
			print(string)
			img = font.render(string, True, (255,255,255))
			screen.blit(img, (10,250))

		screen_display.update()

		time.sleep(3)

		self.__init__()

##########################################################
# main function for calling appropriate functions in Game 
# class
##########################################################
if __name__ == "__main__":
	# Initialize pygame
	pygame.init()
	wd = os.getcwd()
	print_directions()

	# Define constants for the screen width and height
	SCREEN_WIDTH = 425
	SCREEN_HEIGHT = 475

	# Create the screen object
	# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	screen_display = pygame.display

	# set the pygame window name
	screen_display.set_caption('2048')

	# Variable to keep the main loop running
	running = True

	curGame = Game()

	while running:
		# Look at every event in the queue
		for event in pygame.event.get():
			# Did the user hit a key?
			if event.type == KEYDOWN:
				# Was it the Escape key? If so, stop the loop.
				if event.key == K_ESCAPE:
					running = False

				# if the key is space use expectimax for 1 move
				best_move = -1
				if event.key == K_SPACE:
					board = curGame.get_boards()[0]
					# With depth of 4 and run over 50 games is won about 25% of them
					# best_move = curGame.alphabeta(4)
					best_move = curGame.expectimax(3)

				# if the key is E use expectimax for the game
				if event.key == K_e:
					while True:
						best_move = curGame.expectimax(5)
						curGame.move(best_move)

						boards = curGame.get_boards()
						if boards[0] !=  boards[1]:
							curGame.spawn_blocks()
						curGame.print_pygame()

						if curGame.terminal(boards[0]):
							curGame.endGame()
							break
				
				# if the key is R use only random moves
				if event.key == K_r:
					while True:
						move = curGame.random_move()
						curGame.move(move)
						time.sleep(0.02)
						boards = curGame.get_boards()
						if boards[0] !=  boards[1]:
							curGame.spawn_blocks()
						curGame.print_pygame()

						if curGame.terminal(boards[0]):
							curGame.endGame()
							break
				
				# if the key is A use alpha-beta for the game
				if event.key == K_a:
					while True:
						best_move = curGame.alphabeta(6)
						curGame.move(best_move)
						boards = curGame.get_boards()
						if boards[0] !=  boards[1]:
							curGame.spawn_blocks()
						curGame.print_pygame()

						if curGame.terminal(boards[0]):
							curGame.endGame()
							break

				# if the key is B use expectimax when the score is less than 18,000 and
				# alpha-beta when score is greater than 18,000
				# 18,000 is arbitrary
				if event.key == K_b:
					while True:
						if curGame.get_score() > 18000:
							best_move = curGame.alphabeta(6)
						else:
							best_move = curGame.expectimax(4)

						curGame.move(best_move)
						boards = curGame.get_boards()
						if boards[0] !=  boards[1]:
							curGame.spawn_blocks()
						curGame.print_pygame()

						if curGame.terminal(boards[0]):
							curGame.endGame()
							break

                # up down left and right moves if playing manually
				if event.key == K_UP or best_move == 3:
					curGame.move(3)
					boards = curGame.get_boards()
					if boards[0] !=  boards[1]:
						curGame.spawn_blocks()

				if event.key == K_DOWN or best_move == 4:
					curGame.move(4)
					boards = curGame.get_boards()
					if boards[0] !=  boards[1]:
						curGame.spawn_blocks()

				if event.key == K_LEFT or best_move == 1:
					curGame.move(1)
					boards = curGame.get_boards()
					if boards[0] !=  boards[1]:
						curGame.spawn_blocks()

				if event.key == K_RIGHT or best_move == 2:
					curGame.move(2)
					boards = curGame.get_boards()
					if boards[0] !=  boards[1]:
						curGame.spawn_blocks()

            # Did the user click the window close button? If so, stop the loop.
			if event.type == QUIT:
				running = False

		curGame.print_pygame()