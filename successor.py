import copy
import const
from movement import Movement
from tile import Tile
from state import State

class Successor:
    def __init__(self, action: Movement, newState: State):
        self.newState = newState
        self.action = action
        #self.cost = cost        
        
    def __str__(self):
        return f"{self.action},{self.newState},{self.cost}"        
    
    def __repr__(self):
        return self.__str__()
    
    def __gt__(self, other):
        if type(other) is Successor:
            
            return self.action > other.action

    def __lt__(self, other):
        if type(other) is Successor:

            return self.action < other.action

    def __eq__(self, other):
        if type(other) is Successor:
            return self.action == other.action

    def get_successors(self, tablero: State, ficha: Tile):
        successor_list = []

        for i in const.BOARD_POSITIONS: 
            for j in const.BOARD_POSITIONS[i]:
                movimiento = Movement(ficha.position, j)
                nuevo_estado = self.action(tablero, ficha, movimiento)
                if(nuevo_estado != None):
                    successor = Successor(movimiento, nuevo_estado)
                    successor_list.append(successor)
        #successor_list = sorted(successor_list, key = lambda x: (x.action))
        return successor_list

    def action (self, tablero: State, ficha: Tile, action: Movement):
        #Del estado cambiamos el numero de fichas restantes del jugador y actualizamos el movimiento
        nuevo_tablero = copy.deepcopy(tablero)
        valid_action = self.is_possible_action(tablero, ficha, action)
        
        if(valid_action):
            #Jugador 1 o 2
            if (ficha.player == 0):
                if(nuevo_tablero.__p1_n_tiles > 0):
                    nuevo_tablero.__p1_n_tiles -= 1
                nuevo_tablero.__p1_positions.remove(action.initial_pos)
                nuevo_tablero.__p1_positions.append(action.final_pos)
            else:
                if(nuevo_tablero.__p2_n_tiles > 0):
                    nuevo_tablero.__p2_n_tiles -= 1
                nuevo_tablero.__p2_positions.remove(action.initial_pos)
                nuevo_tablero.__p2_positions.append(action.final_pos)            

            return nuevo_tablero
        else:
            return None

    def is_possible_action (self, tablero: State, ficha: Tile, action: Movement):   

        #comprobamos que la accion sea sobre la ficha pasada
        if(ficha.position == action.initial_pos):

            #obtenemos el jugador 1 o 2      
            if (ficha.player == 0):
                fichas_jugador = tablero.get_p1_n_tiles()
            else:
                fichas_jugador = tablero.get_p2_n_tiles()

            #1º se comprueba que la posicion no este ocupada 
            if (action.final_pos in tablero.get_p1_positions or action.final_pos in tablero.get_p2_positions):
                return False
            else:
                #Si quedan fichas por colocar, es decir podemos escoger una posicion libre del tablero
                if (fichas_jugador != 0):
                    return True
                #Si hay que mover la ficha
                else:
                    #Es posible hacer el movimiento
                    if(action.final_pos in const.BOARD_POSITIONS['['+action.initial_pos[0]+', '+action.initial_pos[1]+']']):
                        return True
                    #No es posible hacer el movimientop
                    else:
                        return False
        else:
            return False
            #print diccionario['nombre'] #Carlos

