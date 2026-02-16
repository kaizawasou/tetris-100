from engine.game import Game


def test_spawn_sets_last_event():
    game = Game()
    game.spawn_next()
    assert game.last_event.startswith("spawn ")


def test_hard_drop_updates_last_event():
    game = Game()
    game.spawn_next()
    game.hard_drop()
    assert game.last_event.startswith("hard drop ")
