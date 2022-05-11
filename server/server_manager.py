from datetime import datetime
import uuid
from state import State
import const
from movement import Movement

class ServerManager:
    def __init__(self):
        self.games = {}

    def new_game(self, username, game_name, password=''):
        '''Crea una nueva partida y le asigna un servicio para gestionarla.'''
        game_uid = str(uuid.uuid4())
        board = State()
        board.__state_id = game_uid
        created_on = datetime.now()
        game_data = {
            game_uid: {
                "name": game_name,
                "creator": username,
                "password": password,
                "created_on": created_on.strftime('%d/%m/%Y-%H:%M'),
                "game_data": board.__dict__()
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

    def validate_movement(self, game_uid, movement):
        game = self.get_game_data(game_uid)
        state = State(**game)
        movement = Movement(**movement)
        turn = state.turn % 2
        if turn == 0:
            my_pos_tiles = state.p1_positions
            my_n_tiles = state.p1_n_tiles
        else:
            my_pos_tiles = state.p2_positions
            my_n_tiles = state.p2_n_tiles

        if not movement.initial_pos:
            if (my_n_tiles - len(my_pos_tiles)) <= 0:
                print("Tiles: ", (my_n_tiles - len(my_pos_tiles)))
                return False
        else:
            tile = state.get_tile_data(movement.initial_pos)
            if not tile or not tile.alive:
                print("No tile")
                return False
            if movement.final_pos not in const.BOARD_POSITIONS[str(movement.initial_pos)] or \
                movement.final_pos in state.p1_positions + state.p2_positions:
                print("No valid final pos")
                return False
        if movement.kill_tile and self.is_line(state, movement, my_pos_tiles):
            tile = state.get_tile_data(movement.kill_tile)
            if not tile or not tile.alive or tile.player == turn:
                return False
        return True
    
    def is_line(self, state: State, movement: Movement, player_positions):
        positions = [pos for pos in player_positions if pos != movement.initial_pos]
        line_counter = 1
        for pos in positions:
            if pos[0] == movement.final_pos[0]:
                line_counter += 1
            if line_counter >= 3:
                return True
        line_counter = 1
        for pos in positions:
            if pos[1] == movement.final_pos[1]:
                line_counter += 1
            if line_counter >= 3:
                return True
        return False
    
    def make_movement(self, state, movement):
        n_state = State()
        n_state.load_state(state)
        print("HACIENDO MOVIMIENTO", movement)
        movement = Movement(**dict(movement))
        turn = n_state.turn % 2
        if turn == 0:
            if movement.initial_pos:
                n_state.p1_positions.remove(movement.initial_pos)
            n_state.p1_positions.append(movement.final_pos)
            if movement.kill_tile:
                n_state.p2_positions.remove(movement.kill_tile)
        else:
            if movement.initial_pos:
                n_state.p2_positions.remove(movement.initial_pos)
            n_state.p2_positions.append(movement.final_pos)
            if movement.kill_tile:
                n_state.p1_positions.remove(movement.kill_tile)     
        n_state.turn += 1 
        return n_state.__dict__()
