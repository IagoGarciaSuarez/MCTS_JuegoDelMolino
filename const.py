WIDTH = 700
HEIGHT = 600
BOARD = 'assets/image/BOARD.png'
MUSIC = 'assets/audio/bg_music.mp3'
P1_TILE_IMG = 'assets/image/P1.png'
P2_TILE_IMG = 'assets/image/P2.png'
AVAILABLE_POSITION = 'assets/image/CIRCULO_VERDE.png'
NO_AVAILABLE_POSITION = 'assets/image/CIRCULO_ROJO.png'
SELECTED_POSITION_GREEN = 'assets/image/SELECCION_VERDE.png'
SELECTED_POSITION_RED = 'assets/image/SELECCION_ROJA.png'
STATES_JSON = 'persistence/saved_state.json'
LOGS_DIR = 'logs/'
DATABASES_DIR = 'data/'
GAMES_JSON = 'games.json'
LOGO = 'assets/image/LOGO.png'
BLOCKSIZE = 69
BOARD_POSITIONS = {
    "[0, 0]": [[3, 0], [0, 3]],
    "[3, 0]": [[0, 0], [3, 1], [6, 0]],
    "[6, 0]": [[3, 0], [6, 3]],
    "[1, 1]": [[3, 1], [1, 3]],
    "[3, 1]": [[3, 0], [1, 1], [3, 2], [5, 1]],
    "[5, 1]": [[3, 1], [5, 3]],
    "[2, 2]": [[2, 3], [3, 2]],
    "[3, 2]": [[3, 1], [2, 2], [4, 2]],
    "[4, 2]": [[3, 2], [4, 3]],
    "[0, 3]": [[0, 0], [0, 6], [1, 3]],
    "[1, 3]": [[1, 1], [0, 3], [1, 5], [2, 3]],
    "[2, 3]": [[2, 2], [1, 3], [2, 4]],
    "[4, 3]": [[4, 2], [4, 4], [5, 3]],
    "[5, 3]": [[5, 1], [4, 3], [5, 5], [6, 3]],
    "[6, 3]": [[6, 0], [5, 3], [6, 6]],
    "[2, 4]": [[2, 3], [3, 4]],
    "[3, 4]": [[2, 4], [3, 5], [4, 4]],
    "[4, 4]": [[4, 3], [3, 4]],
    "[1, 5]": [[1, 3], [3, 5]],
    "[3, 5]": [[3, 4], [1, 5], [3, 6], [5, 5]],
    "[5, 5]": [[5, 3], [3, 5]],
    "[0, 6]": [[0, 3], [3, 6]],
    "[3, 6]": [[3, 5], [0, 6], [6, 6]],
    "[6, 6]": [[6, 3], [3, 6]]
}
VALID_POSITIONS = [[0, 0],[3, 0],[6, 0],
[1, 1],[3, 1],[5, 1],
[2, 2],[3, 2],[4, 2],
[0, 3],[1, 3],[2, 3],[4, 3],[5, 3],[6, 3],
[2, 4],[3, 4],[4, 4],
[1, 5],[3, 5],[5, 5],
[0, 6],[3, 6],[6, 6]]
MAX_FICHAS = 9