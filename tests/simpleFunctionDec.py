__author__ = 'yusaira-khan'

import unittest
import main


def boilerplate():
    pass


class FunctionSimple(unittest.TestCase):

    def test_full(self):
        statement = 'function hello(){}'
        exp = 'hello=function(){};'
        ret=main.fun_all(contents=statement)
        self.assertEqual(exp,ret)

    # def test_untouched(self):
    #     statement = 'function (){}'
    #     exp = 'function (){}'
    #     ret=main.fun_all(contents=statement)
    #     self.assertEqual(exp,ret)
    def test_console(self):
        statement = '''function hello(){
    console.log('hello, world');
}'''
        exp = '''hello=function(){
    console.log('hello, world');
};'''
        ret=main.fun_all(contents=statement)
        self.assertEqual(exp,ret)

    def test_if(self):
        statement = '''function hello(){
    if(true){
        console.log('hello, world');
    }
}'''
        exp = '''hello=function(){
    if(true){
        console.log('hello, world');
    }
};'''
        ret=main.fun_all(contents=statement)
        self.assertEqual(exp,ret)

    def test_nested_if(self):
        statement = '''function hello(){
    if(true){
        console.log('hello, world');
        if(true) {
        }
    }
}'''
        exp = '''hello=function(){
    if(true){
        console.log('hello, world');
        if(true) {
        }
    }
};'''
        ret=main.fun_all(contents=statement)
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
        match,rb = main.detect_func_declaration(statement,0)
        info = main.get_fun_info(statement,match,rb)
        self.assertEqual(info,exp)


if __name__ == '__main__':
    unittest.main()
