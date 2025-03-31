import numpy as np
from board import Board
import random
import math

class EnhancedConnectFourAI:
    def __init__(self, max_depth=4, strategy='minimax'):
        self.max_depth = max_depth
        self.strategy = strategy
        self.temperature = 1.0  # For simulated annealing
        
    def get_move(self, board):
        # First check if there are any valid moves
        valid_moves = board.get_valid_moves()
        if not valid_moves:
            return None
            
        if self.strategy == 'minimax':
            move = self.get_best_move_minimax(board)
        elif self.strategy == 'hill_climbing':
            move = self.hill_climbing_move(board)
        elif self.strategy == 'simulated_annealing':
            move = self.simulated_annealing_move(board)
        else:
            move = self.get_best_move_minimax(board)
        
        # If the strategy didn't return a valid move, return the first valid move
        if move is None or not board.is_valid_move(move):
            return valid_moves[0]
            
        return move

    def get_best_move_minimax(self, board):
        best_score = float('-inf')
        best_move = None
        alpha = float('-inf')
        beta = float('inf')
        
        for col in board.get_valid_moves():
            board.make_move(col)
            score = self._minimax(board, self.max_depth - 1, False, alpha, beta)
            board.undo_move(col)
            
            if score > best_score:
                best_score = score
                best_move = col
            alpha = max(alpha, best_score)
            
        return best_move

    def hill_climbing_move(self, board):
        # Start with all valid moves and their scores
        moves = board.get_valid_moves()
        if not moves:
            return None
            
        # Evaluate all initial moves
        move_scores = []
        for move in moves:
            score = self.evaluate_position(board, move)
            move_scores.append((move, score))
        
        # Start with the best move
        current_move, current_score = max(move_scores, key=lambda x: x[1])
        
        # Try to find better moves for several iterations
        for _ in range(10):  # Number of iterations
            # Look at all neighboring moves
            better_move_found = False
            for move in moves:
                if move == current_move:
                    continue
                    
                score = self.evaluate_position(board, move)
                if score > current_score:
                    current_move = move
                    current_score = score
                    better_move_found = True
            
            if not better_move_found:  # Local maximum reached
                break
                
        return current_move

    def simulated_annealing_move(self, board):
        current_move = random.choice(board.get_valid_moves())
        current_score = self.evaluate_position(board, current_move)
        best_move = current_move
        best_score = current_score
        temperature = self.temperature
        
        for _ in range(20):  # Number of iterations
            if temperature < 0.1:
                break
                
            next_move = random.choice(board.get_valid_moves())
            next_score = self.evaluate_position(board, next_move)
            
            # Calculate probability of accepting worse move
            delta = next_score - current_score
            if delta > 0 or random.random() < math.exp(delta / temperature):
                current_move = next_move
                current_score = next_score
                
                if current_score > best_score:
                    best_move = current_move
                    best_score = current_score
            
            temperature *= 0.9  # Cooling schedule
            
        return best_move

    def evaluate_position(self, board, move):
        """A* inspired heuristic evaluation function"""
        score = 0
        # Make the move temporarily
        board.make_move(move)
        
        # Heuristic components (h(n) in A*)
        score += self._evaluate_center_control(board) * 3
        score += self._evaluate_winning_potential(board) * 10
        score += self._evaluate_blocking_opponent(board) * 8
        score += self._evaluate_connectivity(board) * 5
        
        # Undo the move
        board.undo_move(move)
        return score

    def _evaluate_center_control(self, board):
        """Evaluate control of center columns"""
        center_col = board.cols // 2
        center_count = 0
        for row in range(board.rows):
            if board.board[row][center_col] == 2:  # AI pieces
                center_count += 1
        return center_count

    def _evaluate_winning_potential(self, board):
        """Evaluate potential winning moves"""
        score = 0
        # Check for potential wins in next move
        for col in board.get_valid_moves():
            board.make_move(col)
            if board.check_winner() == 2:  # AI wins
                score += 100
            board.undo_move(col)
        return score

    def _evaluate_blocking_opponent(self, board):
        """Evaluate blocking opponent's winning moves"""
        score = 0
        # Check if opponent would win in their next move
        for col in board.get_valid_moves():
            board.make_move(col)
            board.current_player = 1  # Simulate opponent's turn
            for opp_col in board.get_valid_moves():
                board.make_move(opp_col)
                if board.check_winner() == 1:  # Opponent would win
                    score -= 50
                board.undo_move(opp_col)
            board.current_player = 2  # Reset to AI's turn
            board.undo_move(col)
        return score

    def _evaluate_connectivity(self, board):
        """Evaluate piece connectivity for potential future wins"""
        score = 0
        directions = [(0,1), (1,0), (1,1), (1,-1)]
        
        for row in range(board.rows):
            for col in range(board.cols):
                if board.board[row][col] == 2:  # AI piece
                    for dr, dc in directions:
                        connected = 0
                        r, c = row, col
                        # Count connected pieces
                        while (0 <= r < board.rows and 0 <= c < board.cols and 
                               board.board[r][c] == 2):
                            connected += 1
                            r += dr
                            c += dc
                        score += connected ** 2  # Square for emphasis on longer connections
        return score

    def _minimax(self, board, depth, is_maximizing, alpha, beta):
        if depth == 0 or board.is_terminal():
            # If game is over, evaluate without requiring a valid move
            if board.is_terminal():
                winner = board.check_winner()
                if winner == 2:  # AI wins
                    return float('inf')
                elif winner == 1:  # Player wins
                    return float('-inf')
                else:  # Draw
                    return 0
            # For non-terminal states, evaluate normally
            valid_moves = board.get_valid_moves()
            if not valid_moves:
                return 0
            return self.evaluate_position(board, valid_moves[0])
        
        if is_maximizing:
            max_eval = float('-inf')
            for col in board.get_valid_moves():
                board.make_move(col)
                eval = self._minimax(board, depth - 1, False, alpha, beta)
                board.undo_move(col)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for col in board.get_valid_moves():
                board.make_move(col)
                eval = self._minimax(board, depth - 1, True, alpha, beta)
                board.undo_move(col)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval 