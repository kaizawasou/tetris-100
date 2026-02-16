from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple

Coord = Tuple[int, int]  # (x, y)


@dataclass
class IBlock:
    """
    I字ブロック（4マス直線）
    - 4マス
    - rotationは0..3を受け付ける
    - 形状は水平/垂直の2状態で切り替える
    """
    color: str = "#00FFFF"
    rotation: int = 0  # 0..3

    _SHAPES: Tuple[Tuple[Coord, Coord, Coord, Coord], Tuple[Coord, Coord, Coord, Coord]] = (
        ((0, 0), (1, 0), (2, 0), (3, 0)),  # horizontal
        ((0, 0), (0, 1), (0, 2), (0, 3)),  # vertical
    )

    def cells(self, origin_x: int, origin_y: int) -> List[Coord]:
        shape = self._SHAPES[self.rotation % 2]
        return [(origin_x + x, origin_y + y) for (x, y) in shape]

    def rotate_cw(self) -> None:
        self.rotation = (self.rotation + 1) % 4

    def rotate_ccw(self) -> None:
        self.rotation = (self.rotation - 1) % 4

    @staticmethod
    def spawn_position(board_width: int) -> Coord:
        max_width = 4
        x = (board_width - max_width) // 2
        y = 0
        return (x, y)
