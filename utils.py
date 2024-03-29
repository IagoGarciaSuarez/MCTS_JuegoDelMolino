import const
import hashlib
import pygame
import json
from typing import List

def parse_coords(coords):
	return [int((coords[0] - 111)/const.BLOCKSIZE), int((coords[1] - 61)/const.BLOCKSIZE)]

def unparse_coords(coords):
    return [coords[0]*const.BLOCKSIZE + 105 + const.BLOCKSIZE*0.5, coords[1]*const.BLOCKSIZE + 50 + const.BLOCKSIZE*0.5]

def scale_img(route, size):
	img = pygame.image.load(route)
	img = pygame.transform.scale(img, size)
	return img

def get_password_sha256(password):
    '''Genera el sha256 de una password.'''
    return hashlib.sha256(password.encode('utf-8')).hexdigest()