'''Implementacion de la clase dedicada a representar los movimientos.'''
import copy

class Movement(dict):
    def __init__(self, initial_pos, final_pos, kill_tile=None):
        self.initial_pos = initial_pos
        self.final_pos = final_pos
        self.kill_tile = kill_tile

    def load_movement(self, movement_data):
        self.initial_pos = movement_data["initial_pos"]
        self.final_pos = movement_data["final_pos"]
        self.kill_tile = movement_data["kill_tile"]

    def __eq__(self, movement):
        if isinstance(movement, Movement):
            return self.initial_pos == movement.initial_pos and self.final_pos == movement.final_pos and self.kill_tile == movement.kill_tile
        return False
    
    def __str__(self):
        return f'Movement from {self.initial_pos} to {self.final_pos} killing {self.kill_tile}'
    
    def deepcopy(self):
        new_movement = Movement(copy.deepcopy(self.initial_pos), copy.deepcopy(self.final_pos), copy.deepcopy(self.kill_tile))
        return new_movement