import sqlite3
import tictactoe
import json


def init_db():
    """
    Create a simple `game` table that stores only
    the latest board and related info.
    """
    conn = sqlite3.connect("tictactoe.db")
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS game (
                id INTEGER PRIMARY KEY,
                winner TEXT,
                curr_board TEXT,
                curr_player TEXT
            )
            """
        )
        conn.commit()
    finally:
        conn.close()

def create_game():
    conn = sqlite3.connect("tictactoe.db")
    try:
        board = tictactoe.create_empty_board() #list of lists
        board_str = json.dumps(board) # turn it into one string
        cur = conn.execute(
            "INSERT INTO game(winner, curr_board, curr_player) VALUES (?,?,?)",
            (None, board_str, "1")
        )
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()

def get_latest_game(id_number):
    conn = sqlite3.connect("tictactoe.db")
    try:
        current_board = json.loads(conn.execute("SELECT curr_board FROM game WHERE id = ?", (id_number,)).fetchone()[0])
        current_player = conn.execute("SELECT curr_player FROM game WHERE id = ?", (id_number,)).fetchone()[0]
        winner = conn.execute("SELECT winner FROM game WHERE id = ?", (id_number,)).fetchone()[0]
        return {"board": current_board, "curr_player": current_player, "winner": winner}
    finally:
        conn.close()

def update_game(id_number, winner_game, current_board, current_player):
    conn = sqlite3.connect("tictactoe.db")
    try:
        board_str = json.dumps(current_board)
        conn.execute(
            "UPDATE game SET winner = ?, curr_board = ?, curr_player = ? WHERE id = ?",
            (winner_game, board_str, current_player,id_number)
        )
        conn.commit()
    finally:
        conn.close()

if __name__ == "__main__":
    init_db()
    create_game()

    conn = sqlite3.connect("tictactoe.db")
    print(list(conn.execute("SELECT * FROM game")))
    conn.close()