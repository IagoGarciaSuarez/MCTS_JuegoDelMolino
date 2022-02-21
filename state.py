import json
import const
import logging

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
    def __init__(self, state_id, p1_positions, p2_positions, p1_n_tiles, p2_n_tiles, turn):
        self.__state_id = state_id
        self.__p1_positions = p1_positions
        self.__p2_positions = p2_positions
        self.__p1_n_tiles = p1_n_tiles
        self.__p2_n_tiles = p2_n_tiles
        self.__turn = turn

    def save_state(self):
        state_data = {
            "state_id": self.__state_id,
            "p1_positions": self.__p1_positions,
            "p2_positions": self.__p2_positions,
            "p1_n_tiles": self.__p1_n_tiles,
            "p2_n_tiles": self.__p2_n_tiles,
            "turn": self.__turn
        }

        # Currently only saving one state, therefore only load the last saved state.
        with open(const.STATES_JSON, 'w') as states_file:
            json.dump(state_data, states_file)
        #logs.info("Estado actual de la partida guardado correctamente.")
    
    def load_state(self):
        with open(const.STATES_JSON, 'r') as states_file:
            state_data = json.load(states_file)
        
        self.__state_id = state_data["state_id"]
        self.__p1_positions = state_data["p1_positions"]
        self.__p2_positions = state_data["p2_positions"]
        self.__p1_n_tiles = state_data["p1_n_tiles"]
        self.__p2_n_tiles = state_data["p2_n_tiles"]
        self.__turn = state_data["turn"]

        return self.__p1_positions, self.__p2_positions, self.__turn

        #logs.info("Última partida guardada cargada correctamente.")

        