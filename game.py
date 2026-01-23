"""
Tic Tac Toe - Two Player CLI Game

Players are represented as:
- Player 1: 1
- Player 2: 2
- Empty square: .

Board is a 3x3 matrix (list of lists)
Coordinates are 0-indexed: (row, col)
"""
import random

def create_empty_board():
    """
    Create and return a 3x3 board filled with zeros.
    
    Returns:
        A 3x3 list of lists, all values initialized to 0
    
    """
    return [['0' for _ in range(3)] for _ in range(3)]


def display_board(board):
    """
    Print the board to the console in a human-readable format.
    
    Args:
        board: The 3x3 game board
    
    """
    def present(row):
        presentation = []
        for num in row:
            if num in ['1', '2']:
                presentation.append(num)
            else:
                presentation.append('.')
        return presentation
    def combine(board):   
        beg = print('    0   1   2  '+ '\n' + '  ' + '-'*13) 
        for i in range(len(board)):      
            print(f'{i} '+ "| " + " | ".join(present(board[i])) + " |" + '\n' + '  ' + '-'*13 )

    return combine(board)


def is_valid_move(board, row, col):
    """
    Check if a move is valid.
    
    A move is valid if:
    - row and col are within bounds (0-2)
    - The target square is empty (value is 0)
    
    Args:
        board: The 3x3 game board
        row: Row index (0-2)
        col: Column index (0-2)
    
    Returns:
        True if the move is valid, False otherwise
    
    """
    if row <=2 and row >= 0:
        if col <=2 and col >=0:
            if board[row][col] == '0':
                return True
    return False


def make_move(board, row, col, player):
    """
    Place a player's piece on the board.
    
    Args:
        board: The 3x3 game board
        row: Row index (0-2)
        col: Column index (0-2)
        player: Player number (1 or 2)
    
    Returns:
        The updated board
    
    """
    if player == '1':
        board[row][col] = '1'
    elif player == '2':
        board[row][col] = '2'

    return board


def check_winner(board):
    """
    Check if there's a winner.
    
    A player wins if they have 3 in a row:
    - Horizontally (any row)
    - Vertically (any column)  
    - Diagonally (either diagonal)
    
    Args:
        board: The 3x3 game board
    
    Returns:
        The winning player (1 or 2), or None if no winner yet
    
    """
    #diagonal
    if board [0][0] == board[1][1] == board [2][2] and board [0][0] != '0':
        return board[0][0]
    elif board [0][2] == board[1][1] == board [2][0] and board [0][2] != '0':
        return board[0][2]
    else:
        #horizontal
        for i in range(len(board)):
            if board[i][0] == board[i][1] == board[i][2] and board[i][0] != '0':
                return board[i][0]
        #vertical
            elif board[0][i] == board[1][i] == board[2][i] and board[0][i] != '0':
                return board[0][i]
    return None


def is_board_full(board):
    """
    Check if the board is completely filled (no zeros remaining).
    
    Args:
        board: The 3x3 game board
    
    Returns:
        True if the board is full, False otherwise
    
    """
    length = len(board)
    
    for i in range(length):
        if '0' in board[i]:
            return False
    return True


def get_player_move(player):
    """
    Prompt the player for their move and return the coordinates.
    
    Args:
        player: Player number (1 or 2)
    
    Returns:
        A tuple (row, col) representing the player's chosen move
    
    """
    answer = input(f'Player {player} input your next move in this format:\n row,col (0th index-ed)\n')
    row, col = answer.split(",")
    return (int(row),int(col))

def get_random_move(board):
    """
    Random move by AI 

    Args:
        board: The 3x3 game board

    Returns:
        A tuple (row, col) representing the random AI's chosen move
    """
    while True:
        row, col = random.randint(0,2), random.randint(0,2)
        if is_valid_move(board, row, col):
            break
    return (row,col)

def play_game():
    """
    Main game loop.
    
    The flow should be:
    1. Create an empty board
    2. Display the board
    3. Loop:
       a. Get current player's move
       b. Validate the move (if invalid, ask again)
       c. Make the move
       d. Display the updated board
       e. Check for winner -> announce and end
       f. Check for draw -> announce and end
       g. Switch to other player
    """
    player = '1'
    board = create_empty_board()
    display_board(board)
    while not is_board_full(board):
        if player == '1':
            while True:
            # if player == '1':
                row, col = get_player_move(player)
                if is_valid_move(board, row, col):
                    break
                print(f'Input move invalid. Check the following and try again:\n 1) row and col are within bounds (0-2)\n 2) The target square is empty')
        else: 
            row, col = get_random_move(board)
        board = make_move(board, row, col, player)
        display_board(board)
        if check_winner(board) is not None:
            print(f'Winner: Player {check_winner(board)}')
            break
        else:
            if player == '1':
                player = '2'
            elif player == '2':
                player = '1'
    if check_winner(board) is None:
        print (f"Game Ended: It's a cat's game!\n https://english.stackexchange.com/questions/155621/why-is-a-tie-in-tic-tac-toe-called-a-cats-game")

if __name__ == "__main__":
    play_game()
