"""Tic tac toe Implementation
    author: Lillian Lecca
"""
import pandas as pd

board_init = [["A1", "B1", "C1"], ["A2", "B2", "C2"], ["A3", "B3", "C3"]]
board_status = [["-" for _ in range(3)] for _ in range(3)]

tittle_position = "Position names:"
tittle_status = "Status board:  "

dic_row = {"1": 1, "2": 2, "3": 3}
dic_col = {"A": 1, "B": 2, "C": 3}

win=False

def print_two_boards(tittle_1, tittle_2 , board_1 , board_2):
    """Print current board status"""
    print("\n",tittle_1," "*4 ,tittle_2)
    for r in range(0, 3):
        print("\n|", end="")
        for c in range(0, 3):
            print(f"{board_1[r][c]} ", end="| ")
        print("     | ", end="")
        for c in range(0, 3):
            print(f"{board_2[r][c]} ", end="| ")
    print("\n"*2, end="")

def valid_position(position,dic_row,dic_col):
    return(True if (dic_row.get(position[1]) != None and dic_col.get(position[0]) != None ) else False)

def check_win(board, player):
    for row in board:
        if all(cell == player for cell in row):
            return True

    for col in range(3):
        if all(row[col] == player for row in board):
            return True

    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True

    return False

def is_board_full(board):
    return all(cell != "-" for row in board for cell in row)

def play_game(board_status,win):
    current_player="x"
    while win == False:
        print_two_boards(tittle_position, tittle_status , board_init , board_status)
        player_ans = input( f"Choose a position {current_player} :" )

        if valid_position(player_ans,dic_row,dic_col):
            pos_r = dic_row.get(player_ans[1])-1
            pos_c = dic_col.get(player_ans[0])-1

            if board_status[pos_r][pos_c] == "-":
                board_status[pos_r][pos_c]=current_player
                if check_win(board_status, current_player):
                    print_two_boards(tittle_position, tittle_status , board_init , board_status)
                    print(f"Player {current_player} wins!")
#                    break
                elif is_board_full(board_status):
                    print_two_boards(tittle_position, tittle_status , board_init , board_status)
                    print("It's a tie!")
                    break
                current_player = "o" if current_player == "x" else "x"
            else:
                print("\nThat cell is already taken. Choose again.")
        else:
            print("\nInvalid position. Choose again.")

play_game(board_status,win)
