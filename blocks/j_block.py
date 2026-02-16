from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple

Coord = Tuple[int, int]  # (x, y)

@dataclass
class JBlock:
    """
    J字ブロック（L字の左右反転）
    - 4マス
    - 4方向回転（0,1,2,3）
    - 形状は「基準点(0,0)」からの相対座標で定義
    """
    # NOTE: 色はひとまず青系で固定。将来「色管理」が入るなら差し替え前提。
    color: str = "#0000CC"
    rotation: int = 0  # 0..3

    # 0度:     ■
    #         ■
    #        ■■
    # （右縦3 + 左下1）
    _SHAPES: List[Tuple[Coord, Coord, Coord, Coord]] = (
        ((1, 0), (1, 1), (1, 2), (0, 2)),
        ((0, 0), (0, 1), (1, 1), (2, 1)),
        ((0, 0), (0, 1), (0, 2), (1, 0)),
        ((0, 0), (1, 0), (2, 0), (2, 1)),
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
