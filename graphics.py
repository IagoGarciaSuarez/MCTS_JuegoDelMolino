from typing import List
from movement import Movement
from utils import parse_coords, scale_img, unparse_coords, is_line
from state import State
import const
import pygame
from pygame.locals import *

class Graphics:

    def __init__(self, state: State = State(None)):
        self.state = state

    def game(self):
        #INICIO
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(const.MUSIC)
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)

        clock = pygame.time.Clock()

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
        available_pos = pygame.image.load(const.AVAILABLE_POSITION)
        selected_pos_green = scale_img(const.SELECTED_POSITION_GREEN, (const.BLOCKSIZE - 10, const.BLOCKSIZE - 10))
        selected_pos_red = scale_img(const.SELECTED_POSITION_RED, (const.BLOCKSIZE - 10, const.BLOCKSIZE - 10))

        #VARIABLES
        p1_tiles:List = self.state.p1_positions
        p2_tiles:List = self.state.p2_positions
        
        map_tiles = [] 
        positions:List = p1_tiles + p2_tiles  #POSICIONES DE TODAS LAS FICHAS EN EL TABLERO
        positions_to_move=[]
        available_positions = const.VALID_POSITIONS  #POSICIONES SIN OCUPAR EN EL TABLERO
        if(len(p1_tiles) > 0 or len(p2_tiles) > 0):
            for i in positions:
                available_positions.remove(i)
        running = True
        selectedTailP1 = False
        selectedTailP11 = False
        selectedTailP2 = False
        selectedTailP22 = False
        tablasP1 = False
        tablasP2 = False
        turnoTablasP1 = 1000
        turnoTablasP2 = 1000
        line = False #SI ES TRUE HAY UN 3 EN RAYA
        lineP1 = False #EL 3 EN RAYA ES DEL JUGADOR 1
        lineP2 = False #EL 3 EN RAYA ES DEL JUGADOR 2
        linesInTableP1 = []
        positions_to_killP1 = []
        linesInTableP2 = []

        while running:
            #TABLERO
            window.blit(tablero_img, (0,0))
            #FICHAS
            window.blits(map_tiles)
            #MARCADORES
            scoreboard_p1_tiles = font.render(str(self.state.p1_n_tiles), 1, (255, 255, 255))
            window.blit(scoreboard_p1_tiles, (45,225))  
            scoreboard_p2_tiles = font.render(str(self.state.p2_n_tiles), 1, (255, 255, 255))          
            window.blit(scoreboard_p2_tiles, (const.WIDTH-65,225))
            scoreboard_p1_dead_tiles = font.render(str(const.MAX_FICHAS-self.state.p1_n_tiles-len(p1_tiles)), 1, (255, 255, 255))
            window.blit(scoreboard_p1_dead_tiles, (45,415))
            scoreboard_p2_dead_tiles = font.render(str(const.MAX_FICHAS-self.state.p2_n_tiles-len(p2_tiles)), 1, (255, 255, 255))
            window.blit(scoreboard_p2_dead_tiles, (const.WIDTH-65,415)) 
            #TURNO
            if(self.state.turn % 2 == 0):
                window.blit(p1_img_scoreboard, (472,552))
            else: 
                window.blit(p2_img_scoreboard, (472,552))
            
            #MOUSE O KEYBOARD
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    if not (pos[0] < 111 or pos[1] < 61 or pos[0] > const.HEIGHT - 15 or pos[1] > const.WIDTH - 164):
                        if(line == False):
                            if (self.state.p1_n_tiles != 0) or (self.state.p2_n_tiles != 0):
                                if(parse_coords(pos) in available_positions):
                                    pcords = parse_coords(pos)
                                    #P1
                                    if self.state.turn % 2 == 0:
                                        p1_tiles.append(pcords)
                                        available_positions.remove(pcords)
                                        self.state.p1_n_tiles -= 1
                                        lineP1, lines = is_line(p1_tiles)
                                    #P2
                                    if self.state.turn % 2 != 0:
                                        p2_tiles.append(pcords)
                                        available_positions.remove(pcords)
                                        self.state.p2_n_tiles -= 1
                                        lineP2, lines = is_line(p2_tiles)
                                    self.state.turn  += 1
                            else:                            
                                #P1
                                if(parse_coords(pos) in p1_tiles and self.state.turn % 2 == 0): 
                                    positions_to_move = []
                                    pcords = parse_coords(pos)
                                    coord = unparse_coords(pcords) 
                                    selectedTailP1 = True
                                    toDelatePosition = pcords                                                     
                                    for i in const.BOARD_POSITIONS['['+str(pcords[0])+', '+str(pcords[1])+']']:
                                        if i in available_positions:                            
                                            positions_to_move.append(i)
                                            selectedTailP11 = True
                                if (parse_coords(pos) in positions_to_move and self.state.turn % 2 == 0 and selectedTailP11):
                                    pcords2 = parse_coords(pos) 
                                    p1_tiles.append(pcords2)
                                    p1_tiles.remove(toDelatePosition)
                                    available_positions.append(toDelatePosition)
                                    available_positions.remove(pcords2)
                                    map_tiles.clear()
                                    rectAppend = p1_img.get_rect(center = unparse_coords(pcords2))
                                    map_tiles.append((p1_img, rectAppend))                                                          
                                    #ACTUALIZACION ESTADOS
                                    selectedTailP1 = False
                                    selectedTailP11 = False                                    
                                    lineP1, lines = is_line(p1_tiles)
                                    self.state.turn  += 1
                                #P2
                                if (parse_coords(pos) in p2_tiles and self.state.turn % 2 != 0):
                                    positions_to_move = []
                                    pcords = parse_coords(pos)
                                    coord = unparse_coords(pcords) 
                                    selectedTailP2 = True
                                    toDelatePosition = pcords                                                      
                                    for i in const.BOARD_POSITIONS['['+str(pcords[0])+', '+str(pcords[1])+']']:
                                        if i in available_positions:                            
                                            positions_to_move.append(i)
                                            selectedTailP22 = True
                                if (parse_coords(pos) in positions_to_move and self.state.turn % 2 != 0 and selectedTailP22):
                                    pcords2 = parse_coords(pos) 
                                    p2_tiles.append(pcords2)
                                    p2_tiles.remove(toDelatePosition)
                                    available_positions.append(toDelatePosition)
                                    available_positions.remove(pcords2)
                                    map_tiles.clear()
                                    rectAppend = p2_img.get_rect(center = unparse_coords(pcords2))
                                    map_tiles.append((p2_img, rectAppend))
                                    #ACTUALIZACION ESTADOS                                
                                    selectedTailP2 = False
                                    selectedTailP22 = False
                                    lineP2, lines = is_line(p2_tiles)
                                    self.state.turn  += 1                                    
                        else:
                            if(lineP1):
                                if(parse_coords(pos) in p2_tiles_to_eliminate):
                                    pcords = parse_coords(pos)
                                    p2_tiles.remove(pcords)
                                    available_positions.append(pcords)
                                    map_tiles.clear()
                                    #ACTUALIZAR ESTADOS
                                    for i in linesInTableP2[:]:
                                        for j in i:
                                            if j == pcords:
                                                linesInTableP2.remove(i)
                                    linesInTableP1.append(lines)
                                    lineP1 = False
                                    line = False
                            if(lineP2):
                                if(parse_coords(pos) in p1_tiles_to_eliminate):
                                    pcords = parse_coords(pos)
                                    p1_tiles.remove(pcords)
                                    available_positions.append(pcords)
                                    map_tiles.clear()
                                    #ACTUALIZAR ESTADOS
                                    for i in linesInTableP1[:]:
                                        for j in i:
                                            if j == pcords:
                                                linesInTableP1.remove(i)
                                    linesInTableP2.append(lines)
                                    lineP2 = False
                                    line = False

                    if (pos[0] > const.WIDTH-65 and pos[0] < const.WIDTH and pos[1] > 0 and pos[1] < 65):
                        print("tablas")
                        
                        # #P1
                        # if self.state.turn % 2 == 0:
                        #     print("Jugador 1 solicita tablas")
                        #     tablasP1 = True 
                        #     turnoTablasP1 = self.state.turn                           
                        # #P2
                        # if self.state.turn % 2 != 0:
                        #     print("Jugador 2 solicita tablas")
                        #     tablasP2 = True
                        #     turnoTablasP2 = self.state.turn  
                        # self.state.turn  += 1                       

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

            #FICHAS POR COLOCAR
            if(line == False):
                if (self.state.p1_n_tiles != 0) or (self.state.p2_n_tiles != 0):
                    for i in available_positions:
                        coords = unparse_coords(i)
                        window.blit(available_pos, coords)
                elif(selectedTailP1):
                    if positions_to_move:
                        ncord = selected_pos_green.get_rect(center = coord)
                        window.blit(selected_pos_green, ncord)                
                        for i in positions_to_move:                            
                            coords = unparse_coords(i)
                            window.blit(available_pos, coords)
                    else:
                        ncord = selected_pos_red.get_rect(center = coord)
                        window.blit(selected_pos_red, ncord)
                elif(selectedTailP2):
                    if positions_to_move:
                        ncord = selected_pos_green.get_rect(center = coord)
                        window.blit(selected_pos_green, ncord)                
                        for i in positions_to_move:                            
                            coords = unparse_coords(i)
                            window.blit(available_pos, coords)
                    else:
                        ncord = selected_pos_red.get_rect(center = coord)
                        window.blit(selected_pos_red, ncord)

            #HACER LINEA                        
            if(lineP1):
                if lines in linesInTableP1:
                    lineP1 = False
                else:
                    line = True
                    window.blit(p1_img_scoreboard, (472,552))
                    p2_tiles_to_eliminate = p2_tiles[:]
                    for i in linesInTableP2[:]:
                        for j in i:
                            if j in p2_tiles:
                                p2_tiles_to_eliminate.remove(j)
                    for i in lines:
                        ncord = selected_pos_green.get_rect(center = unparse_coords(i))
                        window.blit(selected_pos_green, ncord)
                    for j in p2_tiles_to_eliminate:
                        ncord = selected_pos_green.get_rect(center = unparse_coords(j))
                        window.blit(selected_pos_red, ncord)                    
            if(lineP2):
                if lines in linesInTableP2:
                    lineP2 = False
                else:
                    line = True
                    window.blit(p2_img_scoreboard, (472,552))
                    p1_tiles_to_eliminate = p1_tiles[:]
                    for i in linesInTableP1[:]:
                        for j in i:
                            if j in p1_tiles:
                                p1_tiles_to_eliminate.remove(j)
                    for i in lines:
                        ncord = selected_pos_green.get_rect(center = unparse_coords(i))
                        window.blit(selected_pos_green, ncord) 
                    for j in p1_tiles_to_eliminate:
                        ncord = selected_pos_green.get_rect(center = unparse_coords(j))
                        window.blit(selected_pos_red, ncord)
                            
                   
            #COLOCACIÓN DE FICHAS P1 Y P2
            for p1_tile in p1_tiles:
                rect = p1_img.get_rect(center = unparse_coords(p1_tile))
                map_tiles.append((p1_img, rect))
            
            for p2_tile in p2_tiles:
                rect = p2_img.get_rect(center = unparse_coords(p2_tile))
                map_tiles.append((p2_img, rect))

            # #PANTALLAS
            # if(tablasP1 and tablasP2):
            #     if(abs(turnoTablasP1-turnoTablasP2) == 1):
            #         self.state.game_state = "Tablas"
            #         window.blit(tablas_img, (0,0))
            #         map_tiles.clear()
            #         p1_tiles.clear()
            #         p2_tiles.clear()
            #     else:
            #         tablasP1 = False
            #         tablasP2 = False
            #         turnoTablasP1 = 1000
            #         turnoTablasP2 = 1000
            # if (self.state.game_state == "P1 WINS"):
            #     window.blit(p1_wins_img, (0,0))
            #     map_tiles.clear()
            #     p1_tiles.clear()
            #     p2_tiles.clear()
            # if (self.state.game_state == "P2 WINS"):
            #     window.blit(p2_wins_img, (0,0))
            #     map_tiles.clear()
            #     p1_tiles.clear()
            #     p2_tiles.clear()
            pygame.display.update()
        pygame.quit()
        print(p1_tiles)
        print(p2_tiles)

state = State(1,[[2, 4], [0, 0], [6, 3], [4, 3], [3, 0], [5, 5], [4, 2], [6, 6], [1, 5]],[[2, 3], [6, 0], [3, 6], [3, 1], [0, 3], [0, 6], [5, 1], [1, 1], [1, 3]],0,0,0,"Prueba")
state1 = State(1,[[0,0],[1,0],[3,0]],[],9,2,0,"Prueba")
graphics = Graphics()
graphics.game()


