'''
make movement 
    Request -> body : <movement json>
    Response -> new_state if valid
                same state if invalid
'''
from typing import List
from fastapi import FastAPI, Request, WebSocket
from server.server_manager import ServerManager
from server import data_models
from db_manager import UserDB
from state import State
from movement import Movement
import uuid

app = FastAPI()
server_manager = ServerManager()
users_db = UserDB()
tokens = {} # Dict de los tokens activos. <token>: <user_uid>


'''class ConnectionManager:
    def __init__(self):
        self.connections: List[WebSocket] = []

    #Acepto el mensaje del navegador y añado los clientes a una lista
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)
    
    #Me aseguro de que todos los clientes obtengan la misma información
    async def broadcast(self, data:str):
        for connection in self.connections:
            await connection.send_text("recibido")

manager = ConnectionManager()
'''

@app.websocket('/')
async def echo(websocket: WebSocket):
    await websocket.accept()

    while True:
        data = await websocket.receive_text()
        print('message received: ', data)
        await websocket.send_text(data + '/server')

@app.post("/login")
async def login(credentials: data_models.Credentials):
    result_state = {
        "success": False
    }
    user_uid = users_db.verify_login(credentials.username, credentials.password)
    if user_uid:
        new_token = str(uuid.uuid4())
        tokens[new_token] = user_uid
        result_state["success"] = True
        result_state.update({"token": new_token})
    return result_state

@app.delete("/logout")
async def logout(req: Request):
    result_state = {
        "success": False
    }
    tokens.pop(req.headers["Authorization"], None)
    result_state["success"] = True
    return result_state

@app.post("/newuser")
async def createuser(credentials: data_models.Credentials):
    result_state = {
        "success": False
    }
    user_uid = str(uuid.uuid4())
    if not users_db.is_registered(credentials.username) and users_db.new_user(user_uid, credentials.username, credentials.password):
        result_state["success"] = True
    return result_state

@app.get("/stats")
async def stats(user_uid: str):
    result_state = {
        "success": False
    }
    stats = users_db.get_stats(user_uid)
    if stats:
        result_state.update({"stats": stats})
        result_state["success"] = True
    return result_state

@app.put("/updateuser")
async def updateuser(req: Request, credentials: data_models.Credentials):
    result_state = {
        "success": False
    }
    token = req.headers["Authorization"]
    try:
        user_uid = tokens[token]
    except KeyError:
        return result_state
    users_db.update_user(user_uid, credentials.username, credentials.password)
    result_state = {
        "success": True
    }
    return result_state

@app.delete("/removeuser")
async def remove_user(req: Request):
    result_state = {
        "success": False
    }
    token = req.headers["Authorization"]
    try:
        user_uid = tokens[token]
    except KeyError:
        return result_state
    users_db.remove_user(user_uid)
    result_state["success"] = True
    return result_state

@app.post("/newgame")
async def new_game(req: Request, new_game: data_models.NewGame):
    result_state = {
        "success": False
    }
    token = req.headers["Authorization"]
    try:
        user_uid = tokens[token]
    except KeyError:
        return result_state
    username = users_db.get_name_by_id(user_uid)
    game_uid = server_manager.new_game(username, new_game.game_name, new_game.password)
    game_data = server_manager.get_game_data(game_uid)
    result_state["success"] = True
    result_state.update({"game_uid": game_uid, "game_data": game_data})
    return result_state

@app.get("/game/list")
async def listgames():
    list_games = server_manager.list_games()
    return list_games

@app.post("/game/join")
async def joingame(req: Request, game_cred: data_models.GameJoin):
    result_state = {
        "success": False
    }
    token = req.headers["Authorization"]
    try:
        user_uid = tokens[token]
    except KeyError:
        return result_state
    username = users_db.get_name_by_id(user_uid)
    game_data = server_manager.join_game(username, game_cred.game_uid, game_cred.password)
    if game_data:
        result_state.update({"game_data": game_data})
        result_state["success"] = True
    return result_state

@app.get("/game/{game_uid}")
async def get_game(game_uid: str):
    board = server_manager.get_game_data(game_uid)
    return board

@app.post("/game/{game_uid}")
async def movement(movement: data_models.Movement, game_uid):
    result_state = {
        "success": False
    }
    state = State(**server_manager.get_game_data(game_uid))
    movement = Movement(**dict(movement))
    if state.validate_movement(movement):
        result_state.update(state.make_movement(movement))
        result_state["success"] = True
    return result_state


