import pygame
from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
import const

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

    running = True
    while running:
        clock.tick(15)
        window.blit(bg_img, (0,0))
        pygame.draw.line(window, (255, 0, 0), (25, 25), (25, const.HEIGHT-25))
        pygame.draw.line(window, (255, 0, 0), (25, const.HEIGHT-25), (const.WIDTH-25, const.HEIGHT-25))
        pygame.draw.line(window, (255, 0, 0), (25, 25), (const.WIDTH - 25, 25))
        pygame.draw.line(window, (255, 0, 0), (const.WIDTH - 25, 25), (const.WIDTH-25, const.HEIGHT-25))

        for i in range(1, 7):
            pygame.draw.line(window, (255, 0, 0), (25 + const.BLOCKSIZE*i, 0), (const.BLOCKSIZE*i+25, const.HEIGHT))
            pygame.draw.line(window, (255, 0, 0), (0, 25 + const.BLOCKSIZE*i), (const.HEIGHT, const.BLOCKSIZE*i+25))

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                print(pos)
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False
            elif event.type == QUIT:
                running = False
        pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    main()