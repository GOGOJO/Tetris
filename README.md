# Tetris

A classic Tetris game built with Pygame.

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
python tetris.py
```

## Controls

| Key | Action |
|-----|--------|
| ← / → | Move left/right (hold to repeat) |
| ↑ | Rotate counter-clockwise |
| Z | Rotate clockwise |
| ↓ | Soft drop (hold to repeat) |
| Space | Lock piece |
| R | Restart game |

## Gameplay

- Clear lines by filling them completely
- Score more points for clearing multiple lines at once (1=100, 2=300, 3=500, 4=800)
- Game speeds up as you clear more lines
- Press R to restart after game over
