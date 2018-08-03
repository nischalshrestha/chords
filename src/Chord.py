# CHORD object encapsulating the name, notes, and the chromatic notes around
# when embellishing (for e.g. min/dim/7/aug etc)
class Chord:

    TRIAD = 3
    FOUR_NOTE = 4
    SEVENTH = 7

    FIRST_INVERSION = 1
    SECOND_INVERSION = 2
    THIRD_INVERSION = 3

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

    def flat_interval(self, interval):
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

    def flat_third(self):
        return self.flat_interval(3)
    
    def flat_fifth(self):
        return self.flat_interval(5)
    
    def flat_seventh(self):
        return self.flat_interval(7)

    def sharp_fifth(self):
        sharp = self.chromatics.index(self.notes[2]) + 1
        if sharp >= len(self.chromatics):
            sharp = self.chromatics[sharp % len(self.chromatics)]
        note = self.chromatics[sharp]
        self.notes[2] = note
        return self

    def inversion(self, num):
        """
        Return an inversion of a chord as a list of notes.

        :param chord:
        :return:
        """
        if num < self.FIRST_INVERSION or num > self.THIRD_INVERSION:
            return self.notes
        elif num == self.THIRD_INVERSION and len(self.notes) == self.TRIAD:
            return self.notes
        return self.notes[num:] + self.notes[:num]

    
    def print(self):
        print(self.name, ': ', self.notes)
