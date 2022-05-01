import json
import const
import copy
from movement import Movement
from tile import Tile

class State:
    '''La clase estado corresponde a la clase tablero.'''
    def __init__(self):
        '''Inicialización de la clase estado correspondiente al tablero.'''
        self.__state_id = 'state_id'
        self.p1_positions = []
        self.p2_positions = []
        self.p1_n_tiles = const.MAX_FICHAS
        self.p2_n_tiles = const.MAX_FICHAS
        self.turn = 0
        self.game_state = 3 # 0 -> P1 Wins | 1 -> P2 Wins | 2 -> Tie | 3 -> Playing

    def __eq__(self, state):
        if (isinstance(state, State)):
            return self.p1_positions == state.p1_positions and self.p2_positions == state.p2_positions and \
                self.p1_n_tiles == state.p1_n_tiles and self.p2_n_tiles == state.p2_n_tiles and self.turn == state.turn and self.game_state == state.game_state
        return False
    
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
        return json.dumps(self.__dict__())
    
    @property
    def get_state_id(self):
        return self.__state_id

    def deepcopy(self):
        new_state = State()
        new_state.load_state(self.__dict__())

    def save_state(self):
        '''Guardado del último estado en un archivo JSON.'''
        with open(const.STATES_JSON, 'w') as states_file:
            json.dump(self, states_file)
    
    def load_state(self, state_data):
        # '''Carga del último estado guardado a partir de un dict.'''
        # with open(const.STATES_JSON, 'r') as states_file:
        #     state_data = json.load(states_file)
        
        self.__state_id = state_data["state_id"]
        self.p1_positions = copy.deepcopy(state_data["p1_positions"])
        self.p2_positions = copy.deepcopy(state_data["p2_positions"])
        self.p1_n_tiles = state_data["p1_n_tiles"]
        self.p2_n_tiles = state_data["p2_n_tiles"]
        self.turn = state_data["turn"]
        self.game_state = state_data["game_state"]

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
            my_n_tiles = len(self.p1_positions) + self.p1_n_tiles
        else:
            my_pos_tiles = self.p2_positions
            my_n_tiles = self.p2_n_tiles
        if not movement.initial_pos: # Si aun se estan poniendo las fichas en el tablero
            if my_n_tiles <= 0 or movement.final_pos in (self.p1_positions + self.p2_positions):
                return False
        else:
            tile = self.get_tile_data(movement.initial_pos)
            if not tile or not tile.alive:
                print("No tile")
                return False
            if (movement.final_pos not in const.BOARD_POSITIONS[str(movement.initial_pos)] and my_n_tiles > 3) or \
                movement.final_pos in (self.p1_positions + self.p2_positions):
                print("No valid final pos")
                return False
        if movement.kill_tile and self.is_line(movement, my_pos_tiles):
            tile = self.get_tile_data(movement.kill_tile)
            if not tile or not tile.alive or tile.player == turn:
                return False
        return True

    def is_line(self, movement: Movement, player_positions):
        line_counter = [movement.final_pos]
        player_positions = [p_pos for p_pos in player_positions if not p_pos == movement.initial_pos]
        if len(player_positions) <= 1:
            return False
        for axis in [0, 1]:
            for line_pos in line_counter:
                for board_pos in const.BOARD_POSITIONS[str(line_pos)]:
                    if board_pos[axis] == line_pos[axis] and board_pos in player_positions:
                        line_counter.append(board_pos)
                        if len(line_counter) == 3:
                            return True
                        for b_pos in const.BOARD_POSITIONS[str(board_pos)]:
                            if b_pos[axis] == line_pos[axis] and b_pos in player_positions:
                                line_counter.append(board_pos)
                                if len(line_counter) == 3:
                                    return True
            line_counter = [movement.final_pos]
        return False
    
    def make_movement(self, movement: Movement):
        if not self.validate_movement(movement):
            return self.__dict__()
        turn = self.turn % 2
        if turn == 0:
            my_pos_tiles = self.p1_positions
            op_pos_tiles = self.p2_positions
        else:
            my_pos_tiles = self.p2_positions
            op_pos_tiles = self.p1_positions
        if movement.initial_pos:
            my_pos_tiles.remove(movement.initial_pos)
        else:    
            if turn == 0:
                self.p1_n_tiles -= 1
            else:
                self.p2_n_tiles -= 1
        my_pos_tiles.append(movement.final_pos)
        if movement.kill_tile:
            op_pos_tiles.remove(movement.kill_tile)
        self.turn += 1
        self.update_game_state() # Actualiza el estado de la partida
        # implement http with movement to server
        return self.__dict__()
    
    def update_game_state(self):
        if (len(self.p1_positions) + self.p1_n_tiles) < 3:
            self.game_state = 1
            return
        if (len(self.p2_positions) + self.p2_n_tiles) < 3:
            self.game_state = 0
            return
        turn = self.turn % 2
        if turn == 0:
            my_pos_tiles = self.p1_positions
            my_n_tiles = self.p1_n_tiles
            op_player = 1
        else:
            my_pos_tiles = self.p2_positions
            my_n_tiles = self.p2_n_tiles
            op_player = 0
        if my_n_tiles == 0:            
            for tile in my_pos_tiles: # Si el jugador tiene al menos un movimiento disponible
                found = False
                for pos in const.BOARD_POSITIONS[str(tile)]:
                    if pos not in (self.p1_positions + self.p2_positions):
                        found = True
                        self.game_state = 3
                        break
                if found:
                    break
                self.game_state = op_player # Pierde el jugador que tiene el turno