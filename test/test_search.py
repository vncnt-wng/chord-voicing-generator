from src.Notes import NoteName, Note, Interval
from src.Chord import Voicing
from src.Search import PairWiseDistance

def test_pairwise_distance():
    voicing_1 = Voicing([
        Note(NoteName.G, 4),
        Note(NoteName.B, 4),
        Note(NoteName.D, 5)
    ])
    voicing_2 = Voicing([
        Note(NoteName.G, 4),
        Note(NoteName.C, 5),
        Note(NoteName.E, 5)
    ])
    voicing_3 = Voicing([
        Note(NoteName.G, 3),
        Note(NoteName.B, 3),
        Note(NoteName.D, 4)
    ])

    calculator = PairWiseDistance()

    assert calculator.distance_between(voicing_1, voicing_1) == 0

    assert calculator.distance_between(voicing_1, voicing_2) == 3
    assert calculator.distance_between(voicing_2, voicing_3) == 39
    assert calculator.distance_between(voicing_1, voicing_3) == 36

    assert calculator.distance_between(voicing_1, voicing_2) == calculator.distance_between(voicing_2, voicing_1)
