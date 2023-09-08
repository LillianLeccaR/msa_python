from typing import Dict

BOARD_POSITIONS = [["A1", "B1", "C1"],
                   ["A2", "B2", "C2"],
                   ["A3", "B3", "C3"]]

BOARD_INIT = [["-" for _ in range(3)] for _ in range(3)]

DICT_ROW = {"1": 0, "2": 1, "3": 2}
DICT_COL = {"A": 0, "B": 1, "C": 2}


class TicTacToeGame:
    """Class to create tic tac toe game.
    """

    def __init__(
            self,
            board_positions: list[list] = BOARD_POSITIONS,
            board_init: list[list] = BOARD_INIT,
            dict_row: Dict = DICT_ROW,
            dict_col: Dict = DICT_COL,
            current_player: str = "x") -> None:
        """Initializes the tic tac toe class

        Args:
            board_positions (np.array, optional):
                Matrix with the name of available positions.
                Defaults to BOARD_POSITIONS.
            board_init (np.array, optional): Initial board status.
                                                Defaults to BOARD_INIT.
            dict_row (Dict, optional):
                Dictionary to decode values to get the row position for every
                position enter by the user. Defaults to DICT_ROW.
            dict_col (Dict, optional):
                Dictionary to decode values to get the col position for every
                position enter by the user. Defaults to DICT_COL.
            current_player (str, optional): Icon for the start player.
                                            Defaults to "x".
        """
        self.board_positions = board_positions
        self.board_status = board_init.copy()
        self.current_player = current_player
        self.dict_row = dict_row
        self.dict_col = dict_col

    def _print_board(self) -> None:
        """Function to print the matrix with the available positions and
            the current status board.
        """
        print("\nPosition names      Status board:")
        for r in range(3):
            print("| " + " | ".join(self.board_positions[r]), end=" |   | ")
            print(" | ".join(self.board_status[r]) + " |")

    def _valid_position(self,
                        position: str) -> bool:
        """Function to validate is the position chosen by the current player
            follow the stucture defined in the position names.

        Args:
            position (str): Position enter by the current player.

        Returns:
            bool: Bool to validate if the position enter by the current player follow
            the structure of positiones defined in the "positions names" matrix printed.
        """
        row, col = position[1], position[0]
        return row in self.dict_row and col in self.dict_col

    def _make_move(self, position) -> bool:
        """Function to update the status board, if it has not been used.

        Args:
            position (str): Position enter by the current player.

        Returns:
            bool: Bool with the result of validate is the position chosen by the current
            player was pasted in the board status.
        """
        row, col = self.dict_row[position[1]], self.dict_col[position[0]]
        if self.board_status[row][col] == "-":
            self.board_status[row][col] = self.current_player
            return True
        else:
            print("\nThat cell is already taken. Choose again.")
            return False

    def _check_win(self) -> bool:
        """Function to validate if the current player has won.

        Returns:
            bool: Bool to know if the game should finish because there is a winner.
        """
        for row in self.board_status:
            if all(cell == self.current_player for cell in row):
                return True

        for col in range(3):
            if all(row[col] == self.current_player for row in self.board_status):
                return True

        if all(self.board_status[i][i] == self.current_player for i in range(3)) or all(self.board_status[i][2 - i] == self.current_player for i in range(3)):
            return True

        return False

    def _is_board_full(self) -> bool:
        """Function to validate if exists positions not used in the status board.

        Returns:
            bool: Bool to know if exists positions not used in the status board.
        """
        return all(cell != "-" for row in self.board_status for cell in row)

    def play_game(self) -> None:
        """Function to play tic tac toe.
        """
        win = False
        full = False
        winner = None

        while not win and not full:
            self._print_board()
            player_ans = input(
                f"Choose a position {self.current_player}: ")

            if len(player_ans) == 2 and self._valid_position(player_ans):
                if self._make_move(player_ans):
                    win = self._check_win()
                    full = self._is_board_full()
                    if win:
                        winner = self.current_player
                    self.current_player = "o" if self.current_player == "x" else "x"
                else:
                    continue
            else:
                print("\nInvalid position. Choose again.")

        self._print_board()

        if winner:
            print(f"Player {winner} wins!")
        else:
            print("It's a tie!")


TicTacToe = TicTacToeGame()
TicTacToe.play_game()
