import unittest

import sys
sys.path = ['../src'] + sys.path
import chords

class test_chords(unittest.TestCase):

    def setUp(self):
        pass

    def test_major(self):
        # test a key with all formulas for now
        key = 'C'
        major_formualas = chords.MAJOR_FORMULA
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
        for i, m in enumerate(major_formualas):
            self.assertEqual(expected[i], chords.major(key, m).get_notes())

if __name__ == '__main__':
    unittest.main()