from fastapi import FastAPI
from server.server_manager import ServerManager
from server import data_models

app = FastAPI()
server_manager = ServerManager()

@app.post("/new_game/")
async def new_game(new_game: data_models.NewGame):
    game_uid = server_manager.new_game(**dict(new_game))
    return {"sucess": True, "game_uid": game_uid}

@app.get("/game/{game_uid}")
async def get_game(game_uid):
    board = server_manager.get_game_data(game_uid)
    return board

@app.post("/game/{game_uid}")
async def movement(movement: data_models.Movement, game_uid):
    result_state = {
        "success": False
    }
    if server_manager.validate_movement(game_uid, dict(movement)):
        result_state.update(server_manager.make_movement(server_manager.get_game_data(game_uid), movement))
        result_state["success"] = True
    
    return result_state
