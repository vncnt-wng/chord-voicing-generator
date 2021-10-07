from dataclasses import dataclass
from abc import ABC, abstractmethod
from .Chord import Progression, Voicing
from .Notes import Interval
from typing import Optional


class DistanceCalculator(ABC):
    @abstractmethod
    def distance_between(voicing_1: Voicing, voicing_2: Voicing) -> int:
        ...


@dataclass(frozen=True)
class PairWiseDistance(DistanceCalculator):
    def distance_between(self, voicing_1: Voicing, voicing_2: Voicing) -> int:
        return sum(
            [
                abs(Interval.get_interval(note_pairs[0], note_pairs[1])[1])
                for note_pairs in zip(voicing_1.notes, voicing_2.notes)
            ]
        )


@dataclass(frozen=True)
class EditDistance(DistanceCalculator):
    def distance_between(voicing_1: Voicing, voicing_2: Voicing) -> int:
        return 0


@dataclass(frozen=True)
class Search:
    distance_calculator: DistanceCalculator
    progression: Progression
    inital_voicing: Optional[Voicing] = None
