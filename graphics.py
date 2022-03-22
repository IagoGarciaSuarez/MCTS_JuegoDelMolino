from utils import parse_coords, scale_img, unparse_coords
from state import State
import numpy as np
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
        bg_img = pygame.image.load(const.BOARD)
        bg_img = pygame.transform.scale(bg_img,(const.WIDTH, const.HEIGHT))
        p1_img_scoreboard = pygame.image.load(const.P1_TILE_IMG)
        p2_img_scoreboard = pygame.image.load(const.P2_TILE_IMG)
        p1_img  = scale_img(const.P1_TILE_IMG, (const.BLOCKSIZE - 10, const.BLOCKSIZE - 10))
        p2_img = scale_img(const.P2_TILE_IMG, (const.BLOCKSIZE - 10, const.BLOCKSIZE - 10))
        available_pos = pygame.image.load(const.AVAILABLE_POSITION)
        selected_pos_green = scale_img(const.SELECTED_POSITION_GREEN, (const.BLOCKSIZE - 10, const.BLOCKSIZE - 10))
        selected_pos_red = scale_img(const.SELECTED_POSITION_RED, (const.BLOCKSIZE - 10, const.BLOCKSIZE - 10))

        #VARIABLES
        map_tiles = []
        p1_tiles = []
        p2_tiles = []
        p1_n_tiles = 9
        p2_n_tiles = 9
        turn = 1
        state_num = 0
        game_state = ""

        # map_tiles = []
        p1_tiles = self.state.p1_positions
        # p2_tiles = state.p2_positions
        # p1_n_tiles = 9
        # p2_n_tiles = 9
        # turn = 1
        # state_num = 0
        # game_state = ""
                
        positions = []
        positions = positions + p1_tiles + p2_tiles  #POSICIONES DE TODAS LAS FICHAS EN EL TABLERO
        available_positions = const.VALID_POSITIONS  #POSICIONES SIN OCUPAR EN EL TABLERO
        running = True
        selectedTailP1 = False

        while running:
            #TABLERO
            window.blit(bg_img, (0,0))
            #FICHAS
            window.blits(map_tiles)
            #MARCADORES
            scoreboard_p1_tiles = font.render(str(p1_n_tiles), 1, (255, 255, 255))
            window.blit(scoreboard_p1_tiles, (45,225))  
            scoreboard_p2_tiles = font.render(str(p2_n_tiles), 1, (255, 255, 255))          
            window.blit(scoreboard_p2_tiles, (const.WIDTH-65,225))
            scoreboard_p1_dead_tiles = font.render(str(9-p1_n_tiles-len(p1_tiles)), 1, (255, 255, 255))
            window.blit(scoreboard_p1_dead_tiles, (45,415))
            scoreboard_p2_dead_tiles = font.render(str(9-p2_n_tiles-len(p2_tiles)), 1, (255, 255, 255))
            window.blit(scoreboard_p2_dead_tiles, (const.WIDTH-65,415)) 
            #TURNO
            if(turn==1):
                window.blit(p1_img_scoreboard, (472,552))
            else: 
                window.blit(p2_img_scoreboard, (472,552))

            #MOUSE O KEYBOARD
            saved_state = State(state_num, p1_tiles, p2_tiles, 0, 0, turn)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    if not (pos[0] < 111 or pos[1] < 61 or pos[0] > const.HEIGHT - 15 or pos[1] > const.WIDTH - 164):
                        if (p1_n_tiles != 0) or (p2_n_tiles != 0):
                            if(parse_coords(pos) in const.VALID_POSITIONS and parse_coords(pos) not in positions):
                                pcords = parse_coords(pos)
                                positions.append(pcords)
                                print(positions)
                                if turn == 1:
                                    p1_tiles.append(pcords)
                                    available_positions.remove(pcords)
                                    p1_n_tiles -= 1
                                if turn == -1:
                                    p2_tiles.append(pcords)
                                    available_positions.remove(pcords)
                                    p2_n_tiles -= 1
                                turn *= -1
                                #running = False
                                saved_state = State(state_num, p1_tiles, p2_tiles, p1_n_tiles, p2_n_tiles, turn, game_state)
                                #return saved_state
                        else: 
                            if(parse_coords(pos) in const.VALID_POSITIONS):                          
                                if turn == 1:
                                    selectedTailP1 = True    
                                if turn == -1:
                                    print("por implementar")
                    if (pos[0] > const.WIDTH-65 and pos[0] < const.WIDTH and pos[1] > 0 and pos[1] < 65):
                        print("Tablas")
                        saved_state = State(state_num, p1_tiles, p2_tiles, p1_n_tiles, p2_n_tiles, turn, "Tablas")

                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    elif event.key == K_s:
                        saved_state.save_state()
                        state_num += 1
                        print("State saved")
                    elif event.key == K_r:
                        bg_img = pygame.image.load(const.BOARD)
                        bg_img = pygame.transform.scale(bg_img,(const.WIDTH, const.HEIGHT))
                        map_tiles.clear()
                        p1_tiles.clear()
                        p2_tiles.clear()
                        p1_tiles, p2_tiles, turn = saved_state.load_state()
                        print("State loaded")
                elif event.type == QUIT:
                    running = False
                    print("Bye!")

            #FICHAS POR COLOCAR
            if (p1_n_tiles != 0) or (p2_n_tiles != 0):
                for i in available_positions:
                    coords = unparse_coords(i)
                    window.blit(available_pos, coords)

            #FICHAS YA COLOCADAS
            if(selectedTailP1):
                if(parse_coords(pos) in p1_tiles):
                    no_options_position = True
                    pcords = parse_coords(pos)
                    coord = unparse_coords(pcords) 
                    window.blit(selected_pos_green, coord)                 
                    for i in const.BOARD_POSITIONS['['+str(pcords[0])+', '+str(pcords[1])+']']:
                        if i in available_positions:
                            coords = unparse_coords(i)
                            window.blit(available_pos, coords)
                            no_options_position = False
                        elif(no_options_position):
                            window.blit(selected_pos_red, coord)
                            no_options_position = False  

            #COLOCACIÓN DE FICHAS                
            for p1_tile in p1_tiles:
                rect = p1_img.get_rect(center = unparse_coords(p1_tile))
                map_tiles.append((p1_img, rect))
            
            for p2_tile in p2_tiles:
                rect = p2_img.get_rect(center = unparse_coords(p2_tile))
                map_tiles.append((p2_img, rect))

            pygame.display.update()            
            #return saved_state
        pygame.quit()

    # if __name__ == '__main__':
    #     main()


state = State(1,[],[],9,9,1,"prueba")
graphics = Graphics(state)
graphics.game()