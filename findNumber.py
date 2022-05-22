def numberInLine(board, line, number):
    for j in range(len(board[line])):
        if board[line][j] == number:
            return True
    return False

def numberInColumn(board, col, number):
    for i in range(len(board)):
        if board[i][col] == number:
            return True
    return False

def numberInSquare(board, square, number):
    for i in range(3 * (square//3), 3 * (square//3) + 3):
        for j in range(3 * (square%3), 3 * (square%3) + 3):
            if board[i][j] == number:
                return True
    return False

def numberCanBePlacedOnSquare(board, i, j, number):
    if numberInLine(board, i, number):
        return False
    if numberInColumn(board, j, number):
        return False
    square = 3 * (i//3) + (j//3)
    if numberInSquare(board, square, number):
        return False
    return True

def findNumberToFill(board, line, col):
    for number in range(1, 10):
        if numberCanBePlacedOnSquare(board, line, col, number):
            board[line][col] = number
            return number
    return -1 #no number can be set on that square

