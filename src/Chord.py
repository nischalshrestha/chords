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
    }

    def __init__(self, name, notes=[], chromatics=[]):
        self.name = name
        self.notes = notes
        self.chromatics = chromatics
    
    def flatInterval(self, interval):
        index = 0
        if interval == 3:
            index = 1
        elif interval == 5:
            index = 2
        elif interval == 7 and len(self.notes) >= self.FOUR_NOTE:
            index = 3
        else:
            return self
        flat = self.chromatics.index(self.notes[index]) - 1
        if flat < 0:
            flat = len(self.chromatics) - 1
        note = self.chromatics[flat]
        if note in self.equivalents:
            self.notes[index] = self.equivalents[note]
        else:
            self.notes[index] = note
        return self

    def flatThird(self):
        return self.flatInterval(3)
    
    def flatFifth(self):
        return self.flatInterval(5)
    
    def flatSeventh(self):
        return self.flatInterval(7)

    def sharpFifth(self):
        sharp = self.chromatics.index(self.notes[2]) + 1
        if sharp >= len(self.chromatics):
            sharp = self.chromatics[(sharp) % len(self.chromatics)]
        note = self.chromatics[sharp]
        self.notes[2] = note
        return self
    
    def print(self):
        print(self.name, ': ', self.notes)