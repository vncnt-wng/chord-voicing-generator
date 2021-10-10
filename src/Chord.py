from __future__ import annotations

from dataclasses import dataclass
import itertools
from typing import Optional, List, Set
from enum import Enum
from itertools import combinations
from .Notes import Note, NoteIterator, NoteName, Interval, TEMPERAMENT


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

    def get_all_intervals(self) -> List[Interval]:
        all_intervals: List[Interval] = self.triad.value.copy()
        if self.extensions:
            all_intervals += self.extensions
        return all_intervals

    def get_note_names(self) -> Set[NoteName]:
        """
        Returns the set of all intervals of the chord evaluated against the root
        """
        all_intervals: List[Interval] = self.get_all_intervals()

        note_names = {
            interval.add_to_note_name(self.root) for interval in all_intervals
        }
        note_names.add(self.root)
        return note_names

    def generate_voicings(
        self,
        range_start: Note = Note(NoteName.C, 3),
        range_end: Note = Note(NoteName.A, 6),
        voices: int = 4,
    ) -> List[Voicing]:
        """
        Generates all strict (no extensions) voicings for the chord [range_start, range_end)
        """
        note_names: Set[NoteName] = self.get_note_names()

        # Determine all potential chord tones we can use in the range
        available_notes: List[Note] = []
        note_iterator = iter(range_start)  # type: ignore

        while next(note_iterator) < range_end:
            if note_iterator.note.note_name in note_names:
                available_notes.append(note_iterator.note)

        return [
            Voicing(list(note_list))
            for note_list in itertools.combinations(available_notes, voices)
        ]

    def __hash__(self):
        all_intervals = self.get_all_intervals()
        hash_value = 0
        for index, interval in enumerate(all_intervals):
            hash_value += interval.value * index * TEMPERAMENT
        hash_value = hash_value * (self.root.value + 1) * TEMPERAMENT
        return hash_value


@dataclass(frozen=True, eq=True)
class Voicing:
    # TODO - determine if we should have chord_label: Chord
    # List of notes ordered
    notes: List[Note]

    def is_voicing_for(self, chord: Chord) -> bool:
        """
        Returns true if the set of note names of the voicing is a subset of the chords' note names
        """
        voicing_note_names = {note.note_name for note in self.notes}
        return voicing_note_names.issubset(chord.get_note_names())

    def __hash__(self) -> int:
        """
        Returns a unique integer for every voicing
        """
        hash_value = 0
        sorted_notes = self.notes.copy()
        sorted_notes.sort()
        for index, note in enumerate(sorted_notes):
            # 200 is beyond any reasonable range of notes - typical pianos are 88
            # in this way each
            hash_value += hash(note) * (index + 1) * 200
        return hash_value

    def __str__(self) -> str:
        return f"[{', '.join([str(note) for note in self.notes])}]"


@dataclass(frozen=True)
class Progression:
    chords: List[Chord]
