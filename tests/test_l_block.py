from blocks.l_block import LBlock

def test_color_is_blue():
    b = LBlock()
    assert b.color == "#0000FF"

def test_has_4_cells_each_rotation():
    b = LBlock()
    for r in range(4):
        b.rotation = r
        cells = b.cells(0, 0)
        assert len(cells) == 4
        assert len(set(cells)) == 4  # 重複なし

def test_rotations_are_distinct():
    b = LBlock()
    shapes = []
    for r in range(4):
        b.rotation = r
        shapes.append(tuple(sorted(b.cells(0, 0))))
    assert len(set(shapes)) == 4

def test_spawn_position_center_top():
    # board_width=10 の場合、max_width=3 なので (10-3)//2=3
    x, y = LBlock.spawn_position(10)
    assert (x, y) == (3, 0)
