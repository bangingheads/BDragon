import os

import download
import settings
import translate
import utils


def create_profileicon_json(lang, path):
    cdragon_profileicons = download.download_versioned_cdragon_profileicons_summary()
    profileicon = {
        "type": "profileicon",
        "version": settings.patch['json'],
        "data": {}
    }
    for x in cdragon_profileicons:
        if "iconPath" not in x:
            continue
        icon_id = x["id"]
        profileicon["data"][icon_id] = {
            "id": icon_id,
            "title": translate.t(lang, "summoner_icon_title_" + str(icon_id)),
            "description": translate.t(lang, "summoner_icon_description_" + str(icon_id)),
            "image": {
                "full": str(icon_id) + ".png"
            }
        }
    utils.save_json(profileicon, os.path.join(path, "profileicon.json"))
    return profileicon


def add_sprite_info(lang, path):
    """
    Adds Sprite Info to JSONs
    """
    data = utils.load_json(os.path.join(path, "spriter_output.json"))
    profileicons = utils.load_json(os.path.join(path, f"data/{lang}/profileicon.json"))
    for profileicon in profileicons['data']:
        try:
            profileicons['data'][profileicon]['image'].update({
                'sprite': data['result']['profileicon'][profileicon]['regular']['texture'] + ".png",
                'group': "profileicon",
                'x': data['result']['profileicon'][profileicon]['regular']['x'],
                'y': data['result']['profileicon'][profileicon]['regular']['y'],
                'w': data['result']['profileicon'][profileicon]['regular']['width'],
                'h': data['result']['profileicon'][profileicon]['regular']['height'],
            })
        except KeyError:
            print("Failed to add sprite of profileicon: " + profileicon)
    utils.save_json(profileicons, os.path.join(path, f"data/{lang}/profileicon.json"))
