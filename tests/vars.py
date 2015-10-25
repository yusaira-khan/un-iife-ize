__author__ = 'yusaira-khan'

import unittest
import main


class CheckVar(unittest.TestCase):
    def test_simple(self):
        statement = [('var hello,world=5;', 0)]
        exp = [('hello=undefined,world=5;', 0)]
        v = main.Var(statement)
        v.extract_all()
        ret = v.all
        self.assertEqual(ret, exp)

    def test_multiple(self):
        statement = [('var hello,world=5;\nvar bye,nope;', 0)]
        exp = [('hello=undefined,world=5;', 0), ('bye=undefined,nope=undefined;', 19)]
        v = main.Var(statement)
        v.extract_all()
        print(v.unmodified)
        ret = v.all
        self.assertEqual(ret, exp)

    def test_sections(self):
        statement = [('var hello,world=5;\nvar bye,nope;', 0),
                     ('var hello,world=5;\nvar bye,nope;', 30)]
        exp = [('hello=undefined,world=5;', 0),
               ('bye=undefined,nope=undefined;', 19),
               ('hello=undefined,world=5;', 30),
               ('bye=undefined,nope=undefined;', 49) ]
        v = main.Var(statement)
        v.extract_all()
        ret = v.all
        self.assertEqual(ret, exp)

    def test_sections_unmodified(self):
        statement = [('var hello,world=5;\nfunction(){}\nvar bye,nope;', 0),
                     ('var hello,world=5;\nvar bye,nope;', 30)]
        exp = [('\nfunction(){}\n', 18),
               ('\n', 48), ]
        v = main.Var(statement)
        v.extract_all()
        ret = v.unmodified
        self.assertEqual(ret, exp)


if __name__ == '__main__':
    unittest.main()
