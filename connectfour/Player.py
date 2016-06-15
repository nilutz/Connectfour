#this file implements the different players
import numpy as np

from Minmax import Minmax

class Player(object):

	symbol = 4 # will be overwritten

	def __init__(self,symbol):
		self.symbol = symbol

	def move(self, grid):
		return None


class Human(Player):
	pass
	
	#def __init__(self,symbol):
	#	super(Human,self).__init__(symbol)

	#def move(self,S,p):
	#	'''
	#	@param S: 6x7 grid containing the current game state
	#	@param p: current player
	#	@param col_num: column number

	#	sets the player's number on the grid and returns the grid
	#	'''
	    
		#sanity check
	


class RandomPC(Player):

	def __init__(self,symbol):
		super(RandomPC,self).__init__(symbol)

	def move(self,S):
		'''
		@param S: 6x7 grid containing the current game state
		moves at random 
		'''
		return np.random.randint(0,S.shape[1])


class AiPC(Player):

	difficulty = None
	m = None

	def __init__(self,symbol, difficulty):
		super(AiPC,self).__init__(symbol)
		self.difficulty = difficulty
		self.m = Minmax()

	def move(self,S,p):
		_ , col_num = self.m.minmax(S, p, self.difficulty, -np.inf, np.inf)
		return col_num
