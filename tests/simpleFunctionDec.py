__author__ = 'yusaira-khan'

import unittest
import main
def boilerplate():
    pass

class FunctionSimple(unittest.TestCase):

    def test_single(self):
        statement = 'function hello(){}'
        exp = 'hello = function(){}'
        self.assertEqual(main.correct_var(statement,0,len(statement)-1),exp)
if __name__ == '__main__':

    unittest.main()
