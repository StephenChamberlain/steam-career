'''
Created on 18 Nov 2017

@author: Stephen
'''

import os
import math
import datetime
import steamapi
import subprocess

from tkinter import sys # TODO: shouldnt be any dependency on tkinter here!
from jinja2 import Environment, PackageLoader, select_autoescape
from shutil import copyfile

''' ------------------------------------------------------------------------------------------------ '''
def printSteamDataToConsole(steam_user):
    content = "Your real name is {0}. You have {1} friends and {2} games.".format(steam_user.real_name, len(steam_user.friends), len(steam_user.games))
    
    print ("")    
    print (content)
    
    print ("")
    print ("You recently played:")
    for game in steam_user.recently_played:
        print ("  " + game.name)
    
    print ("")    
    print ("Your collection:")        
    for game in sorted(steam_user.games, key=lambda game: game.playtime_forever, reverse=True):
        total_hours_played = math.ceil(game.playtime_forever / 60)
        print ("  {0}, total play time: {1}".format(game.name, total_hours_played))
                
''' ------------------------------------------------------------------------------------------------ '''
def generateResultPage(apiKey, userId, resultLocation):
    print ("")    
    print ("Generating results page...")        
    
    steamapi.core.APIConnection(api_key=apiKey, validate_key=True)
    steam_user = steamapi.user.SteamUser(userurl=userId)    
    
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
        
    if sys.platform.startswith('darwin'):
        subprocess.call(('open', resultPath))
    elif os.name == 'nt':
        os.startfile(resultPath)
    elif os.name == 'posix':
        subprocess.call(('xdg-open', resultPath))
        
    copyfile("templates\\styles.css", resultLocation + "\\styles.css")        