def select_sort(xs_unsorted):
    xs = xs_unsorted[:]
    for i in range(0, len(xs)):
        ind_min = i
        for j in range(i+1, len(xs)):
            if xs[j] < xs[ind_min]:
                ind_min = j
        xs[i], xs[ind_min] = xs[ind_min], xs[i]
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
        return select_sort
        
        


if __name__ == '__main__' :
    import doctest
    doctest.testmod()
    print 'Running unit tests.'
    unittest.main()
