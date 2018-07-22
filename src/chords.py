from Chord import Chord

# Declaring all constants
OCTAVE = 8
CHROMATIC = 12
INTERVALS = {
    'major': [2, 2, 1, 2, 2, 2, 1],
    'natural_minor': [2, 1, 2, 2, 1, 2, 2],
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

# TODO In future give back both versions that Chord can use to pretty print
def chromatic(root):
    """Returns the chromatic notes given the root note"""
    notes = sharp_notes if root in sharps else flat_notes
    start = notes.index(root)
    return notes[start:] + notes[:start+1]

# test
# print("C chromatic: ", chromatic('C'))
# print("F chromatic: ", chromatic('F'))

# SCALES

def scale(root, scale_type='major'):
    """
    Returns the scale given root note. 
    Default is major scale if no scale is picked
    """
    if root not in sharp_notes and root not in flat_notes: 
        print('Note does not exist!')
        return
    if scale_type not in INTERVALS: 
        print('Scale does not exist or not yet supported!')
        return
    interval = INTERVALS['major']
    if scale_type == 'natural_minor':
        interval = INTERVALS['natural_minor']
    indices = [0]
    for i in interval:
        loc = indices[-1] + i
        if loc >= CHROMATIC:
            loc = loc - CHROMATIC
        indices.append(loc)
    # print(indices)
    root_notes = chromatic(root)
    return [root_notes[i] for i in indices]
# test
# print("Eb natural minor: ", scale('Eb', 'natural_minor'))

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
