__author__ = 'Stephen Chamberlain'

'''
Created on 28 Oct 2017

Experimental Python application which uses the Steam Web API to retrieve player data and present an overview in 
HTML form.

@author: Stephen Chamberlain
'''

import os

from steamcareer import ui

def setWorkingDirectoryToAppRoot():
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
            
    cwd = os.getcwd()
    print ("Current working directory: " + cwd)

''' ------------------------------------------------------------------------------------------------ '''
setWorkingDirectoryToAppRoot()

app = ui.Gui()
app.mainloop()