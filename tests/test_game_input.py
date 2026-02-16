from engine.game import Game
from engine.piece import Piece


def test_move_collision_does_not_change_state():
    game = Game()
    game.current = Piece(kind="L", x=0, y=0)
    before_x = game.current.x
    moved = game.move(-1)
    assert moved is False
    assert game.current.x == before_x


def test_rotate_collision_does_not_change_state():
    game = Game()
    p = Piece(kind="I", x=7, y=0)
    p.block.rotation = 1
    game.current = p
    before = game.current.rotation
    rotated = game.rotate_cw()
    assert rotated is False
    assert game.current.rotation == before


def test_soft_drop_moves_one_row():
    game = Game()
    game.spawn_next()
    assert game.current is not None
    before_y = game.current.y
    dropped = game.soft_drop()
    assert dropped is True
    assert game.current.y == before_y + 1


def test_hard_drop_locks_piece():
    game = Game()
    game.spawn_next()
    before_fixed = len(game.board.fixed)
    distance = game.hard_drop()
    after_fixed = len(game.board.fixed)
    assert distance >= 0
    assert after_fixed > before_fixed
