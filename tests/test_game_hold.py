from engine.game import Game


def test_hold_empty_stores_current_and_spawns_next():
    game = Game()
    game.spawn_next()
    assert game.current is not None
    first_kind = game.current.kind

    ok = game.hold()

    assert ok is True
    assert game.hold_kind == first_kind
    assert game.current is not None
    assert game.can_hold is False


def test_hold_only_once_per_turn():
    game = Game()
    game.spawn_next()

    first = game.hold()
    current_after_first = game.current.kind if game.current is not None else None
    hold_after_first = game.hold_kind
    second = game.hold()

    assert first is True
    assert second is False
    assert game.hold_kind == hold_after_first
    assert (game.current.kind if game.current is not None else None) == current_after_first


def test_hold_resets_after_lock():
    game = Game()
    game.spawn_next()

    assert game.hold() is True
    assert game.can_hold is False

    game.hard_drop()

    assert game.can_hold is True
    assert game.hold() is True
