from enum import Enum
import pandas as pd
from itertools import cycle
from collections import deque

from Chord import Chord
from constants import *

# this is just a convenience function that's used for debugging for now
def convert(notes):
    actual = []
    for n in notes:
        if n in EQUIVALENTS:
            actual.append(EQUIVALENTS[n])
        else:
            actual.append(n)
    return actual

# TODO In future give back both versions that Chord can use to pretty print
def chromatic(root):
    """Returns the chromatic notes given the root note"""
    notes = SHARP_NOTES if root in SHARPS else FLAT_NOTES
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
# print(chromatic_cycle('E', NUM_FRETS))

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
    if root not in SHARP_NOTES and root not in FLAT_NOTES: 
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
        loc = loc - CHROMATIC if loc >= CHROMATIC else loc
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
    if key not in SHARP_NOTES or key not in FLAT_NOTES:
        print('Key does not exist:', key)
        return
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
    if root not in SHARP_NOTES and root not in FLAT_NOTES: 
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
    if root not in SHARP_NOTES and root not in FLAT_NOTES: 
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
    if root not in SHARP_NOTES and root not in FLAT_NOTES: 
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

def chord(root, formula):
    """
    Returns the chord notes given the root note and formula

    root --- the root note (for e.g. C)
    formula --- the type of chord (for e.g. maj)
    """
    if root not in SHARP_NOTES or root not in FLAT_NOTES: 
        print('Root note does not exist!')
    if formula in MAJOR_FORMULA:
        return major(root, formula)
    elif formula in MINOR_FORMULA:
        return minor(root, formula)
    elif formula in DOMINANT_FORMULA:
        return dominant(root, formula)
    else:
        print('Chord does not exist or not yet supported!')

# test
# print('Cmaj', chord('C', 'maj').notes)
# print('Cm', chord('C', 'min').notes)
# print('C7', chord('C', '7').notes)
# print('Cdim', chord('C', 'dim').notes)
# print('C+', chord('C', '+').notes)

# Fretboard

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
# print(guitar_fretboard)

def notes_on_fretboard(notes, frets=NUM_FRETS, open=True):
    """
    Returns a dataframe containing the notes supplied given a
    window of frets (for e.g. 4 frets)

    notes --- the notes to find
    frets --- number of frets to limits search
    open --- whether to consider open notes or not
    """
    # add 1 because we need to consider open notes
    frets = frets + 1
    notes = list(notes) if type(notes) != 'list' else notes
    df = guitar_fretboard
    start = 0 if open else 1
    # looks at specified fret window
    return df[df.iloc[:, start:frets].isin(notes)].iloc[:, start:frets].fillna('.')
# test
# show all notes of Cmaj on fretboard 
# print("Cmaj\n", notes_on_fretboard(major('C', 'maj').notes).to_string())
# print("Cmaj9\n", notes_on_fretboard(major('C', 'maj9').notes).to_string())

# major scale is good but contains notes isn't sufficient for other scales
# print("C major scale\n", notes_on_fretboard(scale('C', 'major')).to_string())

# TODO scale finder
# print("Dorian mode in key of C\n", notes_on_fretboard(mode('C', 'dorian')).to_string())