from typing import List
import random

#Minesweeper in CLI

"""
1 - Initial 8 by 8 board w 10 mines. Need a visible / invisible flag. So the whole board is invisible flag at first. Need an algorithm to count how many mines around.
2 - Take in user's input and check for valid move
3 - Show updated board which uses an algo to show the boundary of what is revealed.
4 - Define actions: Flag is invisible. Everything else is visible
5 - End game logic: When everything is visible and player has not died. They win

Helper functions:
- Save and load game states
- Undo moves
- Counter of mines left and timer of game

"""
class Minesweeper:
    BOMB = "x"
    HIDDEN = "\u2588" 

    def __init__(self, n_board: int = 8, n_mines: int = 10, seed_value: int = 42):
        random.seed(seed_value)
        self.n_board = n_board
        self.n_mines = n_mines
        self.board = [['0' for _ in range(self.n_board)] for _ in range(self.n_board)]
        self.user_board = [[False for _ in range(self.n_board)] for _ in range(self.n_board)]
        
        #shuffle and update for mines
        all_cells = [
            (row, col)
            for row in range(self.n_board)
            for col in range(self.n_board)
        ]

        random.shuffle(all_cells)
        for i in range(self.n_mines):
            row, col = all_cells[i]
            self.board[row][col] = self.BOMB

        #count neighboring mines
        neighbors = [(-1, -1), (-1, 0), (-1,1),
                    (0,-1), (0,1),
                    (1,-1), (1,0), (1,1)]

        for row in range(len(self.board)):
            for col in range(len(self.board[0])):

                if self.board[row][col] != 'x':

                    self.count = 0
                    for neighbor in neighbors:
                        dr,dc = neighbor
                        new_row, new_col = row + dr, col + dc
                        
                        if new_row < len(self.board[0]) and new_row >= 0:
                            if new_col < len(self.board[1]) and new_col >= 0:
                                if self.board[new_row][new_col] == 'x':
                                    self.count+=1
                    self.board[row][col] = str(self.count)

    def visualize_truth(self):
        """
        Underlying board view
        """
        for row in self.board:
            print(row)

    def visualize_board(self):
        """
        User's board view
        """
        for row in range(self.n_board):
            for col in range(self.n_board):

                if self.user_board[row][col] is False:
                    self.user_board[row][col] = self.HIDDEN

                elif self.user_board[row][col] is True: 

                    if self.board[row][col] == self.BOMB:
                        self.user_board[row][col] = '💣'
                        break
                    elif self.board[row][col] == '0':
                        self.user_board[row][col] = '.'
                        break
                    else:
                        self.user_board[row][col] == self.board
                        break

            print(self.user_board[row])
            print(" "*20)

    def user_input(self):
        while True:
            move = input(f'Input your next move in this format:\n row,col (0th index-ed)\n')
            row, col = move.split(",")
            row = int(row)
            col = int(col)
            if row < self.n_board and row >= 0:
                if col < self.n_board and col >= 0:
                    self.user_board[row][col] = True
                    return (row, col)
            
if __name__ == "__main__":
    ms = Minesweeper()
    ms.visualize_truth()
    ms.visualize_board()
    ms.user_input()
    ms.visualize_board()