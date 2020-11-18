import os
import sys

import champion
import download
import settings
import translate
import utils


def create_summoner_json(cdragon_language, ddragon_language, path):
    """
    Creates DDragon summoner.json
    """
    cdragon_summoners = download.download_versioned_cdragon_summoner_spells(
        cdragon_language)
    ddragon_summoners = download.download_versioned_ddragon_summoner_spells(
        ddragon_language)
    spells_bin = download.download_versioned_cdragon_shared_bin()

    summoners = {
        "type": "summoner",
        "version": settings.patch['json'],
        "data": {},
    }
    for x in spells_bin:
        spell_bin = spells_bin[x]['mSpell']
        name = translate.t(
            ddragon_language, spell_bin['mClientData']['mTooltipData']['mLocKeys']['keyName'])
        cdragon_summoner = [d for d in cdragon_summoners if d['name'] == name]
        if len(cdragon_summoner) == 0:
            continue
        else:
            cdragon_summoner = cdragon_summoner[0]
        try:
            summoners['data'].update({
                spells_bin[x]['mScriptName']: {
                    "id": spells_bin[x]['mScriptName'],
                    "name": translate.t(ddragon_language, spell_bin['mClientData']['mTooltipData']['mLocKeys']['keyName']),
                    "description": translate.t(ddragon_language, spell_bin['mClientData']['mTooltipData']['mLocKeys']['keySummary']),
                    "tooltip": champion.get_tooltip(translate.t(ddragon_language, spell_bin['mClientData']['mTooltipData']['mLocKeys']['keyTooltip'])),
                    "maxrank": 1,
                    "cooldown": [spell_bin['cooldownTime'][0]] if "cooldownTime" in spell_bin else [10],
                    "cooldownBurn": champion.remove_trailing_zeros(str(spell_bin['cooldownTime'][0])) if "cooldownTime" in spell_bin else ["10"],
                    "datavalues": {},
                    "effect": [],
                    "effectBurn": [],
                    "vars": [],  # Need f values somehow on these
                    "key": str(cdragon_summoner['id']),
                    "summonerLevel": cdragon_summoner['summonerLevel'],
                    "modes": cdragon_summoner['gameModes'],
                    "costType": translate.t(ddragon_language, "Spell_Cost_NoCost"),
                    "maxammo": champion.remove_trailing_zeros(str(spell_bin['mMaxAmmo'][0])) if "mMaxAmmo" in spell_bin else "-1",
                    "range": [spell_bin['castRangeDisplayOverride'][0] if "castRangeDisplayOverride" in spell_bin else spell_bin['castRange'][0]],
                    "rangeBurn": champion.remove_trailing_zeros(str(spell_bin['castRangeDisplayOverride'][0] if "castRangeDisplayOverride" in spell_bin else spell_bin['castRange'][0])),
                    "image": {
                        "full": spells_bin[x]['mScriptName'] + ".png"
                    },
                    "resource": translate.t(ddragon_language, "Spell_Cost_NoCost"),
                }
            })
            spell = summoners['data'][spells_bin[x]['mScriptName']]
            if "mDataValues" in spell_bin:
                for i in spell_bin['mDataValues']:
                    if "mValues" in i:
                        values = [round(i['mValues'][0], 3)]
                        spell['datavalues'].update({
                            i['mName'].lower(): values,
                        })
            spell['effect'].append(None)
            spell['effectBurn'].append(None)
            if "mEffectAmount" in spell_bin:
                for i in spell_bin['mEffectAmount']:
                    if "value" in i:
                        spell['effect'].append([round(i['value'][0], 3)])
                        spell['effectBurn'].append(
                            champion.remove_trailing_zeros(str(round(i['value'][0], 3))))
                    else:
                        spell['effect'].append([0])
                        spell['effectBurn'].append("0")
            else:
                for i in range(10):
                    spell['effect'].append([0])
                    spell['effectBurn'].append("")
            if spell['maxammo'] != "-1" and "mMaxAmmo" in spell_bin:
                spell['ammorechargetime'] = spell_bin['mAmmoRechargeTime'][0]
            spell['vars'] = ddragon_summoners['data'][spell['id']]['vars']
        except Exception as ex:
            print("Failure on Summoner Spell: " + spells_bin[x]['mScriptName'])
            print(ex)
            continue
    summoners['data'] = {k: summoners['data'][k]
                         for k in sorted(summoners['data'])}
    utils.save_json(summoners, os.path.join(path, "summoner.json"))
    return summoners


def get_ddragon_id(cdragon_id, ddragon_summoners):
    """
    Gets summoner spell from DDragon from CDragon numeric ID
    """
    for x in ddragon_summoners['data']:
        if ddragon_summoners['data'][x]['key'] == str(cdragon_id):
            return ddragon_summoners['data'][x]
    return {}


def add_sprite_info(lang, path):
    """
    Adds Sprite Info to JSONs
    """
    data = utils.load_json(os.path.join(path, "spriter_output.json"))
    summoners = utils.load_json(os.path.join(
        path, f"data/{lang}/summoner.json"))
    for key, _ in summoners['data'].items():
        try:
            summoners['data'][key]['image'].update({
                'sprite': data['result']['spell'][key]['regular']['texture'] + ".png",
                'group': "spell",
                'x': data['result']['spell'][key]['regular']['x'],
                'y': data['result']['spell'][key]['regular']['y'],
                'w': data['result']['spell'][key]['regular']['width'],
                'h': data['result']['spell'][key]['regular']['height'],
            })
        except KeyError:
            print("Failed to add sprite of summoner: " + key)
    utils.save_json(summoners, os.path.join(
        path, f"data/{lang}/summoner.json"))
    return
