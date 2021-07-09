__author__ = 'Stephen Chamberlain'

'''
Created on 18 Nov 2017

@author: Stephen Chamberlain
'''

import unittest
import steamapi

from steamcareer import logic, constants 

class Test(unittest.TestCase):

    def test_APIConfigurationError(self):
        self.assertRaises(steamapi.errors.APIConfigurationError, 
                          logic.generateResultPage, 
                          "invalidApiKey", "nonExistingUser", constants.USER_APP_DIR + "\\steam-career-tests", False)
        
if __name__ == "__main__":
    unittest.main()