__author__ = 'yusaira-khan'

import unittest
import un_iife_ize.un_iife_ize as un_iife_ize


class CheckVar(unittest.TestCase):
    def test_simple(self):
        statement = [('var hello,world=5;', 0)]
        exp = [('hello=undefined,world=5;', 0)]
        v = un_iife_ize.Var(statement)
        v.extract_all()
        ret = v.all
        self.assertEqual(ret, exp)

    def test_multiple(self):
        statement = [('var hello,world=5;\nvar bye,nope;', 0)]
        exp = [('hello=undefined,world=5;', 0), ('bye=undefined,nope=undefined;', 19)]
        v = un_iife_ize.Var(statement)
        v.extract_all()

        ret = v.all

        self.assertEqual(ret, exp)

    def test_sections(self):
        statement = [('var hello,world=5;\nvar bye,nope;', 0),
                     ('var hello,world=5;\nvar bye,nope;', 30)]
        exp = [('hello=undefined,world=5;', 0),
               ('bye=undefined,nope=undefined;', 19),
               ('hello=undefined,world=5;', 30),
               ('bye=undefined,nope=undefined;', 49) ]
        v = un_iife_ize.Var(statement)
        v.extract_all()
        ret = v.all
        self.assertEqual(ret, exp)

    def test_deliberate_iife(self):
        statement = [('var hello=function(){;}', 0)]
        exp = [('hello=function(){;}', 0)]
        v = un_iife_ize.Var(statement)
        v.extract_all()

        ret = v.all
        print(ret)
        self.assertEqual(ret, exp)

    def test_deliberate_iife_barc(self):
        statement = [('var  hello =  (function(){;}())', 0)]
        exp = [(' hello =  (function(){;}())', 0)]
        v = un_iife_ize.Var(statement)
        v.extract_all()

        ret = v.all
        print(ret,len(exp[0][0]),len(ret[0][0]))
        self.assertEqual(ret, exp)

    def test_double_assignment(self):
        statement = [('var hello=wow=;', 0)]
        exp = [('hello=wow=', 0)]
        v = un_iife_ize.Var(statement)
        v.extract_all()

        ret = v.all
        print(ret)
        self.assertEqual(ret, exp)





    def test_sections_unmodified(self):
        statement = [('var hello,world=5;\nfunction(){}\nvar bye,nope;', 0),
                     ('var hello,world=5;\nvar bye,nope;', 30)]
        exp = [('\nfunction(){}\n', 18),('', len(statement[0][0])+statement[0][1]) ,
               ('\n', 48),('', len(statement[1][0])+statement[1][1]) ]
        v = un_iife_ize.Var(statement)
        v.extract_all()
        ret = v.unmodified
        print("ret",ret)
        print("expt",exp)
        self.assertEqual(ret, exp)


if __name__ == '__main__':
    unittest.main()
