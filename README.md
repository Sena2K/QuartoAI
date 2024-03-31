# Quarto AI with Minimax Alpha-Beta Pruning

## Overview
This project implements an AI to play the abstract strategy game Quarto using the Minimax algorithm with Alpha-Beta pruning optimization. Quarto is a two-player game played on a 4x4 board with 16 unique pieces. Each piece has four attributes: color, height, shape, and consistency. The goal is to place the fourth piece in a row where all pieces share at least one attribute. The catch is that your opponent chooses the piece you have to play.

## Features
- Implementation of the Minimax algorithm with Alpha-Beta pruning to efficiently decide the best move.
- A configurable game environment that allows for easy adjustments to game rules or AI behavior.
- A user-friendly interface to play against the AI.

## Getting Started
### Prerequisites
- Python 3.8 or newer
- (Optional) Requirements for a GUI, if implemented

### Installation
1. Clone this repository or download the source code.
2. (Optional) Install any dependencies, if required.

### How to Play

1. **Choosing a Piece**: Unlike traditional games, in Quarto, your opponent selects the piece you will place on the board.
2. **Placing a Piece**: On your turn, you place the piece given by your opponent on any vacant square on the board.
3. **Winning the Game**: You win by placing a piece that completes a row, column, or diagonal with four pieces sharing at least one common attribute.
4. **Draw**: The game ends in a draw if the board is filled without any player completing a winning line.

## How It Works
### The Minimax Algorithm with Alpha-Beta Pruning
The core of our Quarto AI game lies in the Minimax algorithm, optimized with Alpha-Beta pruning. This section dives into how these concepts empower our AI to make strategic decisions and efficiently navigate the vast space of possible game states.

Understanding Minimax
The Minimax algorithm is a decision rule used for minimizing the possible loss for a worst-case scenario. When dealing with AI in games, this translates to optimizing the AI's move considering the best response from the opponent. The algorithm explores all possible moves in the game tree by alternating between maximizing and minimizing players, predicting their moves to determine the best possible outcome.

Optimizing with Alpha-Beta Pruning
Alpha-Beta pruning enhances the Minimax algorithm by reducing the number of nodes that are evaluated in the search tree. It does this by maintaining two values, alpha and beta, which represent the minimum score that the maximizing player is assured of and the maximum score that the minimizing player is assured of, respectively. When it becomes clear that a certain branch does not have the potential to influence the final decision, it is pruned, significantly reducing the search space and computation time.

### Game Rules
The aim of Quarto is to place the fourth piece in a row (horizontally, vertically, or diagonally) where all pieces have at least one attribute in common. The game is played on a 4x4 board, and there are 16 unique pieces. Each piece has four characteristics: color (light or dark), height (tall or short), shape (round or square), and consistency (solid or hollow).

### AI Strategy

Our AI uses the rules of Quarto to its advantage by analyzing the board state to determine the best piece to give to the opponent and the optimal placement for its pieces. It employs the Minimax algorithm with Alpha-Beta pruning to simulate future moves and counter-moves, aiming to maximize its chances of winning while minimizing the opponent's opportunities to win. The AI evaluates each potential board state based on:

- **Immediate Wins**: If a move results in an immediate win, it is given the highest priority.
- **Blocking Opponent's Win**: The AI identifies and blocks any potential winning moves by the opponent.
- **Strategic Piece Selection**: It chooses pieces for the opponent that minimize their chances of creating a winning line on their next turn.

By considering these factors, our AI aims to be a challenging yet beatable opponent, making the game enjoyable for players of all skill levels.

## Developers

- Murilo Sena
- Erik Zaina
- Lucas Gonçalo
