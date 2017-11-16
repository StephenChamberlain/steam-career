__author__ = 'Stephen Chamberlain'

'''
Created on 28 Oct 2017

Simple application to retrieve Steam statistics and present them in some cool way :-)

Uses the steamapi Python library at https://github.com/smiley/steamapi.

@author: Stephen Chamberlain
'''

import subprocess, os, steamapi, math, datetime, appdirs

from tkinter import Tk, Frame, Entry, Label, Button, BOTTOM, END, E, messagebox, sys
from jinja2 import Environment, PackageLoader, select_autoescape
from shutil import copyfile
from steamapi import errors
 
class SteamCareer(Tk):    
    APP_NAME = 'steam-career'
    APP_AUTHOR = 'steve-chamberlain'
    APP_VERSION = '1.0'
    APP_ROAMING = False
    
    CONF_FILE_STEAM_USER = appdirs.user_data_dir(APP_NAME, APP_AUTHOR, APP_VERSION, APP_ROAMING) + '\\steam-user.conf'
    CONF_FILE_STEAM_API_KEY = appdirs.user_data_dir(APP_NAME, APP_AUTHOR, APP_VERSION, APP_ROAMING) + '\\steam-api-key.conf'
    
    ''' ------------------------------------------------------------------------------------------------ '''
    def __init__(self):
        
        ''' set current dir to location of script parent, root of the application '''
        abspath = os.path.abspath(os.path.join(__file__, os.pardir))
        dname = os.path.dirname(abspath)
        os.chdir(dname)
                
        cwd = os.getcwd()
        print ("Current working directory: " + cwd)

        Tk.__init__(self)
        self.title("Steam Career")
        self.iconbitmap(cwd + '\\steamcareer\\favicon.ico')
        
        self.buildGui()   
        self.centre(self)     
        
    ''' ------------------------------------------------------------------------------------------------ '''
    def buildGui(self):
        padx = 5
        pady = 5
        
        self.frame = Frame(self)
        self.frame.pack(padx=padx, pady=pady)
        
        self.bottomframe = Frame(self)
        self.bottomframe.pack(side=BOTTOM, padx=padx, pady=pady)    
        
        self.label = Label(self.frame, text="User Name")
        self.label.grid(row=0, column=0, sticky=E, padx=padx, pady=pady)
            
        self.entry = Entry(self.frame, width=40)
        if os.path.isfile(self.CONF_FILE_STEAM_USER):
            with open(self.CONF_FILE_STEAM_USER, 'r') as myfile:
                steamApiUser = myfile.read().replace('\n', '')        
            self.entry.insert(END, steamApiUser)
        self.entry.grid(row=0, column=1, padx=padx, pady=pady)        

        self.apiKeyLabel = Label(self.frame, text="API Key")
        self.apiKeyLabel.grid(row=1, column=0, sticky=E, padx=padx, pady=pady)
        
        self.apiKeyEntry = Entry(self.frame, width=40)
        if os.path.isfile(self.CONF_FILE_STEAM_API_KEY):
            with open(self.CONF_FILE_STEAM_API_KEY, 'r') as myfile:
                steamApiKey = myfile.read().replace('\n', '')        
            self.apiKeyEntry.insert(END, steamApiKey)    
        self.apiKeyEntry.grid(row=1, column=1, padx=padx, pady=pady)
        
        self.button = Button(self.bottomframe, text="Go", command=self.generateResult, height = 2, width = 30, padx=padx, pady=pady)
        self.button.pack(side=BOTTOM)        
    
    ''' ------------------------------------------------------------------------------------------------ '''
    def generateResult(self):
        try:
            os.makedirs(os.path.dirname(self.CONF_FILE_STEAM_USER), exist_ok=True)
            with open(self.CONF_FILE_STEAM_USER, "wb") as f:
                f.write(self.entry.get().encode("UTF-8"))
            
            os.makedirs(os.path.dirname(self.CONF_FILE_STEAM_API_KEY), exist_ok=True)    
            with open(self.CONF_FILE_STEAM_API_KEY, "wb") as f:
                f.write(self.apiKeyEntry.get().encode("UTF-8"))
                
            steamapi.core.APIConnection(api_key=self.apiKeyEntry.get(), validate_key=True)
            steam_user = steamapi.user.SteamUser(userurl=self.entry.get())
    
    #         self.printSteamDataToConsole(steam_user)
            self.generateResultPage(steam_user)
            
        except errors.APIException as exception:
            messagebox.showerror("Error", str(exception))
        except PermissionError as exception:
            messagebox.showerror("Error", str(exception))

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
            
        copyfile("steamcareer\\templates\\templates\\styles.css", "result-pages\\styles.css")
            
    ''' ------------------------------------------------------------------------------------------------ '''         
    def centre(self, toplevel):
        toplevel.update_idletasks()
        w = toplevel.winfo_screenwidth()
        h = toplevel.winfo_screenheight()
        size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
        x = w/2 - size[0]/2
        y = h/2 - size[1]/2
        toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))
                
''' ------------------------------------------------------------------------------------------------ '''
app = SteamCareer()
app.mainloop()
    
