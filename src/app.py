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
from shutil import copyfile
 
class SteamCareer(Tk):    
    CONF_FILE_STEAM_USER = 'steam-user.conf'
    CONF_FILE_STEAM_API_KEY = 'steam-api-key.conf'
    
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
        self.label.grid(row=0,column=0, sticky=E)
    
        with open(self.CONF_FILE_STEAM_USER, 'r') as myfile:
            steamApiUser = myfile.read().replace('\n', '')        
        self.entry = Entry(self.frame)
        self.entry.insert(END, steamApiUser)
        self.entry.grid(row=0,column=1)

        self.apiKeyLabel = Label(self.frame, text="API Key")
        self.apiKeyLabel.grid(row=1,column=0, sticky=E)

        with open(self.CONF_FILE_STEAM_API_KEY, 'r') as myfile:
            steamApiKey = myfile.read().replace('\n', '')        
        self.apiKeyEntry = Entry(self.frame)
        self.apiKeyEntry.insert(END, steamApiKey)    
        self.apiKeyEntry.grid(row=1,column=1)
        
        self.button = Button(self.bottomframe, text="Go", command=self.doCoolStuff, height = 2, width = 30)
        self.button.pack(side=BOTTOM)
    
    ''' ------------------------------------------------------------------------------------------------ '''
    def doCoolStuff(self):
        with open(self.CONF_FILE_STEAM_USER, "wb") as f:
            f.write(self.entry.get().encode("UTF-8"))
            
        with open(self.CONF_FILE_STEAM_API_KEY, "wb") as f:
            f.write(self.apiKeyEntry.get().encode("UTF-8"))
            
        steamapi.core.APIConnection(api_key=self.apiKeyEntry.get(), validate_key=True)
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
        
        resultPath = "result-pages\\" + steam_user.name + ".html"        
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
            
        copyfile("src\\templates\\templates\\styles.css", "result-pages\\styles.css")
            
''' ------------------------------------------------------------------------------------------------ '''
app = SteamCareer()
app.mainloop()
    
