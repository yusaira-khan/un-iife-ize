__author__ = 'yusaira-khan'

import unittest
import un_iife_ize.un_iife_ize as un_iife_ize


class InsideFunction(unittest.TestCase):
    def test_inside(self):
        # statement = 'function hello(callback){\ncallback()\n}\nhello(function(){});\nfunction world(){}'
        statement = "function(){0;}"
        index = statement.index('0')
        ex = un_iife_ize.Extractor()
        res = ex.is_inside_function(0, index, statement)
        self.assertFalse(not res)

    def test_outside(self):
        # statement = 'function hello(callback){\ncallback()\n}\nhello(function(){});\nfunction world(){}'
        statement = "function(){0;}\nconsole.log('hello');"
        index = statement.index('c')
        ex = un_iife_ize.Extractor()
        res = ex.is_inside_function(0, index, statement)
        self.assertFalse(res)

    def test_function(self):
        # statement = 'function hello(callback){\ncallback()\n}\nhello(function(){});\nfunction world(){}'
        statement = "function(){0;}\nfunction hello(){return 0};"
        index = statement.index('c')
        ex = un_iife_ize.Function(statement)

        res = ex.detect_declaration()
        print(res)
        declaration_start = statement.find('f', 1)
        lbrace = statement.rfind('{') + 1
        rbrace = statement.rfind('}')
        print(declaration_start, lbrace, rbrace)

        self.assertTrue(res[0].start() == declaration_start and res[0].end() == lbrace and res[1] == rbrace)

    def test_recurse(self):
        # statement = 'function hello(callback){\ncallback()\n}\nhello(function(){});\nfunction world(){}'
        statement = "function(){function hello(){return 0};}\nfunction hello(){return 0};"
        index = statement.index('c')
        ex = un_iife_ize.Function(statement)

        res = ex.detect_declaration()
        print(res)
        declaration_start = statement.find('f', 12)
        lbrace = statement.rfind('{') + 1
        rbrace = statement.rfind('}')
        print(declaration_start, lbrace, rbrace)

        self.assertTrue(res[0].start() == declaration_start and res[0].end() == lbrace and res[1] == rbrace)


if __name__ == '__main__':
    unittest.main()
