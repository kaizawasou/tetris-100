from __future__ import annotations

import argparse
import select
import sys
import termios
import tty
from typing import Optional

from engine.game import Game


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


def main() -> None:
    parser = argparse.ArgumentParser(description="Minimal Tetris CLI demo")
    parser.add_argument("--ticks", type=int, default=200, help="max ticks to run")
    parser.add_argument("--interval", type=float, default=0.25, help="seconds per loop")
    args = parser.parse_args()

    game = Game()
    game.spawn_next()
    print("Controls: A/D=move W=rotate S=soft drop Space=hard drop Q=quit")

    with KeyReader() as kr:
        for i in range(args.ticks):
            print(f"tick={i} lines={game.lines_cleared}")
            print("NEXT:", " ".join(game.peek_next(3)))
            print(game.render())
            print("-" * game.board.width)

            key = kr.read_key(args.interval)
            if key:
                k = key.lower()
                if k == "q":
                    print("QUIT")
                    break
                if k == "a":
                    game.move(-1)
                elif k == "d":
                    game.move(1)
                elif k == "w":
                    game.rotate_cw()
                elif k == "s":
                    game.soft_drop()
                elif key == " ":
                    game.hard_drop()

            if not game.tick():
                print("GAME OVER")
                break


if __name__ == "__main__":
    main()
