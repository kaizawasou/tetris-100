from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, List, Set, Tuple

Coord = Tuple[int, int]


@dataclass
class Board:
    width: int = 10
    height: int = 20
    fixed: Set[Coord] = field(default_factory=set)

    def can_place(self, cells: Iterable[Coord]) -> bool:
        for x, y in cells:
            if x < 0 or x >= self.width:
                return False
            if y < 0 or y >= self.height:
                return False
            if (x, y) in self.fixed:
                return False
        return True

    def lock(self, cells: Iterable[Coord]) -> None:
        for x, y in cells:
            if 0 <= x < self.width and 0 <= y < self.height:
                self.fixed.add((x, y))

    def clear_full_rows(self) -> int:
        full_rows = [y for y in range(self.height) if sum((x, y) in self.fixed for x in range(self.width)) == self.width]
        if not full_rows:
            return 0

        full_rows_set = set(full_rows)
        new_fixed: Set[Coord] = set()
        for x, y in self.fixed:
            if y in full_rows_set:
                continue
            drop = sum(1 for row in full_rows if row > y)
            new_fixed.add((x, y + drop))
        self.fixed = new_fixed
        return len(full_rows)

    def to_lines(self, active_cells: Iterable[Coord] = ()) -> List[str]:
        active = set(active_cells)
        lines: List[str] = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                if (x, y) in active:
                    row.append("@")
                elif (x, y) in self.fixed:
                    row.append("#")
                else:
                    row.append(".")
            lines.append("".join(row))
        return lines

