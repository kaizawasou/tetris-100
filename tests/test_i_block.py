from blocks.i_block import IBlock


def test_color_is_cyan():
    b = IBlock()
    assert b.color == "#00FFFF"


def test_cells_always_4():
    b = IBlock()
    for r in range(4):
        b.rotation = r
        cells = b.cells(0, 0)
        assert len(cells) == 4
        assert len(set(cells)) == 4


def test_rotation_changes_shape_between_horizontal_and_vertical():
    b = IBlock()
    b.rotation = 0
    horizontal = tuple(sorted(b.cells(0, 0)))
    b.rotation = 1
    vertical = tuple(sorted(b.cells(0, 0)))
    assert horizontal != vertical
