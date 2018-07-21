# The adventure begins!

OCTAVE = 8
CHROMATIC = 12
INTERVALS = {
    'major': [2, 2, 1, 2, 2, 2, 1],
    'natural_minor': [2, 1, 2, 2, 1, 2, 2],
}
MAJOR_FORMULA = {
    'major': [1, 3, 5],
    'major6': [1, 3, 5, 6],
    'major7': [1, 3, 5, 7],
    'major9': [1, 3, 5, 7, 9],
    'majoradd9': [1, 3, 5, 9],
    'major6/9': [1, 3, 5, 6, 9],
    'major7/6': [1, 3, 5, 6, 7],
    'major13': [1, 3, 5, 7, 9, 13],
}
# TODO: figure out the flats problem.
MINOR_FORMULA = {
    'major': [1, 3, 5],
    'major6': [1, 3, 5, 6],
    'major7': [1, 3, 5, 7],
    'major9': [1, 3, 5, 7, 9],
    'majoradd9': [1, 3, 5, 9],
    'major6/9': [1, 3, 5, 6, 9],
    'major7/6': [1, 3, 5, 6, 7],
    'major13': [1, 3, 5, 7, 9, 13],
}

notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
equivalents = [('C#', 'Db'), ('D#', 'Eb'), ('F#', 'Gb'), ('G#', 'Ab'), ('A#', 'Bb')]

"""
Returns the chromatic cycle given the root note
"""
def cycle(root):
    if root not in notes: 
        print('Note does not exist!')
        return
    start = notes.index(root)
    return notes[start:] + notes[:start+1]

# test
print("C chromatic: ", cycle('C'))

# SCALES

"""
Returns the scale given root note.
Default is major scale if no scale is picked
"""
# inteval: w, w, h, w, w, w, h
def scale(root, scale_type='major'):
    if root not in notes: 
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
    root_notes = cycle(root)
    return [root_notes[i] for i in indices]
# test
print("C natural minor: ", scale('C', 'natural_minor'))

# CHORDS

# TODO: Figure our tright abstraction for representing chord objects

"""
Returns the type of chord for given root note
"""
def chord(root, name):
    if root not in notes: 
        print('Note does not exist!')
        return
    if name not in MAJOR_FORMULA: 
        print('Scale does not exist or not yet supported!')
        return
    indices = [f-1 for f in MAJOR_FORMULA[name]]
    for i, index in enumerate(indices):
        if index >= 8:
            indices[i] = index - OCTAVE + 1
    # indices.sort()
    root_notes = scale(root)
    return [root_notes[i] for i in indices]
# test
print("C major add 9: ", chord('C', 'majoradd9'))