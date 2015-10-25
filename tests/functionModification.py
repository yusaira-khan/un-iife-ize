__author__ = 'yusaira-khan'

import unittest
import un_iife_ize

class functionModification(unittest.TestCase):

    def test_sections(self):
        statement = 'function hello(){}\nhello();\nfunction world(){}'
        f = un_iife_ize.Function(statement)

        exp = 'hello=function(){};world=function(){};'
        f.extract_all()
        b = [x for x,s in f.all]
        ret = ''.join(b)
        self.assertEqual(exp,ret)

    def test_anonymous_modified(self):
        statement = 'function hello(callback){\ncallback()\n}\nhello(function(){});\nfunction world(){}'
        f = un_iife_ize.Function(statement)

        exp = ['hello=function(callback){\ncallback()\n};','world=function(){};']
        f.extract_all()
        print(f.all)
        b = [x for x,s in f.all]
        ret = b
        self.assertEqual(exp,ret)

    def test_anonymous_unmodified(self):
        statement = 'function hello(callback){\ncallback()\n}\nhello(function(){});\nfunction world(){}'
        f = un_iife_ize.Function(statement)

        exp = ['\nhello(function(){});\n']
        f.extract_all()
        print(f.unmodified)
        b = [x for x,s in f.unmodified]
        ret = b
        self.assertEqual(exp,ret)



if __name__ == '__main__':
    unittest.main()
