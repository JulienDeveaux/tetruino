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
                self.gameboard.newGame()
            case MoveEnum.QUIT:
                self.gameboard.pause()
            case MoveEnum.DOWN:
                while self.gameboard.canMove("down"):
                    ms = time.time() * 1000
                    if ms > self.lastMove + 5:
                        self.lastMove = ms
                        self.gameboard.moveInDirection("down")
            case MoveEnum.UP:
                self.gameboard.rotateActive("right")
            case MoveEnum.LEFT:
                self.gameboard.moveInDirection("left")
            case MoveEnum.RIGHT:
                self.gameboard.moveInDirection("right")

    # plays the game of tetris
    def playGame(self):
        while self.playing:
            if not self.gameboard.paused and not self.gameboard.isGameOver():
                # moving the tetris piece
                ms = time.time() * 1000
                if ms > self.lastMove + 110:
                    self.gameboard.moveInDirection("down")
                    self.lastMove = ms

                if self.gameboard.needsTetromino():
                    self.gameboard.setActive(self.sidebar.update())
            time.sleep(0.5)
