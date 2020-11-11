import os

import download
import settings
import utils


def create_profileicon_json(lang, path):
    cdragon_profileicons = download.download_versioned_cdragon_profileicons_summary()
    profileicon = {
        "type": "profileicon",
        "version": settings.patch['json'],
        "data": {}
    }
    for x in cdragon_profileicons:
        icon_id = x["id"]
        profileicon["data"][icon_id] = {
            "id": icon_id,
            "image": {
                "full": str(icon_id) + ".png"
            }
        }
    utils.save_json(profileicon, os.path.join(path, "profileicon.json"))
    return profileicon


def add_sprite_info(lang):
    """
    Adds Sprite Info to JSONs
    """
    data = utils.load_json(f"cdn/{settings.patch['json']}/spriter_output.json")

    profileicons = utils.load_json(
        f"cdn/{settings.patch['json']}/data/{lang}/profileicon.json")
    for profileicon in profileicons['data']:
        try:
            profileicons['data'][profileicon]['image'].update({
                'sprite': data['result']['profileicon'][profileicon]['regular']['texture'] + ".png",
                'group': "mission",
                'x': data['result']['profileicon'][profileicon]['regular']['x'],
                'y': data['result']['profileicon'][profileicon]['regular']['y'],
                'w': data['result']['profileicon'][profileicon]['regular']['width'],
                'h': data['result']['profileicon'][profileicon]['regular']['height'],
            })
        except KeyError:
            print("Failed to add sprite of profileicon: " + profileicon)
    utils.save_json(
        missions, f"cdn/{settings.patch['json']}/data/{lang}/profileicon.json")
