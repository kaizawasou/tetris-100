from cli import build_frame, hex_to_ansi_code
from engine.game import Game


def test_hex_to_ansi_code_is_stable():
    assert hex_to_ansi_code("#FF0000") == 31
    assert hex_to_ansi_code("#00FF00") == 32
    assert hex_to_ansi_code("#0000FF") == 34


def test_build_frame_contains_panels_and_border():
    game = Game()
    game.spawn_next()

    frame = build_frame(game, paused=False, color=False)

    assert "SCORE:" in frame
    assert "LEVEL:" in frame
    assert "LINES:" in frame
    assert "NEXT:" in frame
    assert "HOLD:" in frame
    assert "┌" in frame and "┘" in frame
