from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, List, Set
from enum import Enum
from .Notes import Note, NoteName, Interval


class Triad(Enum):
    MAJOR = [Interval.THIRD_MAJ, Interval.FIFTH_PERF]
    MINOR = [Interval.THIRD_MIN, Interval.FIFTH_PERF]
    DIMINISHED = [Interval.THIRD_MIN, Interval.TRITONE]
    SUSPENDED = [Interval.SECOND_MAJ, Interval.FOURTH_PERF, Interval.FIFTH_PERF]


@dataclass(frozen=True)
class Chord:
    root: NoteName
    triad: Triad
    # TODO abstract extensions out
    extensions: Optional[List[Interval]] = None

    def get_note_names(self) -> Set[NoteName]:
        """
        Returns the set of all intervals of the chord evaluated against the root
        """
        all_intervals: List[Interval] = self.triad.value.copy()
        if self.extensions:
            all_intervals += self.extensions

        note_names = {
            interval.add_to_note_name(self.root) for interval in all_intervals
        }
        note_names.add(self.root)
        return note_names

    def generate_voicings(
        self,
        range_start: Note = Note(NoteName.C, 3),
        range_end: Note = Note(NoteName.C, 6),
    ) -> List[Voicing]:
        """
        Generates all strict (no extensions) voicings for the chord [range_start, range_end)
        """
        notes = self.get_note_names()
        # TODO
        return []


@dataclass(frozen=True)
class Voicing:
    # TODO - determine if we should have chord_label: Chord
    notes: List[Note]

    def is_voicing_for(self, chord: Chord) -> bool:
        """
        Returns true if the set of note names of the voicing is a subset of the chords' note names
        """
        voicing_note_names = {note.note_name for note in self.notes}
        return voicing_note_names.issubset(chord.get_note_names())


@dataclass(frozen=True)
class Progression:
    chords: List[Chord]
