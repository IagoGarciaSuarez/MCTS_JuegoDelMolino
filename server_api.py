from typing import List
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from server.server_manager import ServerManager
from server import data_models
from db_manager import UserDB
from state import State
from movement import Movement
import uuid
import json

app = FastAPI()
server_manager = ServerManager()
users_db = UserDB()
tokens = {} # Dict de los tokens activos. <token>: <user_uid>
in_game_players = []

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

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
        result_state.update({"token": new_token, "user_uid": user_uid})
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
    users_db.new_user(user_uid, credentials.username, credentials.password)
    if users_db.is_registered(credentials.username):
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

@app.websocket("/playgame")
async def playgame(websocket: WebSocket):
    global in_game_players
    await manager.connect(websocket)
    try:
        if websocket not in in_game_players:
            req = await websocket.receive_text()
            req = json.loads(req)
            if 'game_name' in req:
                token = req['token']
                user_uid = tokens[token]
                manager.current_players = 1
                print("Creando juego")
                game_name = req['game_name']
                password = req['game_password']
                username = users_db.get_name_by_id(user_uid)
                game_uid = server_manager.new_game(username, game_name, password)
                state = server_manager.get_game_data(game_uid)
                in_game_players.append(websocket)
            elif 'game_uid' in req:
                token = req['token']
                user_uid = tokens[token]
                game_uid = req['game_uid']
                print("Uniendose a juego ", game_uid)
                password = req['game_password']
                username = users_db.get_name_by_id(user_uid)
                state = server_manager.get_game_data(game_uid)
                if not state:
                    return
                result_state = {"data": state}
                result_state["success"] = True
                await manager.broadcast(json.dumps(result_state))
                in_game_players.append(websocket)
        while True:
            req = await websocket.receive_text()
            if not req:
                continue
            movement = json.loads(req)
            state = server_manager.make_movement(state, movement)
            resp = {
                "success": True,
                "data": state
            }
            await manager.broadcast(json.dumps(resp))
            if state["game_state"] != 3:
                print("Fin de la partida")
                break
    except KeyError:
        result_state = {"success": False, "error": "Keyerror"}
        await manager.send_personal_message(json.dumps(result_state), websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        result = {'success': False}
        await manager.broadcast(json.dumps(result))

@app.get("/gamelist")
async def listgames():
    response = {'success': False}
    list_games = server_manager.list_games()
    response['success'] = True
    response['data'] = list_games
    return response

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


