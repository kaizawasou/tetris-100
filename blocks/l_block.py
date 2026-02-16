from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple

Coord = Tuple[int, int]  # (x, y)

@dataclass
class LBlock:
    """
    L字ブロック（青 #0000FF）
    - 4マス
    - 4方向回転（0,1,2,3）
    - 形状は「基準点(0,0)」からの相対座標で定義
    """
    color: str = "#0000FF"
    rotation: int = 0  # 0..3

    # 4回転分の形状（各4マス）
    # 0度:   ■
    #        ■
    #        ■■
    # （左縦3 + 右下1）
    _SHAPES: List[Tuple[Coord, Coord, Coord, Coord]] = (
        ((0, 0), (0, 1), (0, 2), (1, 2)),
        ((0, 1), (1, 1), (2, 1), (0, 0)),
        ((0, 0), (1, 0), (1, 1), (1, 2)),
        ((0, 0), (1, 0), (2, 0), (2, 1)),
    )

    def cells(self, origin_x: int, origin_y: int) -> List[Coord]:
        """盤面上の絶対座標（originを左上として足す）"""
        shape = self._SHAPES[self.rotation % 4]
        return [(origin_x + x, origin_y + y) for (x, y) in shape]

    def rotate_cw(self) -> None:
        """時計回りに回転"""
        self.rotation = (self.rotation + 1) % 4

    def rotate_ccw(self) -> None:
        """反時計回りに回転"""
        self.rotation = (self.rotation - 1) % 4

    @staticmethod
    def spawn_position(board_width: int) -> Coord:
        """
        初期位置: 画面中央上部（y=0）
        ※横方向は「ブロックの最大幅(3)」を考慮して中央寄せ
        """
        max_width = 3  # Lの回転によって最大幅は3
        x = (board_width - max_width) // 2
        y = 0
        return (x, y)
