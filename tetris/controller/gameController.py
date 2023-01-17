# controller for a game of Tetris
import time

from enum import IntEnum


class MoveEnum(IntEnum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    PAUSE = 4
    QUIT = 5
    RETRY = 6


class GameController:

    # initialize the game controller
    def __init__(self, gameboard, sidebar):
        self.playing = True
        self.gameboard = gameboard
        self.sidebar = sidebar
        self.lastMove = 0
        self.speed = 0

    def event_performed(self, event_type):
        match event_type:
            case MoveEnum.PAUSE:
                self.gameboard.pause()
            case MoveEnum.RETRY:
                self.gameboard.new_game()
            case MoveEnum.QUIT:
                self.gameboard.pause()
            case MoveEnum.DOWN:
                while self.gameboard.can_move("down"):
                    ms = time.time() * 1000
                    if ms > self.lastMove + 5:
                        self.lastMove = ms
                        self.gameboard.move_in_direction("down")
            case MoveEnum.UP:
                self.gameboard.rotate_active("right")
            case MoveEnum.LEFT:
                self.gameboard.move_in_direction("left")
            case MoveEnum.RIGHT:
                self.gameboard.move_in_direction("right")

    # plays the game of tetris
    def play_game(self, callbak):
        while self.playing:
            if not self.gameboard.paused and not self.gameboard.is_game_over():
                # moving the tetris piece
                ms = time.time() * 1000
                if ms > self.lastMove + 500:
                    self.gameboard.move_in_direction("down")
                    self.lastMove = ms

                if self.gameboard.needs_tetromino():
                    self.gameboard.set_active(self.sidebar.update())
            if callbak is not None and callable(callbak):
                callbak()
            time.sleep(0.2)

    def descent(self):
        while self.gameboard.can_move("down"):
            ms = time.time() * 1000
            if ms > self.lastMove + 5:
                self.lastMove = ms
                self.gameboard.move_in_direction("down")
