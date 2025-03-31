# Enhanced AI Agent Line-by-Line Explanation

## Imports
```python
import numpy as np
from board import Board
import random
import math
```
- `numpy`: For efficient array operations
- `board`: Imports the Board class for game state management
- `random`: For simulated annealing random moves
- `math`: For mathematical operations in simulated annealing

## AI Class Definition
```python
class EnhancedConnectFourAI:
    def __init__(self, max_depth=4, strategy='minimax'):
        self.max_depth = max_depth
        self.strategy = strategy
        self.temperature = 1.0  # For simulated annealing
```
- Creates AI class with configurable parameters
- `max_depth`: How many moves ahead to look (default 4)
- `strategy`: Which AI strategy to use (default 'minimax')
- `temperature`: Controls randomness in simulated annealing

## Main Move Selection
```python
def get_move(self, board):
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
```
- Main entry point for AI moves
- Gets list of valid moves
- Selects appropriate strategy based on setting
- Falls back to minimax if strategy invalid

## Minimax Implementation
```python
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
```
- Implements minimax with alpha-beta pruning
- Initializes best score and move tracking
- Evaluates each possible move
- Uses alpha-beta pruning for optimization

## Hill Climbing Implementation
```python
def hill_climbing_move(self, board):
    moves = board.get_valid_moves()
    if not moves:
        return None
        
    move_scores = []
    for move in moves:
        score = self.evaluate_position(board, move)
        move_scores.append((move, score))
    
    current_move, current_score = max(move_scores, key=lambda x: x[1])
    
    for _ in range(10):
        better_move_found = False
        for move in moves:
            if move == current_move:
                continue
                
            score = self.evaluate_position(board, move)
            if score > current_score:
                current_move = move
                current_score = score
                better_move_found = True
        
        if not better_move_found:
            break
```
- Implements local search optimization
- Evaluates all initial moves
- Iteratively improves move selection
- Stops when no better moves found

## Simulated Annealing Implementation
```python
def simulated_annealing_move(self, board):
    current_move = random.choice(board.get_valid_moves())
    current_score = self.evaluate_position(board, current_move)
    best_move = current_move
    best_score = current_score
    temperature = self.temperature
    
    for _ in range(20):
        if temperature < 0.1:
            break
            
        next_move = random.choice(board.get_valid_moves())
        next_score = self.evaluate_position(board, next_move)
        
        delta = next_score - current_score
        if delta > 0 or random.random() < math.exp(delta / temperature):
            current_move = next_move
            current_score = next_score
            
            if current_score > best_score:
                best_move = current_move
                best_score = current_score
        
        temperature *= 0.9
```
- Implements temperature-based exploration
- Randomly explores moves
- Accepts worse moves based on temperature
- Gradually cools down (reduces randomness)

## Position Evaluation
```python
def evaluate_position(self, board, move):
    score = 0
    board.make_move(move)
    
    score += self._evaluate_center_control(board) * 3
    score += self._evaluate_winning_potential(board) * 10
    score += self._evaluate_blocking_opponent(board) * 8
    score += self._evaluate_connectivity(board) * 5
    
    board.undo_move(move)
    return score
```
- Evaluates board position after a move
- Combines multiple heuristic components
- Each component has different weight
- Undoes move after evaluation

## Evaluation Components

### Center Control
```python
def _evaluate_center_control(self, board):
    center_col = board.cols // 2
    center_count = 0
    for row in range(board.rows):
        if board.board[row][center_col] == 2:
            center_count += 1
    return center_count
```
- Evaluates control of center columns
- Counts AI pieces in center
- Weight: 3

### Winning Potential
```python
def _evaluate_winning_potential(self, board):
    score = 0
    for col in board.get_valid_moves():
        board.make_move(col)
        if board.check_winner() == 2:
            score += 100
        board.undo_move(col)
    return score
```
- Checks for immediate winning moves
- Weight: 10

### Opponent Blocking
```python
def _evaluate_blocking_opponent(self, board):
    score = 0
    for col in board.get_valid_moves():
        board.make_move(col)
        board.current_player = 1
        for opp_col in board.get_valid_moves():
            board.make_move(opp_col)
            if board.check_winner() == 1:
                score -= 50
            board.undo_move(opp_col)
        board.current_player = 2
        board.undo_move(col)
    return score
```
- Evaluates need to block opponent wins
- Weight: 8

### Connectivity
```python
def _evaluate_connectivity(self, board):
    score = 0
    directions = [(0,1), (1,0), (1,1), (1,-1)]
    
    for row in range(board.rows):
        for col in range(board.cols):
            if board.board[row][col] == 2:
                for dr, dc in directions:
                    connected = 0
                    r, c = row, col
                    while (0 <= r < board.rows and 0 <= c < board.cols and 
                           board.board[r][c] == 2):
                        connected += 1
                        r += dr
                        c += dc
                    score += connected ** 2
    return score
```
- Evaluates piece connections
- Checks all directions
- Weight: 5

## Minimax Helper
```python
def _minimax(self, board, depth, is_maximizing, alpha, beta):
    if depth == 0 or board.is_terminal():
        if board.is_terminal():
            winner = board.check_winner()
            if winner == 2:
                return float('inf')
            elif winner == 1:
                return float('-inf')
            else:
                return 0
        valid_moves = board.get_valid_moves()
        if not valid_moves:
            return 0
        return self.evaluate_position(board, valid_moves[0])
```
- Recursive minimax implementation
- Handles terminal states
- Uses alpha-beta pruning
- Returns evaluation scores 