import unittest

import sys
sys.path = ['../src'] + sys.path
import chords
from constants import *

class test_chords(unittest.TestCase):

    def setUp(self):
        pass

    def test_major(self):
        # test a key with all formulas for now
        key = 'C'
        major_formulas = MAJOR_FORMULA
        expected = [
            ['C', 'E', 'G'],
            ['C', 'E', 'G', 'A'],
            ['C', 'E', 'G', 'B'],
            ['C', 'E', 'G', 'B', 'D'],
            ['C', 'E', 'G', 'D'],
            ['C', 'E', 'G', 'A', 'D'],
            ['C', 'E', 'G', 'A', 'B'],
            ['C', 'E', 'G', 'B', 'D', 'A']
        ]
        for i, m in enumerate(major_formulas):
            self.assertEqual(expected[i], chords.chord(key, m).notes, msg='{}{} is incorrect'.format(key, m))

    def test_minor(self):
        # test a key with all formulas for now
        key = 'C'
        minor_formulas = MINOR_FORMULA
        expected = [
            ['C', 'Eb', 'G'],
            ['C', 'Eb', 'G', 'A'],
            ['C', 'Eb', 'G', 'Bb'],
            ['C', 'Eb', 'G', 'Bb', 'D'],
            ['C', 'Eb', 'G', 'Bb', 'D', 'F'],
            ['C', 'Eb', 'G', 'Bb', 'F'],
            ['C', 'Eb', 'G', 'D'],
            ['C', 'Eb', 'G', 'A', 'D'],
            ['C', 'Eb', 'G', 'B'],
            ['C', 'Eb', 'G', 'B', 'D'],
        ]
        for i, m in enumerate(minor_formulas):
            self.assertEqual(expected[i], chords.chord(key, m).notes, msg='{}{} is incorrect'.format(key, m))
    
    def test_dominant(self):
        # test a key with all formulas for now
        key = 'C'
        minor_formulas = DOMINANT_FORMULA
        expected = [
            ['C', 'E', 'G', 'Bb'],
            ['C', 'E', 'G', 'Bb', 'A'],
            ['C', 'E', 'G', 'Bb', 'F'],
            ['C', 'F', 'G', 'Bb'],
            ['C', 'F', 'G', 'Bb', 'A'], 
            ['C', 'E', 'G', 'Bb', 'D'],
            ['C', 'E', 'G', 'Bb', 'D', 'F'],
            ['C', 'E', 'G', 'Bb', 'D', 'A'],
            ['C', 'E', 'G', 'Bb', 'F', 'A'],
            ['C', 'E', 'G', 'Bb', 'D', 'F', 'A'],
            ['C', 'Eb', 'Gb', 'A'],
            ['C', 'E', 'G#']
        ]
        for i, m in enumerate(minor_formulas):
            self.assertEqual(expected[i], chords.chord(key, m).notes, msg='{}{} is incorrect'.format(key, m))

if __name__ == '__main__':
    unittest.main()