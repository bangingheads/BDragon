import os

import settings
import download
import utils


def create_mission_json(lang, path):
    cdragon_missions = download.download_versioned_cdragon_mission_assets(lang)
    missions = {
        "type": "mission",
        "version": settings.patch['json'],
        "data": {},
    }
    for x in cdragon_missions:
        mission_id = get_path_from_string(
            x['path'])
        missions["data"][mission_id] = {
            "id": 0,
            "image": {
                "full": mission_id + ".png",
            }
        }
    utils.save_json(missions, os.path.join(path, "mission-assets.json"))
    return missions


def get_id_from_path(path):
    path = path.split("/")[-1]
    x = path.replace(".png", "")
    return x


def get_path_from_string(path):
    path = path.replace("/lol-game-data/assets/ASSETS/Missions/", "")
    path = path.replace(".png", "")
    return path


def add_sprite_info(lang, path):
    """
    Adds Sprite Info to JSONs
    """
    data = utils.load_json(os.path.join(path, "spriter_output.json"))

    missions = utils.load_json(os.path.join(
        path, f"data/{lang}/mission-assets.json"))
    for mission in missions['data']:
        try:
            mission_name = mission.split("/")[-1]
            missions['data'][mission]['image'].update({
                'sprite': data['result']['mission'][mission_name]['regular']['texture'] + ".png",
                'group': "mission",
                'x': data['result']['mission'][mission_name]['regular']['x'],
                'y': data['result']['mission'][mission_name]['regular']['y'],
                'w': data['result']['mission'][mission_name]['regular']['width'],
                'h': data['result']['mission'][mission_name]['regular']['height'],
            })
        except KeyError:
            print("Failed to add sprite of mission: " + mission_name)
    utils.save_json(missions, os.path.join(
        path, f"data/{lang}/mission-assets.json"))
