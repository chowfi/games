import tictactoe_db as db
import tictactoe
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

"""
Example commands in terminal

Create a game: `curl -X POST http://127.0.0.1:8000/game/new`
Get game state: `curl http://127.0.0.1:8000/game/1`
Play a move: curl -X PUT http://127.0.0.1:8000/game/1/play \
  -H "Content-Type: application/json" \
  -d '{"row": 0, "col": 0}'
"""
app = FastAPI()

class UserInput(BaseModel):
    row: int
    col: int

@app.post("/game/new")
def new_game():
    game_id = db.create_game()   
    return {"game_id": game_id}  # returns JSON to client

@app.get("/game/{game_id}")
def game_state(game_id:int):
    result = db.get_latest_game(game_id) 
    return {"board": result["board"], "curr_player": result["curr_player"], "winner": result["winner"]}

@app.put("/game/{game_id}/play")
def update_state(game_id:int, body: UserInput):
    state = db.get_latest_game(game_id) 
    if state["winner"]:
        raise HTTPException(status_code=400, detail = "Game already over")

    board = state["board"]
    curr_player = state["curr_player"]
    if not tictactoe.is_valid_move(board, body.row, body.col):
        raise HTTPException(status_code=400, detail = "Invalid move")
    
    tictactoe.make_move(board, body.row, body.col, curr_player)
    winner= tictactoe.check_winner(board)
    draw = winner is None and tictactoe.is_board_full(board)
    next_player = "2" if curr_player == "1" else "1"
    
    db.update_game(game_id, winner, board, next_player)
    
    return {"board": board, "curr_player": next_player, "winner": winner, "draw": draw}

if __name__ == "__main__":
    db.init_db()
    uvicorn.run(app, host="127.0.0.1", port=8000)
