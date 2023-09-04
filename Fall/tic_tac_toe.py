from typing import Dict
import numpy as np

BOARD_POSITIONS = np.array([["A1", "B1", "C1"],
                            ["A2", "B2", "C2"],
                            ["A3", "B3", "C3"]])

BOARD_INIT = np.array([["-" for _ in range(3)] for _ in range(3)])

DICT_ROW = {"1": 0, "2": 1, "3": 2}
DICT_COL = {"A": 0, "B": 1, "C": 2}


class TicTacToeGame:
    """_summary_
    """

    def __init__(
        self,
        board_positions: np.array = BOARD_POSITIONS,
        board_init: np.array = BOARD_INIT,
        dict_row: Dict = DICT_ROW,
        dict_col: Dict = DICT_COL,
    ) -> None:
        """_summary_

        Args:
            board_positions (np.array, optional): _description_. Defaults to BOARD_POSITIONS.
            board_init (np.array, optional): _description_. Defaults to BOARD_INIT.
            dict_row (Dict, optional): _description_. Defaults to DICT_ROW.
            dict_col (Dict, optional): _description_. Defaults to DICT_COL.
        """
        self.board_init = board_init
        self.board_positions = board_positions
        self.dict_row = dict_row
        self.dict_col = dict_col

    def _print_board(self,
                     board_status):
        """_summary_

        Args:
            board_status (_type_): _description_
        """
        print("\nPosition names      Status board:")
        for r in range(3):
            print("| " + " | ".join(self.board_positions[r]), end=" |   | ")
            print(" | ".join(board_status[r]) + " |")

    def _valid_position(self,
                        position: str):
        """_summary_

        Args:
            position (str): _description_

        Returns:
            _type_: _description_
        """
        row, col = position[1], position[0]
        return row in self.dict_row and col in self.dict_col

    def _check_win(self,
                   board_status: np.array,
                   player: str,
                   ) -> bool:
        """_summary_

        Args:
            board_status (np.array): _description_
            player (str): _description_

        Returns:
            bool: _description_
        """
        for row in board_status:
            if all(cell == player for cell in row):
                return True

        for col in range(3):
            if all(row[col] == player for row in board_status):
                return True

        if all(board_status[i, i] == player for i in range(3)) or all(board_status[i, 2 - i] == player for i in range(3)):
            return True

        return False

    def _is_board_full(self,
                       board_status: np.array) -> bool:
        """_summary_

        Args:
            board_status (np.array): _description_

        Returns:
            bool: _description_
        """
        return all(cell != "-" for row in board_status for cell in row)

    def play_game(self,
                  player_start="x"
                  ) -> None:
        """_summary_

        Args:
            player_start (str, optional): _description_. Defaults to "x".
        """
        board_status = self.board_init.copy()
        current_player = player_start
        win = False
        full = False

        while win is False and full is False:
            self._print_board(board_status=board_status)
            player_ans = input(f"Choose a position {current_player} :")

            if len(player_ans) == 2 and self._valid_position(player_ans):
                pos_r, pos_c = self.dict_row.get(
                    player_ans[1]), self.dict_col.get(player_ans[0])

                if board_status[pos_r, pos_c] == "-":
                    board_status[pos_r, pos_c] = current_player

                    win = self._check_win(board_status, current_player)
                    full = self._is_board_full(board_status)

                    if not win:
                        current_player = "o" if current_player == "x" else "x"

                else:
                    print("\nThat cell is already taken. Choose again.")
            else:
                print("\nInvalid position. Choose again.")

        if win:
            print("-"*60, f"Player {current_player} wins!", sep="\n")
        elif full:
            print("-"*60, "It's a tie!", sep="\n")
        self._print_board(board_status)


TicTacToe = TicTacToeGame()
TicTacToe.play_game()
