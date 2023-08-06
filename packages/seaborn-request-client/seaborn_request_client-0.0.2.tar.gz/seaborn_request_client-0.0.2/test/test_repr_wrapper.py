from seaborn.request_client.repr_wrapper import *
import unittest

TEST_LIST_LIST = [['a', 'b', 'c', 'd', 'e', 'f', 'g'],
                  ['a', 1, 0.0, 1.0, 2.12, 3.123, 4.1234]]

TEST_LIST = TEST_LIST_LIST[0]

TEST_TUPLE = tuple(TEST_LIST)

TEST_STR = "[(0, {'a': 'A', 'c': 'C', 'b': 'B'}), " \
           "\n (1, {'a': 'A', 'c': 'C', 'b': 'B'}), " \
           "\n (2, {'a': 'A', 'c': 'C', 'b': 'B'})]"

TEST_LIST_TUPLE_DICT = [(0, {'a': 'A', 'c': 'C', 'b': 'B'}),
                        (1, {'a': 'A', 'c': 'C', 'b': 'B'}),
                        (2, {'a': 'A', 'c': 'C', 'b': 'B'})]

TEST_DICT = {TEST_LIST_LIST[0][i]: TEST_LIST_LIST[1][i] for i in range(len(TEST_LIST_LIST[0]))}

TEST_LIST_DICT = [TEST_DICT for i in range(3)]

TEST_TUPLE = tuple(TEST_LIST)

TEST_STRING = "Hello World"

TEST_UNICODE = u"Hello World"

EXPECTED_SET_PPRINT_FORMAT = """
[   (   0,
        {   'a': 'A',
            'b': 'B',
            'c': 'C'}),
    (   1,
        {   'a': 'A',
            'b': 'B',
            'c': 'C'}),
    (   2,
        {   'a': 'A',
            'b': 'B',
            'c': 'C'})]""".strip()

PPRINT_DEFAULT = {'indent': PPRINT_INDENT,
                 'width': PPRINT_WIDTH,
                 'depth': PPRINT_DEPTH}

class test_repr_wrapper(unittest.TestCase):

    def test_str_name_value(self):
        self.assertEqual(str_name_value('hello','world'),
                         '    hello                    world')

    def test_set_pprint_format(self):
        set_pprint_format(4,20,10)
        actual = ReprList(TEST_LIST_TUPLE_DICT)
        self.assertEqual(EXPECTED_SET_PPRINT_FORMAT,
                         repr(actual))
        set_pprint_format(**PPRINT_DEFAULT)

    def test_repr_return(self):
        self.assertEqual(repr_return(dict)(a=1,b=2,c=3),{ 'a': 1, 'b': 2, 'c': 3})

    def test_list_list(self):
        actual = ReprListList(TEST_LIST_LIST, digits = 3)
        self.assertEqual("[[ 'a', 'b',     'c',     'd',     'e',     'f',     'g' ],\n"
                         " [ 'a',   1, '0.000', '1.000', '2.120', '3.123', '4.123' ]]",
                         repr(actual))

    def test_list(self):
        actual= ReprList(TEST_LIST)
        self.assertEqual(repr(TEST_LIST),repr(actual))

    def test_dict(self):
        actual = repr(ReprDict(TEST_DICT))
        self.assertEqual("{ 'a': 'a', 'b': 1, 'c': 0.0,"
                         " 'd': 1.0, 'e': 2.12, 'f': 3.123,"
                         " 'g': 4.1234}",
                         actual)

    def test_list_dict(self):
        actual = ReprListDict(TEST_LIST_DICT)
        self.assertEqual("[ { 'a': 'a', 'b': 1, 'c': 0.0, 'd': 1.0, 'e': 2.12, 'f': 3.123, 'g': 4.1234},"
                         "  { 'a': 'a', 'b': 1, 'c': 0.0, 'd': 1.0, 'e': 2.12, 'f': 3.123, 'g': 4.1234},"
                         "  { 'a': 'a', 'b': 1, 'c': 0.0, 'd': 1.0, 'e': 2.12, 'f': 3.123, 'g': 4.1234}]",
                         actual)

    def test_tuple(self):
        actual = ReprTuple(TEST_TUPLE)
        self.assertEqual("(   'a', 'b', 'c', 'd', 'e', 'f', 'g')",
                         repr(actual))

    def test_str(self):
        self.assertEqual(TEST_STR, ReprStr(TEST_STR))

    def test_unicode(self):
        self.assertEqual(TEST_UNICODE, ReprUnicode(TEST_UNICODE))

if __name__ == '__main__':
    unittest.main()

    # def smoke_test():
    #    print(str(ReprListList([['a', 'b', 'c', 'd', 'e', 'f', 'g'],
    #                            ['a', 1, 0.0, 1.0, 2.12, 3.123, 4.1234]],
    #                           digits=3)))
    #
    #    test_str = "[(0, {'a': 'A', 'c': 'C', 'b': 'B'}), \n (1, {'a': 'A', 'c': 'C', 'b': 'B'}), \n (2, {'a': 'A', 'c': 'C', 'b': 'B'})]"
    #    ans_str = rep(test_str)
    #    print(repr(ans_str) + '\n')
    #
    #    test_dict = {'key': [(0, {'a': 'A', 'c': 'C', 'b': 'B'}),
    #                         (1, {'a': 'A', 'c': 'C', 'b': 'B'}),
    #                         (2, {'a': 'A', 'c': 'C', 'b': 'B'})]}
    #    ans_dict = rep(test_dict)
    #    print(repr(ans_dict) + '\n')
    #
    #    test_list = [(0, {'a': 'A', 'c': 'C', 'b': 'B'}),
    #                 (1, {'a': 'A', 'c': 'C', 'b': 'B'}),
    #                 (2, {'a': 'A', 'c': 'C', 'b': 'B'})]
    #    ans_list = rep(test_list)
    #    print(repr(ans_list) + '\n')
    #
    #    test_unicode = u"[(0, {'a': 'A', 'c': 'C', 'b': 'B'}), \n (1, {'a': 'A', 'c': 'C', 'b': 'B'}), \n (2, {'a': 'A', 'c': 'C', 'b': 'B'})]"
    #    ans_unicode = rep(test_unicode)
    #    print(repr(ans_unicode) + '\n')
    #
    #    test_tuple = (
    #        (0, {'a': 'A', 'c': 'C', 'b': 'B'}),
    #        (1, {'a': 'A', 'c': 'C', 'b': 'B'}),
    #        (2, {'a': 'A', 'c': 'C', 'b': 'B'}))
    #    ans_tuple = rep(test_tuple)
    #    print(repr(ans_tuple) + '\n')
    #
    #    test_list_list = [range(i, i + 10) for i in range(10)]
    #    ans_list_list = rep(test_list_list, _type='list_list')
    #    print(repr(ans_list_list) + '\n')
    #
    #    col_names = [l for l in 'abcdefghi'] + ['hello']
    #    ans_list_list.repr_setup(col_names=col_names)
    #    print(repr(ans_list_list))
    #
    #
    # if __name__ == '__main__':
    #    smoke_test()
