import unittest
from CompareSacSS import CompareSacSS
from pathlib import Path


class TestSacSS (unittest.TestCase):

    def test_readSac(self):
        filename = Path('SacAttend.csv')
        self.AssertTrue(filename.exists())

    def test_readSS(self):
        filename = Path('SSAttend.csv')
        self.AssertTrue(filename.exists())

    def test_subtractCallings(self):
        filename = Path('Callings.csv')
        self.AssertTrue(filename.exists())

    def test_findMissingFromSS(self):
       self.AssertTrue(True)  # change this.



if __name__ == '__main__':
    unittest.main()
