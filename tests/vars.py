__author__ = 'yusaira-khan'

import unittest
import main

def boilerplate():
    pass

class CheckVar(unittest.TestCase):

    def test_single(self):
        statement = 'var hello;'
        exp = 'hello=undefined;'
        self.assertEqual(main.correct_var(statement,0,len(statement)-1),exp)

    def test_multiple(self):
        statement = 'var hello, world;'
        exp = 'hello=undefined,world=undefined;'
        self.assertEqual(main.correct_var(statement,0,len(statement)-1),exp)

    def test_hasDefSingle(self):
        statement = 'var hello="world";'
        exp = 'hello="world";'
        self.assertEqual(main.correct_var(statement,0,len(statement)-1),exp)

    def test_hasDefMixed(self):
        statement = 'var hello="world", world;'
        exp = 'hello="world",world=undefined;'
        self.assertEqual(main.correct_var(statement,0,len(statement)-1),exp)

    def test_hasDefMul(self):
        statement = 'var hello="world", world="hello";'
        exp = 'hello="world",world="hello";'
        self.assertEqual(main.correct_var(statement,0,len(statement)-1),exp)

    def test_inside_func(self):
        statement ='''function poop(){var x;}'''
        exp = None
        self.assertEqual(main.detect_var_statement(statement),exp)

if __name__ == '__main__':

    unittest.main()
