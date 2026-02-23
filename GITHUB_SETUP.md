# Push Tetris to GitHub

Your Tetris project is ready to push. Follow these steps:

## 1. Create the initial commit (if needed)

If the commit didn't complete, run:

```bash
cd /Users/joshualu/Tetris
git commit --no-verify -m "Initial commit: Pygame Tetris game"
```

> If you see an error about `--trailer`, you may have a global git config. Try temporarily unsetting it:
> `git config --global --unset-all commit.template` (if set), or run the commit from a fresh terminal.

## 2. Create a new repository on GitHub

1. Go to [github.com/new](https://github.com/new)
2. Set the name to `Tetris` (or another name you prefer)
3. Leave it empty (no README, .gitignore, or license)
4. Click **Create repository**

## 3. Push your code

From the Tetris directory, run (replace `YOUR_USERNAME` with your GitHub username):

```bash
cd /Users/joshualu/Tetris
git remote add origin https://github.com/YOUR_USERNAME/Tetris.git
git branch -M main
git push -u origin main
```

Or with SSH (if you use SSH keys):

```bash
git remote add origin git@github.com:YOUR_USERNAME/Tetris.git
git branch -M main
git push -u origin main
```

## Files included

- `tetris.py` - Main game
- `requirements.txt` - Dependencies (pygame)
- `README.md` - Setup and controls
- `.gitignore` - Ignores __pycache__, venv, etc.
