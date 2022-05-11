from state import State
import random
from node import Node

def mono_loco(state: State):
    print('-------------- MONOLOCO ------------------')
    node = Node(state)
    rand_mov = random.choice(node.possible_movements) # Un movimiento aleatoriamente de los disponibles
    print(f'MONOLOCO ELIGE EL MOVIMIENTO:\n{rand_mov}')
    return rand_mov