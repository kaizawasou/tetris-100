from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional, Set, Tuple

Coord = Tuple[int, int]


@dataclass
class Board:
    width: int = 10
    height: int = 20
    fixed: Set[Coord] = field(default_factory=set)
    fixed_kinds: Dict[Coord, str] = field(default_factory=dict)

    def can_place(self, cells: Iterable[Coord]) -> bool:
        for x, y in cells:
            if x < 0 or x >= self.width:
                return False
            if y < 0 or y >= self.height:
                return False
            if (x, y) in self.fixed:
                return False
        return True

    def lock(self, cells: Iterable[Coord], kind: Optional[str] = None) -> None:
        for x, y in cells:
            if 0 <= x < self.width and 0 <= y < self.height:
                coord = (x, y)
                self.fixed.add(coord)
                if kind is not None:
                    self.fixed_kinds[coord] = kind

    def clear_full_rows(self) -> int:
        full_rows = [y for y in range(self.height) if sum((x, y) in self.fixed for x in range(self.width)) == self.width]
        if not full_rows:
            return 0

        full_rows_set = set(full_rows)
        new_fixed: Set[Coord] = set()
        new_fixed_kinds: Dict[Coord, str] = {}
        for x, y in self.fixed:
            if y in full_rows_set:
                continue
            drop = sum(1 for row in full_rows if row > y)
            new_coord = (x, y + drop)
            new_fixed.add(new_coord)
            kind = self.fixed_kinds.get((x, y))
            if kind is not None:
                new_fixed_kinds[new_coord] = kind
        self.fixed = new_fixed
        self.fixed_kinds = new_fixed_kinds
        return len(full_rows)

    def get_fixed_kind(self, x: int, y: int) -> Optional[str]:
        return self.fixed_kinds.get((x, y))

    def to_lines(self, active_cells: Iterable[Coord] = (), ghost_cells: Iterable[Coord] = ()) -> List[str]:
        active = set(active_cells)
        ghost = set(ghost_cells)
        lines: List[str] = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                if (x, y) in active:
                    row.append("@")
                elif (x, y) in self.fixed:
                    row.append("#")
                elif (x, y) in ghost:
                    row.append(":")
                else:
                    row.append(".")
            lines.append("".join(row))
        return lines
