import pygame
from SudokuSolver import solveBoard, print_board
from initRandomBoard import getFinalGrid
import time

pygame.font.init()
pygame.init()

def copyBoard(board):
    new_board = [9*[0] for i in range(9)]
    for i in range(9):
        for j in range(9):
            new_board[i][j] = board[i][j]
    return new_board

def getSolutionBoard(board):
    solution = copyBoard(board)
    solveBoard(solution)
    return solution

def find_init_number(diff):
    if diff == 'easy':
        return 32
    if diff == 'hard':
        return 25
    return 28

class Grid():
    '''
    board = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]
    '''
    board = getFinalGrid(30)

    solution = getSolutionBoard(board)

    def __init__(self, rows, cols, width, height):
        self.rows = rows
        self.cols = cols
        self.cubes = [[Cube(self.board[i][j], i, j, width, height, self.board) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.model = None
        self.selected = None

    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def place(self, val):
        row, col = self.selected
        print_board(self.board)
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val)
            self.update_model()

            if self.solution[row][col] == val:
                self.board[row][col] = val
                return True
            else:
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.update_model()
                return False

    def sketch(self, val):
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

    def draw(self, win):
        # Draw Grid Lines
        gap = self.width / 9
        for i in range(self.rows+1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(win, (0,0,0), (0, i*gap), (self.width, i*gap), thick)
            pygame.draw.line(win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)

        # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(win)

    def select(self, row, col):
        # Reset all other
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row, col)

    def clear(self):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)

    def click(self, pos):
        """
        :param: pos
        :return: (row, col)
        """
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y),int(x))
        else:
            return None

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True


class Cube:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height, board):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.board = board
        self.selected = False

    def draw(self, win):
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, (128,128,128))
            win.blit(text, (x+5, y+5))
        elif not(self.value == 0):
            text = fnt.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))

        if self.selected:
            if self.value == 0:
                pygame.draw.rect(win, (255,0,0), (x,y, gap ,gap), 3)
            else:
                value = self.value
                for i in range(9):
                    for j in range(9):
                        if self.board[i][j] == value:
                            x = j * gap
                            y = i * gap
                            pygame.draw.rect(win, (255,0,0), (x,y, gap ,gap), 3)


    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val


def redraw_window(win, board, time, strikes, width, height, gameOver):
    win.fill((255,255,255))
    # Draw time
    fnt = pygame.font.SysFont("comicsans", 40)
    text = fnt.render("Time: " + format_time(time), 1, (0,0,0))
    win.blit(text, (width - text.get_width()-10, height-text.get_height()-10))
    # Draw Strikes
    if strikes < 5:
        text = fnt.render("X " * strikes, 1, (255, 0, 0))
    else:
        text = fnt.render(f"Errors: {strikes}", 1, (255, 0, 0))
    win.blit(text, (20, height-text.get_height()-10))
    # Draw grid and board
    board.draw(win)
    # Write text if game's over
    if gameOver:
        fnt = pygame.font.SysFont("calibri", 80)
        text = fnt.render("You've Won!", 1, (0, 255, 0))
        win.blit(text, ((width - text.get_width()) / 2, (height - text.get_height())/2))


def format_time(secs):
    sec = secs%60
    minute = secs//60

    mat = " " + str(minute) + ":" + str(sec)
    return mat


def main():
    screenInfo = pygame.display.Info()
    width = 0.4*screenInfo.current_w
    height = 0.8*screenInfo.current_h
    win = pygame.display.set_mode((width,height))
    pygame.display.set_caption("Sudoku Solver")

    key = None
    run = True
    start = time.time()
    strikes = 0
    gameOver = False
    boardInitialized = False
    print("Initializing the grid")

    while run:
        if not boardInitialized:
            board = Grid(9, 9, width, width)
            boardInitialized = True

        if not gameOver:
            play_time = round(time.time() - start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                numerical_1 = 1073741913
                if event.key == pygame.K_1 or event.key == numerical_1:
                    key = 1
                if event.key == pygame.K_2 or event.key == numerical_1 + 1:
                    key = 2
                if event.key == pygame.K_3 or event.key == numerical_1 + 2:
                    key = 3
                if event.key == pygame.K_4 or event.key == numerical_1 + 3:
                    key = 4
                if event.key == pygame.K_5 or event.key == numerical_1 + 4:
                    key = 5
                if event.key == pygame.K_6 or event.key == numerical_1 + 5:
                    key = 6
                if event.key == pygame.K_7 or event.key == numerical_1 + 6:
                    key = 7
                if event.key == pygame.K_8 or event.key == numerical_1 + 7:
                    key = 8
                if event.key == pygame.K_9 or event.key == numerical_1 + 8:
                    key = 9
                if event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                    board.clear()
                    key = None
                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.cubes[i][j].temp != 0:
                        if board.place(board.cubes[i][j].temp):
                            print("Success")
                        else:
                            print("Wrong")
                            strikes += 1
                        key = None

                        if board.is_finished():
                            print("Game over")
                            gameOver = True
                            #run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None

        if board.selected and key != None:
            board.sketch(key)

        redraw_window(win, board, play_time, strikes, width, height, gameOver)
        pygame.display.update()

main()