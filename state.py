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
        self.__p2_positions = p2_positions
        self.__p1_n_tiles = p1_n_tiles
        self.__p2_n_tiles = p2_n_tiles
        self.__turn = turn
        self.__game_state = game_state
    
    def __repr__(self) -> str:
        state_data = {
            "state_id": self.__state_id,
            "p1_positions": self.__p1_positions,
            "p2_positions": self.__p2_positions,
            "p1_n_tiles": self.__p1_n_tiles,
            "p2_n_tiles": self.__p2_n_tiles,
            "turn": self.__turn,
            "game_state": self.__game_state
        }
        return state_data
    
    def __str__(self) -> str:
        return json.dumps(self.__repr__())
    @property
    def get_state_id(self):
        return self.__state_id

    def save_state(self):
        '''Guardado del último estado en un archivo JSON.'''
        with open(const.STATES_JSON, 'w') as states_file:
            json.dump(self, states_file)

        print(self)
        #logs.info("Estado actual de la partida guardado correctamente.")
    
    def load_state(self):
        '''Carga del último estado guardado a partir de un JSON.'''
        with open(const.STATES_JSON, 'r') as states_file:
            state_data = json.load(states_file)
        
        self.__state_id = state_data["state_id"]
        self.__p1_positions = state_data["p1_positions"]
        self.__p2_positions = state_data["p2_positions"]
        self.__p1_n_tiles = state_data["p1_n_tiles"]
        self.__p2_n_tiles = state_data["p2_n_tiles"]
        self.__turn = state_data["turn"]

        #logs.info("Última partida guardada cargada correctamente.")

    def get_tile_data(self, position):
        '''Genera una instancia de Tile con los datos de una ficha dada una posición del tablero.'''
        if position in const.BOARD_POSITIONS and position in self.__p1_positions:
            return Tile(position, 0)
        elif position in const.BOARD_POSITIONS and position in self.__p2_positions:
            return Tile(position, 1)

    def validate_movement(self, movement: Movement):
        '''
        Verificación del movimiento con forma (pos_inicial, pos_final).
        Comprueba si existe una ficha en la posición inicial, 
        si está viva y si la posición objetivo existe y es alcanzable
        desde la posición inicial.
        '''
        tile = self.get_tile_data(movement.initial_pos)
        if not tile or not tile.alive:
            return False
        if str(movement.final_pos) not in const.BOARD_POSITIONS or \
            movement.final_pos not in const.BOARD_POSITIONS[str(movement.initial_pos)]:
            return False
        

        