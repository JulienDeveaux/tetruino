from flask import Flask
from flask import render_template
from flask_sock import Sock

app = Flask(__name__)
sock = Sock(app)


@app.route('/')
def hello_world():
    return render_template('index.html', name="Hi mom")


@sock.route('/echo')
def echo_socket(sock):
    while True:
        message = sock.receive()
        sock.send(message)


@app.route('/commande/<id>', methods=['GET'])
def commande(id):
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
