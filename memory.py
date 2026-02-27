from typing import List, Optional
import random
import time

#Memory in CLI (clickable + AI Agent + color)
"""
1. Initialize a board like 3 by 2. 
    - Use ansi escape codes for color + unicode 'U2588' for tile
2. Take user input x2, if they match, keep tiles open 
    - The set goes to them..track this as well
3. If not, close the tiles and let computer take two moves
    - Initialize with a hash to remember the color and grid
4. Ends when all tiles have been revealed
5. Winner is the one with more sets.

Helper functions:
- Save game in Json + load it
"""
class Memory:
    COLOR = ["\033[31m", "\033[32m", "\033[33m", "\033[34m", "\033[35m", "\033[36m"] #white: "\033[37m"
    BLOCK = "\u2588"
    RESET = "\033[0m"

    def __init__(self, row: int=2, col: int=3, seed_value: int=42):
        self.seed_value = seed_value
        random.seed(self.seed_value)
        self.row = row
        self.col = col
        self.winning_sets = {'1': 0, '2': 0}
        self.ai_mem = {}

        self.full_combos = []
        for i in range(len(self.COLOR)):
            self.combo = self.COLOR[i] + self.BLOCK + self.RESET
            self.full_combos.append(self.combo)

        #choose some colors
        self.selected_colors = random.sample(self.full_combos, self.col)

        #randomize board of colors
        self.ground_truth = [[self.selected_colors[i] for i in range(self.col)] for _ in range(self.row)]
        cells = []
        for row in range(len(self.ground_truth)):
            for col in range(len(self.ground_truth)):
                cells.append((self.ground_truth[row][col], row, col))        
        random.shuffle(cells)
        index = 0
        for row in range(len(self.ground_truth)):
            for col in range(len(self.ground_truth)):
                obj, _ , _ = cells[index]
                self.ground_truth[row][col] = obj
                index+=1

        # False flag for not visible to user
        self.visibility_board = [[False for i in range(self.col)] for _ in range(self.row)]        
        # what the user sees
        self.user_board = [[self.BLOCK for i in range(self.col)] for _ in range(self.row)]
    
    def visualize_ground_truth(self):
        for row in self.ground_truth:
            print(" ".join(row))
            print("")
        print("-"*20)

    def visualize_user_board(self):
        for r in range(self.row):
            for c in range(self.col):
                if self.visibility_board[r][c] == True:
                    self.user_board[r][c] = self.ground_truth[r][c]

        for row in self.user_board:
            print(" ".join(row))
            print("")

    def user_input(self):
        #start w basic index user input first
        self.temp = []
        for _ in range(2):
            answer = input("Input row,col. It's 0th indexed")
            row, col = answer.split(",")
            row = int(row)
            col = int(col)
            self.temp.append((row,col))
        print(f'user_temp:{self.temp}')
        # advance to enabling mouse clicking: mouse_y, mouse_x, top, left, height, width
    
    def computer_input(self):
        self.computer_temp = []
        count = 0
        while True:
            r, c = random.randint(0,1), random.randint(0,2)
            if self.visibility_board[r][c] == False and count <=1:
                if len(self.computer_temp) == 1:
                    if (r,c) not in self.computer_temp:
                        self.computer_temp.append((r,c))
                        count+=1
                else:   
                    self.computer_temp.append((r,c))
                    count+=1
            if count == 2:
                break
        print(f'computer_temp:{self.computer_temp}')
            
    def check_human_input(self):
        row_0, col_0 = self.temp[0]
        row_1, col_1 = self.temp[1]
        if self.temp[0][0] >= 0 and self.temp[1][0] >= 0 and self.temp[0][0] < self.row and self.temp[1][0] < self.row:
            if self.temp[0][1] >= 0 and self.temp[1][1] >= 0 and self.temp[0][1] < self.col and self.temp[1][1] < self.col:
                if self.visibility_board[row_0][col_0] == False and self.visibility_board[row_1][col_1] == False and (row_0,col_0) != (row_1,col_1):
                    return True
        return False
        
    def evaluate_input(self, player, temporary_list):
        row_0, col_0 = temporary_list[0]
        row_1, col_1 = temporary_list[1]
        if self.ground_truth[row_0][col_0] == self.ground_truth[row_1][col_1]:
            self.visibility_board[row_0][col_0] = True
            self.visibility_board[row_1][col_1] = True
            self.winning_sets[player] +=1
            print(f'player {player} just won 1 set')
        
        else:
            print(f'player {player} did not pick a winning set')

        temporary_list = []

    def is_game_over(self):
        for r in range(self.row):
            for c in range(self.col):
                if self.visibility_board[r][c] == False:
                    return False
        return True

    def game_play(self, first_player: str = '1', player_type: str = 'human'):
        curr_player = first_player
        self.visualize_user_board()
        while not self.is_game_over():
            print(f'curr_player: {curr_player} type:{player_type}')
            if player_type == 'human':
                while True:
                    self.user_input() 
                    if self.check_human_input():
                        break
                    print(f'Input move invalid. Check that row and col are within bounds. The two moves are distinct and unopened.')
                temporary_list = self.temp
            if player_type != 'human':
                self.computer_input()
                temporary_list = self.computer_temp
            self.evaluate_input(curr_player, temporary_list)
            print(f'Sets won: Player 1 - {self.winning_sets['1']}, Player 2 - {self.winning_sets['2']}')
            self.visualize_user_board()
            if player_type == 'human':
                player_type = 'computer'
            elif player_type == 'computer':
                player_type = 'human'
            if curr_player == '1':
                curr_player = '2'
            elif curr_player == '2':
                curr_player = '1'
            time.sleep(5)
        largest_key = sorted(self.winning_sets.items(), key=lambda item:item[1], reverse=True)[0][0]
        largest_val = sorted(self.winning_sets.items(), key=lambda item:item[1], reverse=True)[0][1]
        print(f'Game ended.')
        print(f'Winner is {largest_key} with {largest_val} sets won out of {self.col} total sets')

if __name__ == "__main__":
    mem = Memory()
    mem.visualize_ground_truth() #for testing
    mem.game_play()
