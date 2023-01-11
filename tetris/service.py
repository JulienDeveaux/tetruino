import threading

from tetris.model.gameboard import Gameboard
from tetris.model.sidebar import Sidebar
from tetris.controller.gameController import GameController
from tetris.utils.enums.difficulty import Difficulty
from tetris.utils.variables import Configs


class TetrisService:
    def __init__(self):
        self.columns = Configs.columns
        self.rows = Configs.rows
        self.name = Configs.name

        self.gameboard = Gameboard(Difficulty.BEGINNER, self.columns, self.rows)
        self.sidebar = Sidebar()
        self.gameController = GameController(self.gameboard, self.sidebar)

    def start(self, callback):
        def main():
            # play the game
            self.gameController.playGame(callback)

        thread = threading.Thread(target=main)

        thread.daemon = True

        thread.start()

        return thread

    def get_state(self):
        self.gameboard.active.to_json()
        return {
            'titles': self.gameboard.get_state_titles(),
            'isGameover': self.gameboard.isGameOver(),
            'isPaused': self.gameboard.paused,
            'nexts': [t.to_json() for t in self.sidebar.upNext],
            'score': self.gameboard.score,
            'current': self.gameboard.active.to_json(),
            'currentCoord': self.gameboard.activeCoord
        }

    def move(self, direction):
        self.gameboard.moveInDirection(direction)

    def rotate(self):
        self.gameboard.rotateActive("right")
