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

    def _init_(self):
        super()._init_()

    # N.B. This is a very naive implementation.
    def compute_best_move(self, game_state: GameState) -> None:
        N = game_state.board.N
        n= 1
        m= 2
        
        def compute_location(i, j, n, m):
            x = math.ceil((i+1) / m)
            y = math.ceil((j+1) / n)

            # Getting the range of the boundaries
            range_row = [m * (x-1), (m * (x)-1)]
            range_column = [n * (y-1), (n * (y)-1)]

            return range_row, range_column
        
        def possible_columns(value, j):
            if(value > (N) and value < 1):
                return False
            
            for row in range (N):
                if(game_state.board.get((row,j))== value ):
                    return False
            return True
        
        def possible_rows(value, i):
            
            for row in range (N):
                if(game_state.board.get((i,row))== value ):
                    return False
            return True
        
        def possible_squares(value,i,j,n,m):
            range_row , range_column = compute_location(i,j,n,m)
            for row in range (range_row[0], range_row[1]):
                for column in range (range_column[0], range_column[1]):
                    if (game_state.board.get((row,column))==value):
                        return False
            return True
        
        def possible_moves(value,i,j,n,m):
            
            range_row , range_column = compute_location(i,j,n,m)
            if(value > (n*m+1) and value < 1):
                return False
            
            for row in range (n):
                if(game_state.board.get((row,j))== value ):
                    return False
            for column in range(m):
                if(game_state.board.get((i,column))==value ):
                    return False
                
            for row in range (range_row[0], range_row[1]):
                for column in range (range_column[0], range_column[1]):
                    if (game_state.board.get((row,column))==value):
                        return False
            return True        
        
        def column_completed(value,i,j,n,m):
            empty_count=0
            
            for row in range (n*m):
                if(game_state.board.get((i,row))== 0):
                    empty_count+=1

            if(empty_count==1):
                return 1
            return 0
        
        def row_completed(value,i,j,n,m):
            empty_count=0
            
            for row in range (n*m):
                if(game_state.board.get((row,j))== 0):
                    empty_count+=1

            if(empty_count==1):
                return 1
            return 0
        
        def regions_completed(value,i,j,n,m):
            
            range_row , range_column = compute_location(i,j,n,m)
            empty_count=0
            for row in range (range_row[0], range_row[1]):
                for column in range (range_column[0], range_column[1]):
                    if (game_state.board.get((row,column))==0):
                        empty_count+=1
            
            if(empty_count==1):
                return 1
            return 0


        def score_function(value,i,j,n,m):
            sum = regions_completed(value,i,j,n,m) + column_completed(value, i, j, n, m) + row_completed(value, i, j, n, m)
            if(sum==3):
                return 7
            elif (sum==2):
                return 3
            elif (sum==1):
                return 1
            return 0


        

    
        
        def minmax(depth, all_moves, move, maximizing, game_state : GameState, alpha, beta):
            n=1
            m=2
            if depth == 0:
                return move, score_function(move.value, move.square[0], move.square[1],n,m)
            
            
            #max player
            if maximizing == True:
                val = -1000
                bestmove = None
                for move in all_moves:
                    newstate = copy.deepcopy(game_state)
                    newstate = game_state.board.put(move.square,move.value)
                    tmp_val = minmax(depth-1, all_moves, move, False, newstate, alpha, beta)[1]
                    tmp_move = minmax(depth-1, all_moves, move, False, newstate, alpha, beta)[0]
                    if tmp_val >= val:
                        bestmove = tmp_move
                        val=tmp_val
                        
                    alpha = max(alpha,val)
                    if val >= beta:
                        break
                    
                return bestmove, val
            
            if maximizing == False:
                val = 1000
                for move in all_moves:
                    newstate = copy.deepcopy(game_state)
                    newstate = game_state.board.put(move.square,move.value)
                    tmp_val = minmax(depth-1, all_moves, move, True, newstate, alpha, beta)[1]
                    tmp_move = minmax(depth-1, all_moves, move, False, newstate, alpha, beta)[0]
                    if tmp_val < val:
                        bestmove = tmp_move
                        val=tmp_val
                        
                    beta = min(beta, val)
                    if val <= alpha:
                        break
                    
                return bestmove, val
        # Check whether a cell is empty, a value in that cell is not taboo, and that cell is allowed
        def possible(i, j, value):
            return (i, j) in game_state.player_squares() \
                   and not TabooMove((i, j), value) in game_state.taboo_moves \
                       and game_state.board.get((i, j)) == SudokuBoard.empty \
                           and possible_columns(value, j) \
                               and possible_rows(value, i) \
                                   and possible_squares(value, i, j, n, m)
                                   
                                   

        all_moves = [Move((i, j), value) for i in range(N) for j in range(N)
                     for value in range(1, N+1) if possible(i, j, value)]
        move = minmax(1, all_moves, all_moves[0], True, game_state, -1000, 1000)[0]
        #move = random.choice(all_moves)
        self.propose_move(move)
        while True:
            k=1
            time.sleep(0.2)
            all_moves_up=[Move((i, j), value) for i in range(N) for j in range(N)
                          for value in range(1, N+1) if possible(i, j, value)]
            #self.propose_move(random.choice(all_moves_up))
            self.propose_move(minmax(k, all_moves_up, all_moves_up[0], True, game_state, -1000, 1000)[0])
            k=k+1


# Given i and j ,function to find which rectangle it belongs to 

    def compute_location(i, j, n, m):
        # Getting the range of the boundaries
        x = math.ceil((i+1) / m)
        y = math.ceil((j+1) / n)

        # Getting the range of the boundaries
        range_row = [m * (x-1), (m * (x)-1)]
        range_column = [n * (y-1), (n * (y)-1)]

        return range_row, range_column