__author__ = 'Stephen Chamberlain'

'''
Created on 18 Nov 2017

User interface module.

@author: Stephen Chamberlain
'''

import os
import tkinter

from steamcareer import constants
from steamcareer import logic
from tkinter import Tk, Frame, Entry, Label, Button, BOTTOM, END, W, E, messagebox, filedialog, StringVar, BooleanVar, Checkbutton

class Gui(Tk):
    
    ''' ------------------------------------------------------------------------------------------------ '''
    def __init__(self):

        Tk.__init__(self)
        self.title("Steam Career - " + constants.APP_VERSION)
        self.iconbitmap(os.getcwd() + '\\resources\\favicon.ico')
        
        self.buildGui()   
        self.__centre(self)  
    
    ''' ------------------------------------------------------------------------------------------------ '''         
    def __centre(self, toplevel):
        
        toplevel.update_idletasks()
        
        w = toplevel.winfo_screenwidth()
        h = toplevel.winfo_screenheight()
        
        size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
        
        x = w / 2 - size[0] / 2
        y = h / 2 - size[1] / 2
        
        toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))
        
    ''' ------------------------------------------------------------------------------------------------ '''    
    def __setResultLocation(self):
        filename = filedialog.askdirectory()
        self.resultLocation.set(filename)
        
    ''' ------------------------------------------------------------------------------------------------ '''
    def __generateResult(self):
        try:
            os.makedirs(os.path.dirname(constants.CONF_FILE_STEAM_USER), exist_ok=True)
            with open(constants.CONF_FILE_STEAM_USER, "wb") as f:
                f.write(self.entry.get().encode("UTF-8"))
            
            os.makedirs(os.path.dirname(constants.CONF_FILE_STEAM_API_KEY), exist_ok=True)    
            with open(constants.CONF_FILE_STEAM_API_KEY, "wb") as f:
                f.write(self.apiKeyEntry.get().encode("UTF-8"))
                
            os.makedirs(os.path.dirname(constants.CONF_RESULT_LOCATION), exist_ok=True)    
            with open(constants.CONF_RESULT_LOCATION, "wb") as f:
                f.write(self.resultLocationEntry.get().encode("UTF-8"))      

            os.makedirs(os.path.dirname(constants.OVERWRITE_CSS_LOCATION), exist_ok=True)    
            with open(constants.OVERWRITE_CSS_LOCATION, "wb") as f:
                if (self.overwriteCssState.get()==True):
                    f.write("true".encode("UTF-8"))
                else:
                    f.write("false".encode("UTF-8"))
            
            logic.generateResultPage(self.apiKeyEntry.get(), self.entry.get(), self.resultLocationEntry.get(), self.overwriteCssState.get())
      
        except Exception as exception:            
            messagebox.showerror("Error", str(exception))                
    
    ''' ------------------------------------------------------------------------------------------------ '''
    def buildGui(self):
        padx = 5
        pady = 5
        
        self.frame = Frame(self)
        self.frame.pack(padx=padx, pady=pady)
        
        self.bottomframe = Frame(self)
        self.bottomframe.pack(side=BOTTOM, padx=padx, pady=pady)    
        
        self.__buildUsername(padx, pady)
        self.__buildApiKey(padx, pady)
        self.__buildResultLocation(padx, pady)
        self.__buildOverwriteCss(padx, pady)
        
        self.button = Button(self.bottomframe, text="Go", command=self.__generateResult, height=2, width=30, padx=padx, pady=pady)
        self.button.pack(side=BOTTOM)    
        
    ''' ------------------------------------------------------------------------------------------------ '''
    def __buildUsername(self, padx, pady):
        self.label = Label(self.frame, text="User Name")
        self.label.grid(row=0, column=0, sticky=E, padx=padx, pady=pady)
            
        self.entry = Entry(self.frame, width=40)
        if os.path.isfile(constants.CONF_FILE_STEAM_USER):
            with open(constants.CONF_FILE_STEAM_USER, 'r') as myfile:
                steamApiUser = myfile.read().replace('\n', '')        
            self.entry.insert(END, steamApiUser)
        self.entry.grid(row=0, column=1, padx=padx, pady=pady)
        
    ''' ------------------------------------------------------------------------------------------------ '''
    def __buildApiKey(self, padx, pady):
        self.apiKeyLabel = Label(self.frame, text="API Key")
        self.apiKeyLabel.grid(row=1, column=0, sticky=E, padx=padx, pady=pady)
        
        self.apiKeyEntry = Entry(self.frame, width=40)
        if os.path.isfile(constants.CONF_FILE_STEAM_API_KEY):
            with open(constants.CONF_FILE_STEAM_API_KEY, 'r') as myfile:
                steamApiKey = myfile.read().replace('\n', '')        
            self.apiKeyEntry.insert(END, steamApiKey)    
        self.apiKeyEntry.grid(row=1, column=1, padx=padx, pady=pady)
        
    ''' ------------------------------------------------------------------------------------------------ '''
    def __buildResultLocation(self, padx, pady):
        self.resultLocationLabel = Label(self.frame, text="Result Location")
        self.resultLocationLabel.grid(row=2, column=0, sticky=E, padx=padx, pady=pady)
        
        self.resultLocation = StringVar()
        self.resultLocationEntry = Entry(self.frame, textvariable=self.resultLocation, width=40)
        if os.path.isfile(constants.CONF_RESULT_LOCATION):
            with open(constants.CONF_RESULT_LOCATION, 'r') as myfile:
                resultLocation = myfile.read().replace('\n', '')        
            self.resultLocationEntry.insert(END, resultLocation)
        self.resultLocationEntry.grid(row=2, column=1, padx=padx, pady=pady)
        
        self.resultLocationButton = Button(self.frame, text="...", command=self.__setResultLocation, height=1, width=1, padx=padx, pady=pady)
        self.resultLocationButton.grid(row=2, column=2, padx=padx, pady=pady)
        
    ''' ------------------------------------------------------------------------------------------------ '''
    def __buildOverwriteCss(self, padx, pady):
        self.overwriteCssLabel = Label(self.frame, text="Overwrite CSS?")
        self.overwriteCssLabel.grid(row=3, column=0, sticky=E, padx=padx, pady=pady)
        self.overwriteCssState = BooleanVar()
        self.overwriteCss = Checkbutton(self.frame, justify=tkinter.LEFT, variable=self.overwriteCssState)
        if os.path.isfile(constants.OVERWRITE_CSS_LOCATION):
            with open(constants.OVERWRITE_CSS_LOCATION, 'r') as myfile:
                if myfile.read().replace('\n', '') == 'true':
                    self.overwriteCssState.set(True)
                else:
                    self.overwriteCssState.set(False)
        self.overwriteCss.grid(row=3, column=1, sticky=W, padx=padx, pady=pady)