import steam.steamid
from steam.steamid import SteamID
from steam.webapi import WebAPI
import json
from datetime import datetime

class ID:
    def __init__(self):
        self._id_value = 0

    @property
    def id_value(self):
        #print("--get called--")
        return self._id_value

    @id_value.setter
    def id_value(self, id_link):
        #print("--set called--")
        my_id = steam.steamid.from_url(id_link)
        if hasattr(my_id, 'as_64'):
            self._id_value = my_id.as_64
            print()
            print('ID found: ' + str(self._id_value))
        else:
            print('URL not valid.')

class Tasks:
    def __init__(self):
        pass

    def user_task(self):
        raw_link = input("Enter community url: ")
        return raw_link
                
    def summary_task(self,user_id):
        api = WebAPI(key='E2F33A25C7632339FB2C348D3786332A')
        api.call('ISteamUser.GetPlayerSummaries', steamids = user_id)
        summary_json = api.ISteamUser.GetPlayerSummaries(steamids = user_id, format='json', raw=True)
        summary_python = json.loads(summary_json)
        #print(summary_python['response']['players'])
        #print(type(player_dict))
        #print(player_dict['players'][0])

        for _ in summary_python['response']['players']:
            print("----Steam user " + _['personaname'] + " selected----")
            print(" |")
            #print(" |_ Avatar link: "+ _['avatarfull'])
            #print(" |")
            print(" |_ Location: "+ _['loccountrycode'])
            print(" |")
            print(" |_ Last online: "+ datetime.utcfromtimestamp(int(_['lastlogoff'])).strftime('%d/%m/%Y'))

    def help_task(self):
        print("s: User general summary")
        print("a: User achievement summary")
        print("u: Change user")
        print("h: Print this help block")
        

class Menu:
    def __init__(self):
        self._selection = "none"

    @property
    def selection(self):
        #print("--get called--")
        return self._selection

    @selection.setter
    def selection(self, user_selection):
        #print("--set called--")
        if user_selection == 's' or 'a' or 'h':
            self._selection = user_selection
        else:
            print("Unrecognised selection. Enter h for help.")

    def start(self):
        id = ID()
        running = True
        has_id = False
        while running:
            execute = Tasks()
            while not has_id:
                #print(id.id_value)
                if id.id_value != 0:
                    has_id = True
                else:
                    id.id_value = execute.user_task()
            selection_valid = False
            while not selection_valid:
                if not menu.selection == "none":
                    selection_valid = True
                else:
                    menu.selection = input("> ")
            if menu.selection == 'h':
                execute.help_task()
                menu.selection = "none"
            elif menu.selection == 's':
                execute.summary_task(id._id_value)
                menu.selection = "none"
            elif menu.selection == 'u':
                execute.user_task()
                menu.selection = "none"
            else:
                running = False
    
if __name__ == "__main__":
    menu = Menu()
    menu.start()
    




