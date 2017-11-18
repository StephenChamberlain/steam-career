'''
Created on 18 Nov 2017

@author: Stephen
'''

import appdirs

APP_NAME = 'steam-career'
APP_AUTHOR = 'steve-chamberlain'
APP_VERSION = '1.0'
APP_ROAMING = False

CONF_FILE_STEAM_USER = appdirs.user_data_dir(APP_NAME, APP_AUTHOR, APP_VERSION, APP_ROAMING) + '\\steam-user.conf'
CONF_FILE_STEAM_API_KEY = appdirs.user_data_dir(APP_NAME, APP_AUTHOR, APP_VERSION, APP_ROAMING) + '\\steam-api-key.conf'
CONF_RESULT_LOCATION = appdirs.user_data_dir(APP_NAME, APP_AUTHOR, APP_VERSION, APP_ROAMING) + '\\result-location.conf'