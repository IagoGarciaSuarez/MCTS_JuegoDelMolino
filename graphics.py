import pygame
import numpy as np
from pygame.locals import (
    K_ESCAPE,
    K_s,
    K_r,
    KEYDOWN,
    QUIT,
)
import const
import json
from utils import parse_coords, scale_img, unparse_coords
from state import State

class Graphics:
    
    def __init__(self, state = State):
        self.state = state

    def main():
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(const.MUSIC)
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)

        clock = pygame.time.Clock()

        window = pygame.display.set_mode((const.WIDTH, const.HEIGHT))
        pygame.display.set_caption('Juego del Molino')
        pygame.display.set_icon(pygame.image.load(const.LOGO))

        bg_img = pygame.image.load(const.BOARD)
        bg_img = pygame.transform.scale(bg_img,(const.WIDTH, const.HEIGHT))

        map_tiles = []
        p1_tiles = state.p1_positions
        p2_tiles = state.p2_positions
        p1_n_tiles = state.p1_n_tiles
        p2_n_tiles = state.p2_n_tiles
        turn = state.turn
        state_num = 0
        last_state = None

        #Button
        smallfont = pygame.font.SysFont('Corbel',35)
        text = smallfont.render('Save' , True , (255,255,255))

        positions = np.concatenate(p1_tiles, p2_tiles)
        running = True
        while running:
            window.blit(bg_img, (0,0))
            window.blits(map_tiles)
            clock.tick(15)
            #TABLE LINES
            #UP
            #pygame.draw.line(window, (255, 0, 0), (111, 60), (const.WIDTH - 111, 60))
            #DOWN
            #pygame.draw.line(window, (255, 0, 0), (111, const.HEIGHT-60), (const.WIDTH-111, const.HEIGHT-60))
            #LEFT
            #pygame.draw.line(window, (255, 0, 0), (111, 60), (111, const.HEIGHT-60))
            #RIGHT
            #pygame.draw.line(window, (255, 0, 0), (const.WIDTH - 111, 60), (const.WIDTH-111, const.HEIGHT-60))

            #for i in range(1, 7):
                #COLUMNS
                #pygame.draw.line(window, (255, 0, 0), (111 + const.BLOCKSIZE*i, 60), (const.BLOCKSIZE*i+111, const.HEIGHT-60))
                #ROWS
                #pygame.draw.line(window, (255, 0, 0), (111, 68 + const.BLOCKSIZE*i), (const.HEIGHT-15, const.BLOCKSIZE*i+68))

            mill_p1_img = scale_img("assets/image/P1.png", (const.BLOCKSIZE - 10, const.BLOCKSIZE - 10))
            mill_p2_img = scale_img("assets/image/P2.png", (const.BLOCKSIZE - 10, const.BLOCKSIZE - 10))

            saved_state = State(state_num, p1_tiles, p2_tiles, 0, 0, turn)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    if not (pos[0] < 111 or pos[1] < 61 or pos[0] > const.HEIGHT - 15 or pos[1] > const.WIDTH - 164):
                        if(parse_coords(pos) in const.VALID_POSITIONS and parse_coords(pos) not in positions):
                            pcords = parse_coords(pos)
                            positions.append(pcords)
                            print(positions)
                            if turn == 1:
                                p1_tiles.append(pcords)
                            if turn == -1:
                                p2_tiles.append(pcords)
                            turn *= -1
                            saved_state = State(state_num, p1_tiles, p2_tiles, p1_n_tiles, p2_n_tiles, turn)
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

            for p1_tile in p1_tiles:
                rect = mill_p1_img.get_rect(center = unparse_coords(p1_tile))
                map_tiles.append((mill_p1_img, rect))
            
            for p2_tile in p2_tiles:
                rect = mill_p2_img.get_rect(center = unparse_coords(p2_tile))
                map_tiles.append((mill_p2_img, rect))

            #window.blits()
            pygame.display.update()
            return saved_state
        pygame.quit()

    if __name__ == '__main__':
        main()