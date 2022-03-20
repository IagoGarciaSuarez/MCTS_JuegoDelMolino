import const
import hashlib
import pygame
import json

def parse_coords(coords):
	return [int((coords[0] - 111)/const.BLOCKSIZE), int((coords[1] - 61)/const.BLOCKSIZE)]

def unparse_coords(coords):
    return [coords[0]*const.BLOCKSIZE + 111 + const.BLOCKSIZE*0.5, coords[1]*const.BLOCKSIZE + 61 + const.BLOCKSIZE*0.5]

def scale_img(route, size):
	img = pygame.image.load(route)
	img = pygame.transform.scale(img, size)
	return img

def get_password_sha256(password):
    '''Genera el sha256 de una password.'''
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

# def save_game(game_data, games_db=const.GAMES_JSON):
# 	games = read_games()
# 	games.update(game_data)
# 	with open(const.DATABASES_DIR + games_db, 'w') as game_f:
# 		json.dump(games, game_f)

# def read_games(games_db=const.GAMES_JSON):
# 	with open(const.DATABASES_DIR + games_db, 'r') as game_f:
# 		games_data = json.load(game_f)
# 	return games_data
