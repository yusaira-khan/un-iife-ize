__author__ = 'yusaira-khan'

import unittest
import main


class full(unittest.TestCase):
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
