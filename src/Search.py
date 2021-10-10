from __future__ import annotations
from dataclasses import dataclass
from abc import ABC, abstractmethod
from .Chord import Progression, Voicing, Chord
from .Notes import Interval
from typing import Optional, List, Dict, Tuple
from random import choice
from queue import PriorityQueue


class DistanceCalculator(ABC):
    @abstractmethod
    def distance_between(self, voicing_1: Voicing, voicing_2: Voicing) -> int:
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
    def distance_between(self, voicing_1: Voicing, voicing_2: Voicing) -> int:
        return 0


@dataclass(frozen=True)
class Search:
    progression: Progression

    distance_calculator: DistanceCalculator = PairWiseDistance()
    initial_voicing: Optional[Voicing] = None
    voices: int = 4

    def get_first_voicing(self) -> Voicing:
        if self.initial_voicing is not None:
            return self.initial_voicing

        first_chord_voicings = self.progression.chords[0].generate_voicings()
        return choice(first_chord_voicings)

    # TODO return all lists of voicings with the lowest cost?
    def a_star(self) -> List[Voicing]:
        """
        A star search - expand node with lowest current + step cost
        """
        # Wrap the progression around so the initial voicing can act as the target node
        cyclical_progression = self.progression.chords[1:] + [
            self.progression.chords[0]
        ]

        costs: Dict[VoicingNode, int] = {}
        came_from: Dict[VoicingNode, Optional[VoicingNode]] = {}

        initial_voicing = self.get_first_voicing()
        # Start with index -1 to make the progression cyclical
        initial_node = VoicingNode(initial_voicing, -1)
        target_node = VoicingNode(initial_voicing, len(self.progression.chords) - 1)

        # Set the initial values for cost and
        costs[initial_node] = 0
        came_from[initial_node] = None

        # Generate the voicings allowed for each unique chord in the progression
        all_voicings = {
            chord: chord.generate_voicings() for chord in cyclical_progression
        }
        frontier: PriorityQueue = PriorityQueue()

        def expand(current_node: VoicingNode) -> None:
            """
            Adds search nodes resulting from expanding a given node to the frontier
            """
            # Find out the next chord in the sequece
            next_chord = cyclical_progression[current_node.index_in_progression + 1]
            current_cost = costs[current_node]

            # Add new nodes to the frontier
            for voicing in all_voicings[next_chord]:
                # Add the distance to the new voicing and the heuristic to the accumulated cost
                new_cost = (
                    current_cost
                    + self.distance_calculator.distance_between(
                        current_node.voicing, voicing
                    )
                    + self.distance_calculator.distance_between(
                        voicing, initial_voicing
                    )
                )

                new_node = VoicingNode(voicing, current_node.index_in_progression + 1)

                # Only add the new node to the frontier if hasn't been seen before or is visited at a lower cost
                if new_node not in costs or costs[new_node] > new_cost:
                    costs[new_node] = new_cost
                    came_from[new_node] = current_node
                    frontier.put((new_cost, new_node))

        # Generate the initial frontier
        expand(initial_node)

        # Note frontier should never be empty
        while not frontier.empty():
            value, current = frontier.get()

            # If we are going to expand the goal node, stop
            if current == target_node:
                break

            # Otherwise, expand the current node
            expand(current)
            print(f"Expanding: {current} with f {value}")

        voicing_list: List[Voicing] = []
        # Traverse the came_from graph to produce the list of voicings
        while target_node != initial_node:
            target_node = came_from[target_node]  # type: ignore
            voicing_list.insert(0, target_node.voicing)

        return voicing_list


@dataclass(frozen=True)
class VoicingNode:
    """
    Wrapper class to allow for uniquely identifying search nodes
    We need to keep the index because a progression could have one chord multiple times
    """

    voicing: Voicing
    index_in_progression: int

    def __lt__(self, other: VoicingNode) -> bool:
        """
        Implemented because prioirties in the priority queue are sometimes equal
        Prioritise nodes further through the progression
        """
        return self.index_in_progression > other.index_in_progression
