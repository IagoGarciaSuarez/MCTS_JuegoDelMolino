'''Implementacion de la clase dedicada a representar los movimientos.'''

class Movement:
    def __init__(self, initial_pos, final_pos, kill_tile=None):
        self.initial_pos = initial_pos
        self.final_pos = final_pos
        self.kill_tile = kill_tile

    def load_movement(self, movement_data):
        self.initial_pos = movement_data["initial_pos"]
        self.final_pos = movement_data["final_pos"]
        self.kill_tile = movement_data["kill_tile"]