import threading
import time

from flask import json

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
        self.started = False

        self.gameboard = Gameboard(Difficulty.BEGINNER, self.columns, self.rows)
        self.sidebar = Sidebar()
        self.gameController = GameController(self.gameboard, self.sidebar)

        self.gamepads = []
        self.clients = []

    def start(self, callback):
        def main():
            # play the game
            try:
                self.gameController.play_game(callback)
            except BaseException as e:
                self.started = False
                print(e)
                return

        thread = threading.Thread(target=main)

        thread.daemon = True

        thread.start()
        self.started = True

        return thread

    def get_state(self):
        return {
            'titles': self.gameboard.get_state_titles(),
            'isGameover': self.gameboard.is_game_over(),
            'isPaused': self.gameboard.paused,
            'nexts': [t.to_json() for t in self.sidebar.upNext],
            'score': self.gameboard.score,
            'current': self.gameboard.active.to_json() if self.gameboard.active is not None else None,
            'currentCoord': self.gameboard.activeCoord
        }

    def move(self, direction):
        self.gameboard.move_in_direction(direction)

    def rotate(self):
        self.gameboard.rotate_active("right")

    def pause(self):
        self.gameboard.pause()
        self.__callback()

    def restart(self):
        self.gameboard.new_game()

    def descent(self):
        self.gameController.descent()

    def __callback(self):
        for ws in self.clients:
            if ws.connected:
                ws.send(json.dumps(self.get_state()))

    def register_websocket(self, ws):
        self.clients.append(ws)

        if not self.started:
            self.start(self.__callback)  # auto start game with callback if not started
            self.pause()  # start in pause mode

        ws.send(json.dumps(self.get_state()))

        while ws.connected:
            time.sleep(1)

        self.clients.remove(ws)

    def unregister_gamedpad(self, remote_addr):
        tmpGamepads = self.gamepads.copy()

        for gamepad in tmpGamepads:
            if gamepad['addr'] == remote_addr:
                self.gamepads.remove(gamepad)

    def register_gamepad(self, remote_addr):
        try:
            if remote_addr['addr'].lenth > 0 and remote_addr['port'] > 5000:
                self.gamepads.append(remote_addr)
            else:
                raise Exception('cannot add remote addr with ' + remote_addr['addr'] + str(remote_addr['port']))
        except BaseException:
            print('cannot add remote_add')
