from blocks.j_block import JBlock

def test_color_is_set():
    b = JBlock()
    assert b.color.startswith("#")

def test_has_4_cells_each_rotation():
    b = JBlock()
    for r in range(4):
        b.rotation = r
        cells = b.cells(0, 0)
        assert len(cells) == 4
        assert len(set(cells)) == 4

def test_rotations_are_distinct():
    b = JBlock()
    shapes = []
    for r in range(4):
        b.rotation = r
        shapes.append(tuple(sorted(b.cells(0, 0))))
    assert len(set(shapes)) == 4

def test_spawn_position_center_top():
    x, y = JBlock.spawn_position(10)
    assert (x, y) == (3, 0)
