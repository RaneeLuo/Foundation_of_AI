#  (C) Copyright Wieger Wesselink 2021. Distributed under the GPL-3.0-or-later
#  Software License, (See accompanying file LICENSE or copy at
#  https://www.gnu.org/licenses/gpl-3.0.txt)

import random
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
        n= 1
        m= 2
        
        def compute_location(self,i, j, n, m):
            x = math.ceil((i+1) / m)
            y = math.ceil((j+1) / n)

            # Getting the range of the boundaries
            range_row = [m * (x-1), (m * (x)-1)]
            range_column = [n * (y-1), (n * (y)-1)]

            return range_row, range_column
        
        def possible_columns(value, j):
            if(value > (n*m+1) and value < 1):
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
            range_row , range_column = self.compute_location(i,j,n,m)
            print(n)
            print(i)
            print(math.ceil(i/n))
            print(range_row)
            print(m)
            print(j)
            print(math.ceil(j/m))
            print(range_column)
            for row in range (range_row[0], range_row[1]):
                for column in range (range_column[0], range_column[1]):
                    if (game_state.board.get((row,column))==value):
                        return False
            return True
        
        def possible_moves(value,i,j,n,m):
            
            range_row , range_column = self.compute_location(i,j,n,m)
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
        
        def score_function(self,value,i,j,n,m):
            sum = self.regions_completed + self.column_completed + self.row_completed
            if(sum==3):
                return 7
            elif (sum==2):
                return 3
            elif (sum==1):
                return 1
            return 0


        def regions_completed(self,value,i,j,n,m):
            
            range_row , range_column = self.compute_location(i,j,n,m)
            empty_count=0
            for row in range (range_row[0], range_row[1]):
                for column in range (range_column[0], range_column[1]):
                    if (game_state.board.get((row,column))==0):
                        empty_count+=1
            
            if(empty_count==1):
                return 1
            return 0

        
        def column_completed(self,value,i,j,n,m):
            empty_count=0
            
            for row in range (n*m):
                if(game_state.board.get((i,row))== 0):
                    empty_count+=1

            if(empty_count==1):
                return 1
            return 0


        def row_completed(self,value,i,j,n,m):
            empty_count=0
            
            for row in range (n*m):
                if(game_state.board.get((row,j))== 0):
                    empty_count+=1

            if(empty_count==1):
                return 1
            return 0
        
        # Check whether a cell is empty, a value in that cell is not taboo, and that cell is allowed
        def possible(i, j, value):
            return game_state.board.get((i, j)) == SudokuBoard.empty \
                   and not TabooMove((i, j), value) in game_state.taboo_moves \
                       and (i, j) in game_state.player_squares() \
                           and possible_columns(value, j) \
                               and possible_rows(value, i) \
                                   and possible_squares(value, i, j, n, m)
                                   
                                   

        all_moves = [Move((i, j), value) for i in range(N) for j in range(N)
                     for value in range(1, N+1) if possible(i, j, value)]
        move = random.choice(all_moves)
        self.propose_move(move)
        while True:
            time.sleep(0.2)
            all_moves_up=[Move((i, j), value) for i in range(N) for j in range(N)
                         for value in range(1, N+1) if possible(i, j, value)]
            self.propose_move(random.choice(all_moves_up))


# Given i and j ,function to find which rectangle it belongs to 

    def compute_location(self,i, j, n, m):
        # Getting the range of the boundaries
        x = math.ceil((i+1) / m)
        y = math.ceil((j+1) / n)

        # Getting the range of the boundaries
        range_row = [m * (x-1), (m * (x)-1)]
        range_column = [n * (y-1), (n * (y)-1)]

        return range_row, range_column
    
    
    
    
#minmax
MAX,MIN = 1000,-1000
 
def minimax(depth, nodeIndex, maximizingPlayer, 
            values, alpha, beta): 
    # Terminating condition. i.e 
    # leaf node is reached 
    if depth == 3: 
        return values[nodeIndex] 
 
    if maximizingPlayer: 
      
        best = MIN
 
        # Recur for left and right children 
        for i in range(0, 2): 
             
            val = minimax(depth + 1, nodeIndex * 2 + i, 
                          False, values, alpha, beta) 
            best = max(best, val) 
            alpha = max(alpha, best) 
 
            # Alpha Beta Pruning 
            if beta <= alpha: 
                break
          
        return best 
      
    else:
        best = MAX
 
        # Recur for left and 
        # right children 
        for i in range(0, 2): 
          
            val = minimax(depth + 1, nodeIndex * 2 + i, 
                            True, values, alpha, beta) 
            best = min(best, val) 
            beta = min(beta, best) 
 
            # Alpha Beta Pruning 
            if beta <= alpha: 
                break
          
        return best 
      
# Driver Code 
if __name__ == "__main__": 
  
    values = [3, 5, 6, 9, 1, 2, 0, -1]  
    print("The optimal value is :", minimax(0, 0, True, values, MIN, MAX)) 
     
