# CHORD object encapsulating the name, notes, and the chromatic notes around
# when embellishing (for e.g. min/dim/7/aug etc)
class Chord:

    TRIAD = 3
    FOUR_NOTE = 4
    SEVENTH = 7
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

    def __init__(self, name, notes=[], chromatics=[]):
        self.name = name
        self.notes = notes
        self.chromatics = chromatics

    def flatThird(self):
        flat = self.chromatics.index(self.notes[1]) - 1
        if flat < 0:
            flat = self.chromatics[-1]
        note = self.chromatics[flat]
        if note in self.equivalents:
            self.notes[1] = self.equivalents[note]
        else:
            self.notes[1] = note
        return self
    
    def flatFifth(self):
        flat = self.chromatics.index(self.notes[2]) - 1
        if flat < 0:
            flat = self.chromatics[-1]
        note = self.chromatics[flat]
        if note in self.equivalents:
            self.notes[2] = self.equivalents[note]
        else:
            self.notes[2] = note
        return self
    
    def flatSeventh(self):
        if len(self.notes) < self.FOUR_NOTE:
            return self
        flat = self.chromatics.index(self.notes[3]) - 1
        if flat < 0:
            flat = self.chromatics[-1]
        note = self.chromatics[flat]
        if note in  self.equivalents:
            self.notes[3] =  self.equivalents[note]
        else:
            self.notes[3] = note
        return self

    def sharpFifth(self):
        sharp = self.chromatics.index(self.notes[2]) + 1
        if sharp >= len(self.chromatics):
            sharp = self.chromatics[(sharp) % len(self.chromatics)]
        note = self.chromatics[sharp]
        self.notes[2] = note
        return self
    
    def print(self):
        print(self.name, ': ', self.notes)