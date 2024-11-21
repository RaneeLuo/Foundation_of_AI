#  (C) Copyright Wieger Wesselink 2021. Distributed under the GPL-3.0-or-later
#  Software License, (See accompanying file LICENSE or copy at
#  https://www.gnu.org/licenses/gpl-3.0.txt)

import random
import time
from competitive_sudoku.sudoku import GameState, Move, SudokuBoard, TabooMove
import competitive_sudoku.sudokuai


class SudokuAI(competitive_sudoku.sudokuai.SudokuAI):
    """
    Sudoku AI that computes a move for a given sudoku configuration.
    """

    def __init__(self):
        super().__init__()

    # N.B. This is a very naive implementation.
    def compute_best_move(self, game_state: GameState) -> None:
        N = game_state.board.N

        # Check whether a cell is empty, a value in that cell is not taboo, and that cell is allowed
        def possible(i, j, value):
            return game_state.board.get((i, j)) == SudokuBoard.empty \
                   and not TabooMove((i, j), value) in game_state.taboo_moves \
                       and (i, j) in game_state.player_squares()

        all_moves = [Move((i, j), value) for i in range(N) for j in range(N)
                     for value in range(1, N+1) if possible(i, j, value)]
        move = random.choice(all_moves)
        self.propose_move(move)
        while True:
            time.sleep(0.2)
            self.propose_move(random.choice(all_moves))




# Given i and j ,function to find which rectangle it belongs to 

    def compute_location(self,i, j, n, m):
        x = math.ceil(i / n)
        y = math.ceil(j / m)

        # Getting the range of the boundaries
        range_row = [n * (x - 1), n * x]
        range_column = [m * (y - 1), m * y]

        return range_row, range_column
    
    def possible_moves(self,value,i,j,n,m,game_state : GameState):
        x = math.ceil(i / n)
        y = math.ceil(j / m)
        range_row , range_column = self.compute_location(i,j,n,m)
        if(value > n*m and value < 1):
            return False
        
        for row in range (n*m):
            if(game_state.board.get(row,y)== value ):
                return False
            if(game_state.board.get(x,row)==value ):
                return False
            
        for row in range (range_row[0], range_row[1]):
            for column in range (range_column[0], range_column[1]):
                if (game_state.board.get(row,column)==value):
                    return False


    
    
    