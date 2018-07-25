from enum import Enum
import pandas as pd
from itertools import cycle

from Chord import Chord



# Declaring all constants
OCTAVE = 8
CHROMATIC = 12
# 1 stands for semitone, 2 for whole tone
SCALES = {
    'major': [2, 2, 1, 2, 2, 2, 1],
    'natural_minor': [2, 1, 2, 2, 1, 2, 2],
}
# each mode value stands for the interval to start on for key
MODES = {
    'ionian': 1,
    'dorian': 2,
    'phrygian': 3,
    'lydian': 4,
    'mixolydian': 5,
    'aeolian': 6,
    'locrian': 7,
}
MAJOR_FORMULA = {
    'maj': [1, 3, 5],
    'maj6': [1, 3, 5, 6],
    'maj7': [1, 3, 5, 7],
    'maj9': [1, 3, 5, 7, 9],
    'majadd9': [1, 3, 5, 9],
    'maj6/9': [1, 3, 5, 6, 9],
    'maj7/6': [1, 3, 5, 6, 7],
    'maj13': [1, 3, 5, 7, 9, 13],
}
# This is the basic formula but the 3rd and 7th will receive flat accidental
# by the minor method below
MINOR_FORMULA = {
    'min': [1, 3, 5],
    'min6': [1, 3, 5, 6],
    'min7': [1, 3, 5, 7],
    'min9': [1, 3, 5, 7, 9],
    'min11': [1, 3, 5, 7, 9, 11],
    'min7/11': [1, 3, 5, 7, 11],
    'minadd9': [1, 3, 5, 9],
    'min6/9': [1, 3, 5, 6, 9],
    'minmaj7': [1, 3, 5, 7],
    'minmaj9': [1, 3, 5, 7, 9],
}
# Dominants which will receive accidentals by the dominant method below
DOMINANT_FORMULA = {
    '7': [1, 3, 5, 7],
    '7/6': [1, 3, 5, 6, 7],
    '7/11': [1, 3, 5, 7, 11],
    '7sus4': [1, 4, 5, 7],
    '7/6sus4': [1, 4, 5, 6, 7],
    '9': [1, 3, 5, 7, 9],
    '11': [1, 3, 5, 7, 9, 11],
    '13': [1, 3, 5, 7, 9, 13],
    '7/6/11': [1, 3, 5, 7, 11, 13],
    '11/13': [1, 3, 5, 7, 9, 11, 13],
    'dim': [1, 3, 5, 6], 
    '+': [1, 3, 5],
}
sharps = ['C', 'G', 'D', 'A', 'E', 'B', 'F#', 'C#']
flats = ['F', 'Bb', 'Eb', 'Ab', 'Db', 'Gb']
sharp_notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
flat_notes = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
# these will be used to convert between the representations based
# on whether scale or chord adds accidentals (for e.g. min will use flat)
equivalents = {
    # # to b
    'C#': 'Db', 
    'D#': 'Eb', 
    'F#': 'Gb', 
    'G#': 'Ab', 
    'A#': 'Bb',
    # b to #
    'Db': 'C#',
    'Eb': 'D#',
    'Gb': 'F#', 
    'Ab': 'G#',
    'Bb': 'A#',
}
GUITAR_STANDARD = ['E', 'A', 'D', 'G', 'B', 'E']
NUM_STRINGS = 6
NUM_FRETS = 21

# TODO In future give back both versions that Chord can use to pretty print
def chromatic(root):
    """Returns the chromatic notes given the root note"""
    notes = sharp_notes if root in sharps else flat_notes
    start = notes.index(root)
    return notes[start:] + notes[:start]

# test
# print("C chromatic: ", chromatic('C'))
# print("F chromatic: ", chromatic('F'))

def chromatic_cycle(key, num=1):
    """
    Returns a chromatic scale for a given number of notes.

    key --- the key
    num --- number of notes to return
    """
    chromatics = chromatic(key)
    all_notes = []
    count = 0
    for n in cycle(chromatics):
        if count < num:
            all_notes.append(n)
        else:
            break
        count = count + 1
    return all_notes
# test
# print(chromatic_cycle(chromatic('E'), NUM_FRETS+1))

def fretboard():
    """
    Returns a dataframe containing all notes for each of the guitar string, where
    each row is a string and each column is a fret including the open notes.
    """
    fretboard = []
    for i in range(NUM_STRINGS):
        # NUM_FRETS + 1 because we are counting open string notes as well
        notes_on_string = chromatic_cycle(GUITAR_STANDARD[i], NUM_FRETS+1)
        fretboard.insert(0, notes_on_string)
    return pd.DataFrame(data=fretboard)
guitar_fretboard = fretboard()
print(guitar_fretboard)

# SCALES
# TODO come up with a Scale object representation for easy construction of 
# scales based on major scale. The current method works but it would be more

# intuitive from music theory perspective to do embellishments
# For example a natural minor is 1 2 b3 4 5 b6 b7 
# This is a major with b3, b6, b7
def scale(root, scale_type='major'):
    """
    Returns the scale given root note. 
    Default is major scale if no scale is picked
    """
    if root not in sharp_notes and root not in flat_notes: 
        print('Note does not exist!')
        return
    if scale_type not in SCALES: 
        print('Scale does not exist or not yet supported!')
        return
    interval = SCALES[scale_type]
    # TODO handle case where embellish are flats (minor scale for e.g.)
    # this will be achieved if there is a Scale object representation
    indices = [0]
    for i in interval[:-1]:
        loc = indices[-1] + i
        if loc >= CHROMATIC:
            loc = loc - CHROMATIC
        indices.append(loc)
    # print(indices)
    root_notes = chromatic(root)
    return [root_notes[i] for i in indices]
# test
# print("C major: ", scale('C', 'major'))
# print("C natural minor: ", scale('C', 'natural_minor'))
# print("C dorian: ", scale('C', 'dorian'))

def mode(key, mode_name='ionian'):
    """
    Returns the mode for the given key.

    Keyword arguments:
    key -- the key
    mode_name -- the name of the mode (ionian if not supplied)
    """
    if mode_name not in MODES: 
        print('Mode does not exist:', mode_name)
        return
    if key not in sharp_notes or key not in flat_notes:
        print('Key does not exist:', key)
        return
    # for now, deque is only needed for this function; it makes it convenient
    # to rotate based on index for mode
    from collections import deque
    index = MODES[mode_name]
    major = deque(scale(key))
    major.rotate(-(index-1))
    return list(major)

# test
# print("Ionian mode in key of C", mode('C'))
# print("Dorian mode in key of C", mode('C', 'dorian'))
# print("Lydian mode in key of C", mode('C', 'lydian'))

def major(root, formula, interval=[]):
    """
    Returns a major chord for given root note.

    Keyword arguments:
    root -- the root note
    formula -- the formula part of chord (e.g. maj7)
    interval -- optional custom list of interval to use (not used for now)
    """
    if root not in sharp_notes and root not in flat_notes: 
        print('Note does not exist:', root)
        return
    if formula not in MAJOR_FORMULA:
        print('Chord does not exist or not yet supported!')
        return
    indices = [f-1 for f in MAJOR_FORMULA[formula]]
    for i, index in enumerate(indices):
        if index >= OCTAVE:
            indices[i] = index - OCTAVE + 1
    root_notes = scale(root)
    notes = [root_notes[i] for i in indices]
    return Chord(root + formula, notes, chromatic(root))

# test 
# major('C', 'maj7').print()
# major('F#', 'maj7').print()
# major('Gb', 'maj7').print()
# invalid chords
# major('Fb', 'maj7').print()
# major('Cb', 'maj7').print()

def minor(root, formula, interval=[]):
    """
    Returns a minor chord for given root note.

    Keyword arguments:
    root -- the root note
    formula -- the formula part of chord (e.g. min9)
    interval -- optional custom list of interval to use
    """
    if root not in sharp_notes and root not in flat_notes: 
        print('Note does not exist:', root)
        return
    if formula not in MINOR_FORMULA: 
        print('Chord does not exist or not yet supported!')
        return
    indices = [f-1 for f in MINOR_FORMULA[formula]]
    for i, index in enumerate(indices):
        if index >= OCTAVE:
            indices[i] = index - OCTAVE + 1
    root_notes = scale(root)
    notes = [root_notes[i] for i in indices]
    chord = Chord(root+formula, notes, chromatic(root)).flatThird()
    # exceptions that don't contain a seventh or shouldn't flat it
    if 'minmaj' in formula or '6' in formula or 'add9' in formula:
        return chord
    return chord.flatSeventh()

# minor('C', 'min').print()
# minor('C', 'min7').print()
# minor('C', 'min9').print()
# minor('C', 'minmaj9').print()
# invalid
# minor('D#', 'minmaj9').print()

def dominant(root, formula, interval=[]):
    """
    Returns a dominant chord for given root note.

    Keyword arguments:
    root -- the root note
    formula -- the formula part of chord (e.g. min9)
    interval -- optional custom list of interval to use
    """
    if root not in sharp_notes and root not in flat_notes: 
        print('Note does not exist!')
        return
    if formula not in DOMINANT_FORMULA: 
        print('Chord does not exist or not yet supported!')
        return
    indices = [f-1 for f in DOMINANT_FORMULA[formula]]
    for i, index in enumerate(indices):
        if index >= OCTAVE:
            indices[i] = index - OCTAVE + 1
    root_notes = scale(root)
    notes = [root_notes[i] for i in indices]
    chord = Chord(root+formula, notes, chromatic(root))
    # exceptions that don't contain a seventh or shouldn't flat it
    if '+' in formula:
        return chord.sharpFifth()
    if 'dim' in formula:
        return chord.flatThird().flatFifth()
    return chord.flatSeventh()

# test
# dominant('Db', '7').print()
# dominant('Db', '+').print()
# dominant('Db', 'dim').print()
