import pytest

from engine.game import Game
from engine.piece import Piece


def _setup_two_line_clear_with_o(game: Game) -> None:
    game.board.fixed = set()
    for y in (18, 19):
        for x in range(game.board.width):
            if x not in (0, 1):
                game.board.fixed.add((x, y))
    game.current = Piece(kind="O", x=0, y=17)


def test_score_for_two_line_clear_at_level1():
    game = Game()
    _setup_two_line_clear_with_o(game)

    game.hard_drop()

    assert game.lines_cleared == 2
    assert game.score == 300
    assert game.level == 1
    assert game.drop_interval == pytest.approx(0.6)


def test_level_up_and_drop_interval_decrease():
    game = Game()
    game.lines_cleared = 8
    _setup_two_line_clear_with_o(game)

    game.hard_drop()

    assert game.lines_cleared == 10
    assert game.level == 2
    assert game.drop_interval == pytest.approx(0.55)
