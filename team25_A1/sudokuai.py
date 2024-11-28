#  (C) Copyright Wieger Wesselink 2021. Distributed under the GPL-3.0-or-later
#  Software License, (See accompanying file LICENSE or copy at
#  https://www.gnu.org/licenses/gpl-3.0.txt)

import random
import copy
import time
from competitive_sudoku.sudoku import GameState, Move, SudokuBoard, TabooMove
import competitive_sudoku.sudokuai
import math


class SudokuAI(competitive_sudoku.sudokuai.SudokuAI):
    """
    Sudoku AI that computes a move for a given sudoku configuration.
    """

    def init(self):
        super().init()
    
        
    # N.B. This is a very naive implementation.
    def compute_best_move(self, game_state: GameState) -> None:
        N = game_state.board.N
        n= game_state.board.n
        m= game_state.board.m
        
        def compute_location(i, j, n, m):
            x = math.ceil((i+1) / m)
            y = math.ceil((j+1) / n)
            
            # Getting the range of the boundaries
            range_row = [m * (x-1), ((m * x)-1)]
            range_column = [n * (y-1), ((n * y)-1)]
            
            return range_row, range_column
        
        def possible_columns(value, j, current_state):
            if(value > (N) and value < 1):
                return False
            
            for row in range (N):
                if(current_state.board.get((row,j))== value ):
                    return False
            return True
        
        def possible_rows(value, i, current_state):
            
            for row in range (N):
                if(current_state.board.get((i,row))== value ):
                    return False
            return True
        
        def possible_squares(value,i,j,n,m, current_state):
            range_row , range_column = compute_location(i,j,n,m)
            for row in range (range_row[0], range_row[1]+1):
                for column in range (range_column[0], range_column[1]+1):
                    if (current_state.board.get((row,column))==value):
                        return False
            return True
        
     
        
        def column_completed(value,i,j,n,m, gamestate):
            empty_count=0
            
            for row in range (n*m):
                if(gamestate.board.get((i,row))==  SudokuBoard.empty):
                    empty_count+=1

            if(empty_count==0):
                return 1
            return 0
        
        def row_completed(value,i,j,n,m, gamestate):
            empty_count=0
            
            for row in range (n*m):
                if(gamestate.board.get((row,j))== SudokuBoard.empty):
                    empty_count+=1

            if(empty_count==0):
                return 1
            return 0
        
        def regions_completed(value,i,j,n,m, gamestate):
            
            range_row , range_column = compute_location(i,j,n,m)
            empty_count=0
            for row in range (range_row[0], range_row[1]+1):
                for column in range (range_column[0], range_column[1]+1):
                    if (gamestate.board.get((row,column)) ==  SudokuBoard.empty):
                        empty_count+=1
            if(empty_count==0):
                return 1
            return 0


        def score_function(value,i,j,n,m, gamestate):
            summa = regions_completed(value,i,j,n,m, gamestate) + column_completed(value, i, j, n, m, gamestate) + row_completed(value, i, j, n, m, gamestate)
            if(summa==3):
                return 7
            elif (summa==2):
                return 3
            elif (summa==1):
                return 1
            return 0


        

    
        
        def minmax(depth, all_moves, move, maximizing, current_state, n, m, alpha, beta):
        
            if depth == 0:
                #return score_function(move.value, move.square[0], move.square[1],n,m, current_state), move
                return current_state.scores[0]-current_state.scores[1], move
            if len(all_moves) == 0:
                return current_state.scores[0]-current_state.scores[1], move
            
            bestmove = None
            #max player
            if maximizing == True:
                maxval = -1000
                for cur_move in all_moves:
                    newstate = copy.deepcopy(current_state)

                    newstate.board.put(cur_move.square, cur_move.value)

                    if (newstate.current_player == 1):
                        newstate.current_player = 2
                    else:
                        newstate.current_player = 1
 
                    calculated_score_1 = score_function(cur_move.value, cur_move.square[0], cur_move.square[1], n, m, newstate)
                    newstate.scores[0] += calculated_score_1
                    updated_moves = [Move((i, j), value) for i in range(N) for j in range(N)
                                     for value in range(1, N+1) if possible(i, j, value, newstate)]

                    tmp_val, tmp_move= minmax(depth-1, updated_moves, cur_move, False, newstate, n, m, alpha, beta)
                    newstate.scores[0] = newstate.scores[0] - calculated_score_1

                    if tmp_val>= maxval:
                        maxval = tmp_val
                        bestmove = cur_move
                        
                        
                    alpha = max(alpha,maxval)
                    if alpha >= beta:
                        break
                #cur_score = cur_score + tmp_val
                return maxval, bestmove
            
            if maximizing == False:
                minval = 1000
                for cur_move in all_moves:
                                     
                    newstate = copy.deepcopy(current_state)

                    newstate.board.put(cur_move.square,cur_move.value)

                    if (newstate.current_player == 1):
                        newstate.current_player = 2
                    else:
                        newstate.current_player = 1

                    calculated_score_2 = score_function(cur_move.value, cur_move.square[0], cur_move.square[1], n, m, newstate)
                    newstate.scores[1] += calculated_score_2
                    updated_moves =  [Move((i, j), value) for i in range(N) for j in range(N)
                                     for value in range(1, N+1) if possible(i, j, value, newstate)]

                    tmp_val, tmp_move = minmax(depth-1, updated_moves, cur_move, True, newstate, n, m,alpha, beta)
                    newstate.scores[1] = newstate.scores[1] - calculated_score_2

                    if tmp_val < minval:
                        minval=tmp_val
                        bestmove = cur_move
                        
                        
                    beta = min(beta, minval)
                    if beta <= alpha:
                        break
                #cur_score = cur_score-minval

                return minval, bestmove
                    
                
        # Check whether a cell is empty, a value in that cell is not taboo, and that cell is allowed
        def possible(i, j, value, current_state):
            return (i, j) in current_state.player_squares() \
                   and not TabooMove((i, j), value) in current_state.taboo_moves \
                       and current_state.board.get((i, j)) == SudokuBoard.empty \
                           and possible_columns(value, j, current_state) \
                               and possible_rows(value, i, current_state) \
                                   and possible_squares(value, i, j, n, m, current_state)
                                   
        def possible1(i, j, value, current_state):
            return (i, j) in current_state.allowed_squares1 \
                   and not TabooMove((i, j), value) in current_state.taboo_moves \
                       and current_state.board.get((i, j)) == SudokuBoard.empty \
                           and possible_columns(value, j, current_state) \
                               and possible_rows(value, i, current_state) \
                                   and possible_squares(value, i, j, n, m, current_state)    
                                   
                                   
        def possible2(i, j, value, current_state):
            return (i, j) in current_state.allowed_squares2 \
                   and not TabooMove((i, j), value) in current_state.taboo_moves \
                       and current_state.board.get((i, j)) == SudokuBoard.empty \
                           and possible_columns(value, j, current_state) \
                               and possible_rows(value, i, current_state) \
                                   and possible_squares(value, i, j, n, m, current_state)  
                                   
        all_moves = [Move((i, j), value) for i in range(N) for j in range(N)
                     for value in range(1, N+1) if possible(i, j, value, game_state)]
        k=0
        for k in range(30):
            move = minmax(k, all_moves, all_moves[0], True, game_state, n, m, -math.inf,math.inf)[1]
        #move = random.choice(all_moves)
            
            self.propose_move(move)
            
        

