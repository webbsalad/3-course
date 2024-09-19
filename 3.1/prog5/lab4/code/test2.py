import unittest
from main2 import FibonacciLst

class TestFibonacciLst(unittest.TestCase):


    def test_initialsend1(self):
        self.gen = FibonacciLst([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        result = [x for x in self.gen]
        self.assertEqual(result, [0, 1, 2, 3, 5, 8])

    def test_initialsend2(self):
        self.gen = FibonacciLst([15, 23, 8, 47, 34, 76, 2, 55, 19, 66])
        result = [x for x in self.gen]
        self.assertEqual(result, [8, 34, 2, 55])

    def test_initialsend2(self):
        self.gen = FibonacciLst([84, 56, 19, 23, 47, 3, 67, 15, 91, 74, 
                                22, 8, 34, 58, 92, 41, 77, 2, 12, 65, 
                                39, 4, 48, 33, 6, 73, 16, 27, 60, 30, 
                                80, 10, 26, 66, 90, 13, 44, 82, 17, 69, 
                                24, 50, 61, 94, 11, 20, 79, 36, 87, 1])
        result = [x for x in self.gen]
        self.assertEqual(result, [3, 8, 34, 2, 13, 1])

    def test_initialsend2(self):
        self.gen = FibonacciLst([4])
        result = [x for x in self.gen]
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()
