"""
Tetris - A classic Tetris game built with Pygame
"""

import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
SIDEBAR_WIDTH = 180

# Colors - retro arcade palette
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_GRAY = (40, 40, 40)
LIGHT_GRAY = (180, 180, 180)

# Tetromino colors (classic palette)
COLORS = {
    "I": (0, 255, 255),    # Cyan
    "O": (255, 255, 0),    # Yellow
    "T": (160, 0, 255),    # Purple
    "S": (0, 255, 0),      # Green
    "Z": (255, 0, 0),      # Red
    "J": (0, 0, 255),      # Blue
    "L": (255, 165, 0),    # Orange
}

# Tetromino shapes - each shape has 4 rotations
SHAPES = {
    "I": [
        [(0, 0), (1, 0), (2, 0), (3, 0)],
        [(0, 0), (0, 1), (0, 2), (0, 3)],
        [(0, 0), (1, 0), (2, 0), (3, 0)],
        [(0, 0), (0, 1), (0, 2), (0, 3)],
    ],
    "O": [
        [(0, 0), (1, 0), (0, 1), (1, 1)],
        [(0, 0), (1, 0), (0, 1), (1, 1)],
        [(0, 0), (1, 0), (0, 1), (1, 1)],
        [(0, 0), (1, 0), (0, 1), (1, 1)],
    ],
    "T": [
        [(0, 0), (1, 0), (2, 0), (1, 1)],
        [(1, 0), (1, 1), (1, 2), (0, 1)],
        [(0, 1), (1, 1), (2, 1), (1, 0)],
        [(1, 0), (1, 1), (1, 2), (2, 1)],
    ],
    "S": [
        [(1, 0), (2, 0), (0, 1), (1, 1)],
        [(0, 0), (0, 1), (1, 1), (1, 2)],
        [(1, 0), (2, 0), (0, 1), (1, 1)],
        [(0, 0), (0, 1), (1, 1), (1, 2)],
    ],
    "Z": [
        [(0, 0), (1, 0), (1, 1), (2, 1)],
        [(2, 0), (2, 1), (1, 1), (1, 2)],
        [(0, 1), (1, 1), (1, 0), (2, 0)],
        [(1, 0), (1, 1), (0, 1), (0, 2)],
    ],
    "J": [
        [(0, 0), (0, 1), (1, 1), (2, 1)],
        [(1, 0), (1, 1), (1, 2), (0, 2)],
        [(0, 1), (1, 1), (2, 1), (2, 2)],
        [(2, 0), (1, 0), (1, 1), (1, 2)],
    ],
    "L": [
        [(2, 0), (0, 1), (1, 1), (2, 1)],
        [(0, 0), (1, 0), (1, 1), (1, 2)],
        [(0, 1), (1, 1), (2, 1), (0, 2)],
        [(1, 0), (1, 1), (1, 2), (2, 2)],
    ],
}

# Scoring
SCORE_LINES = {1: 100, 2: 300, 3: 500, 4: 800}

# Key repeat (DAS = Delayed Auto Shift, ARR = Auto Repeat Rate)
DAS_DELAY = 150
ARR_DELAY = 50


class Tetromino:
    """Represents a falling Tetris piece"""

    def __init__(self, shape_name=None):
        self.shape_name = shape_name or random.choice(list(SHAPES.keys()))
        self.color = COLORS[self.shape_name]
        self.rotation = 0
        self.x = GRID_WIDTH // 2 - 2
        self.y = 0

    def get_blocks(self):
        """Return list of (x, y) grid positions occupied by this piece"""
        blocks = []
        for dx, dy in SHAPES[self.shape_name][self.rotation]:
            blocks.append((self.x + dx, self.y + dy))
        return blocks

    def rotate(self):
        self.rotation = (self.rotation + 1) % 4

    def rotate_back(self):
        self.rotation = (self.rotation - 1) % 4


class TetrisGame:
    def __init__(self):
        self.grid = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = None
        self.next_piece = Tetromino()
        self.hold_piece = None  # Shape name of held piece (or None)
        self.can_hold = True   # Can only hold once per piece
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.game_over = False
        self.fall_time = 0
        self.fall_speed = 500  # ms per drop

    def hold(self):
        """Swap current piece with hold (or store current and spawn next). Can only hold once per piece."""
        if self.game_over or not self.current_piece or not self.can_hold:
            return False
        current_shape = self.current_piece.shape_name
        if self.hold_piece is None:
            self.hold_piece = current_shape
            self.current_piece = self.next_piece
            self.next_piece = Tetromino()
        else:
            self.current_piece = Tetromino(shape_name=self.hold_piece)
            self.hold_piece = current_shape
        self.can_hold = False
        if self.collision(self.current_piece):
            self.game_over = True
        return True

    def new_piece(self):
        """Spawn a new piece"""
        self.current_piece = self.next_piece
        self.next_piece = Tetromino()
        self.can_hold = True  # Reset hold after locking

        # Check game over - if new piece overlaps, game is over
        if self.collision(self.current_piece):
            self.game_over = True

    def collision(self, piece, offset_x=0, offset_y=0):
        """Check if piece collides with grid boundaries or locked blocks"""
        for x, y in piece.get_blocks():
            new_x, new_y = x + offset_x, y + offset_y
            if new_x < 0 or new_x >= GRID_WIDTH or new_y >= GRID_HEIGHT:
                return True
            if new_y >= 0 and self.grid[new_y][new_x] is not None:
                return True
        return False

    def lock_piece(self):
        """Lock the current piece to the grid"""
        for x, y in self.current_piece.get_blocks():
            if 0 <= y < GRID_HEIGHT and 0 <= x < GRID_WIDTH:
                self.grid[y][x] = self.current_piece.color
        self.clear_lines()
        self.new_piece()

    def clear_lines(self):
        """Clear completed lines and update score"""
        lines_to_clear = []
        for y in range(GRID_HEIGHT):
            if all(self.grid[y][x] is not None for x in range(GRID_WIDTH)):
                lines_to_clear.append(y)

        for y in lines_to_clear:
            del self.grid[y]
            self.grid.insert(0, [None for _ in range(GRID_WIDTH)])

        if lines_to_clear:
            self.lines_cleared += len(lines_to_clear)
            self.score += SCORE_LINES.get(len(lines_to_clear), 0) * self.level
            # Increase speed every 10 lines
            self.level = 1 + self.lines_cleared // 10
            self.fall_speed = max(100, 500 - (self.level - 1) * 40)

    def move(self, dx, dy):
        """Move piece if valid"""
        if self.game_over or not self.current_piece:
            return False
        if not self.collision(self.current_piece, dx, dy):
            self.current_piece.x += dx
            self.current_piece.y += dy
            return True
        return False

    def rotate_piece(self):
        """Rotate piece if valid"""
        if self.game_over or not self.current_piece:
            return False
        self.current_piece.rotate()
        if self.collision(self.current_piece):
            self.current_piece.rotate_back()
            return False
        return True

    def hard_drop(self):
        """Drop piece to bottom instantly"""
        if self.game_over or not self.current_piece:
            return
        while self.move(0, 1):
            self.score += 2
        self.lock_piece()

    def get_ghost_blocks(self):
        """Return list of (x, y) grid positions where the current piece would land"""
        if not self.current_piece:
            return []
        piece = self.current_piece
        drop = 0
        while not self.collision(piece, 0, drop + 1):
            drop += 1
        blocks = []
        for dx, dy in SHAPES[piece.shape_name][piece.rotation]:
            blocks.append((piece.x + dx, piece.y + dy + drop))
        return blocks


class TetrisApp:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH + SIDEBAR_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.game = TetrisGame()
        self.game.new_piece()
        self.font_large = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 28)
        self.key_first_press = {}
        self.key_last_action = {}

    def draw_block(self, surface, x, y, color, offset_x=0, offset_y=0):
        """Draw a single block with 3D effect"""
        px = offset_x + x * BLOCK_SIZE
        py = offset_y + y * BLOCK_SIZE

        # Main block
        pygame.draw.rect(surface, color, (px + 1, py + 1, BLOCK_SIZE - 2, BLOCK_SIZE - 2))
        # Highlight (top-left)
        lighter = tuple(min(255, c + 60) for c in color)
        pygame.draw.line(surface, lighter, (px + 1, py + BLOCK_SIZE - 2), (px + 1, py + 1))
        pygame.draw.line(surface, lighter, (px + 1, py + 1), (px + BLOCK_SIZE - 2, py + 1))
        # Shadow (bottom-right)
        darker = tuple(max(0, c - 60) for c in color)
        pygame.draw.line(surface, darker, (px + BLOCK_SIZE - 2, py + 1), (px + BLOCK_SIZE - 2, py + BLOCK_SIZE - 2))
        pygame.draw.line(surface, darker, (px + BLOCK_SIZE - 2, py + BLOCK_SIZE - 2), (px + 1, py + BLOCK_SIZE - 2))

    def draw_ghost_block(self, surface, x, y):
        """Draw a ghost (outline) block at grid position (x, y)"""
        if y < 0:
            return
        px = x * BLOCK_SIZE
        py = y * BLOCK_SIZE
        rect = pygame.Rect(px + 2, py + 2, BLOCK_SIZE - 4, BLOCK_SIZE - 4)
        pygame.draw.rect(surface, LIGHT_GRAY, rect, 1)

    def draw_grid(self, surface):
        """Draw the game grid and board"""
        # Board background
        board_rect = pygame.Rect(0, 0, GRID_WIDTH * BLOCK_SIZE, GRID_HEIGHT * BLOCK_SIZE)
        pygame.draw.rect(surface, BLACK, board_rect)
        pygame.draw.rect(surface, DARK_GRAY, board_rect, 2)

        # Grid lines
        for x in range(GRID_WIDTH + 1):
            pygame.draw.line(
                surface, DARK_GRAY,
                (x * BLOCK_SIZE, 0), (x * BLOCK_SIZE, GRID_HEIGHT * BLOCK_SIZE)
            )
        for y in range(GRID_HEIGHT + 1):
            pygame.draw.line(
                surface, DARK_GRAY,
                (0, y * BLOCK_SIZE), (GRID_WIDTH * BLOCK_SIZE, y * BLOCK_SIZE)
            )

        # Locked blocks
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.game.grid[y][x] is not None:
                    self.draw_block(surface, x, y, self.game.grid[y][x])

        # Ghost piece - where current piece will land
        for x, y in self.game.get_ghost_blocks():
            self.draw_ghost_block(surface, x, y)

        # Current piece
        if self.game.current_piece:
            for x, y in self.game.current_piece.get_blocks():
                if y >= 0:
                    self.draw_block(
                        surface, x, y,
                        self.game.current_piece.color
                    )

    def draw_sidebar(self, surface):
        """Draw score, next piece, controls - clean aligned layout"""
        sx = GRID_WIDTH * BLOCK_SIZE + 20
        px = sx - 10

        # HOLD - label at top, preview directly below
        text = self.font_small.render("HOLD", True, WHITE)
        surface.blit(text, (sx, 2))
        if self.game.hold_piece:
            for dx, dy in SHAPES[self.game.hold_piece][0]:
                self.draw_block(surface, dx + 3, dy + 2, COLORS[self.game.hold_piece], px, 16)

        # NEXT - label and preview, pieces close to label
        text = self.font_small.render("NEXT", True, WHITE)
        surface.blit(text, (sx, 72))
        if self.game.next_piece:
            for dx, dy in SHAPES[self.game.next_piece.shape_name][0]:
                self.draw_block(surface, dx + 3, dy + 2, self.game.next_piece.color, px, 88)

        # Score - aligned
        text = self.font_small.render("SCORE", True, WHITE)
        surface.blit(text, (sx, 230))
        text = self.font_large.render(str(self.game.score), True, WHITE)
        surface.blit(text, (sx, 255))

        # Level - aligned
        text = self.font_small.render("LEVEL", True, WHITE)
        surface.blit(text, (sx, 305))
        text = self.font_large.render(str(self.game.level), True, WHITE)
        surface.blit(text, (sx, 330))

        # Lines - aligned with space below
        text = self.font_small.render("LINES", True, WHITE)
        surface.blit(text, (sx, 380))
        text = self.font_large.render(str(self.game.lines_cleared), True, WHITE)
        surface.blit(text, (sx, 405))

        # Controls - well below LINES, use ASCII to avoid font issues
        controls = [
            "CONTROLS",
            "Left/Right: Move",
            "Up: Rotate",
            "Down: Soft drop",
            "Space: Hard drop",
            "C: Hold piece",
            "R: Restart",
        ]
        for i, line in enumerate(controls):
            text = self.font_small.render(line, True, LIGHT_GRAY)
            surface.blit(text, (sx, 438 + i * 22))

    def draw_game_over(self, surface):
        """Draw game over overlay"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        surface.blit(overlay, (0, 0))

        text = self.font_large.render("GAME OVER", True, WHITE)
        rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
        surface.blit(text, rect)

        text = self.font_small.render(f"Score: {self.game.score}", True, WHITE)
        rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10))
        surface.blit(text, rect)

        text = self.font_small.render("Press R to restart", True, LIGHT_GRAY)
        rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        surface.blit(text, rect)

    def restart(self):
        """Restart the game"""
        self.game = TetrisGame()
        self.game.new_piece()
        self.key_first_press = {}
        self.key_last_action = {}

    def run(self):
        running = True
        while running:
            self.screen.fill(DARK_GRAY)

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYUP:
                    self.key_first_press.pop(event.key, None)
                    self.key_last_action.pop(event.key, None)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.restart()
                    elif not self.game.game_over:
                        if event.key == pygame.K_UP:
                            self.game.rotate_piece()
                        elif event.key == pygame.K_c:
                            self.game.hold()
                        elif event.key == pygame.K_SPACE:
                            self.game.hard_drop()

            # Key hold repeat for left, right, down
            if not self.game.game_over:
                now = pygame.time.get_ticks()
                keys = pygame.key.get_pressed()
                for key, (dx, dy) in [(pygame.K_LEFT, (-1, 0)), (pygame.K_RIGHT, (1, 0)), (pygame.K_DOWN, (0, 1))]:
                    if keys[key]:
                        if key not in self.key_first_press:
                            self.key_first_press[key] = now
                            self.key_last_action[key] = now
                            if dy:
                                if self.game.move(0, 1):
                                    self.game.score += 1
                            else:
                                self.game.move(dx, 0)
                        else:
                            elapsed = now - self.key_first_press[key]
                            since_action = now - self.key_last_action[key]
                            if elapsed >= DAS_DELAY and since_action >= ARR_DELAY:
                                self.key_last_action[key] = now
                                if dy:
                                    if self.game.move(0, 1):
                                        self.game.score += 1
                                else:
                                    self.game.move(dx, 0)

            # Auto fall
            if not self.game.game_over:
                self.game.fall_time += self.clock.get_rawtime()
                if self.game.fall_time >= self.game.fall_speed:
                    if not self.game.move(0, 1):
                        self.game.lock_piece()
                    self.game.fall_time = 0

            # Draw
            self.draw_grid(self.screen)
            self.draw_sidebar(self.screen)
            if self.game.game_over:
                self.draw_game_over(self.screen)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()


if __name__ == "__main__":
    app = TetrisApp()
    app.run()
