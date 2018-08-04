def bubble_sort(xs_unsorted):
    xs = xs_unsorted[:]
    while True:
        flip_happened = False
        for i in range(0, len(xs)-1):
            if xs[i]>xs[i+1]:
                xs[i], xs[i+1] = xs[i+1], xs[i]
                flip_happened = True
        if not flip_happened:
            break
    return xs
                



# +-------------------------------------------+
# |                                           |
# |         U N I T    T E S T S              |
# |                                           |
# +-------------------------------------------+

import unittest
import sorting_unittests

class UnitTests(sorting_unittests.AbstractSortingAlgoUnitTestCases):
    def sort_algo(self):
        return bubble_sort
        


if __name__ == '__main__' :
    import doctest
    doctest.testmod()
    print 'Running unit tests.'
    unittest.main()
