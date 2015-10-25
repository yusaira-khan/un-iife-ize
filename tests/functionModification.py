__author__ = 'yusaira-khan'

import unittest
import function

class functionModification(unittest.TestCase):

    def test_sections(self):
        statement = 'function hello(){}\nhello();\nfunction world(){}'
        f = function.Function(statement)

        exp = 'hello=function(){};world=function(){};'
        f.extract_from_contents()
        print(f.all)
        print(f.unmodified)
        b = [x for x,s,e in f.all]
        ret = ''.join(b)
        self.assertEqual(exp,ret)



if __name__ == '__main__':
    unittest.main()
