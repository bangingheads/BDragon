import os

import download
import settings
import utils


def create_map_json(lang, path):
    cdragon_maps = download.download_versioned_cdragon_map_summary(lang)
    maps = {
        "type": "map",
        "version": settings.patch['json'],
        "data": {},
    }
    for x in cdragon_maps:
        id = x["id"]
        maps["data"][id] = {
            "MapName": x['name'],
            "MapId": str(id),
            "image": {
                'full': "map" + str(id) + ".png",
            },
        }

    utils.save_json(maps, os.path.join(path, "map.json"))
    return maps


def add_sprite_info(lang, path):
    data = utils.load_json(os.path.join(path, "spriter_output.json"))
    maps = utils.load_json(os.path.join(path, f"data/{lang}/map.json"))
    for map in maps['data']:
        key = "map" + map
        try:
            maps['data'][map]['image'].update({
                'sprite': data['result']['map'][key]['regular']['texture'] + ".png",
                'group': "map",
                'x': data['result']['map'][key]['regular']['x'],
                'y': data['result']['map'][key]['regular']['y'],
                'w': data['result']['map'][key]['regular']['width'],
                'h': data['result']['map'][key]['regular']['height'],
            })
        except KeyError:
            print("Failed to add sprite of map: " + key)
    utils.save_json(maps, os.path.join(path, f"data/{lang}/map.json"))
