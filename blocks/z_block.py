from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple

Coord = Tuple[int, int]  # (x, y)


@dataclass
class ZBlock:
    """
    Z字ブロック
    - 4マス
    - 4方向回転（0,1,2,3）
    """
    color: str = "#FF0000"
    rotation: int = 0  # 0..3

    _SHAPES: List[Tuple[Coord, Coord, Coord, Coord]] = (
        ((0, 0), (1, 0), (1, 1), (2, 1)),
        ((1, 0), (0, 1), (1, 1), (0, 2)),
        ((0, 1), (1, 1), (1, 2), (2, 2)),
        ((2, 0), (1, 1), (2, 1), (1, 2)),
    )

    def cells(self, origin_x: int, origin_y: int) -> List[Coord]:
        shape = self._SHAPES[self.rotation % 4]
        return [(origin_x + x, origin_y + y) for (x, y) in shape]

    def rotate_cw(self) -> None:
        self.rotation = (self.rotation + 1) % 4

    def rotate_ccw(self) -> None:
        self.rotation = (self.rotation - 1) % 4

    @staticmethod
    def spawn_position(board_width: int) -> Coord:
        max_width = 3
        x = (board_width - max_width) // 2
        y = 0
        return (x, y)
