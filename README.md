# Quarto AI with Q-Learning

## Overview
This project implements an AI to play the abstract strategy game Quarto using Q-Learning, a reinforcement learning algorithm. Quarto is a two-player game played on a 4x4 board with 16 unique pieces. Each piece has four attributes: color, height, shape, and consistency. The goal is to place the fourth piece in a row where all pieces share at least one attribute. The catch is that your opponent chooses the piece you have to play.

## Features
- Implementation of the Q-Learning algorithm to train the AI for strategic gameplay.
- A configurable game environment that allows for easy adjustments to game rules or AI behavior.
- A user-friendly interface to play against the AI, including a graphical interface using Pygame.

## Getting Started
### Prerequisites
- Python 3.8 or newer
- Pygame (for the graphical interface)

### Installation
1. Clone this repository or download the source code.
2. Install Pygame by running:
    ```bash
    pip install pygame
    ```

### How to Play

1. **Choosing a Piece**: Unlike traditional games, in Quarto, your opponent selects the piece you will place on the board.
2. **Placing a Piece**: On your turn, you place the piece given by your opponent on any vacant square on the board.
3. **Winning the Game**: You win by placing a piece that completes a row, column, or diagonal with four pieces sharing at least one common attribute.
4. **Draw**: The game ends in a draw if the board is filled without any player completing a winning line.

## How It Works
### The Q-Learning Algorithm
Q-Learning is a model-free reinforcement learning algorithm that aims to learn the value of an action in a particular state. The AI uses the Q-Learning algorithm to learn the optimal strategy for playing Quarto by iteratively improving its policy based on the rewards received from different game states and actions.

#### Q-Values
Q-Values (or action-value function) represent the expected future rewards for an action taken in a given state. The AI updates these Q-values during training to reflect the learned optimal strategy.

#### Training Process
1. **Initialize Q-Table**: The Q-table is initialized with arbitrary values.
2. **Choose Action**: The AI selects an action using an epsilon-greedy policy to balance exploration and exploitation.
3. **Perform Action**: The chosen action is performed, and the new state is observed.
4. **Update Q-Value**: The Q-value for the state-action pair is updated using the Q-Learning update rule:
   \[
   Q(s, a) \leftarrow Q(s, a) + \alpha \left[ r + \gamma \max_{a'} Q(s', a') - Q(s, a) \right]
   \]
   where:
   - \( \alpha \) is the learning rate
   - \( \gamma \) is the discount factor
   - \( r \) is the reward received
   - \( s' \) is the new state after performing action \( a \)

### Game Rules
The aim of Quarto is to place the fourth piece in a row (horizontally, vertically, or diagonally) where all pieces have at least one attribute in common. The game is played on a 4x4 board, and there are 16 unique pieces. Each piece has four characteristics: color (light or dark), height (tall or short), shape (round or square), and consistency (solid or hollow).

### AI Strategy
The AI employs Q-Learning to learn the optimal strategy for both selecting pieces for the opponent and placing pieces on the board. Key strategies include:

- **Immediate Wins**: Prioritizing moves that result in an immediate win.
- **Blocking Opponent's Win**: Identifying and blocking any potential winning moves by the opponent.
- **Strategic Piece Selection**: Choosing pieces for the opponent that minimize their chances of creating a winning line on their next turn.

By continuously learning from gameplay, the AI becomes more challenging and adaptive over time.

## Usage
To start the game with the graphical interface, run the following command:
```bash
python main.py


By considering these factors, our AI aims to be a challenging yet beatable opponent, making the game enjoyable for players of all skill levels.

## Developers

- Murilo Sena
- Erik Zaina
- Lucas Gonçalo
