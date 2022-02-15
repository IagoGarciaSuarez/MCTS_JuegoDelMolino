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
    j1_tiles = []
    j2_tiles = []
    turn = 1
    state_num = 0
    last_state = None

    running = True
    while running:
        window.blit(bg_img, (0,0))
        window.blits(map_tiles)
        clock.tick(15)
        pygame.draw.line(window, (255, 0, 0), (25, 25), (25, const.HEIGHT-25))
        pygame.draw.line(window, (255, 0, 0), (25, const.HEIGHT-25), (const.WIDTH-25, const.HEIGHT-25))
        pygame.draw.line(window, (255, 0, 0), (25, 25), (const.WIDTH - 25, 25))
        pygame.draw.line(window, (255, 0, 0), (const.WIDTH - 25, 25), (const.WIDTH-25, const.HEIGHT-25))

        for i in range(1, 7):
            pygame.draw.line(window, (255, 0, 0), (25 + const.BLOCKSIZE*i, 0), (const.BLOCKSIZE*i+25, const.HEIGHT))
            pygame.draw.line(window, (255, 0, 0), (0, 25 + const.BLOCKSIZE*i), (const.HEIGHT, const.BLOCKSIZE*i+25))

        molino_j1_img = scale_img("assets/image/molino_j1.png", (const.BLOCKSIZE - 10, const.BLOCKSIZE - 10))
        molino_j2_img = scale_img("assets/image/molino_j2.png", (const.BLOCKSIZE - 10, const.BLOCKSIZE - 10))

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if not (pos[0] < 25 or pos[1] < 25 or pos[0] > const.HEIGHT - 25 or pos[1] > const.WIDTH - 25):
                    pcords = parse_coords(pos)
                    print(pcords)
                    if turn == 1:
                        j1_tiles.append(pcords)
                    if turn == -1:
                        j2_tiles.append(pcords)
                    turn *= -1
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                elif event.key == K_s:
                    last_state = save_state(j1_tiles, j2_tiles, state_num)
                    state_num += 1
                elif event.key == K_r:
                    bg_img = pygame.image.load(const.BOARD)
                    bg_img = pygame.transform.scale(bg_img,(const.WIDTH, const.HEIGHT))
                    j1_tiles, j2_tiles = load_state(state_num)
            elif event.type == QUIT:
                running = False

        for j1_tile in j1_tiles:
            rect = molino_j1_img.get_rect(center = unparse_coords(j1_tile))
            map_tiles.append((molino_j1_img, rect))
        
        for j2_tile in j2_tiles:
            rect = molino_j2_img.get_rect(center = unparse_coords(j2_tile))
            map_tiles.append((molino_j2_img, rect))

        window.blits()
        pygame.display.update()
    pygame.quit()

def save_state(j1_tiles, j2_tiles, state_num):
    state_data = {"state": state_num, "j1": j1_tiles, "j2": j2_tiles}
    with open("states.json", "w") as states:
        json.dump(state_data, states)
    return state_data

def load_state(state_num):
    with open("states.json", "r") as states:
        state_info = json.load(states)
    return (state_info["j1"], state_info["j2"])
    

if __name__ == '__main__':
    main()