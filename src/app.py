__author__ = 'Stephen Chamberlain'

'''
Created on 28 Oct 2017

Simple application to retrieve Steam statistics and present them in some cool way :-)

Uses the steamapi Python library at https://github.com/smiley/steamapi.

@author: Stephen Chamberlain
'''

import io, subprocess, os, steamapi, math, datetime

from tkinter import *
from jinja2 import Template, Environment, PackageLoader, select_autoescape
 
class SteamCareer(Tk):
    
    ''' ------------------------------------------------------------------------------------------------ '''
    def __init__(self):
        Tk.__init__(self)
        
        cwd = os.getcwd()
        print ("Current working directory: " + cwd)
        
        self.buildGui()
        
    ''' ------------------------------------------------------------------------------------------------ '''
    def buildGui(self):
        self.frame = Frame(self)
        self.frame.pack()
        
        self.bottomframe = Frame(self)
        self.bottomframe.pack(side=BOTTOM)    
        
        self.label = Label(self.frame, text="User Name")
        self.label.pack(side=LEFT)
        
        self.entry = Entry(self.frame)
        self.entry.insert(END, 'gobbo18uk')    
        self.entry.pack(side=RIGHT)
        
        self.button = Button(self.bottomframe, text="Go", command=self.doCoolStuff)
        self.button.pack(side=BOTTOM)
    
    ''' ------------------------------------------------------------------------------------------------ '''
    def doCoolStuff(self):
        with open('steam-api-key.conf', 'r') as myfile:
            steamApiKey = myfile.read().replace('\n', '')
            
        steamapi.core.APIConnection(api_key=steamApiKey, validate_key=True)
        steam_user = steamapi.user.SteamUser(userurl=self.entry.get())

#         self.printSteamDataToConsole(steam_user)
        self.generateResultPage(steam_user)

    ''' ------------------------------------------------------------------------------------------------ '''
    def printSteamDataToConsole(self, steam_user):
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
    def generateResultPage(self, steam_user):
        print ("")    
        print ("Generating results page...")        
        
        env = Environment(
            loader=PackageLoader('templates', 'templates'),
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
        
        resultPath = "result.html" 
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
            
''' ------------------------------------------------------------------------------------------------ '''
app = SteamCareer()
app.mainloop()
    
