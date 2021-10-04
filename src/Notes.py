from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class NoteName(Enum):
    C = (0,)
    CS = (1,)
    D = (2,)
    DS = (3,)
    E = (4,)
    F = (5,)
    FS = (6,)
    G = (7,)
    GS = (8,)
    A = (9,)
    AS = (10,)
    B = 11


@dataclass(frozen=True)
class Note:
    note_name: NoteName
    octave: int


@dataclass(frozen=True)
class Interval(Enum):
    SAME = (0,)
    SECOND_MIN = (1,)
    SECOND_MAJ = (2,)
    THIRD_MIN = (3,)
    THIRD_MAJ = (4,)
    FOURTH_PERF = (5,)
    TRITONE = (6,)
    FIFTH_PERF = (7,)
    SIXTH_MIN = (8,)
    SIXTH_MAJ = (9,)
    SEVENTH_MIN = (10,)
    SEVENTH_MAJ = 11

    @staticmethod
    def get_interval(note_1: Note, note_2: Note) -> Interval:
        pass
