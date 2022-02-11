import const

def parse_coords(coords):
	return (int((coords[0] - 25)/const.BLOCKSIZE), int((coords[1] - 25)/const.BLOCKSIZE))