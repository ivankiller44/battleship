import random

LENGTH_OF_SHIPS = [1,2,3,4,5]  
PLAYER_BOARD = [[" "] * 10 for i in range(10)]
COMPUTER_BOARD = [[" "] * 10 for i in range(10)]
PLAYER_GUESS_BOARD = [[" "] * 10 for i in range(10)]
COMPUTER_GUESS_BOARD = [[" "] * 10 for i in range(10)]
LETTERS_TO_NUMBERS = {'A':0, 'B':1, 'C':2, 'D':3, 'E':4, 'F':5, 'G':6, 'H':7, 'I':8, 'J':9}

def print_board(board):
    print("    1 2 3 4 5 6 7 8 9 10")
    print("   +-+-+-+-+-+-+-+-+-+-+")
    row_number = 1
    row_letter = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    for row in board:
        print("%s  |%s|" % (row_letter[row_number-1], "|".join(row)))
        row_number += 1

#place Ships
def place_ships(board):
    #loop through length of ships
    for ship_length in LENGTH_OF_SHIPS:
        #loop until ship fits and doesn't overlap
        while True:
            if board == COMPUTER_BOARD:
                orientation, row, column = random.choice(["H", "V"]), random.randint(0,9), random.randint(0,9)
                if check_ship_fit(ship_length, row, column, orientation):
                    #check if ship overlaps
                    if ship_overlaps(board, row, column, orientation, ship_length) == False:
                        #place ship
                        if orientation == "H":
                            for i in range(column, column + ship_length):
                                board[row][i] = "X"
                        else:
                            for i in range(row, row + ship_length):
                                board[i][column] = "X"
                        break
            else:
                place_ship = True
                print('Place the ship with a length of ' + str(ship_length))
                row, column, orientation = user_input(place_ship)
                if check_ship_fit(ship_length, row, column, orientation):
                    #check if ship overlaps
                        if ship_overlaps(board, row, column, orientation, ship_length) == False:
                            #place ship
                            if orientation == "H":
                                for i in range(column, column + ship_length):
                                    board[row][i] = "X"
                            else:
                                for i in range(row, row + ship_length):
                                    board[i][column] = "X"
                            print_board(PLAYER_BOARD)
                            break 

#check if ship fits in board
def check_ship_fit(SHIP_LENGTH, row, column, orientation):
    if orientation == "H":
        if column + SHIP_LENGTH > 10:
            return False
        else:
            return True
    else:
        if row + SHIP_LENGTH > 10:
            return False
        else:
            return True

#check each position for overlap
def ship_overlaps(board, row, column, orientation, ship_length):
    if orientation == "H":
        for i in range(column, column + ship_length):
            if board[row][i] == "X":
                return True
    else:
        for i in range(row, row + ship_length):
            if board[i][column] == "X":
                return True
    return False


def user_input(place_ship):
    if place_ship == True:
        while True:
            try: 
                orientation = input("Enter orientation (H or V): ").upper()
                if orientation == "H" or orientation == "V":
                    break
            except TypeError:
                print('Enter a valid orientation H or V')
        while True:
            try: 
                column = input("Enter the column 1 - 10 of the ship: ")
                if column in '12345678910':
                    column = int(column) - 1
                    break
            except ValueError:
                print('Enter a valid letter between 1 - 10')
        while True:
            try: 
                row = input("Enter the column A - J of the ship: ").upper()
                if row in 'ABCDEFGHIJ':
                    row = LETTERS_TO_NUMBERS[row]
                    break
            except KeyError:
                print('Enter a valid letter between A - J')
        return row, column, orientation 
    else:
        while True:
            try: 
                column = input("Enter the row 1 - 10 of the ship: ")
                if column in '12345678910':
                    column = int(column) - 1
                    break
            except ValueError:
                print('Enter a valid letter between 1 - 10')
        while True:
            try: 
                row = input("Enter the column A - J of the ship: ").upper()
                if row in 'ABCDEFGHIJ':
                    row = LETTERS_TO_NUMBERS[row]
                    break
            except KeyError:
                print('Enter a valid letter between A - J')
        return row, column        

#check if all ships are hit
def count_hit_ships(board):
    count = 0
    for row in board:
        for column in row:
            if column == '\x1b[7;31;47m' + 'X' + '\x1b[0m':
                count += 1
    return count


#user and computer turn
def turn(board):
    if board == PLAYER_GUESS_BOARD:
        row, column = user_input(PLAYER_GUESS_BOARD)
        if board[row][column] == "-":
            turn(board)
        elif board[row][column] == "X":
            turn(board)
        elif COMPUTER_BOARD[row][column] == "X":
            board[row][column] = '\x1b[7;31;47m' + 'X' + '\x1b[0m'
        else:
            board[row][column] = "-"
    else:
        row, column = random.randint(0,9), random.randint(0,9)
        if board[row][column] == "-":
            turn(board)
        elif board[row][column] == "X":
            turn(board)
        elif PLAYER_BOARD[row][column] == "X":
            board[row][column] = '\x1b[7;31;47m' + 'X' + '\x1b[0m'
        else:
            board[row][column] = "-"

place_ships(COMPUTER_BOARD)
print_board(COMPUTER_BOARD)
print_board(PLAYER_BOARD)
place_ships(PLAYER_BOARD)
        
while True:
    #player turn
    while True:
        print('Guess a battleship location')
        print_board(PLAYER_GUESS_BOARD)
        turn(PLAYER_GUESS_BOARD)
        break
    if count_hit_ships(PLAYER_GUESS_BOARD) == 15:
        print("You win!")
        break   
    #computer turn
    while True:
        turn(COMPUTER_GUESS_BOARD)
        break           
    print_board(COMPUTER_GUESS_BOARD)   
    if count_hit_ships(COMPUTER_GUESS_BOARD) == 15:
        print("Sorry, the computer won.")
        break