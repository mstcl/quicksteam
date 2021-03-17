import steam.steamid
from steam.steamid import SteamID
from steam.webapi import WebAPI
import json
from datetime import datetime
from datetime import time

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
            print('>>> ID found: ' + str(self._id_value))
            print()
        else:
            self._id_value = 0
            print('>>> Error: URL not valid.')

class Tasks:
    def __init__(self):
        pass

    def user_task(self):
        id = ID()
        print()
        id.id_value = input(">>> Enter community url: ")
        if id.id_value != 0:
            return True, id.id_value
        else:
            return False, id.id_value
    
    def privacy_task(self,user_id):
        api = WebAPI(key='E2F33A25C7632339FB2C348D3786332A')
        api.call('ISteamUser.GetPlayerSummaries', steamids = user_id)
        privacy_json = api.ISteamUser.GetPlayerSummaries(steamids = user_id, format='json', raw=True)
        privacy_python = json.loads(privacy_json)
        for _ in privacy_python['response']['players']:
            if _['communityvisibilitystate'] == 1:
                return False

    def summary_task(self,user_id):
        api = WebAPI(key='E2F33A25C7632339FB2C348D3786332A')
        api.call('ISteamUser.GetPlayerSummaries', steamids = user_id)
        summary_json = api.ISteamUser.GetPlayerSummaries(steamids = user_id, format='json', raw=True)
        summary_python = json.loads(summary_json)

        for _ in summary_python['response']['players']:
            print()
            print("---[Steam user " + _['personaname'] + " selected]---")
            print(" |")
            #print(" |_ Avatar link: "+ _['avatarfull'])
            #print(" |")
            print(" |-[Location] "+ _['loccountrycode'])
            print(" |")
            print(" |-[Last online] "+ datetime.utcfromtimestamp(int(_['lastlogoff'])).strftime('%d %b %Y'))
            print()

    def games_task(self,user_id,free_games):
        api = WebAPI(key='E2F33A25C7632339FB2C348D3786332A')
        #print(user_id,free_games)
        api.call('IPlayerService.GetOwnedGames', steamid = user_id, include_played_free_games = free_games, include_appinfo = 1, appids_filter = 0, include_free_sub = 0)
        games_json = api.IPlayerService.GetOwnedGames(steamid = user_id, include_played_free_games = free_games, include_appinfo = 1, appids_filter = 0, include_free_sub = 0, format = 'json', raw = True)
        games_python = json.loads(games_json)
        #print(games_python,games_json)
        print()
        print("---[Game information]---")
        print(" |")
        print(" |-[Game count] "+ str(games_python['response']['game_count']) + " titles")
        title_no = 0
        for _ in games_python['response']['games']:
            title_no += 1
            print(" |")
            print(" |--["+str(title_no)+"] " + str((_['name']).upper()))
            playtime_hour = int(round(_['playtime_forever']/60,0))
            playtime_minutes = int(_['playtime_forever']%60)
            print(" |-------[Playtime] " + str(playtime_hour) + "h " + str(playtime_minutes) + "m")
            print(" |-------[AppID] " + str(_['appid']))
        print()

    def help_task(self):
        print("---[Help]---")
        print(" |-[s] User general summary")
        print(" |")
        print(" |-[g] Games summary")
        print(" |")
        print(" |-[u] Change user")
        print(" |")
        print(" |-[h] Print this help block")
        print(" |")
        print(" |-[x] Exit quicksteam")

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
        valid_selections  = ["s", "g", "h", "x", "u", "none"]
        bad_input = 0
        for _ in valid_selections:
            if user_selection == _:
                self._selection = user_selection
                break
            else:
                bad_input += 1
        if bad_input == len(valid_selections):
            print(">>> Error: Unrecognised selection. Enter h for help.")

    def start(self):
        running = True
        has_id = False
        while running:
            execute = Tasks()
            while not has_id:
                has_id, my_user_id = execute.user_task()
            user_privacy = execute.privacy_task(my_user_id)
            if not user_privacy:
                print(">>> User is set to private, you can only view summary (s).")
            if menu.selection == "none":
                selection_valid = False
            while not selection_valid:
                if menu.selection != "none":
                    selection_valid = True
                else:
                    menu.selection = input("> ").lower()
            if menu.selection == 'h':
                execute.help_task()
                menu.selection = "none"
            elif menu.selection == 's':
                execute.summary_task(my_user_id)
                menu.selection = "none"
            elif menu.selection == 'u':
                has_id, my_user_id = execute.user_task()
                menu.selection = "none"
            elif menu.selection == 'g':
                if user_privacy:
                    #print(my_user_id)
                    free_games_valid = False
                    while not free_games_valid:
                        show_free_games = input('>>> Include free games? (y/n): ').lower()
                        while show_free_games not in ["y", "n"]:
                            show_free_games = input('Error: Invalid input, try again: ').lower()
                        free_games_valid = True
                    if show_free_games == 'y':
                        execute.games_task(user_id = my_user_id, free_games = 1)
                    elif show_free_games == 'n':
                        execute.games_task(user_id = my_user_id, free_games = 0)
                    menu.selection = "none"
                else:
                    print(">>> Error: User is set to private, you can only view summary (s).")
                    menu.selection = "none"
            elif menu.selection == 'x':
                running = False
    
if __name__ == "__main__":
    menu = Menu()
    menu.start()