import numpy as np
from Mechanics import *


class Minmax(object):
    
    '''
    This is a simple MinMax algorithm with score-Hashing and Alpha Beta pruning.
    The score evaluates a heuristic.
    '''
    
    count = 0
    
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
            #_ , b = zip(*(move_was_winning_move(state, cur_player, e) for e in range(2,5)))
            #_ , c = zip(*(move_was_winning_move(state, oponent, f) for f in range(2,5)))
            _, fours_player = move_was_winning_move(state, cur_player, 4)
            _, threes_player = move_was_winning_move(state, cur_player, 3)
            _, twos_player = move_was_winning_move(state, cur_player, 2)
        
            _, fours_oponent = move_was_winning_move(state, oponent, 4)
            _, threes_oponent = move_was_winning_move(state, oponent, 3)
            _, twos_oponent = move_was_winning_move(state, oponent, 2)
            


            score = fours_player*1000+threes_player*100+twos_player*10-fours_oponent*100000-threes_oponent*1000-twos_oponent*100
            
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
        if move_still_possible(board):
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
            score = self.max_play(board_i, depth-1, alpha, beta, cur_player)
                        
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
        elif move_still_possible(board):
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
            score = self.min_play(board_i, depth-1, alpha, beta, cur_player)
                        
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