from blocks.z_block import ZBlock


def test_color_is_red():
    b = ZBlock()
    assert b.color == "#FF0000"


def test_cells_always_4():
    b = ZBlock()
    for r in range(4):
        b.rotation = r
        cells = b.cells(0, 0)
        assert len(cells) == 4
        assert len(set(cells)) == 4


def test_rotation_changes_shape():
    b = ZBlock()
    b.rotation = 0
    shape0 = tuple(sorted(b.cells(0, 0)))
    b.rotation = 1
    shape1 = tuple(sorted(b.cells(0, 0)))
    assert shape0 != shape1
