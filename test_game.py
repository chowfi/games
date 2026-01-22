"""
Test cases for Tic Tac Toe

Run these tests with: python -m pytest test_game.py -v

These tests describe the expected behavior of your functions.
Use them to guide your implementation and verify it works!

NOTE: All board values are strings: '0' (empty), '1' (player 1), '2' (player 2)
"""

import pytest
from game import (
    create_empty_board,
    is_valid_move,
    make_move,
    check_winner,
    is_board_full,
)


# ============================================================
# Tests for create_empty_board
# ============================================================

class TestCreateEmptyBoard:
    def test_returns_3x3_grid(self):
        board = create_empty_board()
        assert len(board) == 3
        assert all(len(row) == 3 for row in board)

    def test_all_squares_are_zero(self):
        board = create_empty_board()
        print(board)
        for row in board:
            for cell in row:
                assert cell == '0'


# ============================================================
# Tests for is_valid_move
# ============================================================

class TestIsValidMove:
    def test_empty_square_is_valid(self):
        board = [['0', '0', '0'], ['0', '0', '0'], ['0', '0', '0']]
        assert is_valid_move(board, 0, 0) is True
        assert is_valid_move(board, 1, 1) is True
        assert is_valid_move(board, 2, 2) is True

    def test_occupied_square_is_invalid(self):
        board = [['1', '0', '0'], ['0', '2', '0'], ['0', '0', '0']]
        assert is_valid_move(board, 0, 0) is False  # Player 1 is here
        assert is_valid_move(board, 1, 1) is False  # Player 2 is here

    def test_out_of_bounds_is_invalid(self):
        board = [['0', '0', '0'], ['0', '0', '0'], ['0', '0', '0']]
        assert is_valid_move(board, -1, 0) is False
        assert is_valid_move(board, 0, -1) is False
        assert is_valid_move(board, 3, 0) is False
        assert is_valid_move(board, 0, 3) is False
        assert is_valid_move(board, 99, 99) is False


# ============================================================
# Tests for make_move
# ============================================================

class TestMakeMove:
    def test_places_player_piece(self):
        board = [['0', '0', '0'], ['0', '0', '0'], ['0', '0', '0']]
        new_board = make_move(board, 0, 0, '1')
        assert new_board[0][0] == '1'

    def test_multiple_moves(self):
        board = [['0', '0', '0'], ['0', '0', '0'], ['0', '0', '0']]
        board = make_move(board, 0, 0, '1')
        board = make_move(board, 1, 1, '2')
        board = make_move(board, 2, 2, '1')
        assert board[0][0] == '1'
        assert board[1][1] == '2'
        assert board[2][2] == '1'


# ============================================================
# Tests for check_winner
# ============================================================

class TestCheckWinner:
    def test_no_winner_empty_board(self):
        board = [['0', '0', '0'], ['0', '0', '0'], ['0', '0', '0']]
        assert check_winner(board) is None

    def test_no_winner_game_in_progress(self):
        board = [['1', '2', '0'], ['0', '1', '0'], ['2', '0', '0']]
        assert check_winner(board) is None

    def test_horizontal_win_row_0(self):
        board = [['1', '1', '1'], ['2', '2', '0'], ['0', '0', '0']]
        assert check_winner(board) == '1'

    def test_horizontal_win_row_1(self):
        board = [['1', '2', '1'], ['2', '2', '2'], ['1', '0', '0']]
        assert check_winner(board) == '2'

    def test_horizontal_win_row_2(self):
        board = [['1', '2', '0'], ['2', '1', '0'], ['1', '1', '1']]
        assert check_winner(board) == '1'

    def test_vertical_win_col_0(self):
        board = [['1', '2', '0'], ['1', '2', '0'], ['1', '0', '0']]
        assert check_winner(board) == '1'

    def test_vertical_win_col_1(self):
        board = [['1', '2', '0'], ['0', '2', '1'], ['1', '2', '0']]
        assert check_winner(board) == '2'

    def test_vertical_win_col_2(self):
        board = [['2', '0', '1'], ['2', '0', '1'], ['0', '0', '1']]
        assert check_winner(board) == '1'

    def test_diagonal_win_top_left_to_bottom_right(self):
        board = [['1', '2', '2'], ['0', '1', '0'], ['2', '0', '1']]
        assert check_winner(board) == '1'

    def test_diagonal_win_top_right_to_bottom_left(self):
        board = [['1', '0', '2'], ['1', '2', '0'], ['2', '0', '1']]
        assert check_winner(board) == '2'


# ============================================================
# Tests for is_board_full
# ============================================================

class TestIsBoardFull:
    def test_empty_board_is_not_full(self):
        board = [['0', '0', '0'], ['0', '0', '0'], ['0', '0', '0']]
        assert is_board_full(board) is False

    def test_partial_board_is_not_full(self):
        board = [['1', '2', '1'], ['2', '1', '2'], ['0', '0', '0']]
        assert is_board_full(board) is False

    def test_one_empty_is_not_full(self):
        board = [['1', '2', '1'], ['2', '1', '2'], ['2', '1', '0']]
        assert is_board_full(board) is False

    def test_full_board_is_full(self):
        board = [['1', '2', '1'], ['2', '1', '2'], ['2', '1', '2']]
        assert is_board_full(board) is True
