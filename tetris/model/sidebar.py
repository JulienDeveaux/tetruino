from tetris.utils.gameUtils import get_random_tetromino


# A sidebar for menu and next pieces
def generate_up_next():
    upNext = []
    for num in range(3):
        upNext.append(get_random_tetromino())
    return upNext


class Sidebar:

    # initializes a sidebar or menu depending on current game state
    def __init__(self):
        self.upNext = []
        self.isMenu = False

        self.reset()

    # randomly generates 3 tetrominoes that are coming up next

    # removes first tetrominoe in the list and adds a new one
    def update(self):
        self.upNext.append(get_random_tetromino())
        return self.upNext.pop(0)

    def reset(self):
        self.upNext = generate_up_next()
