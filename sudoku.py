"""
Program:  SUDOKU         
Author:  Nefi Aguilar

"""

import os.path
from os import path

#This code is necesary to keep the terminal clear all the time. 
# import only system from os 
from os import system, name 
# import sleep to show output for some time period 
from time import sleep
# define our clear function 
def clear(): 
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 

# Global variables for the game
GAME_STATUS = [ ['0','0','0','0','0','0','0','0','0'], 
                ['0','0','0','0','0','0','0','0','0'], 
                ['0','0','0','0','0','0','0','0','0'],  
                ['0','0','0','0','0','0','0','0','0'], 
                ['0','0','0','0','0','0','0','0','0'],  
                ['0','0','0','0','0','0','0','0','0'],  
                ['0','0','0','0','0','0','0','0','0'], 
                ['0','0','0','0','0','0','0','0','0'],  
                ['0','0','0','0','0','0','0','0','0']]
FINISHED_GAME = False
GAME_NAME = ""



"""
   MAIN
   This is the driver function of the game
   The mai purpose of this function is to 
   manage a while loop where the user  is 
   constantly prompted for a command to be 
   excecuted in the game
"""
def  main():
    global GAME_STATUS
    global FINISHED_GAME
    global GAME_NAME
    clear()
    loadOrCreateNewGame()
    displayBoard()
    displayMenu()
    command = "0"
    while (command != "Q" and not FINISHED_GAME):
        command = promptForCommand()
        excecuteCommand(command)



"""
   LOAD OR CREATE NEW GAME
   This function will promt the user for the file that he/she 
   wants to open. If the file exist it will load the saved values 
   of the game. Otherwise it will create a file with the values 
   that correspond to a new game
"""
def loadOrCreateNewGame ():
    global GAME_STATUS
    global GAME_NAME

    GAME_NAME = input("Provide the name of a saved game or the name of a new game: ")
    game_file_name = GAME_NAME + ".txt"
    if(path.exists(game_file_name)):
        print("Game found")
        print("Loading contents...")
        print()
        sleep(1)
        loaded_game = open(game_file_name, "r")
        loaded_game_contents = loaded_game.readlines()
        for i in range(9):
            file_content_line = loaded_game_contents[i]
            for x in range(9):
                GAME_STATUS[i][x] = file_content_line[x]
        loaded_game.close()
    else:
        print("Game not found")
        print("Creating new game...")
        print()
        sleep(1)
        new_game_file = open(game_file_name, "w")
        for z in range(9):
            new_game_file.write("000000000\n")
        new_game_file.close()



"""
   PROMPT FOR COMMAND
   This function will prompt the user for a command. 
   It will verify the command and return it to the caller
"""
def promptForCommand():
    commands = [ '?', 'D','E', 'S', 'Q']
    print("Provide a command. Type '?' to see all commands")
    command = ''
    while True:
        command = input("  > ")
        command = command[0]
        if(command.isalpha() and command.islower()):
            command = command.upper() 
        if(command in commands):
            break
        else:
            print("Please provide a valid command")
    return command



"""
   DISPLAY MENU
  This function will display to the terminal the commands that the user 
  can provide and their corresponding function 
"""
def displayMenu():
    print("Options:")
    print("   ?  Show commands menu")
    print("   D  Display the board")
    print("   E  Edit one square")
    print("   S  Show the possible values for a square")
    print("   Q  Save and Quit")
    print()
    print()



"""
   DISPLAY BOARD
   This function will display to the terminal the sudoku
   board with its current contents
"""
def displayBoard():
    clear()
    global GAME_STATUS
    print("   A B C D E F G H I")
    for row in range(9):
        if (row == 3 or row == 6):
            print("   -----+-----+-----")
        print(str(row + 1) + "  ", end = '')
        for col in range(9):
            if(GAME_STATUS[row][col] == "0"):
                print("0", end = '')
            else:
                print(GAME_STATUS[row][col], end = '')
            if (((col + 1) % 9) == 0):
                print()
            elif(((col + 1) % 9 )== 3 or ((col + 1) % 9) == 6):
                print("|", end = '')
            else:
                print(" ", end = '')
    print()



"""
   EXCECUTE COMMAND
   This function will get a command character from the caller 
   and will call the function that correspond to that command 
"""
def excecuteCommand(command):
    command_Functions = {
        '?' :  displayMenu, 
        'D' :  displayBoard,
        'E' :  editOneSquare,
        'S' :  showPossibleValuesOfSquare, 
        'Q' :  saveAndQuitGame 
    }
    func = command_Functions.get(command,lambda :'Invalid')
    displayBoard()
    func()



"""
   GET COORDINATES
   This function will promt the user for 2 characters that represent 
   the coordinates of on square in the sudoku board
"""
def getCoordinates():
    print("Please provide the row and column of the square")
    rowAndColumn = ''
    coordinates = [0, 0]
    while True:
        columIndexes = {'A':0,'B':1,'C':2,'D':3,'E':4,'F':5,'G':6,'H':7,'I':8}
        temp_rowAndColumn = ''
        while True:
            temp_rowAndColumn = input("  > ")
            columnProvided = len(temp_rowAndColumn) > 1
            if(columnProvided):
                if(temp_rowAndColumn[1] in columIndexes):
                    break
                else:
                    print("Please provide a valid column. (A - I)")
            else:
                print("Please provide 2 values")

        row = temp_rowAndColumn[0]
        column = temp_rowAndColumn[1]
        if(column.isalpha()):
            column = column.upper()
        if((not column.isalpha()) or (not row.isdigit()) or int(row) > 9 or  int(row) < 1):
            print("ERROR: Square " + row + column + " is invalid")
            print("Please provide valid coordinates(e.g. 1A)")
        else:
            rowAndColumn = temp_rowAndColumn
            coordinates[0] = int(row) - 1
            coordinates[1] = columIndexes.get(column)
            break
    return rowAndColumn, coordinates



"""
   SQUARE IS EMPTY
   This function will receive a string representing the coordinates of a square. 
   Then it will return wheather the square is empty or not
"""
def squareIsEmpty(rowAndColumn, coordinates):
    global GAME_STATUS
    row = coordinates[0]
    column = coordinates[1]
    if( GAME_STATUS[row][column] == '0'):
        return True
    else:
        displayBoard()
        print("Square " + rowAndColumn + " is not empty")
        return False



"""
   NUMBER IS VALID IN SQUARE
   Based on the Sudoku rules, this function will chekc if the provided 
   number is valid in the square that has been selected
"""
def numberIsValidInSquare(coordinates, num):
    global GAME_STATUS
    row = coordinates[0]
    column = coordinates[1]
    if(int(num) >= 1 and  int(num) <= 9):
        for column_i in range(9):
            if(GAME_STATUS[row][column_i] == num): 
                return False
        for row_i in range(9):
            if(GAME_STATUS[row_i][column] == num): 
                return False
        squareIndexStartRow = (row // 3) * 3
        squareIndexStartCol = (column // 3) * 3
        for row_check_i in range(squareIndexStartRow, squareIndexStartRow + 3):
            for column_check_i in range(squareIndexStartCol, squareIndexStartCol + 3):
                if(GAME_STATUS[row_check_i][column_check_i] == num):
                    return  False
    else:
        return False
    return True



"""
   EDIT ONE SQUARE
   This function will get from the user a pair of cordinates and 
   a number. It the square is empty and the number is valid, the 
   number will be added to the sudoku in the coordinates that were 
   provided.
"""
def editOneSquare():
    global GAME_STATUS
    rowAndColumn, coordinates = getCoordinates()
    if(squareIsEmpty(rowAndColumn, coordinates)):
        number = input("What value do you want at '" + rowAndColumn + ": ") 
        while(not numberIsValidInSquare(coordinates, number)):
            print("ERROR: Value '" + number + "' in square '"  + rowAndColumn + "' is invalid")
            showPossibleValuesOfSquare(rowAndColumn, coordinates, True)
            number = input("What value do you want at '" + rowAndColumn + ": ") 
        GAME_STATUS[coordinates[0]][coordinates[1]] = number
        displayBoard()
        



"""
 SHOW POSSIBLE VALUES OF SQUARE
 This function will display all the posible values of a square 
 based on the Sudoku rules 

"""
def showPossibleValuesOfSquare(rowAndColumn = '', coordinates = ['0','0'], params_were_passed = False):
    validNumbers = []
    if(not params_were_passed):
        rowAndColumn, coordinates = getCoordinates()
    if(squareIsEmpty(rowAndColumn, coordinates)):
        for number in range (10):
            if(numberIsValidInSquare(coordinates, str(number))):
                validNumbers.append(number)   
        print("The possible values for '" + rowAndColumn + "' are: ", end ='')
        for valid_i in range (len(validNumbers)):
                print(validNumbers[valid_i], end='')
                if(valid_i + 1 == len(validNumbers)):
                    print()
                else:
                    print(", ", end = '')



"""
   WRITE TO FILE
   This function will save the current state of the game in a file 
"""
def writeToFile(gameName):
    global GAME_STATUS
    file_game = open((gameName + ".txt"), "w")
    for i in range(9):
        for x in range(9):
            file_game.write(GAME_STATUS[i][x])
        file_game.write("\n")
    file_game.close()
    print("Game saved successfully")



"""
   SAVE AND QUIT GAME
   This function will prompt the user whether he/she wants to save the game in the 
   current session or in another sassion. Then it will save the game and quit the program
"""
def saveAndQuitGame():
    global GAME_NAME
    print("Would you like to save your game to " + GAME_NAME + "?")
    print("Type 'YES' to confirm or 'NO' to provide another name: ")

    while True:
        confirm = input ("  > ")
        confirm = confirm.upper()
        if(confirm == "YES" or confirm == "NO"):
            break
        else:
            print("Invalid input. Type 'YES' or 'NO'")

    if(confirm == "YES"):
        writeToFile(GAME_NAME)
    else:
        save_to_game = ''
        confirm_2 = ''
        while True:
            if(confirm_2 == "YES"):
                break
            print("Save game as: ")
            save_to_game = input("  > ")
            if(path.exists(save_to_game + ".txt")):
                print("This game already exist. Do you want to overwrite it?")
                confirm_2 = input ("  > ")
                while True:
                    confirm_2 = confirm_2.upper()
                    if(confirm_2 == "YES" or confirm_2 == "NO"):
                        break
                    else:
                        print("Invalid input. Type 'YES' or 'NO'")
                        confirm_2 = input ("  > ")
            else:
                break

        
        writeToFile(save_to_game)


main()




