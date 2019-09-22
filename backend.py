import json
import os
import time
import sys
import urllib.parse
import urllib.request

import user_config
from galaxy.api.consts import LocalGameState
from galaxy.api.types import LocalGame, GameTime
from galaxy.api.plugin import Plugin
from xml.dom import minidom
from xml.etree import ElementTree


def is_dolphin_running():
    tasklist = os.popen('tasklist').read().strip().split('\n')
    for i in range(len(tasklist)):
        if 'Dolphin.exe' in tasklist[i]:
            return True
    return False


def get_the_game_times():
    file = ElementTree.parse(os.path.expandvars(
        r'%LOCALAPPDATA%\GOG.com\Galaxy\plugins\installed\dolphin_gc_6804a766-c1fd-48cf-9a8b-8661a970a6cb\gametimes.xml'))
    game_times = {}
    games_xml = file.getroot()
    for game in games_xml.iter('game'):
        game_id = str(game.find('id').text)
        tt = game.find('time').text
        game_times[game_id] = [tt, time.time()]
    return game_times


class BackendClient:

    def __init__(self):
        self.paths = []
        self.results = []
        self.roms = []

    def get_games_db(self):
        database_records = self.parse_dbf()

        self.get_rom_names()

        for rom in self.roms:
            for record in database_records:
                if rom == record[1]:
                    self.results.append(
                        [record[0], record[1]]
                    )

        for x, y in zip(self.paths, self.results):
            x.extend(y)

        return self.paths

    def parse_dbf(self):
        file = ElementTree.parse(os.path.expandvars(
            r'%LOCALAPPDATA%\GOG.com\Galaxy\plugins\installed\dolphin_gc_6804a766-c1fd-48cf-9a8b-8661a970a6cb\games.xml'))
        games_xml = file.getroot()
        games = games_xml.findall('game')
        records = []
        serials = []
        names = []
        for game in games:
            game_id = game.find('id').text
            game_platform = game.find('type').text
            locale = game.find('locale')
            game_name = locale.find('title').text
            if game_platform == "GameCube":
                if game_name not in names:  # If the name isn't already in the list,
                    names.append(game_name)  # add it
                    serials.append(game_id)  # Add the serial

        for serial, name in zip(serials, names):
            records.append([serial, name])

        return records

    def get_rom_names(self):
        # Search through directory for Dolphin ROMs
        for root, dirs, files in os.walk(user_config.roms_path):
            for file in files:
                if file.lower().endswith(".iso") or file.lower().endswith(".ciso") or file.lower().endswith(
                        ".gcm") or file.lower().endswith(".gcz") or file.lower().endswith(".wbfs"):
                    self.paths.append([os.path.join(root, file)])
                    self.roms.append(
                        os.path.splitext(os.path.basename(file))[0])  # Split name of file from it's path/extension

    def get_state_changes(self, old_list, new_list):
        old_dict = {x.game_id: x.local_game_state for x in old_list}
        new_dict = {x.game_id: x.local_game_state for x in new_list}
        result = []
        # removed games
        result.extend(LocalGame(id, LocalGameState.None_) for id in old_dict.keys() - new_dict.keys())
        # added games
        result.extend(local_game for local_game in new_list if local_game.game_id in new_dict.keys() - old_dict.keys())
        # state changed
        result.extend(
            LocalGame(id, new_dict[id]) for id in new_dict.keys() & old_dict.keys() if new_dict[id] != old_dict[id])
        return result
