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
            else:
                return True

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
            print(" |-")
            print()

    def games_task(self,user_id,free_games, all_details):
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
        total_playtime = 0
        for _ in games_python['response']['games']:
            title_no += 1
            playtime_hour = int(round(_['playtime_forever']/60,0))
            playtime_minutes = int(_['playtime_forever']%60)
            total_playtime += int(_['playtime_forever'])
            if all_details:
                print(" |")
                print(" |--["+str(title_no)+"] " + str((_['name']).upper()))
                print(" |-------[Playtime] " + str(playtime_hour) + "h " + str(playtime_minutes) + "m")
                print(" |-------[AppID] " + str(_['appid']))
        print(" |")
        print(" |-[Total hours played] " + str(int(round(total_playtime/60,0))) + "h " + str(int(total_playtime%60)) + "m")
        print()

    def help_task(self):
        print("---[Help]---")
        print(" |-[s] User summary")
        print(" |")
        print(" |-[g] Games summary")
        print(" |-----[f,a] Optional. 'f' includes free games and 'a' displays all games information.")
        print(' |-----[example] >>> g -fa includes free games AND displays information for every title.')
        print(" |")
        print(" |-[u] Change user")
        print(" |")
        print(" |-[h] Print this help block")
        print(" |")
        print(" |-[x] Exit quicksteam")

class Menu:
    def __init__(self):
        self._selection = "e"

    @property
    def selection(self):
        #print("--get called--")
        return self._selection

    @selection.setter
    def selection(self, user_selection):
        #print("--set called--")
        valid_selections  = ["s", "g", "h", "x", "u", "e"]
        bad_input = 0
        #print("here " + user_selection[0])
        for _ in valid_selections:
            if user_selection[0] == _:
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
            if menu.selection == "e":
                selection_valid = False
            while not selection_valid:
                if menu.selection != "e":
                    selection_valid = True
                    #print(menu.selection)
                else:
                    menu.selection = input("> ").lower()
            if menu.selection == 'h':
                execute.help_task()
                menu.selection = "e"
            elif menu.selection == 's':
                execute.summary_task(my_user_id)
                menu.selection = "e"
            elif menu.selection == 'u':
                has_id, my_user_id = execute.user_task()
                menu.selection = "e"
            elif menu.selection == 'g':
                if user_privacy:
                    #print(my_user_id)
                    execute.games_task(user_id = my_user_id, free_games = 0, all_details = False)
                    menu.selection = "e"
                else:
                    print(">>> Error: User is set to private, you can only view summary (s).")
                    menu.selection = "e"
            elif len(menu.selection) > 1:
                if menu.selection[0] == 'g':
                    if user_privacy:
                        games_option_valid = True
                        show_free_games = 0
                        show_all_details = False
                        for _ in menu.selection[3:len(menu.selection)]:
                            if _ == 'f':
                                show_free_games = 1
                            elif _ == 'a':
                                show_all_details = True
                            elif _ != 'a' and _ != 'f':
                                print("Error: Parameters not right. Enter h for help.")
                                menu.selection = "e"
                                games_option_valid = False
                        if games_option_valid:
                            execute.games_task(user_id= my_user_id, free_games = show_free_games, all_details = show_all_details)
                        menu.selection = "e"
                    else:
                        print(">>> Error: User is set to private, you can only view summary (s).")
                        menu.selection = "e"
            elif menu.selection == 'x':
                running = False
                
    
if __name__ == "__main__":
    menu = Menu()
    menu.start()