__author__ = 'Stephen Chamberlain'

'''
Created on 18 Nov 2017

Contains the logic to generate HTML output from steam API input.

@author: Stephen Chamberlain
'''

import datetime
import math
import os
import subprocess
import steamapi

from jinja2 import Environment, PackageLoader, select_autoescape
from tkinter import sys  # TODO: shouldnt be any dependency on tkinter here!
from shutil import copyfile

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
def __copyStyleSheetToResultLocation(resultLocation):
    cssResultLocation = resultLocation + "\\styles.css"
    if os.path.exists(cssResultLocation):
        print ("")
        print ("Not copying CSS stylesheet, " + cssResultLocation + " already exists, user might have modified it")
    else:
        copyfile("templates\\styles.css", cssResultLocation)
    
''' ------------------------------------------------------------------------------------------------ '''
def __openResultInSystemBrowser(resultPath):
    if sys.platform.startswith('darwin'):
        subprocess.call(('open', resultPath))
    elif os.name == 'nt':
        os.startfile(resultPath)
    elif os.name == 'posix':
        subprocess.call(('xdg-open', resultPath))

''' ------------------------------------------------------------------------------------------------ '''
def generateResultPage(apiKey, userId, resultLocation):
    print ("")    
    print ("Generating results page...")        
    
    steamapi.core.APIConnection(api_key=apiKey, validate_key=True)
    steam_user = steamapi.user.SteamUser(userurl=userId)    
    
    __printSteamDataToConsole(steam_user)
    
    env = Environment(
        loader=PackageLoader("steamcareer"),
        autoescape=select_autoescape(['html', 'xml'])
    )
    
    template = env.get_template('career.html')        
    games = sorted(steam_user.games, key=lambda game: game.playtime_forever, reverse=True)
    
    total_hours_played = 0
    nr_actually_played_games = 0
    for game in games:
        if game.playtime_forever > 0:
            total_hours_played += game.playtime_forever
            nr_actually_played_games += 1            
    
    total_hours_played = total_hours_played / 60;
    
    timestamp = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
    
    resultPath = resultLocation + "\\" + steam_user.name + ".html"        
    os.makedirs(os.path.dirname(resultPath), exist_ok=True)         
    with open(resultPath, "wb") as f:
        result = template.render(
            user=steam_user,
            games=games,
            total_hours_played=total_hours_played,
            nr_actually_played_games=nr_actually_played_games,
            timestamp=timestamp)         
        
        f.write(result.encode("UTF-8")) 
        
    __copyStyleSheetToResultLocation(resultLocation)
    __openResultInSystemBrowser(resultPath)
