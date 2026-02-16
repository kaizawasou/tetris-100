from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple, Type

from blocks.i_block import IBlock
from blocks.j_block import JBlock
from blocks.l_block import LBlock
from blocks.o_block import OBlock
from blocks.s_block import SBlock
from blocks.t_block import TBlock
from blocks.z_block import ZBlock

Coord = Tuple[int, int]

BLOCKS: Dict[str, Type] = {
    "L": LBlock,
    "J": JBlock,
    "O": OBlock,
    "I": IBlock,
    "T": TBlock,
    "S": SBlock,
    "Z": ZBlock,
}


@dataclass
class Piece:
    kind: str
    x: int
    y: int

    def __post_init__(self) -> None:
        self.block = BLOCKS[self.kind]()

    @property
    def rotation(self) -> int:
        return self.block.rotation

    def cells(self, dx: int = 0, dy: int = 0) -> List[Coord]:
        return self.block.cells(self.x + dx, self.y + dy)

    def move(self, dx: int, dy: int) -> None:
        self.x += dx
        self.y += dy

    def rotate_cw(self) -> None:
        self.block.rotate_cw()

    def rotate_ccw(self) -> None:
        self.block.rotate_ccw()

