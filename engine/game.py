from __future__ import annotations

import random
from typing import Optional

from engine.board import Board
from engine.piece import BLOCKS, Piece


class Game:
    BASE_DROP_INTERVAL = 0.6
    DROP_INTERVAL_STEP = 0.05
    MIN_DROP_INTERVAL = 0.1
    LINE_SCORES = {1: 100, 2: 300, 3: 500, 4: 800}

    def __init__(self, width: int = 10, height: int = 20) -> None:
        self.board = Board(width=width, height=height)
        self._all_kinds = ["L", "J", "O", "I", "T", "S", "Z"]
        self._rng = random.Random()
        self.bag: list[str] = []
        self.current: Optional[Piece] = None
        self.hold_kind: Optional[str] = None
        self.can_hold = True
        self.score = 0
        self.lines_cleared = 0
        self.level = 1
        self.drop_interval = self._compute_drop_interval()
        self.game_over = False
        self.last_event = ""

    def _compute_drop_interval(self) -> float:
        return max(
            self.MIN_DROP_INTERVAL,
            self.BASE_DROP_INTERVAL - self.DROP_INTERVAL_STEP * (self.level - 1),
        )

    def _apply_line_clear(self, cleared: int) -> None:
        if cleared <= 0:
            return
        self.score += self.LINE_SCORES.get(cleared, 0) * self.level
        self.lines_cleared += cleared
        self.level = self.lines_cleared // 10 + 1
        self.drop_interval = self._compute_drop_interval()

    def _refill_bag(self) -> None:
        kinds = list(self._all_kinds)
        self._rng.shuffle(kinds)
        self.bag.extend(kinds)

    def next_kind(self) -> str:
        if not self.bag:
            self._refill_bag()
        return self.bag.pop(0)

    def peek_next(self, n: int = 3) -> list[str]:
        if n <= 0:
            return []

        preview = list(self.bag)
        state = self._rng.getstate()
        while len(preview) < n:
            kinds = list(self._all_kinds)
            self._rng.shuffle(kinds)
            preview.extend(kinds)
        self._rng.setstate(state)
        return preview[:n]

    def spawn_next(self, announce: bool = True) -> bool:
        kind = self.next_kind()
        return self._spawn_kind(kind, announce=announce)

    def _spawn_kind(self, kind: str, announce: bool = True) -> bool:
        block_cls = BLOCKS[kind]
        x, y = block_cls.spawn_position(self.board.width)
        piece = Piece(kind=kind, x=x, y=y)
        if not self.board.can_place(piece.cells()):
            self.game_over = True
            self.current = None
            return False
        self.current = piece
        if announce:
            self.last_event = f"spawn {kind}"
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

        self.board.lock(self.current.cells(), kind=self.current.kind)
        cleared = self.board.clear_full_rows()
        self._apply_line_clear(cleared)
        self.can_hold = True
        event = f"cleared {cleared} line(s)" if cleared > 0 else "locked"
        self.current = None
        if not self.spawn_next(announce=False):
            return False
        self.last_event = event
        return True

    def move(self, dx: int) -> bool:
        if self.game_over:
            return False
        if self.current is None and not self.spawn_next():
            return False
        assert self.current is not None

        next_cells = self.current.cells(dx=dx)
        if not self.board.can_place(next_cells):
            return False
        self.current.move(dx, 0)
        return True

    def rotate_cw(self) -> bool:
        if self.game_over:
            return False
        if self.current is None and not self.spawn_next():
            return False
        assert self.current is not None

        self.current.rotate_cw()
        if self.board.can_place(self.current.cells()):
            return True
        self.current.rotate_ccw()
        return False

    def soft_drop(self) -> bool:
        if self.game_over:
            return False
        if self.current is None and not self.spawn_next():
            return False
        assert self.current is not None

        next_cells = self.current.cells(dy=1)
        if not self.board.can_place(next_cells):
            return False
        self.current.move(0, 1)
        return True

    def hard_drop(self) -> int:
        if self.game_over:
            return 0
        if self.current is None and not self.spawn_next():
            return 0
        assert self.current is not None

        distance = 0
        while self.board.can_place(self.current.cells(dy=1)):
            self.current.move(0, 1)
            distance += 1

        self.board.lock(self.current.cells(), kind=self.current.kind)
        cleared = self.board.clear_full_rows()
        self._apply_line_clear(cleared)
        self.can_hold = True
        self.current = None
        self.spawn_next(announce=False)
        self.last_event = f"hard drop {distance}"
        return distance

    def hold(self) -> bool:
        if self.game_over or not self.can_hold:
            return False
        if self.current is None and not self.spawn_next():
            return False
        assert self.current is not None

        current_kind = self.current.kind
        if self.hold_kind is None:
            self.hold_kind = current_kind
            self.current = None
            self.can_hold = False
            ok = self.spawn_next(announce=False)
            if ok:
                self.last_event = f"hold {current_kind}"
            return ok

        swap_kind = self.hold_kind
        self.hold_kind = current_kind
        self.can_hold = False
        ok = self._spawn_kind(swap_kind, announce=False)
        if ok:
            self.last_event = f"hold swap {swap_kind}"
        return ok

    def ghost_cells(self) -> list[tuple[int, int]]:
        if self.current is None:
            return []
        distance = 0
        while self.board.can_place(self.current.cells(dy=distance + 1)):
            distance += 1
        return self.current.cells(dy=distance)

    def render(self) -> str:
        active = self.current.cells() if self.current is not None else ()
        ghost = self.ghost_cells()
        lines = self.board.to_lines(active, ghost)
        return "\n".join(lines)
