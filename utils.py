import const
import pygame

def parse_coords(coords):
	return [int((coords[0] - 25)/const.BLOCKSIZE), int((coords[1] - 25)/const.BLOCKSIZE)]

def unparse_coords(coords):
    return [coords[0]*const.BLOCKSIZE + 25 + const.BLOCKSIZE*0.5, coords[1]*const.BLOCKSIZE + 25 + const.BLOCKSIZE*0.5]

def scale_img(route, size):
	img = pygame.image.load(route)
	img = pygame.transform.scale(img, size)
	return img