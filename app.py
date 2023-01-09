import random
import threading
import time
import json

from flask import Flask
from flask import render_template
from flask_sock import Sock

from tetris.service import TetrisService

app = Flask(__name__)
sock = Sock(app)
clients = []
tetris_service = TetrisService()

@app.route('/test')
def test():
    return tetris_service.get_state()


@app.route('/testStart')
def testStart():
    tetris_service.start()
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


@app.route('/commande/<id>', methods=['GET'])
def commande(id):
    for i in clients:
        if i.connected:
            i.send(id)
    match id:
        case '0':
            return 'up'
        case '1':
            return 'down'
        case '2':
            return 'left'
        case '3':
            return 'right'
        case _:
            return 'error'


if __name__ == '__main__':
    app.run()
