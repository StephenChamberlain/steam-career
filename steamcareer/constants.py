__author__ = 'Stephen Chamberlain'

'''
Created on 18 Nov 2017

Shared constants used elsewhere.

@author: Stephen Chamberlain
'''

import appdirs

APP_NAME = 'steam-career'
APP_AUTHOR = 'steve-chamberlain'
APP_VERSION = '1.1'
APP_ROAMING = False

USER_APP_DIR = appdirs.user_data_dir(APP_NAME, APP_AUTHOR, APP_VERSION, APP_ROAMING)
# TODO: just use one settings file...
CONF_FILE_STEAM_USER = USER_APP_DIR + '\\steam-user.conf'
CONF_FILE_STEAM_API_KEY = USER_APP_DIR + '\\steam-api-key.conf'
CONF_RESULT_LOCATION = USER_APP_DIR + '\\result-location.conf'