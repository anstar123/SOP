# Connect4 AI Agent

A smart computer player for the Connect4 game that can play using different strategies.

## What is this?

This is a computer program that can play Connect4 against you. It uses different ways of thinking (called strategies) to make its moves. The computer can play using three different strategies:
- Minimax (very smart)
- Hill Climbing (medium difficulty)
- Simulated Annealing (changes difficulty)

## How to Set Up

1. Make sure you have Python installed on your computer
2. Install the needed programs:
```bash
pip install -r requirements.txt
```

## How to Play

1. Start the game:
```bash
python main.py
```

2. Choose who goes first:
   - Press 'A' to let the computer go first
   - Press 'S' to go first yourself

3. During the game:
   - Click on any column to drop your piece
   - The computer will automatically make its move
   - You can change the computer's strategy anytime:
     - Press '1' for Minimax (hardest)
     - Press '2' for Hill Climbing (medium)
     - Press '3' for Simulated Annealing (changes difficulty)
   - Press 'R' to restart the game

## Game Rules

1. The game board has 6 rows and 7 columns
2. You and the computer take turns dropping pieces
3. Pieces fall to the lowest available spot in the column
4. First player to connect 4 pieces in a row (horizontally, vertically, or diagonally) wins
5. If the board fills up with no winner, it's a draw

## Tips to Win

1. Try to control the middle columns
2. Look for ways to create multiple winning chances at once
3. Block the computer's winning moves
4. Build your pieces from the bottom up
5. Try to create diagonal patterns

## How the Computer Thinks

The computer uses different ways to make its moves:

1. **Minimax Strategy**
   - Looks ahead several moves
   - Tries to make the best possible move
   - Hardest to beat

2. **Hill Climbing Strategy**
   - Makes moves that improve its position
   - Medium difficulty
   - Can get stuck in local solutions

3. **Simulated Annealing Strategy**
   - Sometimes makes random moves
   - Difficulty changes during the game
   - Can surprise you with unexpected moves

## Files in the Project

- `main.py`: The main game file
- `board.py`: Handles the game board
- `enhanced_ai_agent.py`: Contains the computer's thinking strategies
- `requirements.txt`: Lists the programs needed to run the game

## Thanks

- The Connect4 game idea
- Pygame for making the game look nice
- NumPy for helping the computer think faster
- The AI community for the strategies used 
