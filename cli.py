from __future__ import annotations

import argparse
import select
import sys
import termios
import time
import tty
from typing import Dict, Optional

from engine.game import Game
from engine.piece import BLOCKS

ANSI_RESET = "\x1b[0m"
ANSI_CLEAR_HOME = "\x1b[2J\x1b[H"


class KeyReader:
    def __init__(self) -> None:
        self._fd = sys.stdin.fileno()
        self._isatty = sys.stdin.isatty()
        self._old = None

    def __enter__(self) -> "KeyReader":
        if self._isatty:
            self._old = termios.tcgetattr(self._fd)
            tty.setcbreak(self._fd)
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        if self._isatty and self._old is not None:
            termios.tcsetattr(self._fd, termios.TCSADRAIN, self._old)

    def read_key(self, timeout: float) -> Optional[str]:
        ready, _, _ = select.select([sys.stdin], [], [], timeout)
        if not ready:
            return None
        ch = sys.stdin.read(1)
        return ch if ch else None


def hex_to_ansi_code(hex_color: str) -> int:
    normalized = hex_color.strip().lower()
    fixed = {
        "#ff0000": 31,  # red
        "#00ff00": 32,  # green
        "#ffff00": 33,  # yellow
        "#ffa500": 33,  # orange -> yellow
        "#0000ff": 34,  # blue
        "#00ffff": 36,  # cyan
        "#800080": 35,  # magenta
    }
    return fixed.get(normalized, 37)


def kind_ansi_map() -> Dict[str, int]:
    return {kind: hex_to_ansi_code(block_cls().color) for kind, block_cls in BLOCKS.items()}


def colorize(text: str, code: int, *, dim: bool = False, enabled: bool = True) -> str:
    if not enabled:
        return text
    prefix = f"\x1b[{2 if dim else 1};{code}m"
    return f"{prefix}{text}{ANSI_RESET}"


def build_frame(game: Game, paused: bool = False, color: bool = True) -> str:
    width = game.board.width
    height = game.board.height
    active = set(game.current.cells() if game.current else [])
    ghost = set(game.ghost_cells())
    ansi = kind_ansi_map()
    active_kind = game.current.kind if game.current else None

    board_lines = ["┌" + "─" * width + "┐"]
    for y in range(height):
        row_cells = []
        for x in range(width):
            coord = (x, y)
            if coord in active:
                code = ansi.get(active_kind or "", 37)
                row_cells.append(colorize("■", code, enabled=color))
            elif coord in game.board.fixed:
                fixed_kind = game.board.get_fixed_kind(x, y)
                code = ansi.get(fixed_kind or "", 37)
                row_cells.append(colorize("■", code, enabled=color))
            elif coord in ghost:
                code = ansi.get(active_kind or "", 37)
                row_cells.append(colorize("·", code, dim=True, enabled=color))
            else:
                row_cells.append(" ")
        board_lines.append("│" + "".join(row_cells) + "│")
    board_lines.append("└" + "─" * width + "┘")

    next3 = game.peek_next(3)
    panel = [
        "TETRIS-100",
        "",
        f"SCORE: {game.score}",
        f"LEVEL: {game.level}",
        f"LINES: {game.lines_cleared}",
        "",
        f"HOLD: {game.hold_kind or '-'}",
        f"NEXT: {' '.join(next3)}",
        "",
        "Controls",
        "A/D : Move",
        "W   : Rotate",
        "S   : Soft drop",
        "SPC : Hard drop",
        "C   : Hold",
        "P   : Pause",
        "Q   : Quit",
    ]
    if paused:
        panel.append("")
        panel.append("PAUSED")
    if game.game_over:
        panel.append("")
        panel.append("GAME OVER")

    total = max(len(board_lines), len(panel))
    combined = []
    for i in range(total):
        left = board_lines[i] if i < len(board_lines) else " " * (width + 2)
        right = panel[i] if i < len(panel) else ""
        combined.append(f"{left}  {right}")
    return "\n".join(combined)


def main() -> None:
    parser = argparse.ArgumentParser(description="Rich Tetris CLI demo")
    parser.add_argument("--ticks", type=int, default=600, help="max loops")
    parser.add_argument("--interval", type=float, default=0.05, help="input polling interval")
    parser.add_argument("--no-color", action="store_true", help="disable ANSI color")
    args = parser.parse_args()

    game = Game()
    game.spawn_next()
    paused = False
    next_drop_at = time.monotonic() + game.drop_interval

    with KeyReader() as kr:
        for _ in range(args.ticks):
            frame = build_frame(game, paused=paused, color=not args.no_color)
            sys.stdout.write(ANSI_CLEAR_HOME + frame + "\n")
            sys.stdout.flush()

            key = kr.read_key(args.interval)
            if key:
                k = key.lower()
                if k == "q":
                    break
                if k == "p":
                    paused = not paused
                    if not paused:
                        next_drop_at = time.monotonic() + game.drop_interval
                elif not paused:
                    if k == "a":
                        game.move(-1)
                    elif k == "d":
                        game.move(1)
                    elif k == "w":
                        game.rotate_cw()
                    elif k == "s":
                        game.soft_drop()
                    elif k == "c":
                        game.hold()
                    elif key == " ":
                        game.hard_drop()
                        next_drop_at = time.monotonic() + game.drop_interval

            now = time.monotonic()
            if (not paused) and now >= next_drop_at:
                if not game.tick():
                    frame = build_frame(game, paused=False, color=not args.no_color)
                    sys.stdout.write(ANSI_CLEAR_HOME + frame + "\n")
                    sys.stdout.flush()
                    break
                next_drop_at = now + game.drop_interval


if __name__ == "__main__":
    main()

