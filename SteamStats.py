import steam.steamid
from steam.steamid import SteamID
from steam.webapi import WebAPI
import json
from datetime import datetime
from datetime import time
import requests

class Tasks():
    def __init__(self):
        self._api = WebAPI(key='E2F33A25C7632339FB2C348D3786332A')
        self._id_value = 0

    @property
    def id_value(self):
        return self._id_value

    @id_value.setter
    def id_value(self, id_link):
        my_id = steam.steamid.from_url(id_link)
        if hasattr(my_id, 'as_64'):
            self._id_value = my_id.as_64
        else:
            self._id_value = 0
            
    def user_task(self):
        print()
        self.id_value = input(">>> Enter community url: ")
        if self.id_value != 0:
            print('>>> ID found: ' + str(self._id_value))
            print()
            return True
        else:
            print('>>> Error: URL not valid.')
            return False
    
    def privacy_task(self):
        self._api.call('ISteamUser.GetPlayerSummaries', steamids = self._id_value)
        privacy_json = self._api.ISteamUser.GetPlayerSummaries(steamids = self._id_value, format='json', raw=True)
        privacy_python = json.loads(privacy_json)
        for _ in privacy_python['response']['players']:
            if _['communityvisibilitystate'] == 1:
                return False
            elif _['communityvisibilitystate'] == 3:
                return True

    def summary_task(self):
        self._api.call('ISteamUser.GetPlayerSummaries', steamids = self._id_value)
        summary_json = self._api.ISteamUser.GetPlayerSummaries(steamids = self._id_value, format='json', raw=True)
        summary_python = json.loads(summary_json)
        short_key = "1e9dd91ae565d468bbd8760f0316457072c19"
        for _ in summary_python['response']['players']:
            short_avatar = f"https://cutt.ly/api/api.php?key={short_key}&short={_['avatarfull']}"
            short_avatar_data = requests.get(short_avatar).json()["url"]
            if short_avatar_data["status"] == 7:
                shortened_avatar = short_avatar_data["shortLink"]
            else:
                shortened_avatar = "Error shortening link."
            short_page = f"https://cutt.ly/api/api.php?key={short_key}&short={_['profileurl']}"
            short_page_data = requests.get(short_page).json()["url"]
            if short_page_data["status"] == 7:
                shortened_page = short_page_data["shortLink"]
            else:
                shortened_page = "Error shortening link."
            if _['communityvisibilitystate'] == 3:
                profile_state = "Public"
            else:
                profile_state = "Private"
            if _['personastate'] == 0:
                current_status = "Offline"
            elif _['personastate'] == 1:
                current_status = "Online"
            elif _['personastate'] == 3:
                current_status = "Away"
            elif _['personastate'] == 4:
                current_status = "Snooze"
            else:
                current_status = "Other"
            print()
            print("---[Steam user " + _['personaname'] + " selected]---")
            print(" |")
            print(" |-[Location] "+ _['loccountrycode'])
            print(" |")
            print(" |-[Last online] "+ datetime.utcfromtimestamp(int(_['lastlogoff'])).strftime('%d %b %Y'))
            print(" |")
            print(" |-[Avatar] "+ shortened_avatar)
            print(" |")
            print(" |-[Privacy] "+ profile_state)
            print(" |")
            print(" |-[Current status] "+current_status)
            print(" |")
            print(" |-[Profile page] "+shortened_page)
            print()

    def games_task(self,free_games, all_details):
        self._api.call('IPlayerService.GetOwnedGames', steamid = self._id_value, include_played_free_games = free_games, include_appinfo = 1, appids_filter = 0, include_free_sub = 0)
        games_json = self._api.IPlayerService.GetOwnedGames(steamid = self._id_value, include_played_free_games = free_games, include_appinfo = 1, appids_filter = 0, include_free_sub = 0, format = 'json', raw = True)
        games_python = json.loads(games_json)
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

    def friends_task(self):
        self._api.call('ISteamUser.GetFriendList', steamid = self._id_value)

class Menu:
    def __init__(self):
        self._selection = "e"

    @property
    def selection(self):
        return self._selection

    @selection.setter
    def selection(self, user_selection):
        valid_selections  = ["s", "g", "h", "x", "u", "e"]
        bad_input = 0
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
        execute = Tasks()
        while running:
            while not has_id:
                has_id = execute.user_task()
            user_privacy = execute.privacy_task()
            if menu.selection == "e":
                selection_valid = False
            while not selection_valid:
                if menu.selection != "e":
                    selection_valid = True
                else:
                    menu.selection = input("> ").lower()
            if menu.selection == 'h':
                execute.help_task()
                menu.selection = "e"
            elif menu.selection == 's':
                execute.summary_task()
                menu.selection = "e"
            elif menu.selection == 'u':
                has_id = execute.user_task()
                menu.selection = "e"
            elif menu.selection == 'g':
                if user_privacy:
                    #print(my_user_id)
                    execute.games_task(free_games = 0, all_details = False)
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
                            execute.games_task(free_games = show_free_games, all_details = show_all_details)
                        menu.selection = "e"
                    else:
                        print(">>> Error: User is set to private, you can only view summary (s).")
                        menu.selection = "e"
            elif menu.selection == 'x':
                running = False
                
    
if __name__ == "__main__":
    menu = Menu()
    menu.start()