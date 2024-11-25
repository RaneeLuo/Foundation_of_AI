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
        n= game_state.board.n
        m= game_state.board.m
        
        def compute_location(i, j, n, m):
            x = math.ceil((i+1) / m)
            y = math.ceil((j+1) / n)
            
            # Getting the range of the boundaries
            range_row = [m * (x-1), ((m * x)-1)]
            range_column = [n * (y-1), ((n * y)-1)]
            
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
            for row in range (range_row[0], range_row[1]+1):
                for column in range (range_column[0], range_column[1]+1):
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
        
        def column_completed(value,i,j,n,m, game_state):
            empty_count=0
            
            for row in range (n*m):
                if(game_state.board.get((i,row))== 0):
                    empty_count+=1

            if(empty_count==1):
                return 1
            return 0
        
        def row_completed(value,i,j,n,m, game_state):
            empty_count=0
            
            for row in range (n*m):
                if(game_state.board.get((row,j))== 0):
                    empty_count+=1

            if(empty_count==1):
                return 1
            return 0
        
        def regions_completed(value,i,j,n,m, game_state):
            
            range_row , range_column = compute_location(i,j,n,m)
            empty_count=0
            for row in range (range_row[0], range_row[1]):
                for column in range (range_column[0], range_column[1]):
                    if (game_state.board.get((row,column))==0):
                        empty_count+=1
            
            if(empty_count==1):
                return 1
            return 0


        def score_function(value,i,j,n,m, game_state):
            sum = regions_completed(value,i,j,n,m, game_state) + column_completed(value, i, j, n, m, game_state) + row_completed(value, i, j, n, m, game_state)
            if(sum==3):
                return 7
            elif (sum==2):
                return 3
            elif (sum==1):
                return 1
            return 0

        def possible1(i, j, value, game_state):
            return (i, j) in game_state.player_squares() \
                   and not Move((i, j), value) in game_state.taboo_moves \
                       and game_state.board.get((i, j)) == SudokuBoard.empty \
                           and possible_columns(value, j) \
                               and possible_rows(value, i) \
                                   and possible_squares(value, i, j, n, m)
        

    
        
        def minmax(depth, all_moves, movez, maximizing, game_state, alpha, beta, n, m):
            if depth == 0:
                return movez, score_function(movez.value, movez.square[0], movez.square[1], n, m, game_state)
        
            # Maximizing player
            if maximizing:
                print("here1")
                val = -1000
                best_move = None 
        
                for next_move in all_moves:
                    # Apply the move to create a new game state
                    print("Original state before move:", game_state)
                    newstate = copy.deepcopy(game_state)
                    print("New state after deepcopy:", newstate)

                    

                    if newstate.current_player==1:    
                        newstate.current_player = 2 
                    else:
                        newstate.current_player = 1
                    
                    print("Board before put():", newstate.board)
                    newstate.board.put(next_move.square, next_move.value)
                    print("Board after put():", newstate.board)

                    # Generate updated moves based on the new game state
                    new_moves = [Move((i, j), value) for i in range(n) for j in range(n)
                                 for value in range(1, n + 1) if possible1(i, j, value, newstate)]
        
                    # Recursive call for the minimizing player
                    best_move, tmp_val = minmax(depth - 1, new_moves, next_move, False, newstate, alpha, beta, n, m)
        
                    # Update the best move and value
                    if tmp_val > val:
                        best_move = next_move
                        val = tmp_val
        
                    # Alpha-beta pruning
                    alpha = max(alpha, val)
                    if val >= beta:
                        break
        
                return best_move, val
        
            # Minimizing player
            else:
                print("here2")
                val = 1000
                best_move = None
                for next_move in all_moves:
                    print("here3")
                    # Apply the move to create a new game state
                    print("Original state before move2:", game_state)
                    newstate = copy.deepcopy(game_state)
                    print("New state after deepcopy2:", newstate)
                    if newstate.current_player==1:    
                        newstate.current_player = 2 
                    else:
                        newstate.current_player = 1
                    print("Board before put()2:", newstate.board)
                    newstate.board.put(next_move.square, next_move.value)
                    print("Board after put()2:", newstate.board)
                    # Generate updated moves based on the new game state
                    new_moves = [Move((i, j), value) for i in range(n) for j in range(n)
                                 for value in range(1, n + 1) if possible1(i, j, value, newstate)]
        
                    # Recursive call for the maximizing player
                    best_move, tmp_val = minmax(depth - 1, new_moves, next_move, True, newstate, alpha, beta, n, m)
        
                    # Update the best move and value
                    if tmp_val < val:
                        best_move = next_move
                        val = tmp_val
        
                    # Alpha-beta pruning
                    beta = min(beta, val)
                    if val <= alpha:
                        break
        
                return best_move, val


        # Check whether a cell is empty, a value in that cell is not taboo, and that cell is allowed
        def possible(i, j, value):
            return (i, j) in game_state.player_squares() \
                   and not Move((i, j), value) in game_state.taboo_moves \
                       and game_state.board.get((i, j)) == SudokuBoard.empty \
                           and possible_columns(value, j) \
                               and possible_rows(value, i) \
                                   and possible_squares(value, i, j, n, m)
                                   
                                   

        all_moves = [Move((i, j), value) for i in range(N) for j in range(N)
                     for value in range(1, N+1) if possible(i, j, value)]
        move, val = minmax(3, all_moves, all_moves[0], True, game_state, -1000, 1000, n, m)
        #move = random.choice(all_moves)
        k=1
        self.propose_move(move)
        while k>=1:
            time.sleep(0.2)
            all_moves_up=[Move((i, j), value) for i in range(N) for j in range(N)
                          for value in range(1, N+1) if possible(i, j, value)]
            #self.propose_move(random.choice(all_moves_up))
            self.propose_move(minmax(k, all_moves_up, all_moves_up[0], True, game_state, -1000, 1000, n, m)[0])
            k=k+1


# Given i and j ,function to find which rectangle it belongs to 

    

        

    
   

