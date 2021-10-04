from dataclasses import dataclass
from typing import Optional, List
from enum import Enum
from Notes import Note, NoteName, Interval


class Triad(Enum):
    MAJOR = (1,)
    MINOR = 2


@dataclass(frozen=True)
class Chord:
    root: NoteName
    triad: Triad
    extensions: Optional[List[Interval]]


@dataclass(frozen=True)
class Voicing:
    chord_label: Chord
