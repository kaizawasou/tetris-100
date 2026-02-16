from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple

Coord = Tuple[int, int]  # (x, y)


@dataclass
class OBlock:
    """
    O字ブロック（2x2）
    - 4マス
    - rotationは持つが、形状は回転で不変
    """
    color: str = "#FFFF00"
    rotation: int = 0  # 0..3

    _SHAPE: Tuple[Coord, Coord, Coord, Coord] = (
        (0, 0), (1, 0), (0, 1), (1, 1),
    )

    def cells(self, origin_x: int, origin_y: int) -> List[Coord]:
        return [(origin_x + x, origin_y + y) for (x, y) in self._SHAPE]

    def rotate_cw(self) -> None:
        self.rotation = (self.rotation + 1) % 4

    def rotate_ccw(self) -> None:
        self.rotation = (self.rotation - 1) % 4

    @staticmethod
    def spawn_position(board_width: int) -> Coord:
        max_width = 2
        x = (board_width - max_width) // 2
        y = 0
        return (x, y)
