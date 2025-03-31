# Board.py Line-by-Line Explanation

## Imports
```python
import numpy as np
```
- Imports NumPy library for efficient array operations
- Used for creating and manipulating the game board

## Board Class Definition
```python
class Board:
    def __init__(self, rows=6, cols=7):
        self.rows = rows
        self.cols = cols
        self.board = np.zeros((rows, cols), dtype=int)
        self.current_player = 1  # Default to player 1
```
- Creates a Board class to manage the game state
- `__init__`: Constructor method
  - `rows=6`: Default board height (6 rows)
  - `cols=7`: Default board width (7 columns)
  - `np.zeros()`: Creates empty 6x7 array filled with zeros
  - `current_player=1`: Sets human player as default first player

## Player Management
```python
def set_first_player(self, player):
    """Set who moves first (1 for human, 2 for AI)"""
    self.current_player = player
```
- Allows setting which player goes first
- `player=1`: Human player
- `player=2`: AI player

## Move Validation
```python
def is_valid_move(self, col):
    return 0 <= col < self.cols and self.board[0][col] == 0
```
- Checks if a move is valid
- `0 <= col < self.cols`: Ensures column is within bounds
- `self.board[0][col] == 0`: Checks if top row is empty in that column
- Returns True if move is valid, False otherwise

## Making Moves
```python
def make_move(self, col):
    if not self.is_valid_move(col):
        return False
    
    # Find the lowest empty row in the selected column
    for row in range(self.rows - 1, -1, -1):
        if self.board[row][col] == 0:
            self.board[row][col] = self.current_player
            self.current_player = 3 - self.current_player  # Switch between 1 and 2
            return True
    return False
```
- Places a piece in the specified column
- `if not self.is_valid_move(col)`: Validates move first
- `range(self.rows - 1, -1, -1)`: Iterates from bottom to top
- Places piece in lowest empty position
- Switches current player (1→2 or 2→1)
- Returns True if move successful, False otherwise

## Undoing Moves
```python
def undo_move(self, col):
    for row in range(self.rows):
        if self.board[row][col] != 0:
            self.board[row][col] = 0
            self.current_player = 3 - self.current_player
            return True
    return False
```
- Removes the top piece from a column
- Used by AI for move evaluation
- Switches player back
- Returns True if successful, False otherwise

## Win Detection
```python
def check_winner(self):
    # Check horizontal
    for row in range(self.rows):
        for col in range(self.cols - 3):
            if (self.board[row][col] != 0 and
                self.board[row][col] == self.board[row][col + 1] == 
                self.board[row][col + 2] == self.board[row][col + 3]):
                return self.board[row][col]
```
- Checks for horizontal wins
- Looks for 4 consecutive same pieces in a row

```python
    # Check vertical
    for row in range(self.rows - 3):
        for col in range(self.cols):
            if (self.board[row][col] != 0 and
                self.board[row][col] == self.board[row + 1][col] == 
                self.board[row + 2][col] == self.board[row + 3][col]):
                return self.board[row][col]
```
- Checks for vertical wins
- Looks for 4 consecutive same pieces in a column

```python
    # Check diagonal (positive slope)
    for row in range(3, self.rows):
        for col in range(self.cols - 3):
            if (self.board[row][col] != 0 and
                self.board[row][col] == self.board[row - 1][col + 1] == 
                self.board[row - 2][col + 2] == self.board[row - 3][col + 3]):
                return self.board[row][col]
```
- Checks for diagonal wins (positive slope)
- Looks for 4 consecutive same pieces diagonally up-right

```python
    # Check diagonal (negative slope)
    for row in range(self.rows - 3):
        for col in range(self.cols - 3):
            if (self.board[row][col] != 0 and
                self.board[row][col] == self.board[row + 1][col + 1] == 
                self.board[row + 2][col + 2] == self.board[row + 3][col + 3]):
                return self.board[row][col]
```
- Checks for diagonal wins (negative slope)
- Looks for 4 consecutive same pieces diagonally down-right

```python
    # Check for draw
    if np.all(self.board != 0):
        return 0
    
    return None
```
- Checks if board is full (draw)
- Returns:
  - 1: Human wins
  - 2: AI wins
  - 0: Draw
  - None: Game continues

## Game State Management
```python
def get_valid_moves(self):
    return [col for col in range(self.cols) if self.is_valid_move(col)]
```
- Returns list of all valid columns for next move

```python
def is_terminal(self):
    return self.check_winner() is not None
```
- Checks if game is over (win or draw)

```python
def get_state(self):
    return self.board.copy()
```
- Returns a copy of current board state
- Used by AI for evaluation 