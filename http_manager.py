import json
import websocket
import requests
import const
import asyncio
import threading

class HttpManager:
    def __init__(self, uri=const.SERVER):
        self.uri = uri
        self.ws = None

    def wait_for_update(self):
        upd_state = self.ws.recv()
        upd_state = json.loads(upd_state)
        if upd_state['success']:
            return upd_state['data']

    def new_game(self, token, game_name, game_password=''):
        uri = 'ws://' + self.uri + '/playgame'
        req = {
            "token": token,
            "game_name": game_name,
            "game_password": game_password
        }
        self.ws = websocket.WebSocket()
        self.ws.connect(uri)
        self.ws.send(json.dumps(req))
        response = self.ws.recv()
        print(response)
        response = json.loads(response)
        if response["success"]:
            return response["data"]

    def join_game(self, token, game_uid, game_password=''):
        uri = 'ws://' + self.uri + '/playgame'
        req = {
            "token": token,
            "game_uid": game_uid,
            "game_password": game_password
        }
        self.ws = websocket.WebSocket()
        self.ws.connect(uri)
        self.ws.send(json.dumps(req))
        response = self.ws.recv()
        response = json.loads(response)
        if response["success"]:
            return response["data"]
    
    def login(self, username, password):
        req = {
            "username": username,
            "password": password
        }
        resp = requests.post('http://' + self.uri + '/login', json=req)
        if resp.json()["success"]:
            resp = {"token": resp.json()["token"], "user_uid": resp.json()["user_uid"]}
            return resp
        return
    
    def create_user(self, username, password):
        req = {
            "username": username,
            "password": password
        }
        req = json.loads(json.dumps(req))
        resp = requests.post('http://' + self.uri + '/newuser', json=req)
        if resp.json()["success"]:
            return True
        return False
    
    def logout(self, token):
        resp = requests.delete('http://' + const.SERVER + '/logout', headers={"Authorization": token})
        return resp.json()['success']
    
    def update_user(self, username, password, token):
        resp = requests.put('http://' + const.SERVER + '/updateuser', headers={'Authorization': token}, data={"username": username, "password": password})
        return resp.json()["success"]

    def remove_user(self, token):
        resp = requests.delete('http://' + const.SERVER + '/removeuser', headers={'Authorization': token})
        return resp.json()["success"]

    def make_movement(self, movement):
        print("Movimiento: ", json.dumps(movement.__dict__))
        self.ws.send(json.dumps(movement.__dict__))
        resp = self.ws.recv()
        resp = json.loads(resp)
        print(resp)
        if resp['success']:
            return resp['data']

    def list_games(self):
        resp = requests.get('http://' + const.SERVER + '/game/list')
        if resp.json()['success']:
            return resp.json()['data']

