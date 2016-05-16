import numpy as np


def move_is_correct(grid,num):
	'''
	@param grid: 6x7 grid containing the current game state
	@param num: column

	returns True if move is allowed on that column
	'''

	#if 0 is in column
	if 0 in grid[:,num]:
	
		#move is allowed
		return True

	else:

		return False

def move_still_possible(S):
	'''
	@param S: 6x7 grid containing the current game state
	returns True if grid contains no 0, therefore no move possible anymore
	'''
	return (S[S==0].size == 0)


def move(S,p,col_num):
	'''
	@param S: 6x7 grid containing the current game state
	@param p: current player
	@param col_num: column number

	sets the player's number on the grid and returns the grid
	'''
    
	#sanity check
	if 0 in S[:,col_num]:    
		y = np.where(S[:,col_num]==0)[0][-1]
		S[y,col_num] = p
		return S , y, col_num
	else:
		return S, None, None
		return 

def move_at_random(S):
	'''
	@param S: 6x7 grid containing the current game state
	moves at random 
	'''
	return np.random.randint(0,S.shape[1])


#neat and ugly but the fastest way to search a matrix for a vector is a string find
player1 = '1 1 1 1'
oponent = '2 2 2 2'

def move_was_winning_move(S, p):
	'''
	@param S: 6x7 grid containing the current game state
	@param p: current player

	combines all the allowed formations of the grid and string_finds with 
	the currents player vector. Returns true if match.
	'''
	if p == 1:
		match = player1
	else:
		match = oponent 

	l=[]
	#for every possible diag
	for i in range(-2,4):
		l.append(np.diag(S,k = i))
		l.append(np.diag(np.fliplr(S),k=i))
	#left to right
	l.append(S)
	#top to bottom
	l.append(np.rot90(S)) 

	if ''.join(np.array_str(e) for e in l).find(match) > -1:
		return True
	return False

