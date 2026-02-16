from __future__ import annotations

import argparse
import time

from engine.game import Game


def main() -> None:
    parser = argparse.ArgumentParser(description="Minimal Tetris CLI demo")
    parser.add_argument("--ticks", type=int, default=12, help="number of ticks to run")
    parser.add_argument("--sleep", type=float, default=0.0, help="sleep seconds per tick")
    args = parser.parse_args()

    game = Game()
    game.spawn_next()
    for i in range(args.ticks):
        print(f"tick={i}")
        print(game.render())
        print("-" * game.board.width)
        if not game.tick():
            print("GAME OVER")
            break
        if args.sleep > 0:
            time.sleep(args.sleep)


if __name__ == "__main__":
    main()

