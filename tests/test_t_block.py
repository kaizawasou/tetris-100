from blocks.t_block import TBlock


def test_color_is_purple():
    b = TBlock()
    assert b.color == "#800080"


def test_cells_always_4():
    b = TBlock()
    for r in range(4):
        b.rotation = r
        cells = b.cells(0, 0)
        assert len(cells) == 4
        assert len(set(cells)) == 4


def test_rotation_changes_shape():
    b = TBlock()
    b.rotation = 0
    shape0 = tuple(sorted(b.cells(0, 0)))
    b.rotation = 1
    shape1 = tuple(sorted(b.cells(0, 0)))
    assert shape0 != shape1
