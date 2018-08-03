from chords import *
from constants import *

# Fretboard (experimental)

def fretboard():
    """
    Returns a dataframe containing all notes for each of the guitar string, where
    each row is a string and each column is a fret including the open notes.
    """
    fretboard_notes = []
    for i in range(NUM_STRINGS):
        # NUM_FRETS + 1 because we are counting open string notes as well
        notes_on_string = chromatic_cycle(GUITAR_STANDARD[i], NUM_FRETS+1)
        fretboard_notes.insert(0, notes_on_string)
    return pd.DataFrame(data=fretboard_notes)

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

# TODO scale finder
c_dorian = notes_on_fretboard(mode('C', 'dorian'))

def converter(row, mode_notes):
    """
    Takes each row of a dataframe representing a string of the guitar
    and converts notes to intervals of the mode.

    :param row:
    :param mode_notes:
    :return:
    """
    replace_interval = lambda x, y: y.index(x) + 1 if x in y else x
    row = row.apply(lambda x: replace_interval(x, mode_notes))
    return row

def notes_to_intervals(key, mode_name):
    """
    Given a key and a mode name, this function returns a dataframe
    representing all the notes on a fretboard.

    :param key:
    :param mode_name:
    :return:
    """
    mode_notes = mode(key, mode_name)
    mode_neck = notes_on_fretboard(mode_notes)
    # apply transformation of notes to intervals on each row/col (string or fret)
    return mode_neck.apply(lambda x: converter(x, mode_notes), axis=1)

print(notes_to_intervals('C', 'ionian').to_string())
# print("Ionian mode in key of C\n", notes_to_intervals('C', 'ionian').to_string())
# print("Dorian mode in key of C\n", notes_to_intervals('C', 'dorian').to_string())

# print("Cmaj\n", notes_on_fretboard(major('C', 'maj').notes).to_string())

# Notes:
# can use inversions to determine unique-enough forms
# basic rule can be: note per string, repeat a note only once, and quit once you have all notes
def chord_forms(notes, data, num=1, frets=5):
    # this would hold the list of forms already tried
    forms = {}
    for i in range(num):
        chord_notes = []
        strings = []
        data = data.iloc[::-1]
        for index, row in data.iterrows():
            string_notes = row[0:frets].tolist()
            # print(string_notes)
            for idx, s in enumerate(string_notes):
                # print(index+1, i, s)
                if s not in chord_notes and s in notes:
                    chord_notes.append(s)
                    # store away row and col for the note
                    strings.append((index, idx))
                    break
        # might only need to return a list (string, fret)
        return dict(list(zip(chord_notes, strings)))

# print(chord('C', 'maj').notes)
c_chord = chord_forms(chord('C', 'maj').notes, notes_on_fretboard(major('C', 'maj').notes))

# rough implementation to print tab based on the list of (string, fret) values
tab = ""
for i in reversed(range(NUM_STRINGS)):
    # print(i)
    count = 0
    for k, v in c_chord.items():
        if v[0] == i:
            # print(k, v)
            tab = tab + str(v[1])
            count = count + 1
            break
    if count == 0:
        tab = tab + 'x'
print(tab)

# for k, v in c_chord.items():
#     print(k, v, v[0]+1, v[1])
#     row = v[0]
#     col = v[1]
#     df = guitar_fretboard
#     start = 0 if open else 1
#     frets = 5
#     # looks at specified fret window
#     print(df.iloc[row, col])
# print(df[df.iloc[:, start:frets].isin(notes)].iloc[:, start:frets].fillna('.')

# test
# show all notes of Cmaj on fretboard 
# print("Cmaj\n", notes_on_fretboard(major('C', 'maj').notes).to_string())
# print("Cmaj9\n", notes_on_fretboard(major('C', 'maj9').notes).to_string())

# major scale is good but contains notes isn't sufficient for other scales
# print("C major scale\n", notes_on_fretboard(scale('C', 'major')).to_string())


