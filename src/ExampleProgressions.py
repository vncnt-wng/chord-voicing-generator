from .Chord import Chord, Progression, Triad
from .Notes import NoteName, Interval

# Triad 2 5 1
d_min = Chord(root=NoteName.D, triad=Triad.MINOR)
g_maj = Chord(root=NoteName.G, triad=Triad.MAJOR)
c_maj = Chord(root=NoteName.C, triad=Triad.MAJOR)

two_five_one_traid = Progression(chords=[d_min, g_maj, c_maj])

# Extended 2 5 1
d_min7 = Chord(root=NoteName.D, triad=Triad.MINOR, extensions=[Interval.SEVENTH_MIN])
g_7 = Chord(root=NoteName.G, triad=Triad.MAJOR, extensions=[Interval.SEVENTH_MIN])
c_maj7 = Chord(root=NoteName.C, triad=Triad.MAJOR, extensions=[Interval.SEVENTH_MAJ])

two_five_one_extended = Progression(chords=[d_min7, g_7, c_maj7])
