import sqlite3


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
        conn.execute(
            "INSERT INTO game(winner, curr_board, curr_player) VALUES (?,?,?)",
            (None, None, None)
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