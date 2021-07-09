__author__ = 'Stephen Chamberlain'

'''
Created on 18 Nov 2017

Contains the logic to generate HTML output from steam API input.

@author: Stephen Chamberlain
'''

import math
import os
import subprocess
import steamapi

from steamcareer.playerData import PlayerData
from jinja2 import Environment, PackageLoader, select_autoescape
from tkinter import sys  # TODO: shouldnt be any dependency on tkinter here!
from shutil import copyfile
from pathlib import Path

''' ------------------------------------------------------------------------------------------------ '''
def __printSteamDataToConsole(steam_user):
    content = "{0}s real name is {1}. Player has {2} friends and {3} games.".format(
        steam_user.name,
        steam_user.real_name, 
        len(steam_user.friends), 
        len(steam_user.games))
    
    print ("")    
    print (content)
    
    print ("")
    print ("Recently played:")
    for game in steam_user.recently_played:
        print ("  " + game.name)
    
    print ("")    
    print ("Collection:")        
    for game in sorted(steam_user.games, key=lambda game: game.playtime_forever, reverse=True):
        total_hours_played = math.ceil(game.playtime_forever / 60)
        print ("  {0}, total play time: {1}".format(game.name, total_hours_played))
    
''' ------------------------------------------------------------------------------------------------ '''
def __openResultInSystemBrowser(resultPath):
    if sys.platform.startswith('darwin'):
        subprocess.call(('open', resultPath))
    elif os.name == 'nt':
        os.startfile(resultPath)
    elif os.name == 'posix':
        subprocess.call(('xdg-open', resultPath))

''' ------------------------------------------------------------------------------------------------ '''
def generateResultPage(apiKey, userId, resultLocation, overwriteCss):
    print ("")    
    print ("Generating results page...")        
    
    steamapi.core.APIConnection(api_key=apiKey, validate_key=True)
    steam_user = steamapi.user.SteamUser(userurl=userId)
    
    '''__printSteamDataToConsole(steam_user)'''
    
    env = Environment(
        trim_blocks=True,
        loader=PackageLoader("steamcareer"),
        autoescape=select_autoescape(['html', 'xml'])
    )
    
    finalResultLocation = Path(resultLocation) / steam_user.name
    finalResultLocation.mkdir(exist_ok=True) 
    
    playerData = PlayerData(steam_user);
    
    __copyStyleSheetToResultLocation(finalResultLocation, overwriteCss)
    for file in os.listdir("templates"):
        __generateTemplate(playerData, env, finalResultLocation, file)

    __openResultInSystemBrowser(__generateTemplate(playerData, env, finalResultLocation, 'index.html'))
    
''' ------------------------------------------------------------------------------------------------ '''
def __copyStyleSheetToResultLocation(resultLocation, overwriteCss):
    cssResultLocation = resultLocation / "styles.css"
    if os.path.exists(cssResultLocation) and not overwriteCss:
        print ("")
        print ("Not copying CSS stylesheet, " + str(cssResultLocation) + " already exists, user might have modified it")
    else:
        copyfile("templates\\styles.css", cssResultLocation)
        print ("Copied CSS stylesheet, " + str(cssResultLocation))    
    
''' ------------------------------------------------------------------------------------------------ '''
def __generateTemplate(playerData, env, resultLocation, templatePath):
    template = env.get_template(templatePath)

    resultPath = resultLocation / templatePath
    with open(resultPath, "wb") as f:
        result = template.render(playerData=playerData)                 
        f.write(result.encode("UTF-8"))

    return resultPath
