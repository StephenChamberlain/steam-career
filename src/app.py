'''
Created on 28 Oct 2017

Simple application to retrieve Steam statistics and present them in some cool way :-)

Uses the steamapi Python library at https://github.com/smiley/steamapi.

@author: Stephen Chamberlain
'''

import io
import os
import steamapi
from tkinter import *

''' e.g. "gobbo18uk" ''' 
steamId = ""

''' ------------------------------------------------------------------------------------------------ '''
def main():
    cwd = os.getcwd()
    print ("Current working directory: " + cwd)
    
    buildGui()
    
''' ------------------------------------------------------------------------------------------------ '''
def buildGui():
    top = Tk()
    frame = Frame(top)
    frame.pack()
    
    bottomframe = Frame(top)
    bottomframe.pack(side=BOTTOM)    
    
    label = Label(frame, text="User Name")
    label.pack(side=LEFT)
    
    entry = Entry(frame, textvariable=steamId)    
    entry.pack(side=RIGHT)
    
    button = Button(bottomframe, text="Go", command=doCoolStuff)
    button.pack(side=BOTTOM)
    
    top.mainloop()

''' ------------------------------------------------------------------------------------------------ '''
def doCoolStuff():
    with open('steam-api-key.conf', 'r') as myfile:
        steamApiKey = myfile.read().replace('\n', '')
        
    steamapi.core.APIConnection(api_key=steamApiKey, validate_key=True)
    steam_user = steamapi.user.SteamUser(userurl=steamId)
    content = "Your real name is {0}. You have {1} friends and {2} games.".format(steam_user.real_name, len(steam_user.friends), len(steam_user.games))
        
    print (content)
    
    print ("You recently played:")
    for game in steam_user.recently_played:
        print ("  " + game.name)    

''' ------------------------------------------------------------------------------------------------ '''
if __name__ == '__main__':
    main()
    
