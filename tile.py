# from state import State
# from successor import Successor

class Tile:
    '''La clase Tile sirve como representacion de las fichas del tablero'''
    def __init__(self, position, player):
        self.position = position
        self.player = player
        self.alive = True


