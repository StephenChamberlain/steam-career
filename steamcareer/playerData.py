'''
Created on 13 Apr 2019

@author: Stephen
'''

import datetime

class PlayerData(object):
    
    def __init__(self, steam_user):
        self.user = steam_user
        self.timestamp = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
        self.games = sorted(steam_user.games, key=lambda game: game.playtime_forever, reverse=True)
    
        total_minutes_played = 0
        nr_actually_played_games = 0
        for game in steam_user.games:
            if game.playtime_forever > 0:
                total_minutes_played += game.playtime_forever
                nr_actually_played_games += 1

        self.total_hours_played = total_minutes_played / 60
        self.nr_actually_played_games = nr_actually_played_games