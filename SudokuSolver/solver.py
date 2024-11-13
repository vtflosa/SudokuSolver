""" Solver of sudoku grid 9x9 optimized for speed by Flo """

# file = open("output.txt","w")


def printFileBoard(board):
    """function to print the board on to a file.
        returns a string variable with the board info"""
    string = ""
    string = string + "*********************\n"
    for x in range(0, 9):
        if x == 3 or x == 6:
            string = string + "*********************\n"
        for y in range(0, 9):
            if y == 3 or y == 6:
                string = string + " * "
            string = string + str(board[x][y]) + " "
        string = string + "\n"
    string = string + "*********************\n"
    return string


def printBoard(board):
    """function to print the board on to the console"""
    print("*********************")
    for x in range(0, 9):
        if x == 3 or x == 6:
            print("*********************")
        for y in range(0, 9):
            if y == 3 or y == 6:
                print("*", end=" ")
            print(board[x][y], end=" ")
        print()
    print("*********************")


def isFull(board):
    """ function to check if the board is full or not
        returns true if it is full and false if it isn't
        it works on the fact that if it finds at least one
        zero in the board it returns false"""
    for x in range(0, 9):
        for y in range(0, 9):
            if board[x][y] == 0:
                return False
    return True


def possibleEntries(board, i, j):
    """ function to find all of the possible numbers
        which can be put at the specifies location by
        checking the horizontal and vertical and the
        three by three square in which the numbers are
        housed"""

    possibilityArray = {}

    for x in range(1, 10):
        possibilityArray[x] = 0

    # For horizontal entries
    for y in range(0, 9):
        if not board[i][y] == 0:
            possibilityArray[board[i][y]] = 1

    # For vertical entries
    for x in range(0, 9):
        if not board[x][j] == 0:
            possibilityArray[board[x][j]] = 1

    # For squares of three x three
    k = 0
    l = 0
    if i >= 0 and i <= 2:
        k = 0
    elif i >= 3 and i <= 5:
        k = 3
    else:
        k = 6
    if j >= 0 and j <= 2:
        l = 0
    elif j >= 3 and j <= 5:
        l = 3
    else:
        l = 6
    for x in range(k, k + 3):
        for y in range(l, l + 3):
            if not board[x][y] == 0:
                possibilityArray[board[x][y]] = 1

    for x in range (1, 10):
        if possibilityArray[x] == 0:
            possibilityArray[x] = x
        else:
            possibilityArray[x] = 0

    return possibilityArray


def best_vacant(board):
    """ Optimize search by selecting the line/column/square with the less value to complete"""
    # copy the board and replace with 1 and 0 to make calculation
    calc_board = [[0 for x in range(9)] for x in range(9)]
    for x in range(9):
        for y in range(9):
            if board[x][y] != 0:
                calc_board[x][y] = 1

    # list the lines, columns and sqares as sum of lines, columns and squares
    lines, columns, squares = [], [], [0 for i in range(9)]
    k = 0
    for i in range(9):
        lines.append(sum(calc_board[i]))
        col_sum = 0
        for j in range(9):
            col_sum += calc_board[j][i]
            if j < 3:
                if i < 3:
                    k = 0
                elif 2 < i < 6:
                    k = 1
                else:
                    k = 2
            elif 2 < j < 6:
                if i < 3:
                    k = 3
                elif 2 < i < 6:
                    k = 4
                else:
                    k = 5
            elif j:
                if i < 3:
                    k = 6
                elif 2 < i < 6:
                    k = 7
                else:
                    k = 8
            squares[k] = squares[k] + calc_board[j][i]
        columns.append(col_sum)

    lists_dict = {"line": lines, "column": columns, "square": squares}

    max_nb = 0
    for item in lists_dict:
        for value in lists_dict[item]:
            if value >= max_nb and value != 9:
                max_nb = value
                best_list = lists_dict[item]
                list_type = item

    if lists_dict != {}:
        for index in range(9):
            if max_nb == best_list[index]:
                break
    else:
        list_type = "square"

        # get the indexes of the board to test
    if list_type == "line":
        for x in range(9):
            if calc_board[index][x] == 0:
                break
        i, j = index, x
        return i, j

    elif list_type == "column":
        for x in range(9):
            if calc_board[x][index] == 0:
                break

        i, j = x, index
        return i, j

    else:

        if index < 3:
            # first line of sqares
            xstart , xend, ystart, yend = 0, 3, index * 3, (index + 1) * 3
        elif 2 < index < 6:
            # second line of sqares
            xstart , xend, ystart, yend = 3, 6, (index - 3) * 3, (index - 3 + 1) * 3
        else:
            # third line of sqares
            xstart , xend, ystart, yend = 6, 9, (index - 6) * 3, (index - 6 + 1) * 3

        for y in range(ystart, yend):
            for x in range(xstart, xend):
                if calc_board[x][y] == 0:
                    break
            if calc_board[x][y] == 0:
                break
        return x, y


def grid_not_valid(board):
    """ validate the grid if there is no duplicate in line/colone/region"""

    duplicate_coord = []
    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:  # there is a number to check
                if has_duplicate(board, i, j):  # the number in coord i, j has duplicate
                    duplicate_coord.append((i, j))

    if duplicate_coord:
        return duplicate_coord
    else:
        return False


def has_duplicate(board, coord_x, coord_y):
    """ check if the number at x,y has no duplicate in line/colone/region
        return True or False"""
    # copy the board to modify it
    cpboard = [[0 for i in range(9)] for i in range(9)]
    for i in range(9):
        for j in range(9):
            cpboard[i][j] = board[i][j]

    test_numb = board[coord_x][coord_y]
    cpboard[coord_x][coord_y] = 0  # replace the number by 0 to test if still present in the line/colone/region

    # check line
    if test_numb in cpboard[coord_x]:
        return True

    # check column
    for i in range(9):
        if test_numb == cpboard[i][coord_y]:
            return True

    # check region
    region_list, range_x, range_y = [], [], []
    # build range for region of x, y
    if coord_x < 3:
        range_x = [i for i in range(0, 3)]
    elif 3 <= coord_x < 6:
        range_x = [i for i in range(3, 6)]
    elif 6 <= coord_x:
        range_x = [i for i in range(6, 9)]

    if coord_y < 3:
        range_y = [i for i in range(0, 3)]
    elif 3 <= coord_y < 6:
        range_y = [i for i in range(3, 6)]
    elif 6 <= coord_y:
        range_y = [i for i in range(6, 9)]

    # build list of number in the region of x, y
    for i in range_x:
        for j in range_y:
            region_list.append(cpboard[i][j])

    if test_numb in region_list:  # check region
        return True

    return False  # no duplicate found



def sudokuSolver(board):
    """ recursive function which solved the board and
        prints it."""

    # if board is full, there is no need to solve it any further
    if isFull(board):
        # print("Board Solved Successfully!")
        # printBoard(board)
        return board

    else:

        # # find the first vacant spot
        # """ NON OPTIMIZED SEARCH """
        # for x in range(0, 9):
        #     for y in range(0, 9):
        #         if board[x][y] == 0:
        #             i = x
        #             j = y
        #             break
        #     else:
        #         continue
        #     break
        # # -------------------------------

        # FIND THE BEST VACANT SPOT :
        i, j = best_vacant(board)
        # # -------------------------------

        # get all the possibilities for i,j
        possiblities = possibleEntries(board, i, j)

        # go through all the possibilities and call the the function
        # again and again
        for x in range(1, 10):
            if not possiblities[x] == 0:
                board[i][j] = possiblities[x]
                #file.write(printFileBoard(board))
                result = sudokuSolver(board)
                if result:
                    return board
        # backtrack
        # print("backtrack")
        board[i][j] = 0
    return False


def calc(board=None):
    """ board should be a 9x9 list of numbers"""
    if not board:
        SudokuBoard = [[0 for x in range(9)] for x in range(9)]
        SudokuBoard[0][0] = 0
        SudokuBoard[0][1] = 0
        SudokuBoard[0][2] = 0
        SudokuBoard[0][3] = 3
        SudokuBoard[0][4] = 0
        SudokuBoard[0][5] = 0
        SudokuBoard[0][6] = 2
        SudokuBoard[0][7] = 0
        SudokuBoard[0][8] = 0
        SudokuBoard[1][0] = 0
        SudokuBoard[1][1] = 0
        SudokuBoard[1][2] = 0
        SudokuBoard[1][3] = 0
        SudokuBoard[1][4] = 0
        SudokuBoard[1][5] = 8
        SudokuBoard[1][6] = 0
        SudokuBoard[1][7] = 0
        SudokuBoard[1][8] = 0
        SudokuBoard[2][0] = 0
        SudokuBoard[2][1] = 7
        SudokuBoard[2][2] = 8
        SudokuBoard[2][3] = 0
        SudokuBoard[2][4] = 6
        SudokuBoard[2][5] = 0
        SudokuBoard[2][6] = 3
        SudokuBoard[2][7] = 4
        SudokuBoard[2][8] = 0
        SudokuBoard[3][0] = 0
        SudokuBoard[3][1] = 4
        SudokuBoard[3][2] = 2
        SudokuBoard[3][3] = 5
        SudokuBoard[3][4] = 1
        SudokuBoard[3][5] = 0
        SudokuBoard[3][6] = 0
        SudokuBoard[3][7] = 0
        SudokuBoard[3][8] = 0
        SudokuBoard[4][0] = 1
        SudokuBoard[4][1] = 0
        SudokuBoard[4][2] = 6
        SudokuBoard[4][3] = 0
        SudokuBoard[4][4] = 0
        SudokuBoard[4][5] = 0
        SudokuBoard[4][6] = 4
        SudokuBoard[4][7] = 0
        SudokuBoard[4][8] = 9
        SudokuBoard[5][0] = 0
        SudokuBoard[5][1] = 0
        SudokuBoard[5][2] = 0
        SudokuBoard[5][3] = 0
        SudokuBoard[5][4] = 8
        SudokuBoard[5][5] = 6
        SudokuBoard[5][6] = 1
        SudokuBoard[5][7] = 5
        SudokuBoard[5][8] = 0
        SudokuBoard[6][0] = 0
        SudokuBoard[6][1] = 3
        SudokuBoard[6][2] = 5
        SudokuBoard[6][3] = 0
        SudokuBoard[6][4] = 9
        SudokuBoard[6][5] = 0
        SudokuBoard[6][6] = 7
        SudokuBoard[6][7] = 6
        SudokuBoard[6][8] = 0
        SudokuBoard[7][0] = 0
        SudokuBoard[7][1] = 0
        SudokuBoard[7][2] = 0
        SudokuBoard[7][3] = 7
        SudokuBoard[7][4] = 0
        SudokuBoard[7][5] = 0
        SudokuBoard[7][6] = 0
        SudokuBoard[7][7] = 0
        SudokuBoard[7][8] = 0
        SudokuBoard[8][0] = 0
        SudokuBoard[8][1] = 0
        SudokuBoard[8][2] = 9
        SudokuBoard[8][3] = 0
        SudokuBoard[8][4] = 0
        SudokuBoard[8][5] = 5
        SudokuBoard[8][6] = 0
        SudokuBoard[8][7] = 0
        SudokuBoard[8][8] = 0
        board = SudokuBoard

    # check if board is valid
    if grid_not_valid(board):
        raise ValueError("There is duplicate in the board!"
                         "Board is invalid at coord : {}".format(grid_not_valid(board)))

    # printBoard(board)
    solution = sudokuSolver(board)
    if solution:
        return solution
    else:
        return print("There is no solution to this sudoku")
    # file.close()

if __name__ == "__main__":
    calc()




