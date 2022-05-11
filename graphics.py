from typing import List
from http_manager import HttpManager
from utils import parse_coords, scale_img, unparse_coords
from state import State
from movement import Movement
from monoloco import mono_loco
from montecarlo import monte_carlo
import const
import pygame
from pygame.locals import *
import threading

class Graphics:

    def __init__(self, mode, state: State = State(), player = 0, http_mgr=HttpManager()): # 0 -> PvP Local | 1 -> PvP Online | 2 -> PvMC | 3 -> MCvML | 4 -> MCvMC
        self.state = state
        self.mode = mode
        self.player = player
        self.playing = False
        self.sim = [0, 0]
        self.http_mgr = http_mgr
        self.result = None
    
    def wait_update(self):
        movement = monte_carlo(self.state)
        self.state.make_movement(movement)
        self.playing = False

    def wait_movement(self):
        self.state = State()
        self.state.load_state(self.http_mgr.wait_movement())
        self.playing = False
        print(self.state)
    
    def game(self):
        #INICIO
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(const.MUSIC)
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)

        window = pygame.display.set_mode((const.WIDTH, const.HEIGHT))
        pygame.display.set_caption('Juego del Molino')
        pygame.display.set_icon(pygame.image.load(const.LOGO))
        font = pygame.font.Font(None, 60)

        #IMAGENES
        tablero_img = pygame.image.load(const.BOARD)
        tablero_img = pygame.transform.scale(tablero_img,(const.WIDTH, const.HEIGHT))
        tablas_img = pygame.image.load(const.TABLAS)
        tablas_img = pygame.transform.scale(tablas_img,(const.WIDTH, const.HEIGHT))
        p1_wins_img = pygame.image.load(const.P1_WINS)
        p1_wins_img = pygame.transform.scale(p1_wins_img,(const.WIDTH, const.HEIGHT))
        p2_wins_img = pygame.image.load(const.P2_WINS)
        p2_wins_img = pygame.transform.scale(p2_wins_img,(const.WIDTH, const.HEIGHT))
        p1_img_scoreboard = pygame.image.load(const.P1_TILE_IMG)
        p2_img_scoreboard = pygame.image.load(const.P2_TILE_IMG)
        p1_img  = scale_img(const.P1_TILE_IMG, (const.BLOCKSIZE - 10, const.BLOCKSIZE - 10))
        p2_img = scale_img(const.P2_TILE_IMG, (const.BLOCKSIZE - 10, const.BLOCKSIZE - 10))
        available_pos_img = pygame.image.load(const.AVAILABLE_POSITION)
        gs_pos_img = scale_img(const.SELECTED_POSITION_GREEN, (const.BLOCKSIZE - 10, const.BLOCKSIZE - 10))
        rs_pos_img = scale_img(const.SELECTED_POSITION_RED, (const.BLOCKSIZE - 10, const.BLOCKSIZE - 10))
        
        #VARIABLES
        selected_tile = None
        line = False #SI ES TRUE HAY UN 3 EN RAYA
        map_tiles = [] 
        available_positions = []
        positions_rect = []
        final_pos = None

        running = True
        while running:
            turn = self.state.turn % 2
            #COLOCACIÓN DE FICHAS P1 Y P2
            map_tiles.clear()
            for p1_tile in self.state.p1_positions:
                rect = p1_img.get_rect(center = unparse_coords(p1_tile))
                map_tiles.append((p1_img, rect))
            
            for p2_tile in self.state.p2_positions:
                rect = p2_img.get_rect(center = unparse_coords(p2_tile))
                map_tiles.append((p2_img, rect))
            #TABLERO
            window.blit(tablero_img, (0,0))
            #FICHAS Y POSICIONES DISPONIBLES/NO DISPONIBLES
            window.blits(map_tiles)
            if (self.player == 1 and self.mode in [1, 2] and turn == 1) or (self.player == 1 and self.mode in [1, 3] and turn == 1) or self.mode == 0:
                window.blits(positions_rect)
            #MARCADORES
            scoreboard_p1_tiles = font.render(str(self.state.p1_n_tiles), 1, (255, 255, 255))
            window.blit(scoreboard_p1_tiles, (45,225))  
            scoreboard_p2_tiles = font.render(str(self.state.p2_n_tiles), 1, (255, 255, 255))          
            window.blit(scoreboard_p2_tiles, (const.WIDTH-65,225))
            scoreboard_p1_dead_tiles = font.render(str(const.MAX_FICHAS - (self.state.p1_n_tiles + len(self.state.p1_positions))), 1, (255, 255, 255))
            window.blit(scoreboard_p1_dead_tiles, (45,415))
            scoreboard_p2_dead_tiles = font.render(str(const.MAX_FICHAS - (self.state.p2_n_tiles + len(self.state.p2_positions))), 1, (255, 255, 255))
            window.blit(scoreboard_p2_dead_tiles, (const.WIDTH-65,415)) 
            if turn:
                window.blit(p2_img_scoreboard, (472,552))
            else:
                window.blit(p1_img_scoreboard, (472,552))

            #PANTALLAS  
            if self.state.tie == [True, True]:
                window.blit(tablas_img, (0,0))
            if self.state.game_state == 0:
                window.blit(p1_wins_img, (0,0))
                map_tiles.clear()
            if self.state.game_state == 1:
                window.blit(p2_wins_img, (0,0))
                map_tiles.clear()
            pygame.display.update()
            if turn == 0:
                my_pos_tiles = self.state.p1_positions
                my_n_tiles = self.state.p1_n_tiles
                my_total_tiles = len(self.state.p1_positions) + self.state.p1_n_tiles
                op_pos_tiles = self.state.p2_positions
            else:
                my_pos_tiles = self.state.p2_positions
                my_n_tiles = self.state.p2_n_tiles
                my_total_tiles = len(self.state.p2_positions) + self.state.p2_n_tiles
                op_pos_tiles = self.state.p1_positions
            # SI QUEDAN FICHAS POR PONER O QUEDAN 3 FICHAS POS DISPONIBLES = TODAS LAS NO OCUPADAS, SI NO, SOLO LAS LIBRES ADYACENTES
            if my_n_tiles > 0 or my_total_tiles == 3:
                available_positions = [eval(pos) for pos in const.BOARD_POSITIONS if eval(pos) not in (self.state.p1_positions + self.state.p2_positions)]
            if selected_tile and my_total_tiles > 3:
                available_positions = [pos for pos in const.BOARD_POSITIONS[str(selected_tile)] if pos not in (self.state.p1_positions + self.state.p2_positions)]
            pos_img = available_pos_img            
            if my_n_tiles == 0 and not selected_tile:
                available_positions = my_pos_tiles
                pos_img = gs_pos_img
            if line:
                available_positions = op_pos_tiles
                pos_img = rs_pos_img
            positions_rect.clear()
            for av_pos in available_positions:
                rect = pos_img.get_rect(center = unparse_coords(av_pos))
                positions_rect.append((pos_img, rect)) 

            # Montecarlo
            turn = self.state.turn % 2
            if ((self.player == 1 and self.mode == 2 and turn == 0) or (self.player == 0 and self.mode == 3 and turn == 0) or self.mode == 4) and \
                self.state.game_state == 3 and not self.playing:
                    mc_turn = threading.Thread(target=self.wait_update)
                    self.playing = True
                    mc_turn.start()
            # Monoloco
            if turn == 1 and self.mode == 3 and self.state.game_state == 3 and not self.playing:
                ml_turn = mono_loco(self.state)
                self.state.make_movement(ml_turn)
            if self.mode == 3 and self.state.game_state in [0, 1, 2]:
                self.sim[self.state.game_state] += 1
                self.state = State()
                if sum(self.sim) > 10:
                    running = False
                    self.result = self.sim
            # Online PvP
            if self.mode == 1 and not turn == self.player:
                if not self.playing:
                    wait_th = threading.Thread(target=self.wait_movement())
                    self.playing = True
                    wait_th.start()

            for event in pygame.event.get():
                # KEYBOARD
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                        self.result = self.state.game_state
                elif event.type == QUIT:
                    running = False
                    self.result = self.state.game_state
                    print("Bye!")    
                if self.state.game_state in [0, 1, 2]:
                    break
                if (self.player == 1 and self.mode == 2 and turn == 0) or self.mode in [3, 4]:
                    break
                elif event.type == pygame.MOUSEBUTTONUP:
                    if not self.player == turn and not self.mode == 0:
                        print('No es tu turno')
                        break
                    pos = pygame.mouse.get_pos()
                    if pos[0] > const.WIDTH-65 and pos[0] < const.WIDTH and pos[1] > 0 and pos[1] < 65:  
                        if self.mode == 1:
                            self.state = State()
                            self.state.load_state(self.http_mgr.make_movement(Movement(None, None, None)))
                        else:
                            self.state.make_movement(Movement(None, None, None))
                    if not (pos[0] < 111 or pos[1] < 61 or pos[0] > const.HEIGHT - 15 or pos[1] > const.WIDTH - 164): # DENTRO DEL TABLERO
                        pcoords = parse_coords(pos)
                        # Si se ha hecho linea, es necesario seleccionar una ficha del oponente
                        if pcoords in available_positions:
                            if line:                       
                                movement = Movement(selected_tile, final_pos, pcoords)
                                if self.mode == 1:
                                    self.state = State()
                                    self.state.load_state(self.http_mgr.make_movement(movement))
                                else:
                                    self.state.make_movement(movement)
                                selected_tile = None
                                line = False
                            else:
                                if not selected_tile and my_n_tiles == 0:
                                    selected_tile = pcoords
                                else:
                                    movement = Movement(selected_tile, pcoords)
                                    line = self.state.is_line(movement, my_pos_tiles)
                                    if line:
                                        final_pos = pcoords
                                    else:
                                        if self.mode == 1:
                                            self.state = State()
                                            self.state.load_state(self.http_mgr.make_movement(movement))
                                        else:
                                            self.state.make_movement(movement)
                                        selected_tile = None
                        else:
                            selected_tile = None
        pygame.quit()
        return self.result
