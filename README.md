# tetris-100

Python blocks implementation project.

## Setup

0. Install direnv (macOS/Homebrew):
   `brew install direnv`
   and add shell hook in `~/.zshrc`:
   `eval "$(direnv hook zsh)"`
1. Create virtual environment:
   `python3 -m venv .venv`
2. Install dependencies:
   `. .venv/bin/activate && pip install -r requirements.txt`
3. Enable auto-activation with direnv:
   `direnv allow`

After `direnv allow`, entering this directory activates `.venv` automatically.

## Run Tests

Run:

`pytest -q`
