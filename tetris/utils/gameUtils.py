import random
from tetris.model.tetrominoe import Tetrominoe
from tetris.utils.variables import Configs


# a class containing methods used across the game
def get_random_tetromino():
    type = random.randint(0, 6)
    orientation = random.randint(0, 3)
    return Tetrominoe(type, orientation)


def get_tetromino(type, rotation):
    return Configs.tetrominoes[type][rotation]


def new_row():
    row = []
    for c in range(Configs.columns):
        row.append(0)
    return row
