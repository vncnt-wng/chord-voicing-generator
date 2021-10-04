from dataclasses import dataclass
from typing import Optional, List, Set
from enum import Enum
from Notes import Note, NoteName, Interval


class Triad(Enum):
    MAJOR = [Interval.THIRD_MAJ, Interval.FIFTH_PERF]
    MINOR = [Interval.THIRD_MIN, Interval.FIFTH_PERF]
    DIMINISHED = [Interval.THIRD_MIN, Interval.TRITONE]


@dataclass(frozen=True)
class Chord:
    root: NoteName
    triad: Triad
    extensions: Optional[List[Interval]] = None

    def get_note_names(self) -> Set[NoteName]:
        return set()


@dataclass(frozen=True)
class Voicing:
    chord_label: Chord
    notes: List[Note]


@dataclass(frozen=True)
class Progression:
    chords: List[Chord]

    def generate_voicings(self) -> List[Voicing]:
        return []
