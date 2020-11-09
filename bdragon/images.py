import os
import platform
import shutil
from PIL import Image

import constants
import download
import item
import settings
import utils
import version


unv_path = ""
ver_path = ""


def create_all_images(championfull, items, summoners, path):
    global unv_path
    global ver_path
    unv_path = os.path.join(path, f"{settings.patch['json']}/images")
    ver_path = os.path.join(path, f"{settings.patch['json']}/img")
    # Unversioned Images (/cdn/img)
    create_unversioned_champion_splash(championfull)
    create_unversioned_champion_loading(championfull)
    create_unversioned_champion_tile(championfull)
    create_unversioned_perk_images()
    create_unversioned_perk_styles()

    # Versioned Images (/cdn/settings.patch/img)
    create_versioned_champion_icons()
    create_versioned_item_icons(items)
    create_versioned_map_icons()
    create_versioned_mission_assets()
    create_versioned_champion_passives()
    create_versioned_profile_icons()
    create_versioned_spell_icons(championfull, summoners)
    if platform.system() == "Windows":
        os.system(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                               "dragonspriter.exe") + " " + os.path.join(path, settings.patch['json']))
    else:
        os.system(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                               "dragonspriter") + " " + os.path.join(path, settings.patch['json']))

    if os.path.exists(os.path.join(ver_path, "sprite")):
        shutil.rmtree(os.path.join(ver_path, "sprite"))
    os.makedirs(os.path.join(ver_path, "sprite"))

    file_names = os.listdir(os.path.join(path, "../img/sprite/"))
    for file_name in file_names:
        shutil.move(os.path.join(os.path.join(path, "../img/sprite/"),
                                 file_name), os.path.join(ver_path, "sprite"))

    shutil.rmtree(os.path.join(path, "../img"), ignore_errors=True)


def create_unversioned_champion_splash(championfull):
    if not os.path.exists(os.path.join(unv_path, "champion/splash")):
        os.makedirs(os.path.join(unv_path, "champion/splash"))
    for champion in championfull['data']:
        print(champion)
        champion_key = championfull['data'][champion]['key']

        for i, skin in enumerate(championfull['data'][champion]['skins']):
            print(i)
            image = download.download_versioned_cdragon_champion_splash(
                champion_key, skin['id'])
            print(
                f"{champion}_{championfull['data'][champion]['skins'][i]['num']}"
            )
            with open(os.path.join(unv_path, f"champion/splash/{champion}_{championfull['data'][champion]['skins'][i]['num']}.jpg"), "wb") as f:
                f.write(image)
    return


def create_unversioned_champion_loading(championfull):
    if not os.path.exists(os.path.join(unv_path, "champion/loading")):
        os.makedirs(os.path.join(unv_path, "champion/loading"))
    for champion in championfull['data']:
        champion_key = championfull['data'][champion]['key']
        cdragon_champion = download.download_versioned_cdragon_champion("default",
                                                                        champion_key)
        for i in range(len(cdragon_champion['skins'])):
            url = get_cdragon_url(
                cdragon_champion['skins'][i]['loadScreenPath'])

            image = utils.download_image(url)
            print(
                f"{champion}_{championfull['data'][champion]['skins'][i]['num']}"
            )
            with open(os.path.join(unv_path, f"champion/loading/{champion}_{championfull['data'][champion]['skins'][i]['num']}.jpg"), "wb") as f:
                f.write(image)
    return


def create_unversioned_champion_tile(championfull):
    if not os.path.exists(os.path.join(unv_path, "champion/tiles")):
        os.makedirs(os.path.join(unv_path, "champion/tiles"))
    for champion in championfull['data']:
        champion_key = championfull['data'][champion]['key']
        cdragon_champion = download.download_versioned_cdragon_champion("default",
                                                                        champion_key)
        for i in range(len(cdragon_champion['skins'])):
            url = get_cdragon_url(cdragon_champion['skins'][i]['tilePath'])

            image = download.download_image(url)
            print(
                f"{champion}_{championfull['data'][champion]['skins'][i]['num']}"
            )
            with open(os.path.join(unv_path, f"champion/tiles/{champion}_{championfull['data'][champion]['skins'][i]['num']}.jpg"), "wb") as f:
                f.write(image)
    return


def create_unversioned_perk_images():
    if not os.path.exists(os.path.join(unv_path, "perk-images/Styles")):
        os.makedirs(os.path.join(unv_path, "perk-images/Styles"))
    cdragon_styles = download.download_versioned_cdragon_perkstyles("default")
    for x in cdragon_styles['styles']:
        url = get_cdragon_url(x['iconPath'])
        image = utils.download_image(url)
        name = get_image_name_from_path(x['iconPath'])
        path = get_path_from_string(x['iconPath'])[1:]
        with open(os.path.join(unv_path, f"{path}/{name}"), "wb") as f:
            f.write(image)
    return


def create_unversioned_perk_styles():
    cdragon_perks = download.download_versioned_cdragon_perks("default")
    for x in cdragon_perks:
        url = get_cdragon_url(x['iconPath'])
        image = utils.download_image(url)
        path = get_path_from_string(x['iconPath'])[1:]
        if not os.path.exists(os.path.join(unv_path, path)):
            os.makedirs(os.path.join(unv_path, path))
        name = get_image_name_from_path(x['iconPath'])
        with open(os.path.join(unv_path, f"{path}/{name}"), "wb") as f:
            f.write(image)
    return


def create_versioned_champion_icons():
    if not os.path.exists(os.path.join(ver_path, "champion")):
        os.makedirs(os.path.join(ver_path, "champion"))
    cdragon_champions = download.download_versioned_cdragon_champion_summary()
    for x in cdragon_champions:
        image = download.download_versioned_cdragon_champion_icon(x['id'])
        with open(os.path.join(ver_path, f"champion/{x['alias']}.png"), "wb") as f:
            f.write(image)
    return


def create_versioned_item_icons(items):
    if not os.path.exists(os.path.join(ver_path, "item")):
        os.makedirs(os.path.join(ver_path, "item"))
    cdragon_items_bin = download.download_versioned_cdragon_items_bin()
    for x in items['data']:
        print(x)
        item_bin = item.get_item_bin(x, cdragon_items_bin)
        if int(x) == 4633:
            print(item_bin)
        image = download.download_versioned_cdragon_item_icon(
            item_bin['mItemDataClient']['inventoryIcon'])
        with open(os.path.join(ver_path, f"item/{x}.png"), "wb") as f:
            f.write(image)
    return


def create_versioned_map_icons():
    if not os.path.exists(os.path.join(ver_path, "map")):
        os.makedirs(os.path.join(ver_path, "map"))
    cdragon_maps = download.download_versioned_cdragon_map_summary("default")
    for x in cdragon_maps:
        image = download.download_versioned_cdragon_map_icon(x['id'])
        with open(os.path.join(ver_path, f"map/map{x['id']}.png"), "wb") as f:
            f.write(image)
    return


def create_versioned_mission_assets():
    if not os.path.exists(os.path.join(ver_path, "mission")):
        os.makedirs(os.path.join(ver_path, "mission"))
    cdragon_missions = download.download_versioned_cdragon_mission_assets(
        "default")
    for x in cdragon_missions:
        image = download.download_versioned_cdragon_mission_icon(
            get_cdragon_url(x['path']))
        if not os.path.exists(os.path.join(ver_path, f"mission{get_path_from_string(x['path'])}")):
            os.makedirs(os.path.join(
                ver_path, f"mission{get_path_from_string(x['path'])}"))
        with open(os.path.join(ver_path, f"mission{get_path_from_string(x['path'])}/{get_image_name_from_path(x['path'])}"), "wb") as f:
            f.write(image)
    return


def create_versioned_champion_passives():
    if not os.path.exists(os.path.join(ver_path, "passive")):
        os.makedirs(os.path.join(ver_path, "passive"))
    cdragon_champions = download.download_versioned_cdragon_champion_summary()
    for champion in cdragon_champions:
        cdragon_champion = download.download_versioned_cdragon_champion(
            "default", champion['id'])
        url = get_cdragon_url(cdragon_champion['passive']['abilityIconPath'])
        image = download.download_image(url)
        with open(os.path.join(ver_path, f"passive/{get_image_name_from_path(cdragon_champion['passive']['abilityIconPath'])}"), "wb") as f:
            f.write(image)
    return


def create_versioned_profile_icons():
    if not os.path.exists(os.path.join(ver_path, "profileicon")):
        os.makedirs(os.path.join(ver_path, "profileicon"))
    cdragon_profileicons = download.download_versioned_cdragon_profileicons_summary()
    for x in cdragon_profileicons:
        image = download.download_versioned_cdragon_profile_icon(x['id'])
        with open(os.path.join(ver_path, f"profileicon/{x['id']}.jpg"), "wb") as f:
            f.write(image)
        # This conversion process is really long for bulk images.. Potential for improvement
        im = Image.open(os.path.join(ver_path, f"profileicon/{x['id']}.jpg"))
        im.save(os.path.join(ver_path, f"profileicon/{x['id']}.png"))
        os.remove(os.path.join(ver_path, f"profileicon/{x['id']}.jpg"))
    return


def create_versioned_spell_icons(championfull, summoners):
    if not os.path.exists(os.path.join(ver_path, "spell")):
        os.makedirs(os.path.join(ver_path, "spell"))
    # Champion Spells
    champion_summary = download.download_versioned_cdragon_champion_summary()
    for x in champion_summary:
        champion = download.download_versioned_cdragon_champion(
            "default", x['id'])
        for i, spell in enumerate(champion['spells']):
            image = download.download_image(
                get_cdragon_url(spell['abilityIconPath']))
            name = championfull['data'][x['alias']]['spells'][i]['id']
            with open(os.path.join(ver_path, f"spell/{name}.png"), "wb") as f:
                f.write(image)
    # Summoner Spells
    cdragon_summoners = download.download_versioned_cdragon_summoner_spells(
        "default")
    for summoner, value in summoners['data'].items():
        for x in cdragon_summoners:
            if str(x['id']) == value['key']:
                url = get_cdragon_url(x['iconPath'])
                image = download.download_image(url)
                with open(os.path.join(ver_path, f"spell/{summoner}.png"), "wb") as f:
                    f.write(image)

    return


def get_cdragon_url(path):
    path = path.lower()
    path = path.replace("/lol-game-data/assets/",
                        constants.cdragon_url + f"/{settings.patch['cdragon']}/plugins/rcp-be-lol-game-data/global/default/")
    print(path)
    return path


def get_cdragon_url_game_data(path):
    path = path.lower()
    path = path.replace("/lol-game-data/assets/",
                        constants.cdragon_url + f"/{settings.patch['cdragon']}/plugins/game/data/")
    print(path)
    return path


def get_image_name_from_path(path):
    path = path.split("/")
    return path[-1]


def get_path_from_string(path):
    # Need to perfect this function
    path = path.replace("/lol-game-data/assets", "")
    path = path.replace("/v1", "")
    path = path.replace("/ASSETS/Missions", "")
    path_list = path.split("/")
    path = path.replace("/"+path_list[-1], "")
    return path
