import findNumber as fN

def lineIsValid(board, line):
    for number in range(1, 10):
        if not fN.numberInLine(board, line, number):
            return False
    return True

def columnIsValid(board, col):
    for number in range(1, 10):
        if not fN.numberInColumn(board, col, number):
            return False
    return True

def squareIsValid(board, square):
    for number in range(1, 10):
        if not fN.numberInSquare(board, square, number):
            return False
    return True

def boardIsValid(board):
    for line in range(len(board)):
        if not lineIsValid(board, line):
            return False
    
    for col in range(len(board[0])):
        if not columnIsValid(board, col):
            return False

    for square in range(len(board)):
        if not squareIsValid(board, square):
            return False
    return True

    