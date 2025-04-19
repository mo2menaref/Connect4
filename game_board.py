# game_board.py
import numpy as np

class Connect4Board:
    def __init__(self, rows=6, cols=7):
        self.rows = rows
        self.cols = cols
        self.board = np.zeros((rows, cols), dtype=int)
        self.game_over = False
        self.winner = None

    def drop_piece(self, col, player):
        """
        Drop a piece in the specified column for the given player
        Returns True if move is valid, False otherwise
        """
        for row in range(self.rows-1, -1, -1):
            if self.board[row][col] == 0:
                self.board[row][col] = player
                return True
        return False

    def is_valid_move(self, col):
        """
        Check if a move is valid (column not full and within bounds)
        """
        return 0 <= col < self.cols and self.board[0][col] == 0

    def get_valid_moves(self):
        """
        Return list of valid column moves
        """
        return [col for col in range(self.cols) if self.is_valid_move(col)]

    def check_winner(self, player):
        """
        Check if the specified player has won
        """
        # Horizontal check
        for row in range(self.rows):
            for col in range(self.cols - 3):
                if all(self.board[row][col+i] == player for i in range(4)):
                    return True

        # Vertical check
        for row in range(self.rows - 3):
            for col in range(self.cols):
                if all(self.board[row+i][col] == player for i in range(4)):
                    return True

        # Diagonal checks (positive and negative slopes)
        # Positive slope
        for row in range(self.rows - 3):
            for col in range(self.cols - 3):
                if all(self.board[row+i][col+i] == player for i in range(4)):
                    return True

        # Negative slope
        for row in range(3, self.rows):
            for col in range(self.cols - 3):
                if all(self.board[row-i][col+i] == player for i in range(4)):
                    return True

        return False

    def is_board_full(self):
        """
        Check if the board is completely filled
        """
        return len(self.get_valid_moves()) == 0

    def reset_board(self):
        """
        Reset the board to initial state
        """
        self.board = np.zeros((self.rows, self.cols), dtype=int)
        self.game_over = False
        self.winner = None