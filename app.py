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

@app.route('/test')
def test():
    return tetris_service.get_state()

@app.route('/test-front')
def test_front():
    return render_template('test-front.html')

@app.route('/testStart')
def testStart():
    def callback():
        for ws in clients:
            if ws.connected:
                ws.send(json.dumps(tetris_service.get_state()))

    tetris_service.start(callback)
    return "started"

@app.route('/')
def hello_world():
    return render_template('index.html', name="Hi mom")


@sock.route('/echo')
def echo_socket(ws):
    clients.append(ws)
    while ws.connected:
        message = ws.receive()
        ws.send(message)
    clients.remove(ws)


@sock.route('/ws-game')
def ws_game(ws):
    clients.append(ws)

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
            tetris_service.move("down")
            return 'down'
        case '2':
            tetris_service.move("left")
            return 'left'
        case '3':
            tetris_service.move("right")
            return 'right'
        case _:
            return 'error'


if __name__ == '__main__':
    app.run()
