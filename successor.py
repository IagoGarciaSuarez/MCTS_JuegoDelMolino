import copy
import const
import random
from movement import Movement
from node import Node
from tile import Tile
from state import State

def get_rand_successor(node: Node):
    state = node.state
    if state.game_state in [0, 1]:
        return
    new_state = copy.deepcopy(state) # Se copia el estado para no modificar el del padre
    if state.turn % 2 == 0:
        p_pos = [pos for pos in state.p1_positions]
    else:
        p_pos = [pos for pos in state.p2_positions]
    # Selecciona una ficha aleatoria mientras haya fichas
    while p_pos:
        tile = p_pos.pop(random.randrange(len(p_pos)))
        successor = get_rand_tile_successor(new_state, new_state.get_tile_data(tile))
        if successor not in node.sons:
            return successor
    return

# ES NECESARIO CONTROLAR QUÉ MOVIMIENTOS YA SE HAN COGIDO
def get_rand_tile_successor(state: State, tile: Tile):
    # Se comprueba el turno para reducir el espacio de búsqueda a los movimientos del jugador actual
    if tile.player == 0:
        p_pos_tiles = state.p1_positions
        p_n_tiles = state.p1_n_tiles
        f_pos_tiles = state.p2_positions
    else:
        p_pos_tiles = state.p2_positions
        p_n_tiles = state.p2_n_tiles
        f_pos_tiles = state.p1_positions
    # Si el jugador tiene 3 fichas puede moverse a cualquier posición, si no, sólo a las adyacentes
    if p_n_tiles > 3:
        available_pos = [pos for pos in const.BOARD_POSITIONS[str(tile.position)] if pos not in (state.p1_positions + state.p2_positions)]
    else:
        available_pos = [eval(pos) for pos in const.BOARD_POSITIONS if eval(pos) not in (state.p1_positions + state.p2_positions)]
    if not available_pos:
        return
    # Seleccion de un movimiento aleatorio
    movement = Movement(tile.position, random.choice(available_pos))
    if state.is_line(movement, p_pos_tiles):
        f_pos = random.choice(f_pos_tiles)
        movement.kill_tile = f_pos
    state.make_movement(movement)
    return (movement, state)

def get_possible_movements(node: Node):
    ''' Genera una lista con todos los posibles movimientos desde el nodo '''
    movements = []
    state = node.state
    if state.turn % 2 == 0:
        p_pos = state.p1_positions
        p_n_tiles = state.p1_n_tiles
        f_pos = state.p2_positions
    else:
        p_pos = state.p2_positions
        p_n_tiles = state.p2_n_tiles
        f_pos = state.p1_positions
    for pos in p_pos: # Pos inicial
        if p_n_tiles > 3:
            available_pos = [pos_ for pos_ in const.BOARD_POSITIONS[str(pos)] if pos_ not in (state.p1_positions + state.p2_positions)]
        else:
            available_pos = [eval(pos_) for pos_ in const.BOARD_POSITIONS if eval(pos_) not in (state.p1_positions + state.p2_positions)]
        for final_pos in available_pos: # Pos final
            movement = Movement(pos, final_pos)
            if state.is_line(movement, p_pos):
                for f_pos_ in f_pos:
                    movement.kill_tile = f_pos_
                    if movement not in node.expanded_movements:
                        movements.append(movement)
            elif movement not in node.expanded_movements:
                movements.append(movement)
    if not movements:
        node.is_terminal = True
    return movements
        
