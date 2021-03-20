import os

import download
import utils


def create_runesreforged_json(lang, path):
    cdragon_runes = download.download_versioned_cdragon_perks(lang)
    cdragon_perkstyles = download.download_versioned_cdragon_perkstyles(lang)
    cdragon_perks_bin = download.download_versioned_cdragon_perks_bin()

    y = 0
    perks = []
    for x in cdragon_perkstyles["styles"]:
        new_perk = {
            "id": x["id"],
            "key": x["name"],
            "icon": get_perk_path(x["iconPath"]),
            "name": x["name"],
            "slots": [],
        }
        for slot in x["slots"]:
            if slot["type"] == "kStatMod":
                continue
            runes = []
            for perk in slot["perks"]:
                perk_info = get_perk_info(perk, cdragon_runes)
                perk_bin = get_perk_bin(perk, cdragon_perks_bin)
                runes.append(
                    {
                        "id": perk,
                        "key": perk_bin["mPerkName"],
                        "icon": get_perk_path(perk_info["iconPath"]),
                        "name": perk_info["name"],
                        "shortDesc": perk_info["shortDesc"],
                        "longDesc": perk_info["longDesc"],
                    }
                )
            new_perk["slots"].append({"runes": runes})
        perks.append(new_perk)

    stat_mods = [
        x for x in cdragon_perkstyles["styles"][0]["slots"] if x["type"] == "kStatMod"
    ]
    new_tree = {
        "id": 5000,
        "key": "StatMods",
        "icon": None,
        "name": "StatMods",
        "slots": [],
    }
    for tree in stat_mods:
        runes = []
        for perk in tree["perks"]:
            perk_info = get_perk_info(perk, cdragon_runes)
            perk_bin = get_perk_bin(perk, cdragon_perks_bin)
            runes.append(
                {
                    "id": perk,
                    "key": perk_bin["mPerkName"],
                    "icon": get_perk_path(perk_info["iconPath"]),
                    "name": perk_info["name"],
                    "shortDesc": perk_info["shortDesc"],
                    "longDesc": perk_info["longDesc"],
                }
            )
        new_tree["slots"].append({"runes": runes})
    perks.append(new_tree)

    utils.save_json(perks, os.path.join(path, "runesReforged.json"))
    return perks


def get_perk_info(id, cdragon_runes):
    for x in cdragon_runes:
        if x["id"] == id:
            return x


def get_perk_bin(id, cdragon_perks_bin):
    for x in cdragon_perks_bin:
        if "mPerkId" in cdragon_perks_bin[x]:
            if cdragon_perks_bin[x]["mPerkId"] == id:
                return cdragon_perks_bin[x]
    return {}


def get_perk_path(perk_string):
    return perk_string.replace("/lol-game-data/assets/v1/", "")
