def insert_sort(xs):
    sorted_prefix = []
    N = len(xs)
    for i in range(0, N):
        elem_to_insert = xs[i]
        insertion_occured = False
        for j in range(0, len(sorted_prefix)):
            if sorted_prefix[j]>elem_to_insert:
                head = sorted_prefix[:j]
                tail = sorted_prefix[j:]
                head.append(elem_to_insert)
                head.extend(tail)
                sorted_prefix = head
                insertion_occured = True
                break
        if not insertion_occured:
            sorted_prefix.append(elem_to_insert)
    return sorted_prefix
                



# +-------------------------------------------+
# |                                           |
# |         U N I T    T E S T S              |
# |                                           |
# +-------------------------------------------+

import unittest
import sorting_unittests

class UnitTests(sorting_unittests.AbstractSortingAlgoUnitTestCases):
    def sort_algo(self):
        return insert_sort
        


if __name__ == '__main__' :
    import doctest
    doctest.testmod()
    print 'Running unit tests.'
    unittest.main()
