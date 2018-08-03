import unittest

import sys
sys.path = ['../src'] + sys.path
import chords
from Chord import Chord
from constants import *

class Test_Scales(unittest.TestCase):

    def setUp(self):
        pass

    def test_mode(self):
        # test a key with all formulas for now
        key = 'C'
        modes = [*MODES]
        expected = [
            ['C', 'D', 'E', 'F', 'G', 'A', 'B'],
            ['D', 'E', 'F', 'G', 'A', 'B', 'C'],
            ['E', 'F', 'G', 'A', 'B', 'C', 'D'],
            ['F', 'G', 'A', 'B', 'C', 'D', 'E'],
            ['G', 'A', 'B', 'C', 'D', 'E', 'F'],
            ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
            ['B', 'C', 'D', 'E', 'F', 'G', 'A']
        ]
        for i, m in enumerate(modes):
            self.assertEqual(expected[i], chords.mode(key, m), msg='{}{} is incorrect'.format(key, m))

#     TODO add tests for major and minor scales


if __name__ == '__main__':
    unittest.main()