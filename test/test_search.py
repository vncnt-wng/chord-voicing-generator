from src.Notes import NoteName, Note, Interval
from src.Chord import Voicing, Chord, Triad, Progression
from src.Search import PairWiseDistance, Search


def test_pairwise_distance():
    voicing_1 = Voicing([Note(NoteName.G, 4), Note(NoteName.B, 4), Note(NoteName.D, 5)])
    voicing_2 = Voicing([Note(NoteName.G, 4), Note(NoteName.C, 5), Note(NoteName.E, 5)])
    voicing_3 = Voicing([Note(NoteName.G, 3), Note(NoteName.B, 3), Note(NoteName.D, 4)])

    calculator = PairWiseDistance()

    assert calculator.distance_between(voicing_1, voicing_1) == 0

    assert calculator.distance_between(voicing_1, voicing_2) == 3
    assert calculator.distance_between(voicing_2, voicing_3) == 39
    assert calculator.distance_between(voicing_1, voicing_3) == 36

    assert calculator.distance_between(
        voicing_1, voicing_2
    ) == calculator.distance_between(voicing_2, voicing_1)


def test_get_first_voicing():
    c_maj = Chord(NoteName.C, Triad.MAJOR)
    triad_voicing = Voicing(
        [Note(NoteName.C, 4), Note(NoteName.E, 4), Note(NoteName.G, 4)]
    )

    searcher_with_initial = Search(Progression([c_maj]), initial_voicing=triad_voicing)
    searcher_without_initial = Search(Progression([c_maj]))

    assert searcher_with_initial.get_first_voicing() == triad_voicing

    generated_first_voicing = searcher_without_initial.get_first_voicing()

    assert generated_first_voicing.is_voicing_for(c_maj)
