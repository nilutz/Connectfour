
# coding: utf-8

# In[1]:

import numpy as np


# In[2]:

class Minmax(object):
    
    '''
    This is a simple MinMax algorithm with score-Hashing and Alpha Beta pruning.
    The score evaluates a heuristic.
    '''
    
    DIC ={}
    
    def __init__(self):
        
        #load a DIC with some precalculated values values
        try: 
            self.DIC = self.load_obj('scores')
        except (RuntimeError, TypeError, NameError, OSError, IOError):
            self.DIC  = {}
            print '--> no scores.pkl available. Now it takes way longer to build the tree!!'

    def save_obj(self, obj, name ):
        import pickle
        '''
        save a data object
        '''
        with open(name + '.pkl', 'wb') as f:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
    def load_obj(self, name):
        '''
        loads a data object
        '''
        import pickle
        with open(name + '.pkl', 'rb') as f:
            return pickle.load(f)
    
    def get_hash_key(self, board):
        '''
        This function creates a hashkey for a board so it can be stored in the dictionary.
        '''
        b=np.ndarray.flatten(board)
        string_flat=np.char.mod('%d', b)
        key = "".join(string_flat)
        return key
    
    
    #heuristic to evaluate the next best move
    def score(self, state, depth, cur_player):
        '''
        heuristic function that uses Hashing for the scores if they are already calculated
        
        state: current gameState
        depth: current depth
        cur_player: current player
        
        we are using a simple heuristic here,
        just counting and punishing good and reward good moves with a weight.
        
        score = num of(four in row)*1000+ num of(three in row)* 100+ num of(two in row)*10
        - num of opponent(four in row)*100000- num of opponent(three in row)*100- 
        num of opponent(two in row)*10
                
        returns the score
        '''
        
        if cur_player == 1:
            oponent = 2
        else:
            oponent = 1
            
        hash_key = self.get_hash_key(state)
        
        # Score already calculated
        if hash_key in self.DIC:
            return self.DIC[hash_key]
        
        # else calculate
        else:
                
            #counting the number of good four/threes/twos in a row/column/diag
            _ , b = zip(*(move_was_winning_move(state, cur_player, e) for e in range(2,5)))
            _ , c = zip(*(move_was_winning_move(state, oponent, f) for f in range(2,5)))
            

            score = b[2]*1000+b[1]*100+b[0]*10-c[2]*100000-c[1]*100-c[0]*10
            
            #and put in DIC
            self.DIC[hash_key]  = score
            return score
    
    def listofmoves(self, gameState):
        '''
        returns a list of possible moves = column not full and orders it with middle first
        
        gameState: current gamestate
        
        return: list of possible moves
        '''
        l=[]
        for i in range(gameState.shape[1]):
            if 0 in gameState[:,i]:
                l.append(i)
        
        m=sum(l)/len(l)
        return sorted(l, key=lambda x:abs(x-m))

    
    def min_play(self, board, depth, alpha ,beta , cur_player):
        '''
        recursively building a the tree, min part of minmax
        minimzing the score, moving the oponent
        
        board: a gameState 
        depth: depth parameter of search tree
        alpha: alpha for alphabeta pruning
        beta: beta for alphabeta pruning
        cur_player: the current_player's number
        
        return best score
        '''

        #eval current player
        if cur_player == 1:
            oponent = 2
        else:
            oponent = 1
            
        #termination
        #max depth
        if depth == 0:
            return self.score(board, depth, cur_player)
        #all full
        if not move_still_possible(board):
            return self.score(board, depth, cur_player)
        #or winner
        
        winningmove, _ = move_was_winning_move(board, cur_player, 4)
        if winningmove:
            return self.score(board, depth, cur_player)
        

        
        best_score = np.inf
        
        #get all available moves
        moves = self.listofmoves(board)
        best_move = moves[0]
        
        if len(moves) == 0:
            return self.score(board, depth, cur_player)
        
        for eachmove in moves:
            #copy board and move oponent
            boardcopy = board.copy()
            
            board_i, _ , _ = move(boardcopy, oponent, eachmove)
            
            #build recursivley max
            score = self.max_play(board_i, depth-1,alpha ,beta , cur_player)
                        
            #compare scores MIN
            #if score < best_score:
            #    best_move = eachmove
            #    best_score = score
                #print 'if', best_move, best_score
                
            #with alpha - beta
            if score < beta:
                beta = score
                #best_move = eachmove
            if beta <= alpha:
                return beta

        
        return beta#, best_move
    
    
    def max_play(self, board, depth, alpha ,beta , cur_player):
        '''
        recursively building a the tree, max part of minmax
        maximizing the score
        
        board: a gameState 
        depth: depth parameter of search tree
        alpha: alpha for alphabeta pruning
        beta: beta for alphabeta pruning
        cur_player: the current_player's number
        
        return best score
        '''


        #eval current player
        if cur_player == 1:
            oponent = 2
        else:
            oponent = 1
            
        #termination
        #max depth
        if depth == 0:
            return self.score(board, depth, cur_player)
        #all full
        elif not move_still_possible(board):
            return self.score(board, depth, cur_player)
        #or winner
        winningmove, _ = move_was_winning_move(board, cur_player, 4)
        if winningmove:
            return self.score(board, depth, cur_player)
                
        
        best_score = -np.inf
        
        #get all available moves
        moves = self.listofmoves(board)
        best_move = moves[0]
        
        if len(moves) == 0:
            return self.score(board, depth, cur_player)
        
        for eachmove in moves:

            #copy board and move player
            boardcopy = board.copy()
            
            board_i, _ , _ = move(boardcopy, cur_player, eachmove)
            
            #build recursivley min
            score = self.min_play(board_i, depth-1,alpha ,beta , cur_player)
                        
            #compare scores MAX
            #if score > best_score:
            #    best_move = eachmove
            #    best_score = score
                #print 'if', best_move, best_score
            
            #with alpha-beta
            if score > alpha:
                alpha = score
                #best_move = eachmove
            if alpha >= beta:
                return alpha
        
        return alpha #, best_move
    
    
    def minmax(self, board, cur_player, depth=4, alpha=-np.inf, beta=np.inf):
        '''
        recursively building a the tree with alpha beta pruning
        may not be the best choice but everyone keeps saying: memory is cheap
        
        board: a gameState 
        depth: depth parameter of search tree
        cur_player: the current_player's number
        
        return best score, best move
        '''
        
        #eval current player
        if cur_player == 1:
            oponent = 2
        else:
            oponent = 1
        
        best_score = -np.inf
        
        #get all available moves
        moves = self.listofmoves(board)
        best_move = moves[0]

        #for each move do
        for eachmove in moves:
            #print eachmove
            #copy board and move
            boardcopy = board.copy()               
                
            #build recursivley
            board_i, _ , _ = move(boardcopy, cur_player, eachmove)
            
            score = self.min_play(board_i, depth-1 ,alpha ,beta,  cur_player)
                        
            #compare scores
            if score > alpha:
                alpha = score
                best_move = eachmove
            if alpha >= beta:
                return alpha
        
        return alpha, best_move


# In[3]:

#import numpy as np


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
    return not(S[S==0].size == 0)


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
player1=[' ','1', '1 1', '1 1 1', '1 1 1 1']
oponent=[' ','1', '2 2', '2 2 2', '2 2 2 2']


def move_was_winning_move(S, p, num):
    '''
    @param S: 6x7 grid containing the current game state
    @param p: current player
    @param num: how many occurences to count
    
    combines all the allowed formations of the grid and string_finds with 
    the currents player vector. Returns true if match.
    
    return: True or False whether move was winning move or not,
            and count of occurences
    '''
    if p == 1:
        match = player1[num]
    else:
        match = oponent[num]

    l=[]
    #for every possible diag
    for i in range(-2,4):
        l.append(np.diag(S,k = i))
        l.append(np.diag(np.fliplr(S),k=i))
    #left to right
    l.append(S)
    #top to bottom
    l.append(np.rot90(S)) 
    
    #convert to string
    stringmatrix =''.join(np.array_str(e) for e in l)
    
    #count the occurences
    counter = stringmatrix.count(match)
    
    #print stringmatrix
    
    #if four in a row
    if num == 4 and counter == 1:
        return True, counter
    return False, counter





# relate numbers (1, -1, 0) to symbols ('x', 'o', ' ')
symbols = {1:'m', 2:'r', 0:' '}

# print game state matrix using symbols
def print_game_state(S):
    B = np.copy(S).astype(object)
    for n in [1, 2, 0]:
        B[B==n] = symbols[n]
    print B





if __name__ == '__main__':
    # initialize 6x7 connectfour board
    gameState = np.zeros((6,7), dtype=int)

    # initialize player number, move counter
    player = 1
    mvcntr = 1

    # initialize flag that indicates win
    noWinnerYet = True
    
    m = Minmax()
    le = len(m.DIC)
    print 'This is a Minmax vs Random Connect Four simulation: '
    difficulty = int(raw_input('Difficulty: '))

    while move_still_possible(gameState) and noWinnerYet:
        
        while True:
            # get player symbol
            name = symbols[player]
            print '%s moves' % name
            
            #move with Minmax
            if player == 1:
                _ , col_num = m.minmax(gameState, 1, difficulty, -np.inf, np.inf)
            
            # let player move at random
            else:
                col_num = move_at_random(gameState)
                
            if move_is_correct(gameState, col_num):
                gameState, _ , _ = move(gameState,player,col_num)

                # print current game state
                print_game_state(gameState)

                # evaluate game state
                winningmove, _ = move_was_winning_move(gameState, player, 4)
                if winningmove:
                    print 'player %s wins after %d moves' % (name, mvcntr)
                    noWinnerYet = False


                # switch player and increase move counter
                if player == 1:
                    player = 2
                elif player == 2:
                    player = 1

                mvcntr +=  1

                break




    if noWinnerYet:
        print 'game ended in a draw' 

    #save new DIC for better Hashing
    if le < len(m.DIC):
        m.save_obj(m.DIC,'scores')
    

