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

def is_line(positions: List):
        #COLUMNAS
        if ([0,0] in positions and [0,3] in positions and [0,6] in positions):
            return True, [[0,0],[0,3],[0,6]]
        elif([1,1] in positions and [1,3] in positions and [1,5] in positions):
            return True, [[1,1],[1,3],[1,5]]
        elif([2,2] in positions and [2,3] in positions and [2,4] in positions):
            return True, [[2,2],[2,3],[2,4]] 
        elif([3,0] in positions and [3,1] in positions and [3,2] in positions):
            return True, [[3,0],[3,1],[3,2]]
        elif([3,4] in positions and [3,5] in positions and [3,6] in positions):
            return True, [[3,4],[3,5],[3,6]] 
        elif([4,2] in positions and [4,3] in positions and [4,4] in positions):
            return True, [[4,2],[4,3],[4,4]]
        elif([5,1] in positions and [5,3] in positions and [5,5] in positions):
            return True, [[5,1],[5,3],[5,5]]
        elif([6,0] in positions and [6,3] in positions and [6,6] in positions):
            return True, [[6,0],[6,3],[6,6]]
        #FILAS
        elif ([0,0] in positions and [3,0] in positions and [6,0] in positions):
            return True, [[0,0],[3,0],[6,0]]
        elif([1,1] in positions and [3,1] in positions and [5,1] in positions):
            return True, [[1,1],[3,1],[5,1]]
        elif([2,2] in positions and [3,2] in positions and [4,2] in positions):
            return True, [[2,2],[3,2],[4,2]]
        elif([0,3] in positions and [1,3] in positions and [2,3] in positions):
            return True, [[0,3],[1,3],[2,3]]
        elif([4,3] in positions and [5,3] in positions and [6,3] in positions):
            return True, [[4,3],[5,3],[6,3]]
        elif([2,4] in positions and [3,4] in positions and [4,4] in positions):
            return True, [[2,4],[3,4],[4,4]]
        elif([1,5] in positions and [3,5] in positions and [5,5] in positions):
            return True, [[1,5],[3,5],[5,5]]
        elif([0,6] in positions and [3,6] in positions and [6,6] in positions):
            return True, [[0,6],[3,6],[6,6]]
        else: return False, []

# def save_game(game_data, games_db=const.GAMES_JSON):
# 	games = read_games()
# 	games.update(game_data)
# 	with open(const.DATABASES_DIR + games_db, 'w') as game_f:
# 		json.dump(games, game_f)

# def read_games(games_db=const.GAMES_JSON):
# 	with open(const.DATABASES_DIR + games_db, 'r') as game_f:
# 		games_data = json.load(game_f)
# 	return games_data
