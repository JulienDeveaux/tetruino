from tetris.utils.gameUtils import get_random_tetromino, get_tetromino, new_row


# model for Tetris game board
class Gameboard:

    # initializes the game board
    # @param gameMode: the difficulty of the game of type DIFFICULTY (enum)
    # @param columns: number of cols in the game
    # @param rows: number of rows in the game
    # score: current score of the game
    # isGameOver: boolean to check game over
    def __init__(self, game_mode, columns, rows):
        self.level = 1
        self.gameMode = game_mode
        self.columns = columns
        self.rows = rows
        self.score = 0
        self.gameOver = False
        self.gameTiles = self.generate_tiles()
        self.active = get_random_tetromino()
        self.activeCoord = [3, -1]
        self.paused = False
        self.usedHold = False
        self.hold = None
        self.lastMove = 0

    # generates the game board tiles
    def generate_tiles(self):
        gameboard = []
        for r in range(self.rows):
            row = []
            for c in range(self.columns):
                row.append(0)
            gameboard.append(row)
        return gameboard

    # get a copy of current gameTitles
    def get_state_titles(self):
        return self.gameTiles.copy()

    # gets the current game board block
    def get_block(self, row, column):
        return self.gameTiles[row][column]

    # returns if the game board needs a new active tetromino
    def needs_tetromino(self):
        return self.active is None

    # replaces the current active piece
    def set_active(self, tetromino):
        self.active = tetromino

    # calculates the score added
    def update_score(self, rowCount):
        self.score += rowCount * 100 * self.level

    # checks which parts of the board can be cleared
    def check_cleared(self):
        fullRow = []
        for r in range(self.rows):
            isFull = True
            for c in range(self.columns):
                if self.gameTiles[r][c] == 0:
                    isFull = False
                    break
            if isFull:
                fullRow.append(True)
            else:
                fullRow.append(False)

        rowCount = 0
        for i in range(len(fullRow)):
            isFullRow = fullRow[i]
            if isFullRow:
                rowCount += 1
                self.gameTiles.pop(i)
                self.gameTiles.insert(0, new_row())
        self.update_score(rowCount)

    # places the Tetromino onto the gameboard
    def place_tetromino(self):
        active = self.active.get_matrix()
        for r in range(4):
            for c in range(4):
                curr = active[r][c]
                if curr != 0:
                    row = self.gameTiles[r + self.activeCoord[1]]
                    row[c + self.activeCoord[0]] = curr
        self.activeCoord = [3, -1]
        self.active = None
        self.usedHold = False
        self.score += self.level
        self.check_cleared()

    # determines if the current piece can move in the given direction
    def can_move(self, direction):
        if self.active is None or self.paused or self.gameOver:
            return False

        active = self.active.get_matrix()
        for r in range(4):
            for c in range(4):
                curr = active[r][c]
                if direction == "right":
                    if curr != 0 and (
                            (c + self.activeCoord[0] >= 9) or
                            (curr + self.gameTiles[r + self.activeCoord[1]][c + self.activeCoord[0] + 1] > curr)):
                        return False
                elif direction == "left":
                    if curr != 0 and (
                            (c + self.activeCoord[0] - 1 < 0) or
                            (curr + self.gameTiles[r + self.activeCoord[1]][c + self.activeCoord[0] - 1] > curr)):
                        return False
                elif direction == "down":
                    if curr != 0 and (
                            (r + self.activeCoord[1] >= 19) or
                            (curr + self.gameTiles[r + self.activeCoord[1] + 1][c + self.activeCoord[0]] > curr)):
                        self.place_tetromino()
                        return False

        return True

    # move current piece in the direction given
    def move_in_direction(self, direction):
        if self.can_move(direction):
            if direction == "left":
                self.activeCoord = [self.activeCoord[0] - 1, self.activeCoord[1]]
            if direction == "right":
                self.activeCoord = [self.activeCoord[0] + 1, self.activeCoord[1]]
            if direction == "down":
                self.activeCoord = [self.activeCoord[0], self.activeCoord[1] + 1]

    # determines if the piece can be rotated
    def can_rotate(self, direction):
        for r in range(4):
            for c in range(4):
                if direction == "right":
                    nextRotation = get_tetromino(self.active.get_type(), (self.active.get_rotation() + 1) % 4)
                if direction == "left":
                    nextRotation = get_tetromino(self.active.get_type(), (self.active.get_rotation() - 1) % 4)

                curr = nextRotation[r][c]
                if curr != 0 and (
                        (c + self.activeCoord[0] > 9) or (c + self.activeCoord[0] < 0) or
                        (curr + self.gameTiles[r + self.activeCoord[1]][c + self.activeCoord[0]] > curr)):
                    return False
        return True

    # rotate the active piece in direction given
    def rotate_active(self, direction):
        if self.paused or self.gameOver:
            return

        typeIndex = self.active.get_type()
        rotationIndex = self.active.get_rotation()
        if direction == "right" and self.can_rotate("right"):
            self.active = self.active.transform_tetromino(typeIndex, (rotationIndex + 1) % 4)
        if direction == "left" and self.can_rotate("left"):
            self.active = self.active.transform_tetromino(typeIndex, (rotationIndex - 1) % 4)

    # moves all movable blocks down on clock tick
    def move_down(self):
        self.activeCoord = [self.activeCoord[0], self.activeCoord[1] + 1]

    # retrieves the current position of the active piece
    def get_active_coord(self):
        return self.activeCoord

    # retrieves the current active piece
    def get_active_piece_matrix(self):
        return self.active.get_matrix()

    # pause the game
    def pause(self):
        self.paused = not self.paused

    # returns if the game is over
    def is_game_over(self):
        for c in range(4):
            if self.gameTiles[0][c + 3] != 0:
                self.gameOver = True
                return True
        return False

    # refreshes the gameboard
    def new_game(self):
        self.score = 0
        self.gameOver = False
        self.gameTiles = self.generate_tiles()
        self.active = get_random_tetromino()
        self.activeCoord = [3, -1]
        self.paused = False
        self.usedHold = False
        self.hold = None

    # gets the current score of the game
    def get_score(self):
        return self.score

    # updates the current hold
    def update_hold(self):
        if not self.usedHold:
            temp = self.hold
            self.hold = self.active
            self.active = temp
            self.activeCoord = [3, -1]
        self.usedHold = True

    # gets the current hold
    def get_hold(self):
        return self.hold
