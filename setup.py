'''
Created on 19 Nov 2017

Setup.

@author: Stephen Chamberlain
'''

import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "steam-career",
    version = "1.0",
    author = "Stephen Chamberlain",
    author_email = "steve@steve-chamberlain.co.uk",
    description = ("Experimental Python application which uses the Steam Web API to retrieve player data and present an overview in HTML form."),
    license = "MIT",
    url = "https://github.com/StephenChamberlain/steam-career",
    packages=['steamcareer'],
    long_description=read('README.md'),
)