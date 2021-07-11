'''
Created on 13 Apr 2019

Holds player data so that necessary data processing can happen in one place and the result shared between all templates.

@author: Stephen
'''

import datetime, requests, json, babel.numbers

class PlayerData(object):
    
    def __init__(self, steam_user):
        try:
            self.user = steam_user
            self.timestamp = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
            self.games = sorted(steam_user.games, key=lambda game: game.playtime_forever, reverse=True)
            self.price_map = {}
            self.total_value = 0

            self.fill_price_map()

            total_minutes_played = 0
            nr_actually_played_games = 0
            for game in steam_user.games:
                if game.playtime_forever > 0:
                    total_minutes_played += game.playtime_forever
                    nr_actually_played_games += 1
    
            self.total_hours_played = total_minutes_played / 60
            self.nr_actually_played_games = nr_actually_played_games
        except Exception as exception:
            print ("Error", str(exception))
            self.total_hours_played = 0
            self.nr_actually_played_games = 0
            self.games = []
            self.price_map = {}
            self.total_value = 0

    def fill_price_map(self):
        try:
            gameids = []
            for game in self.games:
                gameids.append(str(game.id))
            appids = ",".join(gameids)
            response = requests.get(f"http://store.steampowered.com/api/appdetails?appids={appids}&filters=price_overview")
            #print(response.text)
            data = json.loads(response.text)
            first = True
            for key in data.keys():
                if first:
                    # Only need to do this once; we aren't getting different currency codes in 1 request
                    self.currency_code = data[f'{key}']['data']['price_overview']['currency']
                    first = False
                try:
                    price = data[f'{key}']['data']['price_overview']['final']
                    # Ensure we have a decimal at position -2 in the price string, then cast the result to a float for formatting in templating.
                    price_str = float(str(price)[:-2] + '.' + str(price)[-2:])
                    self.price_map[int(key)] = price_str
                    self.total_value += price
                except Exception as exception:
                    # TODO: game is part of a collection, no longer sold on Steam or some other issue. Look up again by without "filters" 
                    # attribute in order to provide a better explanation as to why we have no price.
                    #print(f"Exception requesting price information for app {key}")
                    self.price_map[int(key)] = 'unknown'
        except Exception as exception:
            print("General exception when requesting price information")
            self.price_map = {}
            self.total_value = 0
        
        # What if total is less than 1 euro? or 0?
        # Tested with friends account; handled by Python implicitly, results in 0.00 being displayed
        self.total_value = float(str(self.total_value)[:-2] + '.' + str(self.total_value)[-2:])

        self.currency_char = babel.numbers.get_currency_symbol(self.currency_code, locale='en_US')