from engine.board import Board


def test_wall_and_floor_collision():
    board = Board(width=10, height=20)
    assert board.can_place([(0, 0)])
    assert not board.can_place([(-1, 0)])
    assert not board.can_place([(10, 0)])
    assert not board.can_place([(0, 20)])


def test_fixed_block_collision():
    board = Board(width=10, height=20)
    board.lock([(3, 5)])
    assert not board.can_place([(3, 5)])
    assert board.can_place([(4, 5)])


def test_clear_full_row_and_drop_above():
    board = Board(width=10, height=20)
    board.lock([(x, 19) for x in range(10)])
    board.lock([(0, 18)])

    cleared = board.clear_full_rows()
    assert cleared == 1
    assert len(board.fixed) == 1
    assert (0, 19) in board.fixed
