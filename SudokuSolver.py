from findNumber import numberCanBePlacedOnSquare
from validBoard import boardIsValid

board = [
    [7,8,0,4,0,0,1,2,0],
    [6,0,0,0,7,5,0,0,9],
    [0,0,0,6,0,1,0,7,8],
    [0,0,7,0,4,0,2,6,0],
    [0,0,1,0,5,0,9,3,0],
    [9,0,4,0,6,0,0,0,5],
    [0,7,0,3,0,0,0,1,2],
    [1,2,0,0,0,7,4,0,0],
    [0,4,9,2,0,6,0,0,7]
]

def print_board(board, *args):
    if (len(args)) > 0:
        missingChar = args[0]
    else:
        missingChar = " "
    print()
    for i in range(len(board)):
        if i % 3 == 0 and i != 0:
            print("---------------------")
        for j in range(len(board[0])-1):
            border = "| " * (j!=0 and j%3==0) or ""
            tile = str(board[i][j]) * (board[i][j] != 0) or missingChar
            print(border + tile, end=' ')
        print(board[i][8]*(board[i][8]!=0) or missingChar)

def find_empty_square(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return i, j
    return -1, -1 #no empty square on the board

def solveBoard(board):
    line, col = find_empty_square(board)
    if line == -1:
        return True

    for number in range(1, 10):
        if numberCanBePlacedOnSquare(board, line, col, number):
            board[line][col] = number

            if solveBoard(board):
                return True

            board[line][col] = 0

    return False
