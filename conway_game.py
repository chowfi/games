import random
from typing import List

def board(n):
    board_list = []

    for _ in range(n):
        board_list.append([random.randint(0,1) for _ in range(n)])

    return board_list

def count_live_neighbors(b,n):
    neighbors = [(-1,-1),(-1,0),(-1,1),
                (0,-1),(0,1),
                (1,-1), (1,0),(1,1)]
    b_new = []
    for _ in range(n):
        b_new.append([0 for _ in range(n)])

    for i in range(n):
        for j in range(n):
            for (dr, dc) in neighbors:
                new_row, new_col = i + dr, j + dc
                if (0 <= new_row < n) and (0 <= new_col < n):
                    if b[new_row][new_col] == 1:
                        b_new[i][j] +=1
    return b_new


def logic(b,n):
    live_n = count_live_neighbors(b,n)
    for i in range(n):
        for j in range(n):
    # any live cell with more than 3 live neighbors dies
            if live_n[i][j] > 3:
                b[i][j] = 0
    # any cell w <2 live neighbor dies
            if live_n[i][j] < 2:
                b[i][j] = 0
    # any dead cell with 3 live neighbors becomes live cell 
            if b[i][j] == 0 and live_n[i][j] == 3:
                b[i][j] = 1
    # any live cell w 2 to 3 live neighbors lives on
            if 2 <= live_n[i][j] <= 3:
                continue
    return b

def generate_conway_board(board_size: int):
    current_board = board(board_size)

    while True:
        yield current_board

        current_board = logic(current_board, board_size)

def visualize_board(board: List[List[int]]):
    # print("--------------")
    rendered_board = ''
    for row in board:
        # print(row)
        rendered_board += "\n"

if __name__ == "__main__":
    # n=3
    # cur_board = board(n)
    # # cur_board = [[0,0,0],[0,0,1],[0,1,0]]
    # print(f'initial iteration: {cur_board}')
    # print(f'count: {count_live_neighbors(cur_board,n)}')
    # for i in range(2):
    #     print(f'post {i} step curr board: {logic(cur_board, n)}')
    #     print(f'post {i} step count: {count_live_neighbors(cur_board,n)}')
    conway_board_generator = generate_conway_board(5)
    for _ in range(10):
        current_board = next(conway_board_generator)
        visualize_board(current_board)
