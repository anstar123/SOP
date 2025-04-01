# Checkers Game Implementation Documentation
## Line-by-Line Explanation of game3.py

### Imports and Type Hints
```python
import numpy as np
import time
from typing import List, Tuple, Optional
import copy
import random
```
- `numpy`: Used for efficient array operations and board representation
- `time`: For measuring AI search time
- `typing`: For type hints to improve code readability and maintainability
- `copy`: For deep copying board states to prevent unintended modifications
- `random`: For random move selection when multiple moves have equal value

### CheckersGame Class
```python
class CheckersGame:
    def __init__(self):
        self.board = np.full((8, 8), ' ')
        self.current_player = 'b'  # 'b' for black, 'r' for red
        self.move_history = []
        self.move_count = 0
        self.capture_count = 0
        self.board_states = []
        self.nodes_explored = 0
```
- Initializes an 8x8 board with empty spaces
- Sets black as the first player
- Initializes tracking variables for moves, captures, and AI performance

### Board Initialization
```python
def initialize_board(self):
    # Place black pieces
    for row in range(3):
        for col in range(8):
            if (row + col) % 2 == 0:
                self.board[row][col] = 'b'
    
    # Place red pieces
    for row in range(5, 8):
        for col in range(8):
            if (row + col) % 2 == 0:
                self.board[row][col] = 'r'
```
- Places black pieces in top 3 rows
- Places red pieces in bottom 3 rows
- Uses alternating pattern based on (row + col) % 2

### Board Display
```python
def print_board(self):
    print("\n  0 1 2 3 4 5 6 7")
    for row in range(8):
        print(f"{row} {' '.join(self.board[row])}")
```
- Prints column numbers (0-7)
- Prints each row with piece positions
- Uses space separator for readability

### Move Validation
```python
def is_valid_move(self, start: Tuple[int, int], end: Tuple[int, int]) -> bool:
    start_row, start_col = start
    end_row, end_col = end
    
    # Check board boundaries
    if not (0 <= start_row < 8 and 0 <= start_col < 8 and 
            0 <= end_row < 8 and 0 <= end_col < 8):
        return False
    
    # Check if start position has a piece
    piece = self.board[start_row][start_col]
    if piece == ' ':
        return False
    
    # Check piece ownership
    if (self.current_player == 'b' and piece.lower() != 'b') or \
       (self.current_player == 'r' and piece.lower() != 'r'):
        return False
    
    # Check if end position is empty
    if self.board[end_row][end_col] != ' ':
        return False
    
    # Regular move (1 square diagonally)
    if abs(end_row - start_row) == 1 and abs(end_col - start_col) == 1:
        if piece.isupper():  # king can move in any direction
            return True
        elif piece == 'b' and end_row > start_row:  # black moves down
            return True
        elif piece == 'r' and end_row < start_row:  # red moves up
            return True
    
    # Capture move (2 squares diagonally)
    if abs(end_row - start_row) == 2 and abs(end_col - start_col) == 2:
        mid_row = (start_row + end_row) // 2
        mid_col = (start_col + end_col) // 2
        captured_piece = self.board[mid_row][mid_col]
        
        if piece.isupper():  # king can capture in any direction
            return captured_piece != ' ' and captured_piece.lower() != piece.lower()
        elif piece == 'b' and end_row > start_row:  # black captures downward
            return captured_piece != ' ' and captured_piece.lower() == 'r'
        elif piece == 'r' and end_row < start_row:  # red captures upward
            return captured_piece != ' ' and captured_piece.lower() == 'b'
    
    return False
```
- Validates move legality based on:
  - Board boundaries
  - Piece ownership
  - Movement rules (diagonal)
  - Capture rules
  - King movement rules

### Move Execution
```python
def make_move(self, start: Tuple[int, int], end: Tuple[int, int]) -> bool:
    if not self.is_valid_move(start, end):
        return False
    
    start_row, start_col = start
    end_row, end_col = end
    piece = self.board[start_row][start_col]
    
    # Regular move
    if abs(end_row - start_row) == 1:
        self.board[end_row][end_col] = piece
        self.board[start_row][start_col] = ' '
        self.move_count += 1
    
    # Capture move
    else:
        mid_row = (start_row + end_row) // 2
        mid_col = (start_col + end_col) // 2
        self.board[end_row][end_col] = piece
        self.board[start_row][start_col] = ' '
        self.board[mid_row][mid_col] = ' '
        self.capture_count += 1
        self.move_count = 0
    
    # King promotion
    if piece == 'b' and end_row == 7:
        self.board[end_row][end_col] = 'B'
    elif piece == 'r' and end_row == 0:
        self.board[end_row][end_col] = 'R'
    
    self.move_history.append((start, end))
    
    # Store board state for repetition check
    if abs(end_row - start_row) == 1:
        self.board_states.append(copy.deepcopy(self.board))
        if len(self.board_states) > 3:
            self.board_states.pop(0)
    
    return True
```
- Executes valid moves
- Handles regular moves and captures
- Manages king promotion
- Tracks move history and board states

### Valid Move Generation
```python
def get_valid_moves(self, player: str) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
    valid_moves = []
    capture_moves = []
    
    for row in range(8):
        for col in range(8):
            piece = self.board[row][col]
            if piece != ' ' and piece.lower() == player:
                # Check all possible moves
                for drow in [-2, -1, 1, 2]:
                    for dcol in [-2, -1, 1, 2]:
                        if abs(drow) == abs(dcol):
                            end_row, end_col = row + drow, col + dcol
                            if self.is_valid_move((row, col), (end_row, end_col)):
                                move = ((row, col), (end_row, end_col))
                                if abs(drow) == 2:  # capture move
                                    capture_moves.append(move)
                                else:  # regular move
                                    valid_moves.append(move)
    
    return capture_moves if capture_moves else valid_moves
```
- Generates all valid moves for a player
- Prioritizes capture moves
- Considers both regular and king pieces

### Board Evaluation
```python
def evaluate_board(self) -> float:
    score = 0
    piece_values = {
        'r': 1, 'R': 3,  # Regular piece = 1, King = 3
        'b': -1, 'B': -3
    }
    
    # Count pieces and calculate material advantage
    black_pieces = 0
    red_pieces = 0
    for row in range(8):
        for col in range(8):
            piece = self.board[row][col]
            if piece != ' ':
                if piece.lower() == 'b':
                    black_pieces += 1
                else:
                    red_pieces += 1
                score += piece_values[piece]
    
    # Add significant bonus for material advantage
    if self.current_player == 'r':
        score += (red_pieces - black_pieces) * 10
    else:
        score += (black_pieces - red_pieces) * 10
    
    # Penalize repetitive moves
    if len(self.move_history) >= 4:
        last_four_moves = self.move_history[-4:]
        if (last_four_moves[0] == last_four_moves[2] and 
            last_four_moves[1] == last_four_moves[3]):
            score -= 1000
    
    return score
```
- Evaluates board state for AI decision making
- Considers piece values and material advantage
- Penalizes repetitive moves

### Minimax Algorithm
```python
def minimax(self, depth: int, alpha: float, beta: float, maximizing: bool) -> Tuple[float, Optional[Tuple[Tuple[int, int], Tuple[int, int]]]]:
    self.nodes_explored += 1
    
    if depth == 0 or self.is_game_over():
        return self.evaluate_board(), None
    
    valid_moves = self.get_valid_moves(self.current_player)
    if not valid_moves:
        return float('-inf') if maximizing else float('inf'), None
    
    best_move = None
    if maximizing:
        max_eval = float('-inf')
        for move in valid_moves:
            start, end = move
            piece = self.board[start[0]][start[1]]
            self.make_move(start, end)
            self.current_player = 'r' if self.current_player == 'b' else 'b'
            
            eval_score, _ = self.minimax(depth - 1, alpha, beta, False)
            
            self.current_player = 'r' if self.current_player == 'b' else 'b'
            self.board[start[0]][start[1]] = piece
            self.board[end[0]][end[1]] = ' '
            
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in valid_moves:
            start, end = move
            piece = self.board[start[0]][start[1]]
            self.make_move(start, end)
            self.current_player = 'r' if self.current_player == 'b' else 'b'
            
            eval_score, _ = self.minimax(depth - 1, alpha, beta, True)
            
            self.current_player = 'r' if self.current_player == 'b' else 'b'
            self.board[start[0]][start[1]] = piece
            self.board[end[0]][end[1]] = ' '
            
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval, best_move
```
- Implements minimax algorithm with alpha-beta pruning
- Recursively evaluates possible moves
- Tracks nodes explored
- Returns best move and evaluation score

### AI Move
```python
def ai_move(self, player: str) -> None:
    self.nodes_explored = 0
    start_time = time.time()
    
    _, best_move = self.minimax(4, float('-inf'), float('inf'), player == 'b')
    
    if best_move:
        self.make_move(best_move[0], best_move[1])
        self.current_player = 'r' if self.current_player == 'b' else 'b'
    
    end_time = time.time()
    print(f"AI {1 if player == 'b' else 2}'s turn ({'Black' if player == 'b' else 'Red'})")
    print(f"AI {1 if player == 'b' else 2} nodes explored: {self.nodes_explored}")
    print(f"AI {1 if player == 'b' else 2} search time: {end_time - start_time:.2f} seconds")
```
- Executes AI move using minimax
- Measures performance metrics
- Prints AI statistics

### Human Move
```python
def human_move(self) -> None:
    while True:
        try:
            start = tuple(map(int, input("Enter start position (row col): ").split()))
            end = tuple(map(int, input("Enter end position (row col): ").split()))
            
            if self.make_move(start, end):
                self.current_player = 'r' if self.current_player == 'b' else 'b'
                break
            else:
                print("Invalid move! Try again.")
        except ValueError:
            print("Invalid input! Please enter two numbers separated by space.")
```
- Handles human player input
- Validates and executes moves
- Provides error feedback

### Game Over Check
```python
def is_game_over(self) -> bool:
    black_pieces = 0
    red_pieces = 0
    
    for row in range(8):
        for col in range(8):
            if self.board[row][col].lower() == 'b':
                black_pieces += 1
            elif self.board[row][col].lower() == 'r':
                red_pieces += 1
    
    # Check win conditions
    if black_pieces == 0 or red_pieces == 0:
        return True
    
    # Check for valid moves
    current_moves = self.get_valid_moves(self.current_player)
    if not current_moves:
        return True
    
    # Check for threefold repetition
    if len(self.board_states) == 3:
        if (np.array_equal(self.board_states[0], self.board_states[1]) and 
            np.array_equal(self.board_states[1], self.board_states[2])):
            return True
    
    # Check for 100 moves without capture
    if self.move_count >= 100:
        return True
    
    # Check for repetitive moves
    if len(self.move_history) >= 4:
        last_four_moves = self.move_history[-4:]
        if (last_four_moves[0] == last_four_moves[2] and 
            last_four_moves[1] == last_four_moves[3]):
            return True
    
    return False
```
- Checks various game over conditions:
  - No pieces remaining
  - No valid moves
  - Threefold repetition
  - 100 moves without capture
  - Repetitive moves

### Main Game Loop
```python
def main():
    game = CheckersGame()
    game.initialize_board()
    
    while True:
        print("\nCheckers Game Menu:")
        print("1. Human vs AI")
        print("2. AI vs Human")
        print("3. AI vs AI")
        print("4. Human vs Human")
        print("5. Exit")
        
        choice = input("Enter your choice (1-5): ")
        
        if choice == '1':
            while not game.is_game_over():
                game.print_board()
                game.human_move()
                if not game.is_game_over():
                    game.print_board()
                    game.ai_move('r')
        elif choice == '2':
            while not game.is_game_over():
                game.print_board()
                game.ai_move('b')
                if not game.is_game_over():
                    game.print_board()
                    game.human_move()
        elif choice == '3':
            while not game.is_game_over():
                game.print_board()
                game.ai_move('b')
                if not game.is_game_over():
                    game.print_board()
                    game.ai_move('r')
        elif choice == '4':
            while not game.is_game_over():
                game.print_board()
                game.human_move()
                if not game.is_game_over():
                    game.print_board()
                    game.human_move()
        elif choice == '5':
            break
        else:
            print("Invalid choice! Please try again.")
        
        # Determine winner
        black_pieces = sum(1 for row in game.board for piece in row if piece.lower() == 'b')
        red_pieces = sum(1 for row in game.board for piece in row if piece.lower() == 'r')
        
        if black_pieces == 0:
            winner = "Red"
        elif red_pieces == 0:
            winner = "Black"
        elif not game.get_valid_moves('b'):
            winner = "Red"
        elif not game.get_valid_moves('r'):
            winner = "Black"
        elif len(game.board_states) == 3 and \
             np.array_equal(game.board_states[0], game.board_states[1]) and \
             np.array_equal(game.board_states[1], game.board_states[2]):
            winner = "Draw"
        elif game.move_count >= 100:
            winner = "Draw"
        else:
            winner = "Draw"
        
        print(f"\nGame Over! Winner: {winner}")
        game = CheckersGame()
        game.initialize_board()

if __name__ == "__main__":
    main()
```
- Implements game menu and modes
- Manages game flow
- Determines winner
- Handles game restart 