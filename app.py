import random
import threading
import time
import json

from flask import Flask
from flask import render_template
from flask_sock import Sock

from tetris.service import TetrisService

app = Flask(__name__, static_url_path="", static_folder="./static")
sock = Sock(app)
clients = []
tetris_service = TetrisService()


@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/test-front')
def test_front():
    return render_template('test-front.html')


def callback():
    for ws in clients:
        if ws.connected:
            ws.send(json.dumps(tetris_service.get_state()))


@app.route('/')
def hello_world():
    return render_template('index.html', name="Hi mom")


@sock.route('/ws-game')
def ws_game(ws):
    clients.append(ws)

    if not tetris_service.started:
        tetris_service.start(callback)  # auto start game with callback if not started
        tetris_service.pause()  # start in pause mode

    ws.send(json.dumps(tetris_service.get_state()))

    while ws.connected:
        time.sleep(1)

    clients.remove(ws)


@app.route('/commande/<id>', methods=['GET'])
def commande(id):
    match id:
        case '0':
            tetris_service.rotate()
            return 'up'
        case '1':
            tetris_service.descent()
            return 'down'
        case '2':
            tetris_service.move("left")
            return 'left'
        case '3':
            tetris_service.move("right")
            return 'right'
        case '4':
            tetris_service.pause()
            callback()
            return 'pause'
        case '5':
            tetris_service.restart()
            return 'restart'
        case _:
            return 'error'


if __name__ == '__main__':
    app.run()
