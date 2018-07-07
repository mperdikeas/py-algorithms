# -*- coding: utf-8 -*-
from __future__ import unicode_literals


import random


class BSTNode:
    '''
    From Wikipedia:
        A binary search tree is a rooted binary tree, whose internal nodes each store
        a key (and optionally, an associated value) and each have two distinguished 
        sub-trees, commonly denoted left and right. The tree additionally satisfies 
        the binary search property, which states that the key in each node must be
        greater than or equal to any key stored in the left sub-tree, and less than
        or equal to any key stored in the right sub-tree. The leaves (final nodes) 
        of the tree contain no key and have no structure to distinguish them from 
        one another.

    For simplicity, in this implementation we treat the value (v) as the key.
    OTOH, to spice things up I decided to support multiple values which, in retrospect,
    has complicated the implementation a lot.

    Main methods:
    * insert (inserts a new value in the tree). Available in three variants:
        - recursive
        - non-recursive
        - recursive that preserves the previous tree version (persistent data structures)
    * find
    * count
    * size
    * delete
    * preorder traversal. Available in four variants:
        - recursive     with visitor pattern
        - non-recursive --------------------
        - recursive     with yield
        - non-recursive ----------
    * to_string: generates nice schematic of tree
    '''

    def __init__(self, parent, v, left=None, right=None):
        self.parent = parent
        self.v = v
        self.left = left
        self.right = right
        self._sanity_check()

    @staticmethod
    def createTreeUsingRecursiveInsert(values):
        root = BSTNode(None, values[0])
        for v in values[1:]:
            root.insert(v)
        assert root.size()==len(values)
        return root


    def _sanity_check(self):
        assert not ( (self.v is None) and (self.left is None or self.right is None) )
        
        
    def is_right_child(self):
        assert self.parent is not None
        return self.parent.right is self        
        
    def insert(self, v):
        if self.v>=v:
            if self.left==None:
                self.left = BSTNode(self, v)
            else:
                self.left.insert(v)
        else:
            if self.right==None:
                self.right = BSTNode(self, v)
            else:
                self.right.insert(v)

    def insert_non_recursive(self, v):
        p = self
        parent = None
        left_child = None
        while p is not None:
            if p.v >= v:
                parent = p
                p = p.left
                left_child = True
            else:
                parent = p
                p = p.right
                left_child = False
        assert parent is not None
        assert left_child is not None
        if left_child:
            parent.left = BSTNode(parent, v)
        else:
            parent.right = BSTNode(parent, v)

    def insert_persistent(self, v):
        '''
        Insert a value without modifying the original tree: returns a new tree and leaves
        the old one unmodified. This is to support persistent data structures.
        '''
        def _insert_persistent(node, parent, v):
            if (node is None):
                return BSTNode(parent, v)
            else:
                if (node.v>=v):
                    return BSTNode(parent
                                , node.v
                                , _insert_persistent(node.left, node, v)
                                , node.right)
                else:
                    return BSTNode(parent
                                , node.v
                                , node.left
                                , _insert_persistent(node.right, node, v))
        return _insert_persistent(self, self.parent, v)

    def find(self, v):
        def _find(node, v):
            if node is None:
                return False
            else:
                if (node.v == v):
                    return True
                else:
                    if (node.v > v):
                        return _find(node.left, v)
                    else:
                        return _find(node.right, v)
        return _find(self, v)

    def count(self, v):
        def _count(node, v):
            if node is None:
                return 0
            else:
                if node.v == v:
                    return 1 + _count(node.left, v)
                else:
                    if node.v > v:
                        return _count(node.left, v)
                    else:
                        return _count(node.right, v)
        return _count(self, v)

    def max(self):
        if self.right is None:
            return self.v
        else:
            return self.right.max()

    def min(self):
        if self.left is None:
            return self.v
        else:
            return self.left.min()

    def size(self):
        return 1 +(0 if self.left is None else self.left.size()) +(0 if self.right is None else self.right.size())


    def preorder_traversal(self, f): # TODO: write test cases
        '''
        Root, Left, Right
        '''
        if (self is not None):
            f(self)
            preorder_traversal(self.left)
            preorder_traversal(self.right)

    def preorder_traversal_nonrecur(self, f): # TODO: write test cases
        stack = []

        stack.append(self)
        while (stack):
            node = stack.pop()
            f(node)
            if node.right:
                stack.push(node.right)
            if node.left:
                stack.push(node.left)

    def preorder_traversal_yield(self):
        '''
        Root, Left, Right
        '''
        yield self
        if self.left:
            for x in self.left.preorder_traversal_yield():
                yield x
        if self.right:
            for x in self.right.preorder_traversal_yield():
                yield x           


    def preorder_traversal_nonrecur_yield(self):
        stack = []

        stack.append(self)
        while (stack):
            node = stack.pop()
            yield node
            if node.right:
                stack.append(node.right)
            if node.left:
                stack.append(node.left)
                
    
    def delete(self, v, delete_all):
        assert delete_all is True or delete_all is False
        def _delete(node, v):
            if node is None:
                return 0
            else:
                if node.v == v:
                    if node.left is not None:
                        maxInLeft = node.left.max()
                        node.v = maxInLeft
                        assert _delete(node.left, maxInLeft) is 1
                    elif node.right is not None:
                        minInRight = node.right.min()
                        node.v = minInRight
                        assert _delete(node.right, minInRight) is 1
                        # we're not done yet, there may be more values equal to minInRight in the right subTree
                        # and now that we've placed this value in the root, we have to suck them all into the
                        # left subtree. This is because equality is only allowed for left subtree values, not
                        # right subtree values: all values in the right subtree must be strictly greater than
                        # the value of the root
                        while (_delete(node.right, minInRight) is 1):
                            node.insert(minInRight)
                    else:
                        if node.parent is None:
                            raise Exception('cannot delete the root if it contains the sole key in the tree; set the root pointer to None instead')
                        else:
                            if node.is_right_child():
                                node.parent.right = None
                            else:
                                node.parent.left = None
                    return 1
                elif node.v > v:
                    return _delete(node.left, v)
                else:
                    return _delete(node.right, v)
        if delete_all:
            howManyWereDeleted = 0
            while (_delete(self, v) is 1):
                howManyWereDeleted += 1
            return howManyWereDeleted
        else:
            return _delete(self, v)
    

    def visit_RL(self, visitor, depth=0):
        visitor.visit(self.parent, depth, None if self.parent is None else self.is_right_child(), self)
        if self.right != None:
            self.right.visit_RL(visitor, depth+1)
        if self.left != None:
            self.left.visit_RL(visitor, depth+1)

    def to_string(self):
        '''
        Produces a stringification of the BST
        >>> n = BSTNode(None, 2)
        >>> n.insert(1)
        >>> n.insert(3)
        >>> print(n.to_string())
        2
        ├─R──>3
        └─L──>1
        '''
        return '\n'.join(self._to_string(0))

    def _to_string(self, depth):
        T = u'\u251c'
        L = u'\u2514'
        bar = u'\u2500'
        def adornR(x):
            if (x[0]==0):
                return T+bar+'R'+(2*bar)+'>'+x[1]
            else:
                return '|     '+x[1]

        def adornL(x):
            if (x[0]==0):
                return L+bar+'L'+(2*bar)+'>'+x[1]
            else:
                return '      '+x[1]            
            
        rv = []
        rv.append(str(self.v))
        if (not (self.right is None and self.left is None)):
            if (self.right is None):
                x = [T+bar+'R'+(2*bar)+'>nil']
            else:
                right_subtree_strings = self.right._to_string(depth+1)
                x = map(adornR,
                        [x for x in enumerate(right_subtree_strings)]) # purposefully use a different idiom than in sse-1530890265
            rv.extend(x)
            if (self.left is None):
                x = [L+bar+'L'+(2*bar)+'>nil']            
            else:
                left_subtree_strings = self.left._to_string(depth+1)
                x = map(adornL
                        , zip(range(0, len(left_subtree_strings)) # sse-1530890265 (another passable idiom)
                              , left_subtree_strings))
            rv.extend(x)
        return rv

    def depth(self):
        '''
        Reports the depth of the BST
        >>> n = BSTNode(None, 0)
        >>> print(n.depth())
        0
        >>> n.insert(1)
        >>> print(n.depth())
        1
        >>> n.insert(2)
        >>> print(n.depth())
        2
        >>> n.insert(0.75)
        >>> print(n.depth())
        2
        >>> n.insert(-1)
        >>> print(n.depth())
        2
        >>> n.insert(-2)
        >>> print(n.depth())
        2
        >>> n.insert(-3)
        >>> print(n.depth())
        3
        '''        
        return max(0
                   , 1+self.left.depth()  if self.left  is not None else 0
                   , 1+self.right.depth() if self.right is not None else 0)

    def pathTo(self, x):
        pass # todo


# +-------------------------------------------+
# |                                           |
# |         U N I T    T E S T S              |
# |                                           |
# +-------------------------------------------+

import unittest
class UnitTestCases(unittest.TestCase):

    def test_tree_creation(self):
        values = [2, 14, 18, 15, 13, 9, 9, 17, 11, 1, 16, 17, 15, 16, 16, 2, 17, 5, 4, 14, 16, 2, 13, 12, 18, 0, 16, 9, 20, 18]
        expected_stringification = '''
2
├─R──>14
|     ├─R──>18
|     |     ├─R──>20
|     |     └─L──>15
|     |           ├─R──>17
|     |           |     ├─R──>18
|     |           |     |     ├─R──>nil
|     |           |     |     └─L──>18
|     |           |     └─L──>16
|     |           |           ├─R──>17
|     |           |           |     ├─R──>nil
|     |           |           |     └─L──>17
|     |           |           └─L──>16
|     |           |                 ├─R──>nil
|     |           |                 └─L──>16
|     |           |                       ├─R──>nil
|     |           |                       └─L──>16
|     |           |                             ├─R──>nil
|     |           |                             └─L──>16
|     |           └─L──>15
|     └─L──>13
|           ├─R──>14
|           └─L──>9
|                 ├─R──>11
|                 |     ├─R──>13
|                 |     |     ├─R──>nil
|                 |     |     └─L──>12
|                 |     └─L──>nil
|                 └─L──>9
|                       ├─R──>nil
|                       └─L──>5
|                             ├─R──>9
|                             └─L──>4
└─L──>1
      ├─R──>2
      |     ├─R──>nil
      |     └─L──>2
      └─L──>0
'''.strip()
        root = BSTNode(None, values[0])
        for i in range(1, len(values)):
            root.insert(values[i])
        actual_stringification = root.to_string()
        self.assertEqual(actual_stringification, expected_stringification)
            
    def test_that_the_three_versions_of_insert_all_yield_identical_trees(self):
        random.seed(0)
        N_TESTS = 10
        MAX_N_NODES = 50
        random_value = lambda : random.randint(0, MAX_N_NODES/2) # divide by 2 to ensure lots of clashes
        for _ in range(1, N_TESTS):
            for num_of_nodes in range(1, MAX_N_NODES+1):
                # incrementally create a tree with i nodes by means of successive inserts
                # using all three available methods and verify that identical trees are
                # produced every step of the way
                rootValue = random_value()
                tree1 = BSTNode(None, rootValue)
                tree2 = BSTNode(None, rootValue)
                tree3 = BSTNode(None, rootValue)
                for j in range(0, num_of_nodes):
                    s1 = tree1.to_string()
                    s2 = tree2.to_string()
                    s3 = tree3.to_string()                    
                    self.assertEquals(s1, s2)
                    self.assertEquals(s1, s3)
                    if False:
                        print 'just tested this tree with {} nodes:\n{}'.format(j+1, s1)
                    v = random_value()
                    tree1.insert(v)
                    tree2.insert_non_recursive(v)
                    tree3 = tree3.insert_persistent(v)


    def test_that_the_persistent_insert_method_preserves_previous_tree(self):
        random.seed(0)
        N_TESTS = 10
        MAX_N_NODES = 50
        random_value = lambda : random.randint(0, MAX_N_NODES/2) # divide by 2 to ensure lots of clashes
        for _ in range(1, N_TESTS):
            for num_of_nodes in range(1, MAX_N_NODES+1):
                # incrementally create a tree with i nodes by means of successive inserts
                # using all three available methods and verify that identical trees are
                # produced every step of the way
                tree = BSTNode(None, random_value())
                for j in range(0, num_of_nodes):
                    treeOld = tree
                    treeOldStr = treeOld.to_string()
                    tree = tree.insert_persistent(random_value())
                    treeOldStr2 = treeOld.to_string()
                    self.assertEquals(treeOldStr, treeOldStr2)
                    if False:
                        print 'old tree was preserved:\n{}'.format(treeOldStr)

    def test_find(self):
        random.seed(0)
        N_TESTS = 10
        MAX_N_NODES = 50
        random_value = lambda : random.randint(0, MAX_N_NODES*2) # mul by 2 to ensure sufficient gaps (for failed finds)
        for _ in range(1, N_TESTS):
            for num_of_nodes in range(1, MAX_N_NODES+1):
                random_values = [random_value() for _ in range(0, num_of_nodes)]
                tree = BSTNode.createTreeUsingRecursiveInsert(random_values)
                for f in range(0, MAX_N_NODES/2+1):
                    if f in random_values:
                        self.assertTrue(tree.find(f))
                        if False:
                            print '{} found in below tree:\n{} as expected'.format(f, tree.to_string())
                    else:
                        self.assertFalse(tree.find(f))
                        if False:
                            print '{} not found in below tree:\n{} as expected'.format(f, tree.to_string())                        

    def test_count(self):
        random.seed(0)
        N_TESTS = 3
        MAX_N_NODES = 100
        random_value = lambda : random.randint(0, MAX_N_NODES/5) # div by 2 to ensure multiples
        for _ in range(1, N_TESTS):
            for num_of_nodes in range(1, MAX_N_NODES+1):
                random_values = [random_value() for _ in range(0, num_of_nodes)]
                tree = BSTNode.createTreeUsingRecursiveInsert(random_values)
                for f in range(0, MAX_N_NODES/2+1):
                    self.assertEquals(random_values.count(f), tree.count(f))
                    if False:
                        print '{} found {} times in below tree:\n{} as expected'.format(f
                                                                                        , random_values.count(f)

                                                                                        , tree.to_string())

    def test_delete_and_size(self):
        random.seed(0)
        N_TESTS = 3
        MAX_N_NODES = 100
        random_value = lambda : random.randint(0, MAX_N_NODES/5) # div by 2 to ensure multiples
        for _ in range(1, N_TESTS):
            for num_of_nodes in range(1, MAX_N_NODES+1):
                random_values = [random_value() for _ in range(0, num_of_nodes)]
                tree = BSTNode.createTreeUsingRecursiveInsert(random_values)
                deletionsSoFar = 0
                indexOfOnlyValueToNotDelete = random.randint(0, len(random_values)-1)
                for i in range(0, len(random_values)):
                    if (i==indexOfOnlyValueToNotDelete):
                        continue
                    else:
                        self.assertIs(tree.delete(random_values[i], False), 1)
                        deletionsSoFar += 1
                        self.assertEquals(tree.size(), num_of_nodes-deletionsSoFar)
                self.assertEquals(tree.v, random_values[indexOfOnlyValueToNotDelete])
                self.assertIs(tree.left  , None)
                self.assertIs(tree.right , None)
                self.assertIs(tree.parent, None)
                self.assertIs(tree.size(), 1)

    def test_delete_all_and_size(self):
        random.seed(0)
        N_TESTS = 3
        MAX_N_NODES = 100
        random_value = lambda : random.randint(0, MAX_N_NODES/5) # div by 3 to ensure many multiples
        for _ in range(1, N_TESTS):
            for num_of_nodes in range(1, MAX_N_NODES+1):
                random_values = [random_value() for _ in range(0, num_of_nodes)]
                tree = BSTNode.createTreeUsingRecursiveInsert(random_values)
                deletionsSoFar = 0
                valueToNotDelete = random.choice(random_values)
                for v in set(random_values):
                    if (v == valueToNotDelete):
                        continue
                    else:
                        elementsDeleted = tree.delete(v, True)
                        self.assertEquals(elementsDeleted
                                          , random_values.count(v))
                        deletionsSoFar += elementsDeleted
                        self.assertEquals(tree.size(), num_of_nodes-deletionsSoFar)
                self.assertEquals(tree.v, valueToNotDelete)
                self.assertIs(tree.right , None) # only one value is left so it will be placed in the root, or
                                                 # (if duplicate) in the left subtree, at any rate the right
                                                 # subtree will *have* to be empty
                self.assertIs(tree.parent, None)
                self.assertEquals(tree.size(), random_values.count(valueToNotDelete))

    def test_preorder_traversal_recursive_and_nonrecursive_with_yield_a(self):
        random.seed(0)
        tree = BSTNode.createTreeUsingRecursiveInsert([random.randint(0, 10) for _ in range(0, 10)])
        self.assertEqual(tree.to_string(),
'''
9
├─R──>nil
└─L──>8
      ├─R──>nil
      └─L──>4
            ├─R──>5
            |     ├─R──>8
            |     |     ├─R──>nil
            |     |     └─L──>6
            |     └─L──>5
            └─L──>2
                  ├─R──>4
                  |     ├─R──>nil
                  |     └─L──>3
                  └─L──>nil

'''.strip())
                         
        nodes_visited1 = [x.v for x in tree.preorder_traversal_yield()]
        nodes_visited2 = [x.v for x in tree.preorder_traversal_nonrecur_yield()]
        self.assertSequenceEqual(nodes_visited1, nodes_visited2)
        self.assertSequenceEqual(nodes_visited1, [9, 8, 4, 2, 4, 3, 5, 5, 8, 6])


    def test_preorder_traversal_recursive_and_nonrecursive_with_yield_b(self):
        random.seed(1)
        tree = BSTNode.createTreeUsingRecursiveInsert([random.randint(0, 20) for _ in range(0, 20)])
        self.assertEqual(tree.to_string(),
'''
2
├─R──>17
|     ├─R──>19
|     |     ├─R──>nil
|     |     └─L──>18
|     └─L──>16
|           ├─R──>17
|           └─L──>5
|                 ├─R──>10
|                 |     ├─R──>13
|                 |     |     ├─R──>16
|                 |     |     |     ├─R──>nil
|                 |     |     |     └─L──>16
|                 |     |     |           ├─R──>nil
|                 |     |     |           └─L──>15
|                 |     |     └─L──>nil
|                 |     └─L──>9
|                 |           ├─R──>nil
|                 |           └─L──>9
|                 |                 ├─R──>nil
|                 |                 └─L──>9
|                 └─L──>4
└─L──>1
      ├─R──>nil
      └─L──>0
            ├─R──>nil
            └─L──>0
                  ├─R──>nil
                  └─L──>0

'''.strip())
                         
        nodes_visited1 = [x.v for x in tree.preorder_traversal_yield()]
        nodes_visited2 = [x.v for x in tree.preorder_traversal_nonrecur_yield()]
        self.assertSequenceEqual(nodes_visited1, nodes_visited2)
        self.assertSequenceEqual(nodes_visited1, [2, 1, 0, 0, 0, 17, 16, 5, 4, 10, 9, 9, 9, 13, 16, 16, 15, 17, 19, 18])

        


if __name__ == '__main__' :
    import doctest
    doctest.testmod()
    print 'Running unit tests. Please be patient...'
    unittest.main()
