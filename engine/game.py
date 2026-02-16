from __future__ import annotations

from itertools import cycle
from typing import Optional

from engine.board import Board
from engine.piece import BLOCKS, Piece


class Game:
    def __init__(self, width: int = 10, height: int = 20) -> None:
        self.board = Board(width=width, height=height)
        self._kinds = cycle(["L", "J", "O", "I", "T", "S", "Z"])
        self.current: Optional[Piece] = None
        self.lines_cleared = 0
        self.game_over = False

    def spawn_next(self) -> bool:
        kind = next(self._kinds)
        block_cls = BLOCKS[kind]
        x, y = block_cls.spawn_position(self.board.width)
        piece = Piece(kind=kind, x=x, y=y)
        if not self.board.can_place(piece.cells()):
            self.game_over = True
            self.current = None
            return False
        self.current = piece
        return True

    def tick(self) -> bool:
        if self.game_over:
            return False
        if self.current is None and not self.spawn_next():
            return False
        assert self.current is not None

        if self.board.can_place(self.current.cells(dy=1)):
            self.current.move(0, 1)
            return True

        self.board.lock(self.current.cells())
        self.lines_cleared += self.board.clear_full_rows()
        self.current = None
        if not self.spawn_next():
            return False
        return True

    def render(self) -> str:
        active = self.current.cells() if self.current is not None else ()
        lines = self.board.to_lines(active)
        return "\n".join(lines)

