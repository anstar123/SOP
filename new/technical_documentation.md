# Connect4 Game Technical Documentation

## Overview
This document provides a detailed technical explanation of the Connect4 game implementation, focusing on the three main Python files: `board.py`, `ai_agent.py`, and `main.py`.

```
Project Structure:
├── main.py              # Game interface and main loop
├── board.py            # Game board logic
├── ai_agent.py         # AI implementation
└── requirements.txt    # Project dependencies
```

## 1. Board Implementation (board.py)

### Class: Board
The `Board` class manages the game board state and core game logic.

#### Board Representation:
```
   0 1 2 3 4 5 6
5 | | | | | | | |
4 | | | | | | | |
3 | | | | | | | |
2 | | | | | | | |
1 | | | | | | | |
0 | | | | | | | |
   ---------------
```

#### Key Components:

1. **Initialization**
   ```python
   def __init__(self, rows=6, cols=7):
       self.rows = rows
       self.cols = cols
       self.board = np.zeros((rows, cols), dtype=int)
       self.current_player = 1
   ```
   - Creates a 6x7 grid using NumPy
   - Initializes empty board (0 represents empty)
   - Sets default first player to 1 (human)

2. **Move Management**
   - `set_first_player(player)`: Sets who moves first (1=human, 2=AI)
   - `is_valid_move(col)`: Checks if a move is valid
   - `make_move(col)`: Places a piece in the lowest available position
   - `undo_move(col)`: Removes a piece (used by AI for move evaluation)

3. **Win Detection**
   - `check_winner()`: Checks for winning conditions in:
     - Horizontal lines
     - Vertical lines
     - Diagonal lines (both directions)
   - Returns:
     - 1: Human wins
     - 2: AI wins
     - 0: Draw
     - None: Game continues

4. **Game State Management**
   - `get_valid_moves()`: Returns list of valid columns
   - `is_terminal()`: Checks if game is over
   - `get_state()`: Returns current board state

## 2. AI Agent Implementation (ai_agent.py)

### Class: Connect4AI
Implements three different AI strategies for playing Connect4.

#### AI Strategy Flow:
```
┌─────────────────┐
│   Game State    │
└────────┬────────┘
         ▼
┌─────────────────┐
│ Strategy Select │
└────────┬────────┘
         ▼
┌─────────────────┐
│  Minimax (1)    │
├─────────────────┤
│ Hill Climbing(2)│
├─────────────────┤
│ Simulated(3)    │
└────────┬────────┘
         ▼
┌─────────────────┐
│   Make Move     │
└─────────────────┘
```

#### Evaluation Function Components:
```
┌─────────────────┐
│  Position Eval  │
├─────────────────┤
│ Center Control  │
│ Weight: 3       │
├─────────────────┤
│ Win Potential   │
│ Weight: 10      │
├─────────────────┤
│ Block Opponent  │
│ Weight: 8       │
├─────────────────┤
│ Connectivity    │
│ Weight: 5       │
└─────────────────┘
```

#### Key Components:

1. **Initialization**
   ```python
   def __init__(self, max_depth=4, strategy='minimax'):
       self.max_depth = max_depth
       self.strategy = strategy
       self.temp = 1.0
   ```
   - Sets search depth for minimax
   - Selects AI strategy
   - Initializes temperature for simulated annealing

2. **Strategy Selection**
   - `get_move(board)`: Main entry point for AI moves
   - Supports three strategies:
     - Minimax (default)
     - Hill Climbing
     - Simulated Annealing

3. **Minimax Implementation**
   - `get_best_move_minimax(board)`: Finds best move using minimax
   - `minimax(board, depth, is_maximizing, alpha, beta)`: Recursive minimax with alpha-beta pruning
   - Features:
     - Depth-limited search
     - Alpha-beta pruning for optimization
     - Terminal state evaluation

4. **Hill Climbing Implementation**
   - `hill_climbing_move(board)`: Uses local search optimization
   - Features:
     - Evaluates all possible moves
     - Iteratively improves move selection
     - Can get stuck in local optima

5. **Simulated Annealing Implementation**
   - `simulated_annealing_move(board)`: Uses temperature-based exploration
   - Features:
     - Random move exploration
     - Temperature-based acceptance of worse moves
     - Cooling schedule for convergence

6. **Position Evaluation**
   - `evaluate_position(board, move)`: A* inspired heuristic evaluation
   - Components:
     - Center control (weight: 3)
     - Winning potential (weight: 10)
     - Opponent blocking (weight: 8)
     - Piece connectivity (weight: 5)

## 3. Game Interface Implementation (main.py)

### Main Components:

#### Game Window Layout:
```
┌─────────────────────┐
│                     │
│   Game Board        │
│                     │
│                     │
│                     │
│                     │
│                     │
├─────────────────────┤
│ Status Bar          │
└─────────────────────┘
```

#### Control Keys:
```
┌─────────────────────┐
│ Game Controls       │
├─────────────────────┤
│ 1: Easy (Hill Climbing)│
│ 2: Medium (Simulated)  │
│ 3: Hard (Minimax)      │
│ R: Restart Game     │
│ A: AI First         │
│ S: Human First      │
└─────────────────────┘
```

1. **Initialization and Constants**
   ```python
   WINDOW_SIZE = 800
   BOARD_ROWS = 6
   BOARD_COLS = 7
   SQUARE_SIZE = WINDOW_SIZE // BOARD_COLS
   ```
   - Sets up game window and board dimensions
   - Defines color constants
   - Initializes Pygame display

2. **Graphics Functions**
   - `draw_board()`: Renders the game board
     - Draws empty slots
     - Places player pieces
     - Shows game status
     - Displays winner/draw messages
   - `draw_difficulty_menu()`: Shows difficulty selection menu
   - `draw_first_move_menu()`: Shows first move selection menu

3. **Game Flow Management**
   - `get_difficulty_choice()`: Handles difficulty selection
   - `get_first_move_choice()`: Handles initial player selection
   - `main()`: Main game loop
     - Manages game state
     - Handles user input
     - Coordinates AI moves
     - Controls game flow

4. **Event Handling**
   - Mouse clicks for moves
   - Keyboard input for:
     - Difficulty selection (1, 2, 3)
     - Game restart (R)
     - First move selection (A, S)

5. **AI Integration**
   - Maps difficulty levels to AI strategies
   - Manages AI initialization
   - Coordinates AI moves with game flow

## Technical Details

### Data Structures

#### Board State Representation:
```
┌─────────────────┐
│ 2D NumPy Array  │
├─────────────────┤
│ 0: Empty        │
│ 1: Human        │
│ 2: AI           │
└─────────────────┘
```

### Game Flow
1. Player selects difficulty level
2. Player chooses who moves first
3. Game begins with appropriate AI strategy
4. Players alternate turns
5. Game continues until:
   - A player wins
   - The board is full (draw)
   - Player restarts
6. Player can restart at any time

### AI Strategy Mapping
- Easy: Hill Climbing
  - Local search optimization
  - Fast but suboptimal moves
- Medium: Simulated Annealing
  - Temperature-based exploration
  - Balanced between speed and optimality
- Hard: Minimax with Alpha-Beta Pruning
  - Complete game tree search
  - Most optimal moves within depth limit

## Dependencies
- Python 3.x
- Pygame: For graphics and user interface
- NumPy: For efficient array operations and board management

## Usage Notes
1. The game supports three AI strategies that can be switched during gameplay
2. The AI can play first or second
3. The game can be restarted at any time
4. The interface provides visual feedback for all game states 