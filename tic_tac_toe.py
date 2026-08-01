"""
Unbeatable Tic-Tac-Toe
-----------------------
Human plays X, Computer plays O.
The computer uses the Minimax algorithm (with alpha-beta pruning) to search
every possible outcome of the game and always pick the move that is best
for it -- meaning it can never lose. Best case for you: a draw.

Controls:
    - Click a cell to place your mark.
    - Press R to restart after the game ends.
    - Press ESC or close the window to quit.

Run with:  python tic_tac_toe.py
"""

import sys
import pygame

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
WIDTH, HEIGHT = 600, 700          # extra height at the bottom for status text
BOARD_SIZE = 600
CELL_SIZE = BOARD_SIZE // 3
LINE_WIDTH = 8
MARK_WIDTH = 15
CIRCLE_RADIUS = CELL_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 20
SPACE = CELL_SIZE // 4

# Colors
BG_COLOR = (28, 30, 38)
BOARD_COLOR = (39, 42, 54)
LINE_COLOR = (90, 95, 115)
CIRCLE_COLOR = (95, 205, 228)   # O - human
CROSS_COLOR = (240, 110, 110)   # X - computer... wait, humans are X below
TEXT_COLOR = (230, 230, 235)
WIN_LINE_COLOR = (255, 210, 90)
HOVER_COLOR = (48, 52, 66)

HUMAN = "X"
AI = "O"
EMPTY = None

FONT_NAME = "freesansbold.ttf"


class TicTacToe:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Unbeatable Tic-Tac-Toe — Minimax AI")
        self.clock = pygame.time.Clock()

        self.font_status = pygame.font.Font(FONT_NAME, 32)
        self.font_small = pygame.font.Font(FONT_NAME, 20)

        self.reset_game()

    # -----------------------------------------------------------------
    # Game state management
    # -----------------------------------------------------------------
    def reset_game(self):
        self.board = [[EMPTY for _ in range(3)] for _ in range(3)]
        self.game_over = False
        self.winner = None          # "X", "O", or "Draw"
        self.winning_line = None    # ((r1,c1),(r2,c2),(r3,c3)) if a line won
        self.turn = HUMAN           # human always starts
        self.ai_thinking = False

    def available_moves(self, board):
        return [(r, c) for r in range(3) for c in range(3) if board[r][c] is EMPTY]

    def make_move(self, board, row, col, player):
        board[row][col] = player

    # -----------------------------------------------------------------
    # Win / draw detection
    # -----------------------------------------------------------------
    def check_winner(self, board):
        """Returns (winner_symbol_or_None, winning_line_or_None)."""
        lines = []

        # rows & columns
        for i in range(3):
            lines.append([(i, 0), (i, 1), (i, 2)])   # row i
            lines.append([(0, i), (1, i), (2, i)])   # col i

        # diagonals
        lines.append([(0, 0), (1, 1), (2, 2)])
        lines.append([(0, 2), (1, 1), (2, 0)])

        for line in lines:
            a, b, c = line
            va, vb, vc = board[a[0]][a[1]], board[b[0]][b[1]], board[c[0]][c[1]]
            if va is not EMPTY and va == vb == vc:
                return va, line

        return None, None

    def is_full(self, board):
        return all(cell is not EMPTY for row in board for cell in row)

    # -----------------------------------------------------------------
    # Minimax with alpha-beta pruning
    # -----------------------------------------------------------------
    def minimax(self, board, depth, is_maximizing, alpha, beta):
        winner, _ = self.check_winner(board)

        if winner == AI:
            return 10 - depth          # prefer faster wins
        elif winner == HUMAN:
            return depth - 10          # prefer slower losses
        elif self.is_full(board):
            return 0                   # draw

        if is_maximizing:
            best_score = float("-inf")
            for (r, c) in self.available_moves(board):
                board[r][c] = AI
                score = self.minimax(board, depth + 1, False, alpha, beta)
                board[r][c] = EMPTY
                best_score = max(best_score, score)
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break  # beta cut-off
            return best_score
        else:
            best_score = float("inf")
            for (r, c) in self.available_moves(board):
                board[r][c] = HUMAN
                score = self.minimax(board, depth + 1, True, alpha, beta)
                board[r][c] = EMPTY
                best_score = min(best_score, score)
                beta = min(beta, best_score)
                if beta <= alpha:
                    break  # alpha cut-off
            return best_score

    def best_ai_move(self):
        best_score = float("-inf")
        best_move = None
        alpha, beta = float("-inf"), float("inf")

        for (r, c) in self.available_moves(self.board):
            self.board[r][c] = AI
            score = self.minimax(self.board, 0, False, alpha, beta)
            self.board[r][c] = EMPTY
            if score > best_score:
                best_score = score
                best_move = (r, c)
            alpha = max(alpha, best_score)

        return best_move

    # -----------------------------------------------------------------
    # Drawing
    # -----------------------------------------------------------------
    def draw_board(self):
        self.screen.fill(BG_COLOR)
        pygame.draw.rect(self.screen, BOARD_COLOR, (0, 0, BOARD_SIZE, BOARD_SIZE))

        # grid lines
        for i in range(1, 3):
            pygame.draw.line(
                self.screen, LINE_COLOR,
                (0, i * CELL_SIZE), (BOARD_SIZE, i * CELL_SIZE), LINE_WIDTH
            )
            pygame.draw.line(
                self.screen, LINE_COLOR,
                (i * CELL_SIZE, 0), (i * CELL_SIZE, BOARD_SIZE), LINE_WIDTH
            )

        # hover highlight (only while it's the human's turn and game is live)
        if not self.game_over and self.turn == HUMAN:
            mx, my = pygame.mouse.get_pos()
            if my < BOARD_SIZE:
                hr, hc = my // CELL_SIZE, mx // CELL_SIZE
                if self.board[hr][hc] is EMPTY:
                    pygame.draw.rect(
                        self.screen, HOVER_COLOR,
                        (hc * CELL_SIZE, hr * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    )

        # marks
        for r in range(3):
            for c in range(3):
                val = self.board[r][c]
                cx = c * CELL_SIZE + CELL_SIZE // 2
                cy = r * CELL_SIZE + CELL_SIZE // 2
                if val == HUMAN:
                    self.draw_cross(cx, cy)
                elif val == AI:
                    self.draw_circle(cx, cy)

        # winning line
        if self.winning_line:
            (r1, c1), (_, _), (r3, c3) = self.winning_line
            start = (c1 * CELL_SIZE + CELL_SIZE // 2, r1 * CELL_SIZE + CELL_SIZE // 2)
            end = (c3 * CELL_SIZE + CELL_SIZE // 2, r3 * CELL_SIZE + CELL_SIZE // 2)
            pygame.draw.line(self.screen, WIN_LINE_COLOR, start, end, 10)

        self.draw_status_bar()

    def draw_circle(self, cx, cy):
        pygame.draw.circle(self.screen, CIRCLE_COLOR, (cx, cy), CIRCLE_RADIUS, CIRCLE_WIDTH)

    def draw_cross(self, cx, cy):
        offset = CELL_SIZE // 2 - SPACE
        pygame.draw.line(
            self.screen, CROSS_COLOR,
            (cx - offset, cy - offset), (cx + offset, cy + offset), CROSS_WIDTH
        )
        pygame.draw.line(
            self.screen, CROSS_COLOR,
            (cx - offset, cy + offset), (cx + offset, cy - offset), CROSS_WIDTH
        )

    def draw_status_bar(self):
        pygame.draw.rect(self.screen, BG_COLOR, (0, BOARD_SIZE, WIDTH, HEIGHT - BOARD_SIZE))

        if self.game_over:
            if self.winner == "Draw":
                text = "It's a draw! Nobody beats the Minimax AI."
            elif self.winner == AI:
                text = "Computer (O) wins. The Minimax AI cannot be beaten."
            else:
                text = "You (X) won?! That shouldn't be possible..."
            sub = "Press R to play again"
        else:
            if self.ai_thinking:
                text = "Computer is thinking..."
            elif self.turn == HUMAN:
                text = "Your turn — click a square (X)"
            else:
                text = "Computer's turn (O)"
            sub = "Press ESC to quit"

        status_surf = self.font_status.render(text, True, TEXT_COLOR)
        status_rect = status_surf.get_rect(center=(WIDTH // 2, BOARD_SIZE + 40))
        self.screen.blit(status_surf, status_rect)

        sub_surf = self.font_small.render(sub, True, LINE_COLOR)
        sub_rect = sub_surf.get_rect(center=(WIDTH // 2, BOARD_SIZE + 80))
        self.screen.blit(sub_surf, sub_rect)

    # -----------------------------------------------------------------
    # Turn resolution
    # -----------------------------------------------------------------
    def resolve_state(self):
        winner, line = self.check_winner(self.board)
        if winner:
            self.game_over = True
            self.winner = winner
            self.winning_line = line
        elif self.is_full(self.board):
            self.game_over = True
            self.winner = "Draw"

    def handle_click(self, pos):
        if self.game_over or self.turn != HUMAN:
            return
        mx, my = pos
        if my >= BOARD_SIZE:
            return
        row, col = my // CELL_SIZE, mx // CELL_SIZE
        if self.board[row][col] is not EMPTY:
            return

        self.make_move(self.board, row, col, HUMAN)
        self.resolve_state()
        if not self.game_over:
            self.turn = AI

    def ai_move(self):
        self.ai_thinking = True
        self.draw_board()
        pygame.display.flip()

        move = self.best_ai_move()
        if move:
            r, c = move
            self.make_move(self.board, r, c, AI)

        self.ai_thinking = False
        self.resolve_state()
        if not self.game_over:
            self.turn = HUMAN

    # -----------------------------------------------------------------
    # Main loop
    # -----------------------------------------------------------------
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_r:
                        self.reset_game()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.handle_click(event.pos)

            # Let the AI move right after the human, on its turn.
            if not self.game_over and self.turn == AI and not self.ai_thinking:
                self.ai_move()

            self.draw_board()
            pygame.display.flip()
            self.clock.tick(60)


if __name__ == "__main__":
    TicTacToe().run()
