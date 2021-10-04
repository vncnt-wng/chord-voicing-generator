from src.Notes import NoteName, Note, Interval


def test_add_to_note_name():
    c = NoteName.C
    b = NoteName.B
    fifth = Interval.FIFTH_PERF

    assert fifth.add_to_note_name(c) == NoteName.G
    assert fifth.add_to_note_name(b) == NoteName.FS


def test_get_relation():
    c = NoteName.C
    g = NoteName.G

    assert Interval.get_relation(g, c) == Interval.FOURTH_PERF
    assert Interval.get_relation(c, g) == Interval.FIFTH_PERF


def test_get_interval():
    c = NoteName.C
    g = NoteName.G

    # Test closed postion
    assert Interval.get_interval(Note(g, 4), Note(c, 4)) == (Interval.FOURTH_PERF, -7)
    assert Interval.get_interval(Note(c, 4), Note(g, 4)) == (Interval.FIFTH_PERF, 7)

    # Test closed postion
    assert Interval.get_interval(Note(g, 5), Note(c, 4)) == (Interval.FOURTH_PERF, -19)
    assert Interval.get_interval(Note(c, 4), Note(g, 5)) == (Interval.FIFTH_PERF, 19)

    # Test octaves/same
    assert Interval.get_interval(Note(c, 4), Note(c, 4)) == (Interval.SAME, 0)
    assert Interval.get_interval(Note(c, 4), Note(c, 5)) == (Interval.SAME, 12)
