import pygame
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
    p1_tiles = []
    p2_tiles = []
    turn = 1
    nTurn = 1
    state_num = 0
    last_state = None

    #Button
    smallfont = pygame.font.SysFont('Corbel',35)
    text = smallfont.render('Save' , True , (255,255,255))

    running = True
    while running:
        window.blit(bg_img, (0,0))
        window.blits(map_tiles)
        clock.tick(15)
        #TABLE LINES
        #UP
        pygame.draw.line(window, (255, 0, 0), (25, 25), (const.WIDTH - 25, 25))
        #DOWN
        pygame.draw.line(window, (255, 0, 0), (25, const.HEIGHT-142), (const.WIDTH-25, const.HEIGHT-142))
        #LEFT
        pygame.draw.line(window, (255, 0, 0), (25, 25), (25, const.HEIGHT-142))
        #RIGHT
        pygame.draw.line(window, (255, 0, 0), (const.WIDTH - 25, 25), (const.WIDTH-25, const.HEIGHT-142))

        #BUTTONS LINES
        #UP
        pygame.draw.line(window, (255, 0, 0), (25, 562), (const.WIDTH - 25, 562))
        #DOWN
        pygame.draw.line(window, (255, 0, 0), (25, const.HEIGHT-5), (const.WIDTH-25, const.HEIGHT-5))
        #COLUMNS
        pygame.draw.line(window, (255, 0, 0), (25, 562), (25, const.HEIGHT-5))
        pygame.draw.line(window, (255, 0, 0), (195, 562), (195, const.HEIGHT-5))
        pygame.draw.line(window, (255, 0, 0), (380, 562), (380, const.HEIGHT-5))
        pygame.draw.line(window, (255, 0, 0), (const.WIDTH - 25, 562), (const.WIDTH-25, const.HEIGHT-5))

        for i in range(1, 7):
            #COLUMNS
            pygame.draw.line(window, (255, 0, 0), (25 + const.BLOCKSIZE*i, 25), (const.BLOCKSIZE*i+25, const.HEIGHT-142))
            #ROWS
            pygame.draw.line(window, (255, 0, 0), (25, 25 + const.BLOCKSIZE*i), (const.HEIGHT-125, const.BLOCKSIZE*i+25))

        mill_p1_img = scale_img("assets/image/mill_p1.png", (const.BLOCKSIZE - 10, const.BLOCKSIZE - 10))
        mill_p2_img = scale_img("assets/image/mill_p2.png", (const.BLOCKSIZE - 10, const.BLOCKSIZE - 10))

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if not (pos[0] < 25 or pos[1] < 25 or pos[0] > const.HEIGHT - 125 or pos[1] > const.WIDTH - 25):
                    pcords = parse_coords(pos)
                    print(pcords)
                    if turn == 1:
                        p1_tiles.append(pcords)
                    if turn == -1:
                        p2_tiles.append(pcords)
                    turn *= -1
                if (pos[0] > 25 and pos[0] < 195 and pos[1] > 562 and pos[1] < const.HEIGHT-5):
                    savedState = State(state_num, p1_tiles, p2_tiles, 0, 0, nTurn)
                    savedState.save_state()
                    state_num += 1
                    nTurn += 1
                    print("State saved")
                if (pos[0] > 195 and pos[0] < 380 and pos[1] > 562 and pos[1] < const.HEIGHT-5):
                    bg_img = pygame.image.load(const.BOARD)
                    bg_img = pygame.transform.scale(bg_img,(const.WIDTH, const.HEIGHT))
                    map_tiles.clear()
                    p1_tiles.clear()
                    p2_tiles.clear()
                    p1_tiles, p2_tiles, turn = savedState.load_state()
                    print("State loaded")
                if (pos[0] > 380 and pos[0] < const.WIDTH - 25 and pos[1] > 562 and pos[1] < const.HEIGHT-5):
                    map_tiles.clear()
                    p1_tiles.clear()
                    p2_tiles.clear()
                    print("Emptied board")
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                elif event.key == K_s:
                    savedState = State(state_num, p1_tiles, p2_tiles, 0, 0, turn)
                    savedState.save_state()
                    state_num += 1
                    print("State saved")
                elif event.key == K_r:
                    bg_img = pygame.image.load(const.BOARD)
                    bg_img = pygame.transform.scale(bg_img,(const.WIDTH, const.HEIGHT))
                    map_tiles.clear()
                    p1_tiles.clear()
                    p2_tiles.clear()
                    p1_tiles, p2_tiles, turn = savedState.load_state()
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
    pygame.quit()

if __name__ == '__main__':
    main()