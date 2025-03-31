# Connect4 Game with AI

A Python implementation of the classic Connect4 game featuring an AI opponent using the Minimax algorithm with Alpha-Beta pruning.

## Description

This project implements the Connect4 game where players take turns dropping colored discs into a vertical grid. The objective is to connect four discs of the same color horizontally, vertically, or diagonally before the opponent does. The game features:

- A graphical user interface using Pygame
- An AI opponent using the Minimax algorithm with Alpha-Beta pruning
- Human vs AI gameplay
- Visual feedback for moves and game state

## Prerequisites

- Python 3.x
- Pygame
- NumPy

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Connect4_v1.0.git
cd Connect4_v1.0
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## How to Run the Game

1. Navigate to the project directory:
```bash
cd Connect4_v1.0
```

2. Run the main game file:
```bash
python main.py
```

3. Game Controls:
   - Use the mouse to click on the column where you want to drop your disc
   - The AI will automatically make its move after yours
   - The game will announce the winner when someone connects four discs

## Project Structure

- `main.py`: Contains the main game loop and UI implementation
- `board.py`: Implements the game board logic and move validation
- `enhanced_ai_agent.py`: Contains the AI implementation using Minimax with Alpha-Beta pruning
- `requirements.txt`: Lists all project dependencies

## Features

- Interactive graphical interface
- AI opponent using Minimax algorithm with Alpha-Beta pruning
- Real-time game state updates
- Win detection for all possible winning combinations
- Visual feedback for player moves and game status

## Game Rules

1. Players take turns dropping colored discs into a 6x7 grid
2. The first player to connect four discs of their color wins
3. Winning combinations can be:
   - Horizontal (4 discs in a row)
   - Vertical (4 discs in a column)
   - Diagonal (4 discs diagonally)
4. The game ends when:
   - A player wins
   - The board is full (draw)

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Pygame library for the graphical interface
- NumPy for efficient array operations
- Connect4 game concept by Milton Bradley 