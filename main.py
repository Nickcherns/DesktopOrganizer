import os
from datetime import datetime
from pathlib import Path
from steam_web_api import Steam

# declare steam API key and Steam ID
STEAM_API_KEY: str = ""
    # DELETE THIS AFTER EVERY USE
STEAM_ID: str = ""
# create steam variable that holds given API key
steam = Steam(STEAM_API_KEY)

# might not need environment value, dont really understand at the moment
# KEY = os.environ.get(STEAM_API_KEY)

# get user owned games dictionary
user_games = steam.users.get_owned_games(STEAM_ID)
# split user_games dictionary into game_count and game list
game_count = str(user_games.get("game_count"))
user_games_list: list = user_games.get("games")

# set desktop path
desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'OneDrive\\Desktop')

# DEBUG: print directory path
print("desktop:", desktop_path)


# function to convert data time to readable dates
def convert_time(time):
    date_time = time
    new_time = datetime.fromtimestamp(date_time)
    return new_time.date()


# function to convert and format byte sizes to KB and MB
def format_size(size):
    kb_format = format(size / 1024, ".2f")
    mb_format = format(float(kb_format) / 1024, ".2f")
    return kb_format + " KB / " + mb_format + " MB"


def print_file_list(dir_path, game_list):
    # get total number of files
    desktop_file_total = len(os.listdir(dir_path))
    # create dictionary of dictionaries (files + data)
    file_list, dir_list = get_file_data(dir_path)

    print("\n\n======= FILE LIST =======")
    print("=========================  \n")
    # for each name and attributes, print key with value

    print("\n     ======== DIRECTORIES ========  ")
    print("     =============================  \n")
    for n, a in dir_list.items():
        for i, j in a.items():
            print(f"{i} : {j}")
        print()

    print("\n     ======== FILES ========  ")
    print("     =======================  \n")
    for n, a in file_list.items():
        for i, j in a.items():
            print(f"{i} : {j}")
        print()

    # print desktop file total
    print("==== Number of Files:", desktop_file_total, "====")

    move_file_data(file_list, game_list)


def move_file_data(file_list, game_list):
    print("move_file_data Starting\n")
    for file in file_list:
        print(file)
        if 'JPG' in file:
            print("JPG FILE FOUND\n")
        # search steam API to see if there is a steam page for the file
        game_search = steam.apps.search_games(file[slice(-4)])
        # if the API response is NOT empty, then file is a game
        if game_search != {}:
            print("GAME FOUND!\n")

def get_file_data(dir_path):
    file_dict: dict = {}
    dir_dict: dict = {}
    # for each name(file) in directory
    for name in os.listdir(dir_path):
        name_path = Path(name)
        # get data for each iteration
        data = os.stat(name)
        # set attributes from data
        if os.path.isdir(name_path):
            attributes = {
                "Directory Name": name,
                "Creation Date": convert_time(data.st_ctime),
                "Modified Date": convert_time(data.st_mtime),
                "Last Accessed Data": convert_time(data.st_atime)
            }
            dir_dict[name] = attributes
        if os.path.isfile(name_path):
            attributes = {
                "File Name": name,
                "Extension": name_path.suffix,
                'Size (KB/MB)': format_size(data.st_size),
                "Creation Date": convert_time(data.st_ctime),
                "Modified Date": convert_time(data.st_mtime),
                "Last Accessed Data": convert_time(data.st_atime)
            }
            file_dict[name] = attributes

    # return file dictionary (attributes)
    return file_dict, dir_dict


# get list of game names that is owned by SteamID, sort list alphabetically
def print_steam_owned_games(count, games_list):
    print("\n\nGame Count: " + count)
    print("Games: ")
    game_name_list = []
    for game in games_list:
        # print("\n")
        name = game.get('name')
        game_name_list.append(name)
        for item in game:
            pass
            # print(item + ":", game.get(item))
    game_name_list.sort()
    for name in game_name_list:
        print("name: ", name)




# change os directory to desktop
os.chdir(desktop_path)

# print list of games owned by steam profile
print_steam_owned_games(game_count, user_games_list)

# print file list with data
print_file_list(desktop_path, user_games_list)




