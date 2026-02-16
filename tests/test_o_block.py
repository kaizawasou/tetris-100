from blocks.o_block import OBlock


def test_color_is_yellow():
    b = OBlock()
    assert b.color == "#FFFF00"


def test_has_4_cells():
    b = OBlock()
    cells = b.cells(0, 0)
    assert len(cells) == 4
    assert len(set(cells)) == 4


def test_rotation_is_shape_invariant():
    b = OBlock()
    shapes = []
    for r in range(4):
        b.rotation = r
        shapes.append(tuple(sorted(b.cells(0, 0))))
    assert len(set(shapes)) == 1
