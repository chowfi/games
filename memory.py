from typing import List, Optional
import random

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
"""
class Memory:
    COLOR = ["\033[31m", "\033[32m", "\033[33m", "\033[34m", "\033[35m", "\033[36m"] #white: "\033[37m"
    BLOCK = "\u2588"
    RESET = "\033[0m"

    def __init__(self, row:int=2, col:int=3):
        self.row = row
        self.col = col

        self.full_combos = []
        for i in range(len(self.COLOR)):
            self.combo = self.COLOR[i] + self.BLOCK + self.RESET
            self.full_combos.append(self.combo)

        self.selected_colors = random.sample(self.full_combos, self.row)

        self.ground_truth = [[self.selected_colors[i] for i in range(self.col)] for _ in range(self.row)]
        self.user_board = [[self.BLOCK for i in range(self.col)] for _ in range(self.row)]