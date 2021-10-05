from src.Chord import Chord, Voicing, Triad
from src.Notes import Interval, NoteName, Note


def test_get_note_names():
    # Test Triads
    c_major_notes = Chord(NoteName.C, Triad.MAJOR).get_note_names()

    assert NoteName.C in c_major_notes
    assert NoteName.E in c_major_notes
    assert NoteName.G in c_major_notes

    a_dim_notes = Chord(NoteName.A, Triad.DIMINISHED).get_note_names()

    assert NoteName.A in a_dim_notes
    assert NoteName.C in a_dim_notes
    assert NoteName.DS in a_dim_notes

    # Test with extensions
    flat_seven = [Interval.SEVENTH_MIN]
    six_nine = [Interval.SIXTH_MAJ, Interval.SECOND_MAJ]

    c_seven_notes = Chord(
        NoteName.C, Triad.MAJOR, extensions=flat_seven
    ).get_note_names()
    assert NoteName.C in c_seven_notes
    assert NoteName.E in c_seven_notes
    assert NoteName.G in c_seven_notes
    assert NoteName.AS in c_seven_notes

    c_six_nine_notes = Chord(
        NoteName.C, Triad.MAJOR, extensions=six_nine
    ).get_note_names()

    assert NoteName.C in c_six_nine_notes
    assert NoteName.E in c_six_nine_notes
    assert NoteName.G in c_six_nine_notes
    assert NoteName.A in c_six_nine_notes
    assert NoteName.D in c_six_nine_notes


def test_generate_voicings():
    pass


def test_is_voicing_for():
    c_major = Chord(NoteName.C, Triad.MAJOR)
    six_nine = [Interval.SIXTH_MAJ, Interval.SECOND_MAJ]
    c_major_six_nine = Chord(NoteName.C, Triad.MAJOR, extensions=six_nine)

    c_major_voices = [Note(NoteName.C, 4), Note(NoteName.E, 3), Note(NoteName.G, 3)]
    c_major_voicing = Voicing(c_major_voices)

    c_major_six_nine_voices = c_major_voices + [
        Note(NoteName.D, 4),
        Note(NoteName.A, 4),
    ]
    c_major_six_nine_voicing = Voicing(c_major_six_nine_voices)

    # Test contains all notes
    assert c_major_voicing.is_voicing_for(c_major)
    assert c_major_six_nine_voicing.is_voicing_for(c_major_six_nine)

    # Test voicing is subset
    assert c_major_voicing.is_voicing_for(c_major_six_nine)

    # Assert unexpected extensions will return false
    assert not c_major_six_nine_voicing.is_voicing_for(c_major)
