import random


import unittest
class AbstractSortingAlgoUnitTestCases(unittest.TestCase):

    def test_00(self):
        self.assertSequenceEqual(self.sort_algo()([]), [])

    def test_01(self):
        self.assertSequenceEqual(self.sort_algo()([42]), [42])

    def test_02(self):
        self.assertSequenceEqual(self.sort_algo()([1, 2]), [1, 2])

    def test_03(self):
        self.assertSequenceEqual(self.sort_algo()([2, 1]), [1, 2])

    def test_04(self):
        self.assertSequenceEqual(self.sort_algo()([1, 1, 1]), [1, 1, 1])
        
    def test_05(self):
        xs_unsorted = [3, 1, 6, 4, 5, 2]
        xs_expected = xs_unsorted[:]
        xs_expected.sort()
        self.assertSequenceEqual(self.sort_algo()(xs_unsorted), xs_expected)

    def test_05b(self):
        xs_unsorted = [2, 1, 4, 3]
        xs_expected = xs_unsorted[:]
        xs_expected.sort()
        self.assertSequenceEqual(self.sort_algo()(xs_unsorted), xs_expected)
        
    def test_06(self):
        random.seed(0)
        xs_unsorted = []
        for i in range(0, 5000):
            xs_unsorted.append(random.randint(0, 100))
        xs_expected = xs_unsorted[:]
        xs_expected.sort()
        self.assertSequenceEqual(self.sort_algo()(xs_unsorted), xs_expected)

    def test_07(self):
        random.seed(0)
        xs_unsorted = []
        for i in range(0, 5000):
            xs_unsorted.append(i) # this is actually sorted - to try BubbleSort's immediate exit
        xs_expected = xs_unsorted[:]
        xs_expected.sort()
        self.assertSequenceEqual(self.sort_algo()(xs_unsorted), xs_expected)

    def test_08(self):
        random.seed(0)
        for _ in range(0, 100):
            arr = []
            for i in range(0, random.randint(50, 51)):
                arr.append(random.randint(0, 21))
            xs_expected = arr[:]
            xs_expected.sort()
            self.assertSequenceEqual(self.sort_algo()(arr), xs_expected)
                
                
