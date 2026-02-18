from random import randint, seed
from typing import List
from datetime import datetime
import time

def visualize_board(board: List[List[int]]):
    print("--------------")
    for row in board:
        print(row)

class Conway:
    def __init__(self, size: int, seed_value: int = 12345678):
        seed(seed_value)
        self.size = size
        self.board = []
        for _ in range(size):
            self.board.append([randint(0,1) for _ in range(size)])

    def play(self, iterations: int):
        count = 0
        while count < iterations:
            count += 1
            print(f"pre-yield - count {count}")
            print(datetime.now()) 
            yield self.board
            print(f"post-yield - count {count}")
            print(datetime.now()) 
            self.simulate()

    def simulate(self):
        print("i am simulating!!!!")
        print(datetime.now()) 
        live_neighbors_count = self.count_live_neighbors()
        for row in range(self.size):
            for col in range(self.size):
                # any live cell with more than 3 live neighbors dies
                if live_neighbors_count[row][col] > 3:
                    self.board[row][col] = 0

                # any cell w <2 live neighbor dies
                if live_neighbors_count[row][col] < 2:
                    self.board[row][col] = 0

                # any dead cell with 3 live neighbors becomes live cell 
                if self.board[row][col] == 0 and live_neighbors_count[row][col] == 3:
                    self.board[row][col] = 1

                # any live cell w 2 to 3 live neighbors lives on
                if 2 <= live_neighbors_count[row][col] <= 3:
                    continue

    def count_live_neighbors(self):
        neighbors = [
            (-1, -1),
            (-1,  0),
            (-1,  1),
            ( 0, -1),
            ( 0,  1),
            ( 1, -1),
            ( 1,  0),
            ( 1,  1),
        ]

        live_neighbors_count = []
        for _ in range(self.size):
            live_neighbors_count.append([0 for _ in range(self.size)])
        
        for row in range(self.size):
            for col in range(self.size):
                for (d_row, d_col) in neighbors:
                    new_row, new_col = row + d_row, col + d_col
                    if (0 <= new_row < self.size) and (0 <= new_col < self.size):
                        if self.board[new_row][new_col] == 1:
                            live_neighbors_count[row][col] += 1

        return live_neighbors_count

if __name__ == "__main__":
    conway = Conway(5)
    print("for board in conway.play(2):")
    for board in conway.play(2):
        # visualize_board(board)
        time.sleep(0.5)




    print("")
    print("while true")
    conway_board_generator = conway.play(2)
    while True:
        try:
            current_board = next(conway_board_generator)
            time.sleep(0.5)
        except StopIteration as e:
            print("done iterating")
            break



    print("")
    print("for_ in range(2)")
    conway_board_generator = conway.play(2)
    for _ in range(2):
        time.sleep(0.5)
        current_board = next(conway_board_generator)
        # print("visualizing board")
        # print(datetime.now())
        # visualize_board(current_board)
        time.sleep(0.5)