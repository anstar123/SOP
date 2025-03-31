# Connect4 AI Agent

An advanced AI agent implementation for the Connect4 game using multiple search strategies and optimization techniques.

## Description

This project focuses on developing and training an AI agent to play Connect4 using various artificial intelligence techniques. The agent implements multiple strategies including Minimax with Alpha-Beta pruning, Hill Climbing, and Simulated Annealing. The agent is designed to play against human opponents in an existing Connect4 game implementation.

## AI Features

- **Multiple Search Strategies**:
  - Minimax with Alpha-Beta pruning
  - Hill Climbing optimization
  - Simulated Annealing for global optimization

- **Advanced Evaluation Function**:
  - Center control evaluation
  - Winning potential assessment
  - Opponent blocking strategy
  - Piece connectivity analysis

- **Optimization Techniques**:
  - Alpha-Beta pruning for improved search efficiency
  - Configurable search depth
  - Temperature-based simulated annealing
  - Adaptive hill climbing

## Prerequisites

- Python 3.x
- Pygame (for the game interface)
- NumPy (for efficient array operations)

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

## Project Structure

- `enhanced_ai_agent.py`: Core AI implementation with multiple strategies
- `board.py`: Game board interface for the AI agent
- `main.py`: Game interface and AI integration
- `requirements.txt`: Project dependencies

## AI Agent Implementation Details

### Search Strategies

1. **Minimax with Alpha-Beta Pruning**
   - Implements depth-limited minimax search
   - Uses alpha-beta pruning for optimization
   - Configurable search depth

2. **Hill Climbing**
   - Local search optimization
   - Iterative improvement of move selection
   - Prevents getting stuck in local optima

3. **Simulated Annealing**
   - Temperature-based exploration
   - Allows occasional worse moves to escape local optima
   - Adaptive cooling schedule

### Evaluation Function Components

1. **Center Control**
   - Evaluates control of center columns
   - Weighted importance for strategic advantage

2. **Winning Potential**
   - Identifies immediate winning opportunities
   - Prioritizes winning moves

3. **Opponent Blocking**
   - Prevents opponent's winning moves
   - Strategic defensive play

4. **Connectivity Analysis**
   - Evaluates piece connections
   - Considers multiple directions (horizontal, vertical, diagonal)

## Game Manual

### Overview
Connect4 is a two-player strategy game where players take turns dropping colored discs into a vertical grid. The objective is to connect four discs of the same color horizontally, vertically, or diagonally before the opponent does.

### Game Rules
1. **Board Setup**
   - 6 rows × 7 columns grid
   - Empty at the start
   - Players use different colored discs (typically red and yellow)

2. **Gameplay**
   - Players take turns dropping one disc at a time
   - Discs are placed in the lowest available position in the chosen column
   - Players cannot place discs in full columns
   - The game continues until a winner is determined or the board is full

3. **Winning Conditions**
   - Connect four discs of the same color in any of these patterns:
     - Horizontal (4 discs in a row)
     - Vertical (4 discs in a column)
     - Diagonal (4 discs diagonally)
   - First player to achieve this wins
   - If the board fills up without a winner, the game is a draw

4. **Controls**
   - Use mouse to select a column
   - Click on the desired column to drop your disc
   - The AI will automatically make its move after yours

### Tips for Playing Against the AI
1. **Strategic Play**
   - Control the center columns when possible
   - Create multiple winning threats simultaneously
   - Block the AI's potential winning moves

2. **Common Strategies**
   - Build from the bottom up
   - Create diagonal patterns
   - Force the AI to block your moves
   - Look for opportunities to create multiple winning threats

3. **Difficulty Levels**
   - The AI uses different strategies that can be selected:
     - Minimax: Most challenging, uses perfect play
     - Hill Climbing: Medium difficulty, uses local optimization
     - Simulated Annealing: Varies in difficulty based on temperature

## Usage

1. Run the game with the AI agent:
```bash
python main.py
```

2. Select your preferred AI strategy in the game settings:
   - Minimax (default)
   - Hill Climbing
   - Simulated Annealing

3. Play against the AI:
   - Use mouse to select columns
   - AI will automatically respond with its chosen strategy

## Performance

The AI agent demonstrates strong performance through:
- Efficient move evaluation
- Strategic decision making
- Multiple optimization techniques
- Adaptive play style

## Contributing

Feel free to submit issues and enhancement requests for the AI agent implementation!

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Connect4 game implementation (external source)
- Pygame for the game interface
- NumPy for efficient array operations
- AI/ML community for search and optimization algorithms 
