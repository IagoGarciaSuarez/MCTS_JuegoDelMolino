from state import State
import time
import random
from node import Node

max_time = None
def monte_carlo(state: State):
    global max_time
    max_time = time.time() + 5
    node = Node(None, state)
    while time.time() < max_time:
        selected_node = seleccionar(node) # Select son from node
        print(f'Selected node with ucb {selected_node.ucb}')
        expanded_node = expandir(selected_node) # Expansion
        sim_node = expanded_node.deepcopy()
        value = simular(sim_node) # Simulation
        retropropagacion(expanded_node, value) # Backpropagation
    sel_node = max(node.sons, key = lambda n: n.ucb)
    print(f"selected movement with ucb {sel_node.ucb} ")
    print(f"state {sel_node.state}")
    print(sel_node.movement)
    return max(node.sons, key = lambda n: n.ucb).movement

def seleccionar(node: Node):        
    if node.is_terminal or not node.fully_expanded:
        selected_node = node
    else:
        selected_node = seleccionar(max(node.sons, key=lambda n: n.ucb))
    return selected_node

def expandir(node: Node):
    if node.is_terminal:
        return node
    rand_mov = random.choice(node.possible_movements)
    new_node = node.make_movement(rand_mov)
    return new_node

def simular(node: Node):
    if time.time() > max_time:
        p1_tiles = len(node.state.p1_positions) + node.state.p1_n_tiles
        p2_tiles = len(node.state.p2_positions) + node.state.p2_n_tiles
        if p1_tiles > p2_tiles:
            return 0
        elif p1_tiles < p2_tiles:
            return 1
        else:
            return 2
    if node.is_terminal:
        return node.state.game_state
    rand_mov = random.choice(node.possible_movements)
    # print(rand_mov)
    new_node = node.make_movement(rand_mov)
    # print(f"Montecarlo en nodo con visitas: {new_node.visits}")
    # print(new_node.state)
    simular(new_node)
    
    # if node.is_terminal:
    #     return node.state.game_state
    # p1_tiles = (node.state.p1_n_tiles + len(node.state.p1_positions))
    # p2_tiles = (node.state.p2_n_tiles + len(node.state.p2_positions))
    # if p1_tiles > p2_tiles:
    #     return 0
    # elif p1_tiles < p2_tiles:
    #     return 1
    # else:    
    #     return 2 # Si no encuentra solución, el resultado es Tie

def retropropagacion(node:Node, value):
    node.visits += 1
    if value in [0, 1]:
        node.wins[value] += 1
    node.update_ucb()
    if node.parent:
        retropropagacion(node.parent, value)