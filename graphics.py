from typing import List
from utils import parse_coords, scale_img, unparse_coords, is_line
from state import State
from movement import Movement
import const
import pygame
from pygame.locals import *

class Graphics:

    def __init__(self, state: State = State('test')):
        self.state = state

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
        selected_pos_green_img = scale_img(const.SELECTED_POSITION_GREEN, (const.BLOCKSIZE - 10, const.BLOCKSIZE - 10))
        selected_pos_red_img = scale_img(const.SELECTED_POSITION_RED, (const.BLOCKSIZE - 10, const.BLOCKSIZE - 10))

        #VARIABLES
        

        selected_tile_p1 = False
        selected_tile_p2 = False
        tablas = []
        line = False #SI ES TRUE HAY UN 3 EN RAYA

        map_tiles = [] 
        green_positions = []
        red_positions = []
        available_positions = []

        final_pos = None

        running = True
        while running:
            p1_tiles:List = self.state.p1_positions
            p2_tiles:List = self.state.p2_positions
            #TABLERO
            window.blit(tablero_img, (0,0))
            #FICHAS Y POSICIONES DISPONIBLES/NO DISPONIBLES
            window.blits(map_tiles)
            window.blits(green_positions)
            window.blits(red_positions)
            #MARCADORES
            scoreboard_p1_tiles = font.render(str(self.state.p1_n_tiles), 1, (255, 255, 255))
            window.blit(scoreboard_p1_tiles, (45,225))  
            scoreboard_p2_tiles = font.render(str(self.state.p2_n_tiles), 1, (255, 255, 255))          
            window.blit(scoreboard_p2_tiles, (const.WIDTH-65,225))
            # scoreboard_p1_dead_tiles = font.render(str(const.MAX_FICHAS - (self.state.p1_n_tiles + len(p1_tiles))), 1, (255, 255, 255))
            # window.blit(scoreboard_p1_dead_tiles, (45,415))
            # scoreboard_p2_dead_tiles = font.render(str(const.MAX_FICHAS - (self.state.p2_n_tiles + len(p2_tiles))), 1, (255, 255, 255))
            # window.blit(scoreboard_p2_dead_tiles, (const.WIDTH-65,415)) 
            #TURNO

            if(self.state.turn % 2 == 0):
                window.blit(p1_img_scoreboard, (472,552))
                if self.state.p1_n_tiles > 0: # SI TURNO P1 Y QUEDAN FICHAS POR PONER
                    available_positions = [eval(pos) for pos in const.BOARD_POSITIONS if eval(pos) not in (p1_tiles + p2_tiles)]         
            else: 
                window.blit(p2_img_scoreboard, (472,552))
                if self.state.p2_n_tiles > 0: # SI TURNO P1 Y QUEDAN FICHAS POR PONER
                    available_positions = [eval(pos) for pos in const.BOARD_POSITIONS if eval(pos) not in (p1_tiles + p2_tiles)]
                            
            
            
            #MOUSE O KEYBOARD
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    if not (pos[0] < 111 or pos[1] < 61 or pos[0] > const.HEIGHT - 15 or pos[1] > const.WIDTH - 164): # DENTRO DEL TABLERO
                        pcoords = parse_coords(pos)
                        print(pcoords, (self.state.turn % 2) + 1)
                        if self.state.turn % 2 == 0:
                            if self.state.p1_n_tiles > 0: # SI TURNO P1 Y QUEDAN FICHAS POR PONER
                                available_positions = [eval(pos) for pos in const.BOARD_POSITIONS if eval(pos) not in (p1_tiles + p2_tiles)]
                                if line:                            
                                    if pcoords in self.state.p2_positions:
                                        movement = Movement([], final_pos, pcoords)
                                        self.state.make_movement(movement)
                                        available_positions.clear()
                                        red_positions.clear()
                                        green_positions.clear()
                                        selected_tile_p1 = None
                                        selected_tile_p2 = None
                                else:
                                    if pcoords in available_positions:
                                        movement = Movement([], pcoords)
                                        is_line = self.state.is_line(movement, [p_pos for p_pos in self.state.p1_positions if p_pos != pcoords])
                                        if is_line[0]:
                                            final_pos = pcoords
                                            line = True
                                            print('LINEA P1')
                                            print(is_line)
                                            available_positions.clear()
                                            red_positions.clear()
                                        else:
                                            self.state.make_movement(movement)
                                            available_positions.clear()
                                            red_positions.clear()
                                            green_positions.clear()
                                            selected_tile_p1 = None
                                            selected_tile_p2 = None
                            else: # SI TURNO P1 Y NO QUEDAN FICHAS POR PONER
                                if pcoords in self.state.p1_positions and not selected_tile_p1:
                                    selected_tile_p1 = pcoords
                                if pcoords in available_positions:
                                    movement = Movement([], pcoords)
                                    is_line = self.state.is_line(movement, [p_pos for p_pos in self.state.p1_positions if p_pos != pcoords])
                                    if is_line[0]:
                                        final_pos = pcoords
                                        line = True
                                        available_positions.clear()
                                        red_positions.clear()
                                    else:
                                        self.state.make_movement(movement)
                                        available_positions.clear()
                                        red_positions.clear()
                                        green_positions.clear()
                                        selected_tile_p1 = None
                                        selected_tile_p2 = None
                        else:
                            if self.state.p2_n_tiles > 0: # SI TURNO P2 Y QUEDAN FICHAS POR PONER
                                available_positions = [eval(pos) for pos in const.BOARD_POSITIONS if eval(pos) not in (p1_tiles + p2_tiles)]
                                if line:
                                    if pos in self.state.p1_positions:
                                        movement = Movement([], final_pos, pcoords)
                                        self.state.make_movement(movement)
                                        available_positions.clear()
                                        red_positions.clear()
                                        green_positions.clear()
                                        selected_tile_p1 = None
                                        selected_tile_p2 = None
                                else:
                                    if pcoords in available_positions:
                                        movement = Movement([], pcoords)
                                        is_line = self.state.is_line(movement, [p_pos for p_pos in self.state.p2_positions if p_pos != pcoords])
                                        if is_line[0]:
                                            final_pos = pcoords
                                            line = True
                                            print('LINEA P2')
                                            print(is_line[1])
                                            available_positions.clear()
                                            red_positions.clear()
                                        else:
                                            self.state.make_movement(movement)
                                            available_positions.clear()
                                            red_positions.clear()
                                            green_positions.clear()
                                            selected_tile_p1 = None
                                            selected_tile_p2 = None
                            else: # SI TURNO P1 Y NO QUEDAN FICHAS POR PONER
                                if pcoords in self.state.p2_positions and not selected_tile_p2:
                                    selected_tile_p2 = pcoords
                                if pcoords in available_positions:
                                    movement = Movement([], pcoords)
                                    is_line = self.state.is_line(movement, [p_pos for p_pos in self.state.p2_positions if p_pos != pcoords])
                                    if is_line[0]:
                                        final_pos = pcoords
                                        line = True
                                        available_positions.clear()
                                        red_positions.clear()
                                    else:
                                        self.state.make_movement(movement)
                                        available_positions.clear()
                                        red_positions.clear()
                                        green_positions.clear()
                                        selected_tile_p1 = None
                                        selected_tile_p2 = None
                    #     if(line == False):
                    #         if (self.state.p1_n_tiles != 0) or (self.state.p2_n_tiles != 0):
                    #             if(parse_coords(pos) in available_positions):
                    #                 pcords = parse_coords(pos)
                    #                 #P1
                    #                 if self.state.turn % 2 == 0:
                    #                     p1_tiles.append(pcords)
                    #                     available_positions.remove(pcords)
                    #                     self.state.p1_n_tiles -= 1
                    #                     line_p1, lines = is_line(p1_tiles)
                    #                 #P2
                    #                 if self.state.turn % 2 != 0:
                    #                     p2_tiles.append(pcords)
                    #                     available_positions.remove(pcords)
                    #                     self.state.p2_n_tiles -= 1
                    #                     line_p2, lines = is_line(p2_tiles)
                    #                 self.state.turn  += 1
                    #         else:                            
                    #             #P1
                    #             if(parse_coords(pos) in p1_tiles and self.state.turn % 2 == 0): 
                    #                 positions_to_move = []
                    #                 pcords = parse_coords(pos)
                    #                 coord = unparse_coords(pcords) 
                    #                 selected_tile_p1 = True
                    #                 to_delate_position = pcords                                                     
                    #                 for i in const.BOARD_POSITIONS['['+str(pcords[0])+', '+str(pcords[1])+']']:
                    #                     if i in available_positions:                            
                    #                         positions_to_move.append(i)
                    #                         selected_tile_p11 = True
                    #             if (parse_coords(pos) in positions_to_move and self.state.turn % 2 == 0 and selected_tile_p11):
                    #                 pcords2 = parse_coords(pos) 
                    #                 p1_tiles.append(pcords2)
                    #                 p1_tiles.remove(to_delate_position)
                    #                 available_positions.append(to_delate_position)
                    #                 available_positions.remove(pcords2)
                    #                 map_tiles.clear()
                    #                 rect_append = p1_img.get_rect(center = unparse_coords(pcords2))
                    #                 map_tiles.append((p1_img, rect_append))                                                          
                    #                 #ACTUALIZACION ESTADOS
                    #                 for i in lines_in_table_p1[:]:
                    #                     for j in i:
                    #                         if j == to_delate_position:
                    #                             lines_in_table_p1.remove(i) 
                    #                 selected_tile_p1 = False
                    #                 selected_tile_p11 = False                                    
                    #                 line_p1, lines = is_line(p1_tiles)
                    #                 self.state.turn  += 1
                    #             #P2
                    #             if (parse_coords(pos) in p2_tiles and self.state.turn % 2 != 0):
                    #                 positions_to_move = []
                    #                 pcords = parse_coords(pos)
                    #                 coord = unparse_coords(pcords) 
                    #                 selected_tile_p2 = True
                    #                 to_delate_position = pcords                                                      
                    #                 for i in const.BOARD_POSITIONS['['+str(pcords[0])+', '+str(pcords[1])+']']:
                    #                     if i in available_positions:                            
                    #                         positions_to_move.append(i)
                    #                         selected_tile_p22 = True
                    #             if (parse_coords(pos) in positions_to_move and self.state.turn % 2 != 0 and selected_tile_p22):
                    #                 pcords2 = parse_coords(pos) 
                    #                 p2_tiles.append(pcords2)
                    #                 p2_tiles.remove(to_delate_position)
                    #                 available_positions.append(to_delate_position)
                    #                 available_positions.remove(pcords2)
                    #                 map_tiles.clear()
                    #                 rect_append = p2_img.get_rect(center = unparse_coords(pcords2))
                    #                 map_tiles.append((p2_img, rect_append))
                    #                 #ACTUALIZACION ESTADOS
                    #                 for i in lines_in_table_p2[:]:
                    #                     for j in i:
                    #                         if j == to_delate_position:
                    #                             lines_in_table_p2.remove(i)                                
                    #                 selected_tile_p2 = False
                    #                 selected_tile_p22 = False
                    #                 line_p2, lines = is_line(p2_tiles)
                    #                 self.state.turn  += 1                                    
                    #     else:
                    #         if(line_p1):
                    #             if(parse_coords(pos) in p2_tiles_to_eliminate):
                    #                 pcords = parse_coords(pos)
                    #                 p2_tiles.remove(pcords)
                    #                 available_positions.append(pcords)
                    #                 map_tiles.clear()
                    #                 #ACTUALIZAR ESTADOS
                    #                 for i in lines_in_table_p2[:]:
                    #                     for j in i:
                    #                         if j == pcords:
                    #                             lines_in_table_p2.remove(i)
                    #                 lines_in_table_p1.append(lines)
                    #                 line_p1 = False
                    #                 line = False
                    #         if(line_p2):
                    #             if(parse_coords(pos) in p1_tiles_to_eliminate):
                    #                 pcords = parse_coords(pos)
                    #                 p1_tiles.remove(pcords)
                    #                 available_positions.append(pcords)
                    #                 map_tiles.clear()
                    #                 #ACTUALIZAR ESTADOS
                    #                 for i in lines_in_table_p1[:]:
                    #                     for j in i:
                    #                         if j == pcords:
                    #                             lines_in_table_p1.remove(i)
                    #                 lines_in_table_p2.append(lines)
                    #                 line_p2 = False
                    #                 line = False
                    # #TABLAS
                    # if (pos[0] > const.WIDTH-65 and pos[0] < const.WIDTH and pos[1] > 0 and pos[1] < 65):
                    #     tablas.append(self.state.turn)                                            
                #KEYBOARD
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    elif event.key == K_s:
                        saved_state = State(p1_tiles, p2_tiles, self.state.p1_n_tiles, self.state.p2_n_tiles, self.state.turn , self.state.game_state)
                        saved_state.save_state()
                        print("State saved")
                    elif event.key == K_r:
                        tablero_img = pygame.image.load(const.BOARD)
                        tablero_img = pygame.transform.scale(tablero_img,(const.WIDTH, const.HEIGHT))
                        map_tiles.clear()
                        p1_tiles.clear()
                        p2_tiles.clear()
                        p1_tiles, p2_tiles, self.state.turn  = saved_state.load_state()
                        print("State loaded")
                elif event.type == QUIT:
                    running = False
                    print("Bye!")    

            #CIRCULOS VERDES EN ACCIONES DISPONIBLES
            if not line:
                if self.state.turn % 2 == 0:
                    if self.state.p1_n_tiles != 0 or (selected_tile_p1 and len(self.state.p1_positions) == 3):
                        for av_pos in available_positions:
                            rect = available_pos_img.get_rect(center = unparse_coords(av_pos))
                            green_positions.append((available_pos_img, rect))
                    elif not selected_tile_p1:
                        for p1_pos in self.state.p1_positions:
                            rect = selected_pos_green_img.get_rect(center = unparse_coords(p1_pos))
                            green_positions.append((selected_pos_green_img, rect))                    
                    elif len(self.state.p1_positions) > 3:
                        for p1_pos in [
                            pos for pos in const.BOARD_POSITIONS[str(selected_tile_p1)] if pos not in \
                                (self.state.p1_positions + self.state.p2_positions)]:
                            rect = available_pos_img.get_rect(center = unparse_coords(av_pos))
                            green_positions.append((available_pos_img, rect))
                else:
                    if self.state.p2_n_tiles != 0 or (selected_tile_p2 and len(self.state.p2_positions) == 3):
                        for av_pos in available_positions:
                            rect = available_pos_img.get_rect(center = unparse_coords(av_pos))
                            green_positions.append((available_pos_img, rect))
                    elif not selected_tile_p2:
                        for p2_pos in self.state.p2_positions:
                            rect = selected_pos_green_img.get_rect(center = unparse_coords(p2_pos))
                            green_positions.append((selected_pos_green_img, rect))                    
                    elif len(self.state.p2_positions) > 3:
                        for p2_pos in [
                            pos for pos in const.BOARD_POSITIONS[str(selected_tile_p2)] if pos not in \
                                (self.state.p1_positions + self.state.p2_positions)]:
                            rect = available_pos_img.get_rect(center = unparse_coords(av_pos))
                            green_positions.append((available_pos_img, rect))


            # SI ES LINEA IMPLEMENTAR CIRCULOS ROJOS EN P2 POSITIONS


            # #HACER LINEA                        
            # if(line_p1):
            #     if lines in lines_in_table_p1:
            #         line_p1 = False
            #     else:
            #         line = True
            #         window.blit(p1_img_scoreboard, (472,552))
            #         p2_tiles_to_eliminate = p2_tiles[:]
            #         for i in lines_in_table_p2[:]:
            #             for j in i:
            #                 if j in p2_tiles:
            #                     p2_tiles_to_eliminate.remove(j)
            #         for i in lines:
            #             ncord = selected_pos_green.get_rect(center = unparse_coords(i))
            #             window.blit(selected_pos_green, ncord)
            #         for j in p2_tiles_to_eliminate:
            #             ncord = selected_pos_green.get_rect(center = unparse_coords(j))
            #             window.blit(selected_pos_red, ncord)                    
            # if(line_p2):
            #     if lines in lines_in_table_p2:
            #         line_p2 = False
            #     else:
            #         line = True
            #         window.blit(p2_img_scoreboard, (472,552))
            #         p1_tiles_to_eliminate = p1_tiles[:]
            #         for i in lines_in_table_p1[:]:
            #             for j in i:
            #                 if j in p1_tiles:
            #                     p1_tiles_to_eliminate.remove(j)
            #         for i in lines:
            #             ncord = selected_pos_green.get_rect(center = unparse_coords(i))
            #             window.blit(selected_pos_green, ncord) 
            #         for j in p1_tiles_to_eliminate:
            #             ncord = selected_pos_green.get_rect(center = unparse_coords(j))
            #             window.blit(selected_pos_red, ncord)                            
                   
            #COLOCACIÓN DE FICHAS P1 Y P2
            for p1_tile in p1_tiles:
                rect = p1_img.get_rect(center = unparse_coords(p1_tile))
                map_tiles.append((p1_img, rect))
            
            for p2_tile in p2_tiles:
                rect = p2_img.get_rect(center = unparse_coords(p2_tile))
                map_tiles.append((p2_img, rect))

            #PANTALLAS        
            if(len(tablas)==2):
                if(tablas[0]==tablas[1]):
                    window.blit(tablas_img, (0,0))
                else:
                    tablasP1 = False
                    tablasP2 = False
                    tablas.clear()
            self.state.endgame()
            if (self.state.game_state == "P1 WINS"):
                window.blit(p1_wins_img, (0,0))
                map_tiles.clear()
            if (self.state.game_state == "P2 WINS"):
                window.blit(p2_wins_img, (0,0))
                map_tiles.clear()
            pygame.display.update()
        pygame.quit()

graphics = Graphics()
graphics.game()


