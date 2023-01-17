from flask import json

from tetris.utils.variables import Configs


# class for a Tetromino
class Tetrominoe:

    # creates a new tetromino with the given type and rotation as well as the appropriate matrix
    def __init__(self, type, rotation):
        self.tetromino = Configs.tetrominoes[type][rotation]
        self.type = type
        self.rotation = rotation

    # returns the tetromino matrix
    def get_matrix(self):
        return self.tetromino

    # gets the type of this tetromino
    def get_type(self):
        return self.type

    # gets the current rotation of this tetromino
    def get_rotation(self):
        return self.rotation

    # transforms the tetromino to the new type and rotation
    def transform_tetromino(self, type, rotation):
        self.tetromino = Configs.tetrominoes[type][rotation]
        self.type = type
        self.rotation = rotation
        return self

    def to_json(self):
        dic = {}
        for attr in vars(self):
            attr_value = getattr(self, attr)
            dic[attr] = attr_value
        return dic
