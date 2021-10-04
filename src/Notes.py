from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Tuple

TEMPERAMENT = 12


class NoteName(Enum):
    C = 0
    CS = 1
    D = 2
    DS = 3
    E = 4
    F = 5
    FS = 6
    G = 7
    GS = 8
    A = 9
    AS = 10
    B = 11


@dataclass(frozen=True)
class Note:
    """
    Concrete instance of a note - specifies note name and pitch
    """

    note_name: NoteName
    octave: int


class Interval(Enum):
    SAME = 0
    SECOND_MIN = 1
    SECOND_MAJ = 2
    THIRD_MIN = 3
    THIRD_MAJ = 4
    FOURTH_PERF = 5
    TRITONE = 6
    FIFTH_PERF = 7
    SIXTH_MIN = 8
    SIXTH_MAJ = 9
    SEVENTH_MIN = 10
    SEVENTH_MAJ = 11

    def add_to_note_name(self, note_name: NoteName) -> NoteName:
        """
        Adds the interval to note_name
        """
        return NoteName((note_name.value + self.value) % TEMPERAMENT)

    @staticmethod
    def get_relation(root: NoteName, note: NoteName) -> Interval:
        """
        Returns the relation of a note to a given root (ascending interval)
        """
        semitone_difference = (note.value + TEMPERAMENT - root.value) % TEMPERAMENT
        return Interval(semitone_difference)

    @staticmethod
    def get_interval(note_1: Note, note_2: Note) -> Tuple[Interval, int]:
        """
        Returns the effective (closed) ascending interval from note_1 to note_2 and the actual semitone difference
        """
        semitone_difference = (
            note_2.note_name.value - note_1.note_name.value
        ) + TEMPERAMENT * (note_2.octave - note_1.octave)
        return (
            Interval.get_relation(note_1.note_name, note_2.note_name),
            semitone_difference,
        )
