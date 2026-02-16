from collections import Counter

from engine.game import Game


def test_next_kind_has_7_unique_in_one_bag():
    g = Game()
    picks = [g.next_kind() for _ in range(7)]
    assert len(set(picks)) == 7


def test_next_kind_has_two_each_in_two_bags():
    g = Game()
    picks = [g.next_kind() for _ in range(14)]
    counts = Counter(picks)
    assert set(counts.keys()) == {"L", "J", "O", "I", "T", "S", "Z"}
    assert all(v == 2 for v in counts.values())


def test_peek_next_does_not_consume_order():
    g = Game()
    preview = g.peek_next(3)
    assert len(preview) == 3
    first = g.next_kind()
    second = g.next_kind()
    third = g.next_kind()
    assert [first, second, third] == preview
