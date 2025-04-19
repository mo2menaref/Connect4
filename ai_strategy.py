# ai_strategy.py
import numpy as np
import random
from game_board import Connect4Board

class Connect4AI:
    def __init__(self, depth=4):
        self.depth = depth
        self.ai_player = 2  # AI is player 2
        self.human_player = 1  # Human is player 1

    def evaluate_window(self, window, player):
        """
        Evaluate a window of 4 pieces for scoring
        """
        opponent = 3 - player  # Switch between 1 and 2
        score = 0

        # Count pieces in the window
        player_count = window.count(player)
        empty_count = window.count(0)
        opponent_count = window.count(opponent)

        # Scoring strategy
        if player_count == 4:
            score += 100  # Winning move
        elif player_count == 3 and empty_count == 1:
            score += 5  # Potential win
        elif player_count == 2 and empty_count == 2:
            score += 2  # Building up

        # Defensive scoring
        if opponent_count == 3 and empty_count == 1:
            score -= 4  # Block opponent's potential win

        return score

    def score_position(self, board, player):
        """
        Evaluate the entire board state for the given player
        """
        score = 0

        # Score center column (strategic advantage)
        center_col = board.cols // 2
        center_array = [int(board.board[row][center_col]) for row in range(board.rows)]
        center_count = center_array.count(player)
        score += center_count * 3

        # Horizontal score
        for row in range(board.rows):
            for col in range(board.cols - 3):
                window = [int(board.board[row][col+i]) for i in range(4)]
                score += self.evaluate_window(window, player)

        # Vertical score
        for col in range(board.cols):
            for row in range(board.rows - 3):
                window = [int(board.board[row+i][col]) for i in range(4)]
                score += self.evaluate_window(window, player)

        # Positive diagonal score
        for row in range(board.rows - 3):
            for col in range(board.cols - 3):
                window = [int(board.board[row+i][col+i]) for i in range(4)]
                score += self.evaluate_window(window, player)

        # Negative diagonal score
        for row in range(3, board.rows):
            for col in range(board.cols - 3):
                window = [int(board.board[row-i][col+i]) for i in range(4)]
                score += self.evaluate_window(window, player)

        return score

    def is_terminal_node(self, board):
        """Check if the game is over or reached maximum depth"""
        return (board.check_winner(self.ai_player) or 
                board.check_winner(self.human_player) or 
                board.is_board_full())

    def minimax(self, board, depth, alpha, beta, maximizing_player):
        """
        Minimax algorithm with Alpha-Beta Pruning
        """
        valid_moves = board.get_valid_moves()
        is_terminal = self.is_terminal_node(board)
        
        # Terminal conditions
        if depth == 0 or is_terminal:
            if is_terminal:
                # If game is over
                if board.check_winner(self.ai_player):
                    return None, 10000  # AI wins
                elif board.check_winner(self.human_player):
                    return None, -10000  # Human wins
                else:
                    return None, 0  # Draw
            else:
                # Depth limit reached, evaluate position
                return None, self.score_position(board, self.ai_player)

        if maximizing_player:
            value = float('-inf')
            column = random.choice(valid_moves)
            for col in valid_moves:
                # Create a copy of the board to simulate move
                board_copy = Connect4Board(board.rows, board.cols)
                board_copy.board = np.copy(board.board)
                board_copy.drop_piece(col, self.ai_player)
                
                # Recursive minimax call
                new_score = self.minimax(board_copy, depth-1, alpha, beta, False)[1]
                
                if new_score > value:
                    value = new_score
                    column = col
                
                # Alpha-Beta pruning
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
                    
            return column, value

        else:  # Minimizing player (human)
            value = float('inf')
            column = random.choice(valid_moves)
            for col in valid_moves:
                # Create a copy of the board to simulate move
                board_copy = Connect4Board(board.rows, board.cols)
                board_copy.board = np.copy(board.board)
                board_copy.drop_piece(col, self.human_player)
                
                # Recursive minimax call
                new_score = self.minimax(board_copy, depth-1, alpha, beta, True)[1]
                
                if new_score < value:
                    value = new_score
                    column = col
                
                # Alpha-Beta pruning
                beta = min(beta, value)
                if alpha >= beta:
                    break
                    
            return column, value

    def get_best_move(self, board):
        """
        Get the best move for the AI using minimax with alpha-beta pruning
        """
        # Check if there are any winning moves first
        for col in board.get_valid_moves():
            board_copy = Connect4Board(board.rows, board.cols)
            board_copy.board = np.copy(board.board)
            board_copy.drop_piece(col, self.ai_player)
            if board_copy.check_winner(self.ai_player):
                return col
        
        # Use minimax to find the best move
        col, minimax_score = self.minimax(
            board,
            self.depth,
            float('-inf'),
            float('inf'),
            True
        )
        
        return col