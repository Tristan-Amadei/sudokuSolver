import random
from findNumber import listOfPossibleNumbersOnSquare
from SudokuSolver import print_board, solveBoard

def copyBoard(board):
    new_board = [9*[0] for i in range(9)]
    for i in range(9):
        for j in range(9):
            new_board[i][j] = board[i][j]
    return new_board

def initialize_empty_board():
    board = [9*[0] for i in range(9)]
    return board

def initGrid(nbToAdd):
    total = 0
    board = initialize_empty_board()
    for _ in range(nbToAdd):
        i, j = random.randint(0, 8), random.randint(0, 8)
        while board[i][j] != 0 or len(listOfPossibleNumbersOnSquare(board, i, j)) == 0:
            i, j = random.randint(0, 8), random.randint(0, 8)
        number = random.choice(listOfPossibleNumbersOnSquare(board, i, j))
        board[i][j] = number
        total += 1
        #print(f"Coord -> {i}, {j}, number -> {number} // total -> {total}")
    return board

def getFinalGrid(nbToAdd):
    grid = initGrid(nbToAdd)
    solution = copyBoard(grid)
    if solveBoard(solution):
        return grid
    else:
        return getFinalGrid(nbToAdd)