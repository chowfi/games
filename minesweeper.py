from typing import List
import csv
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
- Print coordinates on game board

"""
class Minesweeper:
    BOMB = "x"
    HIDDEN = "\u2588" 
    FLAG = "🚩"

    def __init__(self, n_board: int = 8, n_mines: int = 10, seed_value: int = 42, * , board: List[List[str]] = None, reveal_board: List[List[bool]] = None, visual_board: List[List[str]] = None, count_flags: int = 0):
        self.seed_value = seed_value
        random.seed(self.seed_value)
        self.n_board = n_board
        self.n_mines = n_mines
        self.count_flags = count_flags
        if board is None:
            self.board = [['0' for _ in range(self.n_board)] for _ in range(self.n_board)]
        if board is not None:
            self.board = board
        if reveal_board is None:
            self.reveal_board = [[False for _ in range(self.n_board)] for _ in range(self.n_board)]
        if reveal_board is not None:
            self.reveal_board = reveal_board
        if visual_board is None:
            self.visual_board = [['0' for _ in range(self.n_board)] for _ in range(self.n_board)]
        if visual_board is not None:
            self.visual_board = visual_board

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

                if self.reveal_board[row][col] is False:
                    self.visual_board[row][col] = self.HIDDEN

                elif self.reveal_board[row][col] is True: 

                    if self.board[row][col] == self.BOMB and self.visual_board[row][col] != self.FLAG:
                        self.visual_board[row][col] = '💣'

                    elif self.board[row][col] == '0':
                        self.visual_board[row][col] = '.'

                    elif self.board[row][col] != self.BOMB and self.visual_board[row][col] != self.FLAG:
                        self.visual_board[row][col] = self.board[row][col]

            print(self.visual_board[row])
            print(" "*20)

    def user_input(self):
        while True:
            move = input(f'Input your next move in this format:\n R / F / S, row, col (0th index-ed) or 0,0 (for saving) to reveal board / plant flag / save board \n')
            mode, row, col = move.split(",")
            row = int(row)
            col = int(col)
            # if row < self.n_board and and col >= 0:
            if mode == 'R':
                if self.board[row][col] == '0':
                    self.boundary_detection(row, col)  # dfs reveals this cell and all connected 0s
                elif self.board[row][col] == self.BOMB: 
                    self.reveal_board[row][col] = True  
                    print("Game Over")
                    break
                else:
                    self.reveal_board[row][col] = True  
            elif mode == 'F':
                self.reveal_board[row][col] = True
                self.visual_board[row][col] = self.FLAG
                self.count_flags +=1
            elif mode == 'S':
                self.save_game()
                break
            return True
        return False 

    def boundary_detection(self, row, col):
        """
        If given cell is visible and has 0 neighboring bombs,
        this algorithm will expand the search space until we find the boundary of eiher the edge of the board
        or a cell with a string value of >0.

        Returns the new user_board view with expanded visibility

        Algo:
        1) if !='0', return after changing user_board visibility or if reach boundary of game, return  " "
        2) if not, dfs a neighboring node
        """
        def dfs(row, col):

            if row >= self.n_board or row < 0 or col >= self.n_board or col < 0:
                return 
            
            if self.reveal_board[row][col] == True:
                return

            if self.board[row][col] != '0':
                self.reveal_board[row][col] = True
                return

            if self.board[row][col] == '0':
                self.reveal_board[row][col] = True
                
            neighbors = [(-1, -1), (-1, 0), (-1,1),
            (0,-1), (0,1),
            (1,-1), (1,0), (1,1)]

            for dr,dc in neighbors:
                new_row, new_col = row + dr, col + dc
                dfs(new_row, new_col)
        
        return dfs(row, col)

    def is_end_game(self):
        # Loss
        for row in range(self.n_board):
            for col in range(self.n_board):
                if self.reveal_board[row][col] == True and self.board[row][col] == self.BOMB and self.visual_board[row][col] != self.FLAG:
                    return True
        # Game continues or win
        for row in range(self.n_board):
            for col in range(self.n_board):
                if self.reveal_board[row][col] == False:
                    return False

    def save_game(self):
        with open('save.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self.n_board, self.n_mines, self.seed_value, self.count_flags])
            writer.writerows(self.board)
            writer.writerows(self.reveal_board)
            writer.writerows(self.visual_board)
    
    def load_game(self):
        with open('save.csv', 'r') as file:
            reader = list(csv.reader(file))
            self.n_board, self.n_mines, self.seed_value, self.count_flags = reader[0]
            self.n_board = int(self.n_board)
            self.n_mines = int(self.n_mines)
            self.seed_value = int(self.seed_value)
            self.count_flags = int(self.count_flags)
            self.board = reader[1:5] #hardcoded to board size
            # CSV gives strings even booleans become strings; hence converting back to boolean below
            self.reveal_board = [[cell == 'True' for cell in row] for row in reader[5:9]]
            self.visual_board = reader[9:13] #hardcoded to board size

        ms = Minesweeper(self.n_board, self.n_mines, self.seed_value, board = self.board, reveal_board= self.reveal_board, visual_board = self.visual_board, count_flags = self.count_flags) 
        ms.game_play()

    def game_play(self):
        """
        1] Visualize truth board and visual board
        2] Take user input
        3] Show updated visual board
        4] Check if end game, if not continue user input
        """
        self.visualize_truth() # for me to check the game play during testing
        print("-"*40)
        self.visualize_board()

        while not self.is_end_game():
            while self.user_input():
                self.visualize_board()
                if self.count_flags == self.n_mines:
                    print("You Win! 🙂")
                    break
            break

if __name__ == "__main__":
    ms = Minesweeper(4,1)
    # ms.game_play()
    ms.load_game()