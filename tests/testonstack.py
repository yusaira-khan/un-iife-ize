__author__ = 'yusaira-khan'

import unittest
import un_iife_ize.un_iife_ize as main


class Full(unittest.TestCase):
    def test_all(self):
        file = 'function hello(callback){\ncallback()\n}'
        file += '\nhello(function(){});'
        file += '\nfunction world(){}'
        file += '\nvar bye,nope;'

        stuff = main.handle_contents(file)
        test='hello=function(callback){\ncallback()\n};'
        test+='\nhello(function(){});\n'
        test+='world=function(){};'
        test+='\nbye=undefined,nope=undefined;'
        self.assertEqual(stuff,test)
if __name__ == '__main__':
    unittest.main()