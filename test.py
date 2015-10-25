__author__ = 'yusaira-khan'

import unittest
import un_iife_ize


class full(unittest.TestCase):
    def test_all(self):
        file = 'function hello(callback){\ncallback()\n}'
        file += '\nhello(function(){});'
        file += '\nfunction world(){}'
        file += '\nvar bye,nope;'

        stuff = un_iife_ize.handle_contents(file)
        test='hello=function(callback){\ncallback()\n};'
        test+='\nhello(function(){});\n'
        test+='world=function(){};'
        test+='\nbye=undefined,nope=undefined;'
        self.assertEqual(stuff,test)
if __name__ == '__main__':
    unittest.main()