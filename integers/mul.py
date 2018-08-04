import numbers

def assert_digit(x):
     if not (isinstance(x, numbers.Number) and ((x % 1) == 0) and (0<=x<=9)):
         raise ArithmeticError('{} is not a digit'.format(x))
     return x


def eff(a, i):
    if (i >= len(a)):
        return 0
    else:
        return a[i]

def add(_lista, _listb):
    lista = [x for x in reversed(_lista)]
    listb = [x for x in reversed(_listb)]
    rv = []
    carry = 0
    for i in range(0, max(len(lista), len(listb))):
        v = carry + assert_digit(eff(lista, i))+assert_digit(eff(listb, i))
        digit = v % 10
        carry = v / 10
        assert (carry == 0) or (carry == 1)
        rv.append(digit)
    if carry > 0:
        rv.append(carry)
    return [x for x in reversed(rv)]
            
    

# TODO: mul is totally untested
def mul(lista, listb):
    summands = []
    for i in range(0, len(lista)):
        carry = 0
        summand = []
        for j in range(0, len(listb)):
            for k in range(0, j):
                summand.append(0)
            v = lista[i]*listb[j]+carry
            if (v>=10):
                if (j<len(listb)-1):
                    summand.append( v % 10 )
                    carry = v / 10
                else:
                    summand.append( v % 10 )
                    summand.append( v / 10 )
        summands.append([x for x in reversed(summand)])
    
                
# +-------------------------------------------+
# |                                           |
# |         U N I T    T E S T S              |
# |                                           |
# +-------------------------------------------+

import unittest
import random
        
class AdditionAlgorithmUnitTests(unittest.TestCase):

    def test_00(self):
        self.assertSequenceEqual(add([0], [0]), [0])

    def test_01(self):
        self.assertSequenceEqual(add([4, 2], [3, 1]), [7, 3])

    def test_02(self):
        self.assertSequenceEqual(add([4, 3], [3, 9]), [8, 2])

    def test_03(self):
        self.assertSequenceEqual(add([4, 3], [5, 3, 9]), [5, 8, 2])

    def test_04(self):
        self.assertSequenceEqual(add([8, 3], [5, 8, 9]), [6, 7, 2])

    def test_05(self):
        self.assertSequenceEqual(add([9, 3, 8], [7, 6, 2]), [1, 7, 0, 0])

    def test_06(self):
        random.seed(0)
        for _ in range(0, 1000000):
            num_of_digits_a = random.randint(0, 20)
            num_of_digits_b = random.randint(0, 20)
            a = random.randint(0, 10**num_of_digits_a - 1)
            b = random.randint(0, 10**num_of_digits_b - 1)
            result = a+b
            lista = [int(d) for d in str(a)]
            listb = [int(d) for d in str(b)]
            expected = [int(d) for d in str(result)]
            print 'adding {} to {} and expecting: {}'.format(lista, listb, expected)
            self.assertSequenceEqual(add(lista, listb), expected)
            
        

if __name__ == '__main__' :
    import doctest
    doctest.testmod()
    print 'Running unit tests.'
    unittest.main()



        
