from state import State
import time
import random
from node import Node

max_time = None
def monte_carlo(state: State):
    print('-------------- MONTECARLO ------------------')
    global max_time
    max_time = time.time() + 3
    node = Node(state)
    while time.time() < max_time:
        selected_node = seleccionar(node) # Selecciona un hijo y lo expande si es necesario
        sim_node = selected_node.deepcopy()
        value = simular(sim_node) # Simula la partida con el nodo seleccionado
        retropropagacion(selected_node, value) # Retropropaga el resultado de la simulación
    for n in node.sons:
        n.update_ucb()
    result = max(node.sons, key = lambda n: n.ucb)
    print("Nodo seleccionado:\n", result)
    return result.movement

def seleccionar(node: Node):    
    if node.is_terminal:
        return node
    if not node.fully_expanded:
        return expandir(node)
    for son in node.sons:
        if son.visits == 0:
            return expandir(node)
        son.update_ucb()
    selected_node = seleccionar(max(node.sons, key=lambda n: n.ucb))
    return selected_node

def expandir(node: Node):
    if not node.possible_movements:
        return node
    rand_mov = random.choice(node.possible_movements)
    new_node = node.make_movement(rand_mov)
    return new_node

def simular(node: Node):
    if time.time() > max_time:
        return 2
    if node.is_terminal:
        return node.state.game_state
    rand_mov = random.choice(node.possible_movements)
    new_node = node.make_movement(rand_mov)
    return simular(new_node)

def retropropagacion(node:Node, value):
    if node.is_terminal:
        node.visits = 1
        node.wins[value] = 1
    else:
        node.visits += 1
        node.wins[value] += 1
    if node.parent:
        retropropagacion(node.parent, value)