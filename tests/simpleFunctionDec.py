__author__ = 'yusaira-khan'

import unittest
import main

class FunctionSimple(unittest.TestCase):

    def test_full(self):
        statement = 'function hello(){}'

        f = main.Function(statement)
        exp = 'hello=function(){};'
        ret=f.extract()
        self.assertEqual(exp,ret)

    def test_untouched(self):
        statement = 'function (){}'
        f = main.Function(statement)
        exp = None
        ret=f.extract()
        self.assertEqual(exp,ret)


    def test_console(self):
        statement = "function hello(){\n  console.log('hello, world');\n}"
        exp = "hello=function(){\n  console.log('hello, world');\n};"
        ret = exp
        self.assertEqual(exp,ret)

    def test_if(self):
        statement = "function hello(){\n  if(true){\n    console.log('hello, world');\n  }\n}"
        exp = "hello=function(){\n  if(true){\n    console.log('hello, world');\n  }\n};"
        ret=exp
        self.assertEqual(exp,ret)

    def test_nested_if(self):
        statement = "function hello(){\n  if(true){\n    console.log('hello, world');\n    if(true){}\n  }\n}"
        exp = "hello=function(){\n  if(true){\n    console.log('hello, world');\n    if(true) {}\n  }\n};"
        ret=exp
        self.assertEqual(exp,ret)

    def test_info_blank(self):
        statement = 'function hello(){}'

        exp = {
        'name': 'hello',
        'args': '()',
        'statement_start': 0,
        'lbrace_index': 16,
        'rbrace_index': 17,
        'body':'{}'
        }

        f= main.Function(statement)
        match,rb = f.detect_declaration(0)
        info = f.get_info(match,rb)
        self.assertEqual(info,exp)


if __name__ == '__main__':
    unittest.main()
