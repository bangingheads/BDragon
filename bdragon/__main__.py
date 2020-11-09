import os
import shutil
import sys

import champion
import constants
import images
import item
import language
import maps
import mission
import profileicon
import runesreforged
import settings
import sticker
import summoner
import tarball
import translate
import utils
import version


directory = os.path.abspath(os.path.join(
    os.path.dirname(os.path.realpath(__file__)), ".."))

files = os.path.join(directory, "files")


def main():

    if settings.production == True:
        cache = os.path.join(directory, "__cache__")
        if os.path.exists(cache):
            shutil.rmtree(cache)
            os.mkdir(cache)

    # No new updated patch, die (Off for development)
    if os.path.exists(os.path.join(files, settings.patch['json'])) and settings.production == True and settings.patch['json'] != "pbe":
        sys.exit("No new patch exists")

    # Check if PBE patch matches
    if settings.patch['cdragon'] == "pbe" and settings.production == True:
        if os.path.exists(os.path.join(directory, "pbe.txt")):
            with open(os.path.join(directory, "pbe.txt"), "r") as file:
                pbe_patch_string = file.read()
            if pbe_patch_string == version.get_cdragon_pbe_version():
                sys.exit("No new pbe exists")

        with open(os.path.join(directory, "pbe.txt"), "w") as file:
            file.write(version.get_cdragon_pbe_version())

        if os.path.exists(os.path.join(files, "pbe")):
            shutil.rmtree(os.path.join(files, "pbe"))

    if not os.path.exists(os.path.join(files, settings.patch['json'])):
        os.makedirs(os.path.join(files, settings.patch['json']))
    for lang in constants.languages:
        path = os.path.join(files, f"{settings.patch['json']}/data/{lang}")
        if not os.path.exists(path):
            os.makedirs(path)

        championfull = champion.create_champion_jsons(
            constants.languages[lang], lang, path)
        items = item.create_item_json(constants.languages[lang], lang, path)
        maps.create_map_json(constants.languages[lang], path)
        mission.create_mission_json(constants.languages[lang], path)
        profileicon.create_profileicon_json(constants.languages[lang], path)
        runesreforged.create_runesreforged_json(
            constants.languages[lang], path)
        summoners = summoner.create_summoner_json(
            constants.languages[lang], lang, path)
        language.create_language_json(lang, path)
        sticker.create_sticker_json(path)

    images.create_all_images(championfull, items, summoners, files)
    path = os.path.join(files, settings.patch['json'])
    for lang in constants.languages:
        champion.add_sprite_info(lang, path)
        item.add_sprite_info(lang, path)
        summoner.add_sprite_info(lang, path)
        maps.add_sprite_info(lang, path)
        mission.add_sprite_info(lang, path)
        summoner.add_sprite_info(lang, path)

    os.remove(os.path.join(path, "spriter_output.json"))
    if settings.tarball:
        tarball.create_tarball(path)


if __name__ == "__main__":
    settings.init()
    main()
