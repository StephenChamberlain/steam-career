'''
Created on 18 Nov 2017

@author: Stephen
'''

import unittest
# import os

# from steamcareer import logic 

class Test(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')
        
if __name__ == "__main__":
    unittest.main()