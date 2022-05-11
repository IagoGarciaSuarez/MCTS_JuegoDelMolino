import numpy
import const
from state import State
from movement import Movement

class Node:
    def __init__(self, state: State, movement: Movement=None, parent=None): 
        self.movement = movement
        self.state = state
        self.parent = parent
        self.wins = [0, 0, 0] # Wins = [J1, J2, T]
        self.visits = 0
        self.sons = []
        self.possible_movements = self.get_possible_movements()
        self.is_terminal = self.state.game_state in [0, 1, 2]
        self.fully_expanded = not self.possible_movements
        self.ucb = None
    
    def __str__(self):
        node_info = f'Estado {self.state}\nVictorias: {self.wins[0]}\nDerrotas: {self.wins[1]}\nEmpates: {self.wins[2]}' + \
            f'Visitas: {self.visits}\nEs Terminal: {self.is_terminal}\nTotalmente expandido: {self.fully_expanded}\n' + \
                f'Posibles movimientos sin expandir: {self.possible_movements}\nUCB: {self.ucb}\n'
        if self.parent:
            node_info += f'Estado del Padre: {self.parent.state}'
            node_info += f'\nVisitas al padre: {self.parent.visits}\nMovimiento: {self.movement}\n'
        return node_info
    
    def __eq__(self, other):
        if isinstance(other, Node):
            return self.movement == other.movement and self.state == other.state and self.parent == other.parent and self.wins == other.wins and \
                self.visits == other.visits and self.sons == other.sons and self.possible_movements == other.possible_movements and self.is_terminal == other.is_terminal and \
                    self.fully_expanded == other.fully_expanded and self.ucb == other.ucb
        return False

    def update_ucb(self):
        if not self.parent:
            return
        if self.visits == 0:
            self.ucb = float('inf')
        cte = 2 * 1/numpy.sqrt(2)
        self.ucb = ((self.wins[self.parent.state.turn%2] - self.wins[self.state.turn%2]) / self.visits) + cte * numpy.sqrt((2 * numpy.log(self.parent.visits) / self.visits))
    
    def get_possible_movements(self):
        ''' Genera una lista con todos los posibles movimientos desde el nodo '''
        movements = []
        if self.state.turn % 2 == 0:
            p_pos = self.state.p1_positions
            p_n_tiles = self.state.p1_n_tiles
            op_pos = self.state.p2_positions
        else:
            p_pos = self.state.p2_positions
            p_n_tiles = self.state.p2_n_tiles
            op_pos = self.state.p1_positions
        p_total_tiles = p_n_tiles + len(p_pos)
        if p_n_tiles == 0:
            for i_pos in p_pos: # Por cada ficha que tenga el jugador
                if p_total_tiles == 3: # Si tiene 3 fichas, puede moverlas a cualquier posicion libre
                    available_pos = [eval(pos_) for pos_ in const.BOARD_POSITIONS if eval(pos_) not in (self.state.p1_positions + self.state.p2_positions)]
                else: # Si no, solo a las adyacentes libres
                    available_pos = [pos_ for pos_ in const.BOARD_POSITIONS[str(i_pos)] if pos_ not in (self.state.p1_positions + self.state.p2_positions)]
                for f_pos in available_pos: # Por cada posicion a la que se puede mover
                    movement = Movement(i_pos, f_pos)
                    if self.state.is_line(movement, p_pos):
                        for k_pos in op_pos: # Por cada ficha que puede eliminar
                            movement = Movement(i_pos, f_pos, k_pos)
                            movements.append(movement)
                    else:
                        movements.append(movement)
        else:
            available_pos = [eval(pos_) for pos_ in const.BOARD_POSITIONS if eval(pos_) not in (self.state.p1_positions + self.state.p2_positions)]
            for f_pos in available_pos:
                movement = Movement(None, f_pos)
                if self.state.is_line(movement, p_pos):
                    for k_pos in op_pos:
                        movement = Movement(None, f_pos, k_pos)
                        movements.append(movement)
                else:
                    movements.append(movement)
        return movements
    
    def make_movement(self, movement):
        new_state = State()
        new_state.load_state(self.state.__dict__())
        new_state.make_movement(movement)
        self.possible_movements.remove(movement)
        if not self.possible_movements:
            self.fully_expanded = True
        new_node = Node(new_state, movement=movement, parent=self)
        self.sons.append(new_node)
        return new_node
    
    def deepcopy(self):
        new_state = State()
        new_state.load_state(self.state.__dict__())
        new_node = Node(new_state, movement=self.movement, parent=self.parent)
        new_node.wins = [val for val in self.wins]
        new_node.visits = self.visits
        new_node.sons = [son.deepcopy() for son in self.sons]
        new_node.is_terminal = self.is_terminal
        new_node.fully_expanded = self.fully_expanded
        new_node.ucb = self.ucb
        return new_node

