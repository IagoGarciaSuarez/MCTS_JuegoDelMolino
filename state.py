import json
import const
from movement import Movement
from tile import Tile
# import logging

# logs = logging.getLogger(__name__)
# logs.setLevel(logging.DEBUG)

# logsformat = logging.Formatter("%(asctime)s:%(levelname)s:%(message)s")
# logfile = logging.FileHandler(const.LOGS_PATH + __name__ + '.log')
# logfile.setFormatter(logsformat)

# stream = logging.StreamHandler()
# streamformat = logging.Formatter("%(levelname)s:%(module)s:%(message)s")
# stream.setLevel(logging.DEBUG)
# stream.setFormatter(streamformat)

# logs.addHandler(logfile)
# logs.addHandler(stream)

class State:
    '''La clase estado corresponde a la clase tablero.'''
    def __init__(self, state_id, p1_positions=[], p2_positions=[], p1_n_tiles=9, p2_n_tiles=9, turn=0, game_state=""):
        '''Inicialización de la clase estado correspondiente al tablero.'''
        self.__state_id = state_id
        self.p1_positions = p1_positions
        self.p2_positions = p2_positions
        self.p1_n_tiles = p1_n_tiles
        self.p2_n_tiles = p2_n_tiles
        self.turn = turn
        self.game_state = game_state

    def __dict__(self):
        state_data = {
            "state_id": self.__state_id,
            "p1_positions": self.p1_positions,
            "p2_positions": self.p2_positions,
            "p1_n_tiles": self.p1_n_tiles,
            "p2_n_tiles": self.p2_n_tiles,
            "turn": self.turn,
            "game_state": self.game_state
        }
        return state_data
    
    # def __repr__(self) -> str:
    #     state_data = {
    #         "state_id": self.__state_id,
    #         "p1_positions": self.p1_positions,
    #         "p2_positions": self.p2_positions,
    #         "p1_n_tiles": self.p1_n_tiles,
    #         "p2_n_tiles": self.p2_n_tiles,
    #         "turn": self.turn
    #     }
    #     return state_data
    
    def __str__(self) -> str:
        return json.dumps(self.__dict__)
    @property
    def get_state_id(self):
        return self.__state_id

    def save_state(self):
        '''Guardado del último estado en un archivo JSON.'''
        with open(const.STATES_JSON, 'w') as states_file:
            json.dump(self, states_file)

        print(self)
        #logs.info("Estado actual de la partida guardado correctamente.")
    
    def load_state(self, state_data):
        # '''Carga del último estado guardado a partir de un JSON.'''
        # with open(const.STATES_JSON, 'r') as states_file:
        #     state_data = json.load(states_file)
        
        self.__state_id = state_data["state_id"]
        self.p1_positions = state_data["p1_positions"]
        self.p2_positions = state_data["p2_positions"]
        self.p1_n_tiles = state_data["p1_n_tiles"]
        self.p2_n_tiles = state_data["p2_n_tiles"]
        self.turn = state_data["turn"]

        #logs.info("Última partida guardada cargada correctamente.")

    def get_tile_data(self, position):
        '''Genera una instancia de Tile con los datos de una ficha dada una posición del tablero.'''
        if str(position) in const.BOARD_POSITIONS and position in self.p1_positions:
            return Tile(position, 0)
        elif str(position) in const.BOARD_POSITIONS and position in self.p2_positions:
            return Tile(position, 1)

    def validate_movement(self, movement: Movement):
        turn = self.turn % 2
        if turn == 0:
            my_pos_tiles = self.p1_positions
            my_n_tiles = self.p1_n_tiles
        else:
            my_pos_tiles = self.p2_positions
            my_n_tiles = self.p2_n_tiles

        if not movement.initial_pos:
            if my_n_tiles <= 0 or movement.final_pos in (self.p1_positions + self.p2_positions):
                return False
        else:
            tile = self.get_tile_data(movement.initial_pos)
            if not tile or not tile.alive:
                print("No tile")
                return False
            if movement.final_pos not in const.BOARD_POSITIONS[str(movement.initial_pos)] or \
                movement.final_pos in (self.p1_positions + self.p2_positions):
                print("No valid final pos")
                return False
        if movement.kill_tile and self.is_line(movement, my_pos_tiles)[0]:
            tile = self.get_tile_data(movement.kill_tile)
            if not tile or not tile.alive or tile.player == turn:
                return False
        return True

    def is_line(self, movement: Movement, player_positions):
        line_counter = [movement.final_pos]
        print('COMPRUEBA LINEA', player_positions, movement.final_pos)
        if len(player_positions) <= 1:
            return (False, [])
        for line_pos in line_counter:
            for board_pos in const.BOARD_POSITIONS[str(line_pos)]:
                if board_pos[0] == line_pos[0] and board_pos in player_positions:
                    line_counter.append(board_pos)
                    if len(line_counter) == 3:
                        print('LINE')
                        return (True, line_counter)
                    for b_pos in const.BOARD_POSITIONS[str(board_pos)]:
                        if b_pos[0] == line_pos[0] and b_pos in player_positions:
                            line_counter.append(board_pos)
                            if len(line_counter) == 3:
                                print('LINE')
                                return (True, line_counter)
        line_counter = [movement.final_pos]
        for line_pos in line_counter:
            for board_pos in const.BOARD_POSITIONS[str(line_pos)]:
                if board_pos[1] == line_pos[1] and board_pos in player_positions:
                    line_counter.append(board_pos)
                    if len(line_counter) == 3:
                        print('LINE')
                        return (True, line_counter)
                    for b_pos in const.BOARD_POSITIONS[str(board_pos)]:
                        if b_pos[1] == line_pos[1] and b_pos in player_positions:
                            line_counter.append(board_pos)
                            if len(line_counter) == 3:
                                print('LINE')
                                return (True, line_counter)
        return (False, [])
    
    def make_movement(self, movement: Movement):
        if not self.validate_movement(movement):
            return self.__dict__()
        turn = self.turn % 2
        if turn == 0:
            if movement.initial_pos:
                self.p1_positions.remove(movement.initial_pos)
            self.p1_positions.append(movement.final_pos)
            if movement.kill_tile:
                self.p2_positions.remove(movement.kill_tile)
        else:
            if movement.initial_pos:
                self.p2_positions.remove(movement.initial_pos)
            self.p2_positions.append(movement.final_pos)
            if movement.kill_tile:
                self.p1_positions.remove(movement.kill_tile)     
        self.turn += 1 
        return self.__dict__()
    
    def endgame(self):
        if (const.MAX_FICHAS-self.p1_n_tiles-len(self.p1_positions)) > 6:
            self.game_state = "P2 WINS"
        if (const.MAX_FICHAS-self.p2_n_tiles-len(self.p2_positions)) > 6:
            self.game_state = "P1 WINS"
