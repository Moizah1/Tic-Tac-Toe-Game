# Unbeatable Tic-Tac-Toe (Pygame + Minimax)

A classic Tic-Tac-Toe game with a graphical interface built in **Pygame**, featuring a computer opponent that is mathematically **unbeatable**. The AI is powered by the **Minimax algorithm** with **alpha-beta pruning**, which exhaustively searches the game tree to always choose the optimal move.

Play against it and the best you can achieve is a **draw** — it will never lose.

## Features

- Clean, modern graphical board rendered with Pygame
- Human (**X**) vs. Computer (**O**)
- Unbeatable AI using Minimax + alpha-beta pruning
- Highlights the winning line when the game ends
- Hover highlight for the square under your cursor
- Restart anytime with a single keypress
- Runs at 60 FPS with instant AI response (pruning keeps the search fast even though it explores the full game tree)

## Requirements

- Python 3.8+
- [Pygame](https://www.pygame.org/) 2.x

## Installation

1. Clone or download this repository / copy `tic_tac_toe.py` into a folder.
2. Install Pygame:

   ```bash
   pip install pygame
   ```

## Usage

Run the game from the project folder:

```bash
python tic_tac_toe.py
```

### Controls

| Input          | Action                          |
|----------------|----------------------------------|
| Left click     | Place your mark (X) on a square |
| `R`            | Restart the game (after it ends) |
| `Esc`          | Quit the game                   |
| Close window   | Quit the game                   |

You always go first as **X**. After you click a square, the computer (**O**) automatically responds.

## How the AI Works

The computer opponent uses the **Minimax algorithm**, a decision-making technique for two-player, zero-sum games:

1. For every available move, the AI simulates the game continuing to completion, assuming both players play optimally (the AI tries to **maximize** its score, the human is assumed to **minimize** it).
2. Each terminal board state is scored:
   - `+10 - depth` → AI wins (faster wins score higher)
   - `depth - 10` → Human wins (slower losses are "less bad")
   - `0` → Draw
3. The AI picks the move that leads to the best guaranteed outcome, no matter what the human does in response.
4. **Alpha-beta pruning** skips branches of the search tree that can't possibly change the final decision, making the search essentially instantaneous despite exploring the (small but complete) tic-tac-toe game tree.

Because the algorithm considers every possible sequence of future moves, it never makes a mistake — the worst outcome you can force is a draw.

## Project Structure

```
.
├── tic_tac_toe.py   # Full game: rendering, input handling, and Minimax AI
└── README.md        # This file
```

Everything lives in a single file for simplicity — no external assets required.

## License

Free to use, modify, and share for personal or educational purposes.
