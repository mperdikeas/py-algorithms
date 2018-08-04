def merge_sort(xs):
    if len(xs)<=1:
        return xs
    else:
        fst_half = merge_sort(xs[        0: len(xs)/2])
        snd_half = merge_sort(xs[len(xs)/2: len(xs)  ])
        rv = []
        a = 0
        b = 0
        for i in range(0, len(xs)):
            v = None
            if fst_half[a] <= snd_half[b]:
                v = fst_half[a]
                a+=1
            else:
                v = snd_half[b]
                b+=1
            rv.append(v)
            if (a == len(fst_half)) or (b == len(snd_half)):
                src  = snd_half if (a == len(fst_half)) else fst_half
                idx  = b if (a == len(fst_half)) else a
                for k in range(idx, len(src)):
                    rv.append(src[k])
                break
        return rv



                



# +-------------------------------------------+
# |                                           |
# |         U N I T    T E S T S              |
# |                                           |
# +-------------------------------------------+

import unittest
import sorting_unittests

class UnitTests(sorting_unittests.AbstractSortingAlgoUnitTestCases):
    def sort_algo(self):
        return merge_sort
        
        


if __name__ == '__main__' :
    import doctest
    doctest.testmod()
    print 'Running unit tests.'
    unittest.main()
