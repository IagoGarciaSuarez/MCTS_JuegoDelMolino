from datetime import datetime
import uuid
from state import State

class Server:
    def __init__(self):
        self.games = {}

    def new_game(self, username, game_name, password=''):
        '''Crea una nueva partida y le asigna un servicio para gestionarla.'''
        game_uid = str(uuid.uuid4())
        board = State(game_uid)
        created_on = datetime.now()
        game_data = {
            game_uid: {
                "name": game_name,
                "creator": username,
                "password": password,
                "created_on": created_on.strftime('%d/%m/%Y-%H:%M'),
                "game_data": board
            }
        }
        # Asignación de un servidor dedicado a la nueva partida
        self.games.update(game_data)
        return game_uid
    
    def list_games(self):
        games_list = {}
        for game in self.games:
            game_data = self.games[game]
            game_data = {
                game: {
                    "name": game_data["name"],
                    "creator": game_data["creator"],
                    "public": not game_data["password"],
                    "created_on": game_data["created_on"]
                }
            }
            games_list.update(game_data)
        return games_list
    
    def get_game_data(self, game_uid):
        try:
            game = self.games[game_uid]["game_data"]
        except KeyError:
            return
        return game
