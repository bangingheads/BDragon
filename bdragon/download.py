import json

import champion
import constants
import settings
import utils


def download_versioned_cdragon_champion_summary():
    json = utils.download_json(
        constants.cdragon_url + f"/{settings.patch['cdragon']}/plugins/rcp-be-lol-game-data/global/default/v1/champion-summary.json")
    json = list(filter(lambda x: (x['id'] != -1), json))
    # for x in json:
    #     if x['alias'] == "FiddleSticks":
    #         x['alias'] = "Fiddlesticks"
    json.sort(key=champion.get_alias)
    return json


def download_versioned_cdragon_champion_summary_files():
    # Using this as an alternative for PBE files since champion summary missing new PBE champs
    json = utils.download_json(
        constants.cdragon_url + f"/json/{settings.patch['cdragon']}/plugins/rcp-be-lol-game-data/global/default/v1/champions/")
    json = list(filter(lambda x: (x['name'] != "-1.json"), json))

    for x in json:
        utils.download_json(
            constants.cdragon_url +
            f"/{settings.patch['cdragon']}/plugins/rcp-be-lol-game-data/global/default/v1/champions/{x['name']}"
        )


def download_versioned_cdragon_items_bin():
    json = utils.download_json(
        constants.cdragon_url + f"/{settings.patch['cdragon']}/game/global/items/items.bin.json")
    json = {k: v for k, v in json.items() if "itemID" in json[k]}
    return json


def download_versioned_ddragon_items(language):
    return utils.download_json(
        constants.ddragon_url + f"/cdn/{settings.patch['ddragon']}/data/{language}/item.json")


def download_versioned_cdragon_items(language):
    json = utils.download_json(
        constants.cdragon_url + f"/{settings.patch['cdragon']}/plugins/rcp-be-lol-game-data/global/{language}/v1/items.json")
    return json


def download_versioned_cdragon_perks(language):
    # returns CDragon Perks JSON
    return utils.download_json(constants.cdragon_url + f"/{settings.patch['cdragon']}/plugins/rcp-be-lol-game-data/global/{language}/v1/perks.json")


def download_versioned_cdragon_perkstyles(language):
    # returns CDragon Perkstyles JSON
    return utils.download_json(constants.cdragon_url + f"/{settings.patch['cdragon']}/plugins/rcp-be-lol-game-data/global/{language}/v1/perkstyles.json")


def download_versioned_cdragon_perks_bin():
    return utils.download_json(constants.cdragon_url + f"/{settings.patch['cdragon']}/game/global/perks/perks.bin.json")


def download_versioned_cdragon_champion_splash(champion_key, skin_id):
    # returns CDragon Champion Splash Image
    return utils.download_image(constants.cdragon_url + f"/{settings.patch['cdragon']}/plugins/rcp-be-lol-game-data/global/default/v1/champion-splashes/uncentered/{champion_key}/{skin_id}.jpg")


def download_versioned_cdragon_champion(language, champion_id):
    return utils.download_json(constants.cdragon_url + f"/{settings.patch['cdragon']}/plugins/rcp-be-lol-game-data/global/{language}/v1/champions/{champion_id}.json")


def download_versioned_cdragon_champion_icon(champion_id):
    return utils.download_image(constants.cdragon_url + f"/{settings.patch['cdragon']}/plugins/rcp-be-lol-game-data/global/default/v1/champion-icons/{champion_id}.png")


def download_versioned_cdragon_item_icon(item_id):
    item_id = item_id.lower().split("/")[-1].replace(".dds", ".png")
    # Season 11 items in different location
    if settings.patch['cdragon'] == "pbe" or settings.patch['cdragon'] > "10.22":
        return utils.download_image(constants.cdragon_url + f"/{settings.patch['cdragon']}/game/assets/items/icons2d/{item_id}")
    else:
        return utils.download_image(constants.cdragon_url + f"/{settings.patch['cdragon']}/game/data/items/icons2d/{item_id}")


def download_versioned_cdragon_map_summary(language):
    json = utils.download_json(
        constants.cdragon_url + f"/{settings.patch['cdragon']}/plugins/rcp-be-lol-game-data/global/{language}/v1/maps.json")
    return list(filter(lambda x: (x['id'] != 0), json))


def download_versioned_cdragon_map_icon(map_id):
    return utils.download_image(constants.cdragon_url + f"/{settings.patch['cdragon']}/game/levels/map{map_id}/info/2dlevelminimap.png")


def download_versioned_cdragon_mission_assets(language):
    json = utils.download_json(
        constants.cdragon_url + f"/{settings.patch['cdragon']}/plugins/rcp-be-lol-game-data/global/{language}/v1/mission-assets.json")
    return list(filter(lambda x: (".png" in x['path'] and "Loadouts" not in x['path']), json))


def download_versioned_cdragon_mission_icon(url):
    return utils.download_image(url)


def download_versioned_cdragon_profileicons_summary():
    return utils.download_json(constants.cdragon_url + f"/{settings.patch['cdragon']}/plugins/rcp-be-lol-game-data/global/default/v1/profile-icons.json")


def download_versioned_cdragon_profile_icon(id):
    return utils.download_image(constants.cdragon_url + f"/{settings.patch['cdragon']}/plugins/rcp-be-lol-game-data/global/default/v1/profile-icons/{id}.jpg")


def download_image(url):
    return utils.download_image(url)


def download_versioned_cdragon_champion_bin(champion):
    cdragon_bin = utils.download_json(
        constants.cdragon_url + f"/{settings.patch['cdragon']}/game/data/characters/{champion.lower()}/{champion.lower()}.bin.json")
    cdragon_hash = f"Characters/{champion.title()}/CharacterRecords/Root"
    if cdragon_hash in cdragon_bin:
        return cdragon_bin[cdragon_hash]
    for x in cdragon_bin:
        if 'baseHP' in cdragon_bin[x]:
            return cdragon_bin[x]
    return False


def download_versioned_cdragon_champion_bin_ability(champion, ability):
    cdragon_bin = utils.download_json(
        constants.cdragon_url + f"/{settings.patch['cdragon']}/game/data/characters/{champion.lower()}/{champion.lower()}.bin.json")
    for x in cdragon_bin:
        if "mScriptName" in cdragon_bin[x] and cdragon_bin[x]['mScriptName'] == ability:
            return cdragon_bin[x]
    return False


def download_versioned_cdragon_summoner_spells(language):
    return utils.download_json(constants.cdragon_url + f"/{settings.patch['cdragon']}/plugins/rcp-be-lol-game-data/global/{language}/v1/summoner-spells.json")


def download_versioned_ddragon_language(language):
    return utils.download_json(constants.ddragon_url + f"/cdn/{settings.patch['ddragon']}/data/{language}/language.json")


def download_versioned_ddragon_summoner_spells(language):
    return utils.download_json(constants.ddragon_url + f"/cdn/{settings.patch['ddragon']}/data/{language}/summoner.json")


def download_versioned_ddragon_championfull(language):
    return utils.download_json(constants.ddragon_url + f"/cdn/{settings.patch['ddragon']}/data/{language}/championFull.json")


def download_versioned_cdragon_recommended(recommended_string):
    return utils.download_json(constants.cdragon_url +
                               f"/{settings.patch['cdragon']}/plugins/rcp-be-lol-game-data/global/default/{recommended_string.lower()}")


def download_cdragon_rstfile(language):
    return utils.download_file(constants.cdragon_url + f"/{settings.patch['cdragon']}/game/data/menu/fontconfig_{language.lower()}.txt")
