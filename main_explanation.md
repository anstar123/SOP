# Main.py Line-by-Line Explanation

## Imports and Initialization
```python
import pygame
import sys
from board import Board
from enhanced_ai_agent import EnhancedConnectFourAI

# Initialize Pygame
pygame.init()
```
- Imports required libraries
  - `pygame`: For graphics and user interface
  - `sys`: For system operations
  - `Board`: Game board implementation
  - `EnhancedConnectFourAI`: AI implementation
- Initializes Pygame system

## Constants and Setup
```python
# Constants
WINDOW_SIZE = 800
BOARD_ROWS = 6
BOARD_COLS = 7
SQUARE_SIZE = WINDOW_SIZE // BOARD_COLS
BOARD_HEIGHT = SQUARE_SIZE * BOARD_ROWS
PADDING = 50
TEXT_AREA_HEIGHT = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

# Set up the display
screen = pygame.display.set_mode((WINDOW_SIZE, BOARD_HEIGHT + TEXT_AREA_HEIGHT))
pygame.display.set_caption("Connect Four - AI First Move")
```
- Defines window and board dimensions
- Sets up color constants
- Creates game window with status bar

## Board Drawing Function
```python
def draw_board(board, game_over=False, winner=None, current_ai='minimax', ai_first=False):
    # Clear the entire screen with blue
    screen.fill(BLUE)
    
    # Draw the board background
    pygame.draw.rect(screen, BLUE, (0, 0, WINDOW_SIZE, BOARD_HEIGHT))
```
- Clears screen and draws board background
- Takes game state parameters for display

```python
    # Draw the pieces area background
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            pygame.draw.circle(screen, WHITE,
                             (col * SQUARE_SIZE + SQUARE_SIZE // 2,
                              row * SQUARE_SIZE + SQUARE_SIZE // 2),
                             SQUARE_SIZE // 2 - 5)
```
- Draws empty circles for board positions
- Calculates circle positions based on grid

```python
    # Draw the pieces
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board.board[row][col] != 0:
                color = YELLOW if board.board[row][col] == 2 else RED
                pygame.draw.circle(screen, color,
                                 (col * SQUARE_SIZE + SQUARE_SIZE // 2,
                                  row * SQUARE_SIZE + SQUARE_SIZE // 2),
                                 SQUARE_SIZE // 2 - 5)
```
- Draws player pieces
- Yellow for AI, Red for human

```python
    # Draw game over message
    if game_over and winner is not None:
        font = pygame.font.Font(None, 74)
        if winner == 0:
            text = font.render('Draw!', True, WHITE)
        else:
            text = font.render(f'{"AI" if winner == 2 else "Player"} Wins!', True, WHITE)
        text_rect = text.get_rect(center=(WINDOW_SIZE // 2, BOARD_HEIGHT // 2))
        s = pygame.Surface((WINDOW_SIZE, BOARD_HEIGHT))
        s.set_alpha(128)
        s.fill(BLACK)
        screen.blit(s, (0,0))
        screen.blit(text, text_rect)
```
- Shows game over message
- Displays winner or draw
- Adds semi-transparent overlay

```python
    # Draw the text area background
    pygame.draw.rect(screen, BLACK, (0, BOARD_HEIGHT, WINDOW_SIZE, TEXT_AREA_HEIGHT))
    
    # Draw the status text
    font = pygame.font.Font(None, 36)
    if not game_over:
        status_text = f"AI Strategy: {current_ai} ({'AI' if ai_first else 'Human'} moves first)"
    else:
        status_text = "Press R to restart"
    text = font.render(status_text, True, WHITE)
    text_rect = text.get_rect(center=(WINDOW_SIZE // 2, BOARD_HEIGHT + TEXT_AREA_HEIGHT // 2))
    screen.blit(text, text_rect)
```
- Draws status bar
- Shows current AI strategy and turn order
- Updates status based on game state

## Menu Drawing Function
```python
def draw_menu(screen):
    screen.fill(BLUE)
    
    # Draw title
    font = pygame.font.Font(None, 74)
    title = font.render('Who Makes First Move?', True, WHITE)
    title_rect = title.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 4))
    screen.blit(title, title_rect)
    
    # Draw instructions
    font = pygame.font.Font(None, 48)
    instructions = font.render('Press A for AI, S for Human', True, WHITE)
    instructions_rect = instructions.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2))
    screen.blit(instructions, instructions_rect)
```
- Draws initial menu screen
- Shows title and instructions
- Handles first move selection

## First Move Selection
```python
def get_first_move_choice():
    choice_made = False
    
    while not choice_made:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    return 2  # AI moves first
                elif event.key == pygame.K_s:
                    return 1  # Human moves first
        
        draw_menu(screen)
        pygame.time.Clock().tick(60)
```
- Handles initial player selection
- Waits for user input
- Returns player number (1=human, 2=AI)

## Main Game Loop
```python
def main():
    board = Board(BOARD_ROWS, BOARD_COLS)
    # Initialize AI with different strategies
    ai_agents = {
        'minimax': EnhancedConnectFourAI(max_depth=4, strategy='minimax'),
        'hill_climbing': EnhancedConnectFourAI(max_depth=4, strategy='hill_climbing'),
        'simulated_annealing': EnhancedConnectFourAI(max_depth=4, strategy='simulated_annealing')
    }
```
- Creates game board
- Initializes AI agents with different strategies

```python
    current_ai = 'minimax'  # Default strategy
    game_over = False
    winner = None
    
    while True:  # Main game loop
        # Get first move choice
        choice = get_first_move_choice()
        ai_first = (choice == 2)
        
        # Reset game state
        board = Board(BOARD_ROWS, BOARD_COLS)
        board.set_first_player(2 if ai_first else 1)
        game_over = False
        winner = None
```
- Sets up game variables
- Handles game initialization
- Manages game state

```python
        # If AI moves first
        if ai_first:
            ai_move = ai_agents[current_ai].get_move(board)
            board.make_move(ai_move)
```
- Handles AI's first move if selected

```python
        while not game_over:  # Game round loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Restart game
                        game_over = True
                        break
                    elif not game_over:  # Strategy changes
                        if event.key == pygame.K_1:
                            current_ai = 'minimax'
                        elif event.key == pygame.K_2:
                            current_ai = 'hill_climbing'
                        elif event.key == pygame.K_3:
                            current_ai = 'simulated_annealing'
```
- Main game event loop
- Handles keyboard input
- Manages strategy changes
- Handles game restart

```python
                if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                    x, y = event.pos
                    col = x // SQUARE_SIZE
                    
                    if board.is_valid_move(col):
                        if board.current_player == 1:
                            board.make_move(col)
                            
                            winner = board.check_winner()
                            if winner is not None:
                                game_over = True
                            else:
                                ai_move = ai_agents[current_ai].get_move(board)
                                if ai_move is not None and board.is_valid_move(ai_move):
                                    board.make_move(ai_move)
                                    
                                    winner = board.check_winner()
                                    if winner is not None:
                                        game_over = True
                                else:
                                    winner = 0
                                    game_over = True
```
- Handles mouse clicks for moves
- Validates moves
- Manages turn alternation
- Checks for game over conditions

```python
            # Draw the board and current AI strategy
            draw_board(board, game_over, winner, current_ai, ai_first)
            pygame.time.Clock().tick(60)  # Limit frame rate
```
- Updates display
- Maintains frame rate

```python
        # Show game over screen and wait for restart
        if winner is not None:
            waiting_for_restart = True
            while waiting_for_restart:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                        waiting_for_restart = False
                draw_board(board, game_over, winner, current_ai, ai_first)
                pygame.time.Clock().tick(60)
```
- Handles game over state
- Waits for restart command
- Maintains display

## Program Entry Point
```python
if __name__ == "__main__":
    main()
```
- Starts the game when run directly
- Calls main game loop 