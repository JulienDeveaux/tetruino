from flask import Flask, request, url_for
from flask import render_template
from flask_sock import Sock

from tetris.service import TetrisService

app = Flask(__name__, static_url_path="", static_folder="./static")
sock = Sock(app)
tetris_service = TetrisService(app)


@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/test-front')
def test_front():
    return render_template('test-front.html')


@sock.route('/ws-game')
def ws_game(ws):
    tetris_service.register_websocket(ws)


@app.route('/register_gamepad', methods=['GET'])
def register_gamedpad():
    port = request.args.get('port', default=6511, type=int)

    tetris_service.register_gamepad({
        'addr': request.remote_addr,
        'port': port
    })

    return 'gamepad registered'

@app.route('/unregister_gamepad', methods=['GET'])
def unregister_gamedpad():
    tetris_service.unregister_gamedpad(request.remote_addr)

    print(request.remote_addr)

    return 'gamepad unregistered'


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
            return 'pause'
        case '5':
            tetris_service.restart()
            return 'restart'
        case _:
            return 'error'


if __name__ == '__main__':
    app.run()
