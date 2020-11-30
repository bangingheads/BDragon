import os
import re

import download
import utils
import settings
import translate


def create_champion_jsons(cdragon_language, ddragon_language, path):
    create_champion_json(cdragon_language, ddragon_language)
    championfull = create_championfull_json(cdragon_language, ddragon_language)
    create_individual_champion_json(
        cdragon_language, ddragon_language, championfull)
    return championfull


def create_champion_json(cdragon_language, ddragon_language):
    cdragon_champions = download.download_versioned_cdragon_champion_summary()
    champions = {
        'type': 'champion',
        'format': 'standAloneComplex',
        'version': settings.patch['json'],
    }
    champions["data"] = {}
    for champion in cdragon_champions:
        champions['data'][champion['alias']] = {
            "version": settings.patch['json'],
            'id': champion['alias'],
            'key': str(champion['id']),
        }

    for champion in champions["data"]:
        cdragon_champion = download.download_versioned_cdragon_champion(
            cdragon_language, champions['data'][champion]['key'])
        cdragon_bin = download.download_versioned_cdragon_champion_bin(
            champion)
        champions['data'][champion].update({
            'name': cdragon_champion['name'] if "name" in cdragon_champion else "",
            'title': cdragon_champion['title'] if "title" in cdragon_champion else "",
            'blurb': blurb(cdragon_champion['shortBio']),
            'info': {
                'attack': cdragon_bin['characterToolData']['attackRank'] if "attackRank" in cdragon_bin['characterToolData'] else 0,
                'defense': cdragon_bin['characterToolData']['defenseRank'] if "defenseRank" in cdragon_bin['characterToolData'] else 0,
                'magic': cdragon_bin['characterToolData']['magicRank'] if "magicRank" in cdragon_bin['characterToolData'] else 0,
                'difficulty': cdragon_bin['characterToolData']['difficultyRank'] if "difficultyRank" in cdragon_bin['characterToolData'] else 0,
            },
            'image': {
                'full': cdragon_champion['alias'] + '.png'
            },
            'tags': list(map(lambda x: x.title(), cdragon_champion['roles'])),
            'partype': "",
            'stats': {
                'hp': round(cdragon_bin['baseHP'], 3) if "baseHP" in cdragon_bin else 0,
                'hpperlevel': round(cdragon_bin['hpPerLevel'], 3) if "hpPerLevel" in cdragon_bin else 0,
                'mp': round(cdragon_bin['primaryAbilityResource']['arBase'], 3) if "arBase" in cdragon_bin['primaryAbilityResource'] else 0,
                'mpperlevel': round(cdragon_bin['primaryAbilityResource']['arPerLevel'], 3) if "arPerLevel" in cdragon_bin['primaryAbilityResource'] else 0,
                'movespeed': cdragon_bin['baseMoveSpeed'] if "baseMoveSpeed" in cdragon_bin else 0,
                'armor': round(cdragon_bin['baseArmor'], 3) if "baseArmor" in cdragon_bin else 0,
                'armorperlevel': round(cdragon_bin['armorPerLevel'], 3) if "armorPerLevel" in cdragon_bin else 0,
                'spellblock': round(cdragon_bin['baseSpellBlock'], 3) if "baseSpellBlock" in cdragon_bin else 0,
                'spellblockperlevel': round(cdragon_bin['spellBlockPerLevel'], 3) if "spellBlockPerLevel" in cdragon_bin else 0,
                'attackrange': round(cdragon_bin['attackRange'], 3) if "attackRange" in cdragon_bin else 0,
                'hpregen': round(cdragon_bin['baseStaticHPRegen'] * 5, 3) if "baseStaticHPRegen" in cdragon_bin else 0,
                'hpregenperlevel': round(cdragon_bin['hpRegenPerLevel'] * 5, 3) if "hpRegenPerLevel" in cdragon_bin else 0,
                'mpregen': round(cdragon_bin['primaryAbilityResource']['arBaseStaticRegen'] * 5, 3) if "arBaseStaticRegen" in cdragon_bin['primaryAbilityResource'] else 0,
                'mpregenperlevel': round(cdragon_bin['primaryAbilityResource']['arRegenPerLevel'] * 5, 3) if "arRegenPerLevel" in cdragon_bin['primaryAbilityResource'] else 0,
                'crit': 0,
                'critperlevel': 0,
                'critdamage': round(cdragon_bin['critDamageMultiplier'], 3) if "critDamageMultiplier" in cdragon_bin else 1.75,
                'attackdamage': round(cdragon_bin['baseDamage'], 3) if "baseDamage" in cdragon_bin else 0,
                'attackdamageperlevel': round(cdragon_bin['damagePerLevel'], 3) if "damagePerLevel" in cdragon_bin else 0,
                'attackspeedperlevel': round(cdragon_bin['attackSpeedPerLevel'], 3) if "attackSpeedPerLevel" in cdragon_bin else 0,
                'attackspeed': round(cdragon_bin['attackSpeed'], 3) if "attackSpeed" in cdragon_bin else 0,
                'attackspeedratio': round(cdragon_bin['attackSpeedRatio'], 3) if "attackSpeedRatio" in cdragon_bin else 0,
            },
        })
        # Need to be able to find the game_ability_resource strings from CDragon
        try:
            champions['data'][champion]['partype'] = ddragon_champions['data'][champion]['partype']
        except Exception:
            champions['data'][champion]['partype'] = get_partype(
                cdragon_bin, ddragon_language).title()
    utils.save_json(
        champions, os.path.join(
            settings.files, f"{settings.patch['json']}/data/{ddragon_language}/champion.json"))
    return champions


def create_championfull_json(cdragon_language, ddragon_language, capitalization=False):
    cdragon_champions = download.download_versioned_cdragon_champion_summary()
    ddragon_champions = download.download_versioned_ddragon_championfull(
        ddragon_language)
    champions = {
        'type': 'champion',
        'format': 'full',
        'version': settings.patch['json'],
        "data": {},
        "keys": {},
    }
    champions["data"] = {}
    for champion in cdragon_champions:
        champions['data'][champion['alias']] = {
            'id': champion['alias'],
            'key': str(champion['id']),
        }
        champions['keys'][champion['id']] = champion['alias']

    for champion in champions["data"]:
        id = champions["data"][champion]["key"]
        cdragon_champion = download.download_versioned_cdragon_champion(
            cdragon_language, id)
        cdragon_bin = download.download_versioned_cdragon_champion_bin(
            champion)
        champions['data'][champion].update({
            'name': cdragon_champion['name'],
            'title': cdragon_champion['title'],
            'image': {
                'full': cdragon_champion['alias'] + '.png'
            },
            'skins': {
            },
            'lore': cdragon_champion['shortBio'],
            'blurb': blurb(cdragon_champion['shortBio']),
            "allytips": get_tip_list(ddragon_language, cdragon_bin['tips1']) if "tips1" in cdragon_bin else "",
            "enemytips": get_tip_list(ddragon_language, cdragon_bin['tips2']) if "tips2" in cdragon_bin else "",
            'tags': list(map(lambda x: x.title(), cdragon_champion['roles'])),
            'partype': "",
            'info': {
                'attack': cdragon_bin['characterToolData']['attackRank'] if "attackRank" in cdragon_bin['characterToolData'] else 0,
                'defense': cdragon_bin['characterToolData']['defenseRank'] if "defenseRank" in cdragon_bin['characterToolData'] else 0,
                'magic': cdragon_bin['characterToolData']['magicRank'] if "magicRank" in cdragon_bin['characterToolData'] else 0,
                'difficulty': cdragon_bin['characterToolData']['difficultyRank'] if "difficultyRank" in cdragon_bin['characterToolData'] else 0,
            },
            'stats': {
                'hp': round(cdragon_bin['baseHP'], 3) if "baseHP" in cdragon_bin else 0,
                'hpperlevel': round(cdragon_bin['hpPerLevel'], 3) if "hpPerLevel" in cdragon_bin else 0,
                'mp': round(cdragon_bin['primaryAbilityResource']['arBase'], 3) if "arBase" in cdragon_bin['primaryAbilityResource'] else 0,
                'mpperlevel': round(cdragon_bin['primaryAbilityResource']['arPerLevel'], 3) if "arPerLevel" in cdragon_bin['primaryAbilityResource'] else 0,
                'movespeed': cdragon_bin['baseMoveSpeed'] if "baseMoveSpeed" in cdragon_bin else 0,
                'armor': round(cdragon_bin['baseArmor'], 3) if "baseArmor" in cdragon_bin else 0,
                'armorperlevel': round(cdragon_bin['armorPerLevel'], 3) if "armorPerLevel" in cdragon_bin else 0,
                'spellblock': round(cdragon_bin['baseSpellBlock'], 3) if "baseSpellBlock" in cdragon_bin else 0,
                'spellblockperlevel': round(cdragon_bin['spellBlockPerLevel'], 3) if "spellBlockPerLevel" in cdragon_bin else 0,
                'attackrange': round(cdragon_bin['attackRange'], 3) if "attackRange" in cdragon_bin else 0,
                'hpregen': round(cdragon_bin['baseStaticHPRegen'] * 5, 3) if "baseStaticHPRegen" in cdragon_bin else 0,
                'hpregenperlevel': round(cdragon_bin['hpRegenPerLevel'] * 5, 3) if "hpRegenPerLevel" in cdragon_bin else 0,
                'mpregen': round(cdragon_bin['primaryAbilityResource']['arBaseStaticRegen'] * 5, 3) if "arBaseStaticRegen" in cdragon_bin['primaryAbilityResource'] else 0,
                'mpregenperlevel': round(cdragon_bin['primaryAbilityResource']['arRegenPerLevel'] * 5, 3) if "arRegenPerLevel" in cdragon_bin['primaryAbilityResource'] else 0,
                'crit': 0,
                'critperlevel': 0,
                'critdamage': round(cdragon_bin['critDamageMultiplier'], 3) if "critDamageMultiplier" in cdragon_bin else 1.75,
                'attackdamage': round(cdragon_bin['baseDamage'], 3) if "baseDamage" in cdragon_bin else 0,
                'attackdamageperlevel': round(cdragon_bin['damagePerLevel'], 3) if "damagePerLevel" in cdragon_bin else 0,
                'attackspeedperlevel': round(cdragon_bin['attackSpeedPerLevel'], 3) if "attackSpeedPerLevel" in cdragon_bin else 0,
                'attackspeed': round(cdragon_bin['attackSpeed'], 3) if "attackSpeed" in cdragon_bin else 0,
                'attackspeedratio': round(cdragon_bin['attackSpeedRatio'], 3) if "attackSpeedRatio" in cdragon_bin else 0,
            },
            'spells': [],
            'passive': {},
            'recommended': [],
        })
        champions['data'][champion]['skins'] = []
        for y, i in enumerate(cdragon_champion["skins"]):
            skin_num = get_skin_num(id, cdragon_champion["skins"][y]['id'])
            skin = {
                'id': str(cdragon_champion["skins"][y]['id']),
                'num': skin_num,
                'name': cdragon_champion["skins"][y]['name'] if cdragon_champion["skins"][y]['isBase'] != True else "default",
                'chromas': True if "chromaPath" in cdragon_champion["skins"][y] and cdragon_champion["skins"][y]['chromaPath'] is not None else False,
            }
            champions['data'][champion]['skins'].append(skin)

        y = 0
        for x in cdragon_champion['spells']:
            cdragon_champion['spells'][y] = process_spell_variables(
                cdragon_champion['spells'][y])
            spell = {
                'id': cdragon_bin['spellNames'][y].split("/")[-1],
            }
            cdragon_ability_bin = download.download_versioned_cdragon_champion_bin_ability(
                champion, spell['id'])
            spell.update({
                'name': cdragon_champion['spells'][y]['name'],
                'description': cdragon_champion['spells'][y]['description'],
                'tooltip': "",
                'leveltip': {
                    'label': [],
                    "effect": [],
                },
            })
            if "mClientData" in cdragon_ability_bin['mSpell'] and "mTooltipData" in cdragon_ability_bin['mSpell']['mClientData'] and "mLocKeys" in cdragon_ability_bin['mSpell']['mClientData']['mTooltipData']:
                if "keyTooltipExtendedBelowLine" in cdragon_ability_bin['mSpell']['mClientData']['mTooltipData']['mLocKeys']:
                    spell['tooltip'] = get_tooltip(ddragon_language, translate.t(ddragon_language, cdragon_ability_bin['mSpell']['mClientData']['mTooltipData']['mLocKeys']['keyTooltip']) +
                                                   " " + translate.t(ddragon_language, cdragon_ability_bin['mSpell']['mClientData']['mTooltipData']['mLocKeys']['keyTooltipExtendedBelowLine']))
                else:
                    if "keyTooltip" in cdragon_ability_bin['mSpell']['mClientData']['mTooltipData']['mLocKeys']:
                        spell['tooltip'] = get_tooltip(ddragon_language, translate.t(
                            ddragon_language, cdragon_ability_bin['mSpell']['mClientData']['mTooltipData']['mLocKeys']['keyTooltip']))
            try:
                spell['maxrank'] = cdragon_ability_bin['mSpell']['mClientData']['mTooltipData']['mLists']['LevelUp']['levelCount']
            except KeyError:
                spell['maxrank'] = 6  # Aphelios
            spell['cooldown'] = []
            spell['cooldownBurn'] = ""
            for i in range(spell['maxrank']):
                spell['cooldown'].append(
                    cdragon_champion['spells'][y]['cooldownCoefficients'][i])
                spell['cooldownBurn'] = spell['cooldownBurn'] + remove_trailing_zeros(
                    cdragon_champion['spells'][y]['cooldownCoefficients'][i]) + "/"
            spell['cooldownBurn'] = get_burn_string(spell['cooldownBurn'])
            spell['cost'] = []
            spell['costBurn'] = ""
            for i in range(spell['maxrank']):
                spell['cost'].append(
                    cdragon_champion['spells'][y]['costCoefficients'][i])
                spell['costBurn'] = spell['costBurn'] + \
                    remove_trailing_zeros(
                        cdragon_champion['spells'][y]['costCoefficients'][i]) + "/"
            spell['costBurn'] = get_burn_string(spell['costBurn'])
            spell['datavalues'] = {}
            if "mDataValues" in cdragon_ability_bin['mSpell']:
                for i in cdragon_ability_bin['mSpell']['mDataValues']:
                    if "mValues" in i:
                        values = []
                        for m in range(spell['maxrank']):
                            value = i['mValues'][m]
                            if "mFormula" in i:
                                try:
                                    value = round(eval(i['mFormula'].replace(
                                        "P", str(value)).replace("N", str(m))), 3)
                                except Exception:
                                    value = round(eval(re.sub(
                                        r'\b0+(?!\b)', '', i['mFormula'].replace("P", str(value)).replace("N", str(m)))), 4)
                            else:
                                value = round(value, 4)
                            values.append(value)
                        spell['datavalues'].update({
                            i['mName'] if capitalization else i['mName'].lower(): values,
                        })
            if "{94572284}" in cdragon_ability_bin['mSpell']:
                spell['calculations'] = {}
                for i in cdragon_ability_bin['mSpell']['{94572284}']:
                    spell['calculations'].update({
                        translate.__getitem__(i).lower(): get_calculation(cdragon_ability_bin['mSpell']['{94572284}'][i])
                    })
            if "formulas" in cdragon_champion['spells'][y]:
                spell['formulas'] = {}
                for i in cdragon_champion['spells'][y]['formulas']:
                    if cdragon_champion['spells'][y]['formulas'][i]['link'] != "":
                        spell['formulas'].update(
                            {i: cdragon_champion['spells'][y]['formulas'][i]})
            spell['effect'] = []
            spell['effectBurn'] = []

            for i in range(11):
                if i == 0:
                    spell['effect'].append(None)
                    spell['effectBurn'].append(None)
                    continue
                spell['effectBurn'].append("")
                spell['effect'].append([])
                for j in range(spell['maxrank']):
                    spell['effect'][i].append(cdragon_champion[
                        'spells'][y]['effectAmounts'][f'Effect{i}Amount'][j+1])
                    spell['effectBurn'][i] = spell['effectBurn'][i] + remove_trailing_zeros(
                        cdragon_champion['spells'][y]['effectAmounts'][f'Effect{i}Amount'][j+1]) + "/"
                spell['effectBurn'][i] = get_burn_string(
                    spell['effectBurn'][i])
            spell['vars'] = []
            j = 0
            for i in cdragon_champion['spells'][y]['coefficients']:
                if cdragon_champion['spells'][y]['coefficients'][i] != 0:
                    spell_var = {}
                    spell_var['link'] = "spelldamage"
                    spell_var['coeff'] = cdragon_champion['spells'][y]['coefficients'][i]
                    if "a" + str(j + 1) in spell['tooltip']:
                        spell_var['key'] = "a" + str(j + 1)
                        spell['vars'].append(spell_var)
                    j += 1
            spell['costType'] = remove_html_tags(get_tooltip(ddragon_language,
                                                             cdragon_champion['spells'][y]['cost']))
            if "}}" in spell['costType']:
                spell['costType'] = spell['costType'].split("}}", 1)[1]
            spell['maxammo'] = str(cdragon_champion['spells'][y]['ammo']['maxAmmo'][0]
                                   ) if cdragon_champion['spells'][y]['ammo']['maxAmmo'][0] != 0 else "-1"
            spell['range'] = []
            spell['rangeBurn'] = ""
            for i in range(spell['maxrank']):
                spell['range'].append(
                    cdragon_champion['spells'][y]['range'][i])
                spell['rangeBurn'] = spell['rangeBurn'] + remove_trailing_zeros(
                    cdragon_champion['spells'][y]['range'][i]) + "/"
            spell['rangeBurn'] = get_burn_string(spell['rangeBurn'])
            spell['image'] = {}
            spell['image']['full'] = spell['id'] + ".png"
            champions['data'][champion]['spells'].append(spell)
            spell['resource'] = remove_html_tags(get_tooltip(ddragon_language,
                                                             cdragon_champion['spells'][y]['cost']))
            try:
                for desc in cdragon_ability_bin['mSpell']['mClientData']['mTooltipData']['mLists']['LevelUp']['elements']:
                    if "nameOverride" in desc:
                        if desc['nameOverride'] == "Spell_Cost_NoCost":
                            continue
                        elif desc['nameOverride'] == "Spell_ListType_Cost":
                            desc['nameOverride'] = "Spell_ListType_UnnamedCost"
                        spell['leveltip']['label'].append(
                            translate.t(ddragon_language, desc['nameOverride']))
                    else:
                        # Fix RST anomalies
                        if desc['type'] == "CastRange":
                            desc['type'] = "Range"
                        elif desc['type'] == "AmmoRechargeTime":
                            desc['type'] = "RechargeTime"
                        elif desc['type'] == "BasePhysicalDamagePerStack":
                            desc['type'] = "DamageperStack"
                        spell['leveltip']['label'].append(
                            translate.t(ddragon_language, "Spell_ListType_" + desc['type']))
                    percent = ""
                    if "Style" in desc and desc['Style'] == 1:
                        percent = "%"
                    multiplier = ""
                    newvalue = "NL"
                    if "multiplier" in desc:
                        multiplier = "*" + str(desc['multiplier']) + "00000"
                        newvalue = "nl"
                    if "Effect" in desc['type']:
                        effect = "e" + str(desc['typeIndex'])
                        spell['leveltip']['effect'].append(
                            f"{{{{ {effect}{multiplier} }}}}{percent} -> {{{{ {effect}{newvalue}{multiplier} }}}}")
                    else:
                        spell['leveltip']['effect'].append(
                            f"{{{{ {desc['type'].lower()}{multiplier} }}}}{percent} -> {{{{ {desc['type'].lower()}{newvalue}{multiplier} }}}}{percent}")
            except KeyError:
                print("No leveltip " + spell['id'])
            y += 1

        # Passive
        cdragon_passive_bin = download.download_versioned_cdragon_champion_bin_ability(
            champion, cdragon_bin['{e96f0412}'] if "{e96f0412}" in cdragon_bin else cdragon_bin['passiveSpell'])
        champions['data'][champion]['passive'].update({
            'id': cdragon_passive_bin['mScriptName'].split("/")[-1],
            'name': cdragon_champion['passive']['name'],
            'description': cdragon_champion['passive']['description'],
            'tooltip': get_tooltip(ddragon_language, translate.t(ddragon_language, cdragon_passive_bin['mSpell']['mClientData']['mTooltipData']['mLocKeys']['keyTooltip'])),
            'image': {
                'full': get_icon_name(cdragon_champion['passive']['abilityIconPath'])
            },
            'datavalues': {},
        })
        if "mDataValues" in cdragon_passive_bin['mSpell']:
            for i in cdragon_passive_bin['mSpell']['mDataValues']:
                if "mValues" in i:
                    values = []
                    for m in range(spell['maxrank']):
                        value = i['mValues'][m]
                        if "mFormula" in i:
                            try:
                                value = round(eval(i['mFormula'].replace(
                                    "P", str(value)).replace("N", str(m))), 3)
                            except Exception:
                                value = round(eval(re.sub(
                                    r'\b0+(?!\b)', '', i['mFormula'].replace("P", str(value)).replace("N", str(m)))), 3)
                        else:
                            value = round(value, 3)
                        values.append(value)
                    champions['data'][champion]['passive']['datavalues'].update({
                        i['mName'] if capitalization else i['mName'].lower(): values,
                    })
        if "{94572284}" in cdragon_passive_bin['mSpell']:
            champions['data'][champion]['passive']['calculations'] = {}
            for i in cdragon_passive_bin['mSpell']['{94572284}']:
                champions['data'][champion]['passive']['calculations'].update({
                    translate.__getitem__(i).lower(): get_calculation(cdragon_passive_bin['mSpell']['{94572284}'][i])
                })
        for x in cdragon_champion['recommendedItemDefaults']:
            champions['data'][champion]['recommended'].append(
                download.download_versioned_cdragon_recommended(x))
        try:
            champions['data'][champion]['partype'] = ddragon_champions['data'][champion]['partype']
        except Exception:
            champions['data'][champion]['partype'] = get_partype(
                cdragon_bin, ddragon_language).title()
            print("ddragon failed")

    utils.save_json(
        champions, os.path.join(
            settings.files, f"{settings.patch['json']}/data/{ddragon_language}/championFull.json"))
    return champions


def create_individual_champion_json(cdragon_language, ddragon_language, championfull):
    if not os.path.exists(os.path.join(
            settings.files, f"{settings.patch['json']}/data/{ddragon_language}/champion")):
        os.makedirs(os.path.join(
            settings.files, f"{settings.patch['json']}/data/{ddragon_language}/champion"))
    for x in championfull['data']:
        champion = {
            "type": "champion",
            "format": "standAloneComplex",
            "version": settings.patch['json'],
            "data": {
                x: championfull['data'][x],
            },
        }
        utils.save_json(
            champion, os.path.join(
                settings.files, f"{settings.patch['json']}/data/{ddragon_language}/champion/{x}.json"))


def add_sprite_info(lang, path):
    """Adds Sprite Info to JSONs"""
    data = utils.load_json(os.path.join(path, "spriter_output.json"))

    # champion.json
    champions = utils.load_json(os.path.join(
        path, f"data/{lang}/champion.json"))
    for champion in champions['data']:
        try:
            champions['data'][champion]['image'].update({
                'sprite': data['result']['champion'][champion]['regular']['texture'] + ".png",
                'group': "champion",
                'x': data['result']['champion'][champion]['regular']['x'],
                'y': data['result']['champion'][champion]['regular']['y'],
                'w': data['result']['champion'][champion]['regular']['width'],
                'h': data['result']['champion'][champion]['regular']['height'],
            })
        except KeyError:
            print("FAILED TO ADD CHAMPION SPRITE: " + champion)
    utils.save_json(champions, os.path.join(
        path, f"data/{lang}/champion.json"))

    # championFull.json
    championfull = utils.load_json(os.path.join(
        path, f"data/{lang}/championFull.json"))
    for champion in championfull['data']:
        championfull['data'][champion]['image'].update({
            'sprite': data['result']['champion'][champion]['regular']['texture'] + ".png",
            'group': "champion",
            'x': data['result']['champion'][champion]['regular']['x'],
            'y': data['result']['champion'][champion]['regular']['y'],
            'w': data['result']['champion'][champion]['regular']['width'],
            'h': data['result']['champion'][champion]['regular']['height'],
        })
        for spell in championfull['data'][champion]['spells']:
            spell_id = spell['id']
            spell['image'].update({
                'sprite': data['result']['spell'][spell_id]['regular']['texture'] + ".png",
                'group': "spell",
                'x': data['result']['spell'][spell_id]['regular']['x'],
                'y': data['result']['spell'][spell_id]['regular']['y'],
                'w': data['result']['spell'][spell_id]['regular']['width'],
                'h': data['result']['spell'][spell_id]['regular']['height'],
            })
        passive = championfull['data'][champion]['passive']['image']['full'].split(".png")[
            0]
        championfull['data'][champion]['passive']['image'].update({
            'sprite': data['result']['passive'][passive]['regular']['texture'] + ".png",
            'group': "passive",
            'x': data['result']['passive'][passive]['regular']['x'],
            'y': data['result']['passive'][passive]['regular']['y'],
            'w': data['result']['passive'][passive]['regular']['width'],
            'h': data['result']['passive'][passive]['regular']['height'],
        })
    utils.save_json(
        championfull, os.path.join(path, f"data/{lang}/championFull.json"))

    # Resave Individual Champion JSONs
    for x in championfull['data']:
        champion = {
            "type": "champion",
            "format": "standAloneComplex",
            "version": settings.patch['json'],
            "data": {
                x: championfull['data'][x],
            },
        }
        utils.save_json(
            champion, os.path.join(path, f"data/{lang}/champion/{x}.json"))
    return championfull


def get_alias(champion):
    return champion.get('alias')


def get_partype(cdragon_bin, ddragon_language):
    """
    Gets partype in the requested language.
    This is a backup to relying on ddragon, still not pretty, could use improvement
    """
    if 'arType' not in cdragon_bin['primaryAbilityResource']:
        return translate.t(ddragon_language, "game_ability_resource_None")
    elif cdragon_bin['primaryAbilityResource']['arType'] == 0:
        return translate.t(ddragon_language, "game_ability_resource_MP")
    elif cdragon_bin['primaryAbilityResource']['arType'] == 1:
        return translate.t(ddragon_language, "game_ability_resource_Energy")
    elif cdragon_bin['primaryAbilityResource']['arType'] == 3:
        return translate.t(ddragon_language, "game_ability_resource_Shield")
    elif cdragon_bin['primaryAbilityResource']['arType'] == 4 or cdragon_bin['primaryAbilityResource']['arType'] == 5 or cdragon_bin['primaryAbilityResource']['arType'] == 6:
        return translate.t(ddragon_language, "game_ability_resource_Dragonfury")
    elif cdragon_bin['primaryAbilityResource']['arType'] == 7:
        return translate.t(ddragon_language, "game_ability_resource_Heat")
    elif cdragon_bin['primaryAbilityResource']['arType'] == 8:
        if 'arIncrements' not in cdragon_bin['primaryAbilityResource']:
            return translate.t(ddragon_language, "game_ability_resource_Gnarfury")
        elif cdragon_bin['primaryAbilityResource']['arIncrements'] == 0:
            return translate.t(ddragon_language, "game_ability_resource_Grit")
        elif cdragon_bin['primaryAbilityResource']['arIncrements'] == 1:
            return translate.t(ddragon_language, "game_ability_resource_CrimsonRush")
        elif cdragon_bin['primaryAbilityResource']['arIncrements'] > 1:
            return translate.t(ddragon_language, "game_ability_resource_Gnarfury")
    elif cdragon_bin['primaryAbilityResource']['arType'] == 9:
        return translate.t(ddragon_language, "game_ability_resource_Ferocity")
    elif cdragon_bin['primaryAbilityResource']['arType'] == 10:
        return translate.t(ddragon_language, "game_ability_resource_BloodWell")
    elif cdragon_bin['primaryAbilityResource']['arType'] == 11:
        return translate.t(ddragon_language, "game_ability_resource_Wind")
    else:
        return 'Unknown'


def blurb(bio):
    """Returns champion blurb which cuts off around 250 characters"""
    if " " not in bio:
        return bio
    bio = bio[0:254]
    bio = ' '.join(bio.split(' ')[:-1])
    try:
        if bio[-1] == ",":
            bio = bio[:-1]
    except Exception as ex:
        print(ex)
    return bio + "..."


def remove_trailing_zeros(x):
    return str(x).rstrip('0').rstrip('.')


def get_icon_name(x):
    """Returns the icon name from a CDragon path"""
    return x.split('/')[-1]


def get_skin_num(id, skin_id):
    """Returns Skin Number from the Skin ID"""
    skin = str(id)
    length = len(skin)
    new_id = str(skin_id)[length:]
    return int(new_id)


def get_burn_string(burn_string):
    """Makes a burn string from a list"""
    new_burn = ""
    burn_list = burn_string.split("/")[:-1]
    res = []
    [res.append(x) for x in burn_list if x not in res]
    for burn in res:
        new_burn = new_burn + burn + "/"
    return new_burn[:-1]


def get_tooltip(lang, tooltip):
    """CDragon descriptions are @Effect@, DDragon has them in {{ effect }}"""
    for f in re.findall(r'\{\{(.*?)\}\}', tooltip):
        string = f.replace(" ", "")
        string = translate.t(lang, string)
        tooltip = tooltip.replace(f"{{{{{f}}}}}", string, 1)
    for f in re.findall(r'\@(.*?)\@', tooltip):
        tooltip = tooltip.replace(f"@{f}@", f"@{f.lower()}@", 1)
    x = re.sub(r'\@(.*?)\@', r'{{ \1 }}', tooltip)
    x = x.replace("<br>", "<br />")
    for i in range(11):
        x = x.replace("effect" + str(i) + "amount",
                      "e" + str(i))
    x = x.replace("charabilitypower2", "a2")
    x = x.replace("charabilitypower", "a1")

    # Replace font tags with span classes, if there are multiple they can end up in the wrong order but it is classes so it shouldn't matter
    x = x.replace("<font", '<span class=\"')
    x = x.replace(" size='", "size")
    x = x.replace("'>", '\">')
    x = x.replace(" color='#", "color")
    x = x.replace("'size", " size")
    x = x.replace("</font>", "</span>")
    return x


def process_spell_variables(spell):
    """DDragon has effects preprocessed where CDragon does not, need to calculate the effect amount and remove it from description"""
    for f in re.findall(r'\@(.*?)\@', spell['dynamicDescription']):
        if "Effect" in f and "Amount*" in f:
            expression = f.split("*")
            for x in range(len(spell['effectAmounts'][expression[0]])):
                spell['effectAmounts'][expression[0]][x] = eval(
                    str(spell['effectAmounts'][expression[0]][x]) + "*" + expression[1])
            spell['dynamicDescription'] = spell['dynamicDescription'].replace(
                f, expression[0], 1)
    return spell


def remove_html_tags(text):
    """Remove html tags from a string"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def get_stat_name(stat):
    """Returns the stat name from an integer"""
    if stat == 1:
        return "armor"
    elif stat == 2:
        return "attackdamage"
    elif stat == 3:
        return "movespeed"
    elif stat == 4:
        return "magicresist"
    elif stat == 5:
        return "movespeed"
    elif stat == 6:
        return "critchance"
    elif stat == 7:
        return "critdamage"
    elif stat == 10:
        return "maximumhealth"
    elif stat == 23:
        return "lethality"
    elif stat == 25:
        return "attackrange"
    else:
        return stat


def get_tip_list(ddragon_language, text):
    """Returns a list of tips from an html string"""
    text = translate.t(ddragon_language, text)
    if text != "":
        text = text.replace("<ul><li>", "").replace("</ul>", "")
        return text.split("<li>")
    return []


def create_damage_list(damagelist):
    """Creates a damage list from a dict. This is the function that creates calculations"""
    totaldamagetooltip = []
    for i in damagelist:
        if isinstance(i, str):
            i = damagelist
        listitem = {}
        if "mEffectIndex" in i:
            listitem.update({
                'effectIndex': i['mEffectIndex']
            })
        if "mBreakpoints" in i:
            damage = []
            modifier = 0
            number = 0
            for j in range(18):
                if j == 0:
                    if "mLevel1Value" in i:
                        number = round(i['mLevel1Value'], 3)
                    if '{02deb550}' in i:
                        modifier = round(i['{02deb550}'], 3)
                    if "mLevel" not in i['mBreakpoints'][0]:
                        number = round(
                            number + i['mBreakpoints'][0]['{57fdc438}'], 3)
                        modifier = round(i['mBreakpoints'][0]['{57fdc438}'], 3)
                    damage.append(number)
                    continue
                for k in i['mBreakpoints']:
                    if "mLevel" in k and j + 1 == k['mLevel']:
                        modifier = round(
                            k['{57fdc438}'], 3) if '{57fdc438}' in k else 0
                        if "{d5fd07ed}" in k:
                            number = number + round(k['{d5fd07ed}'], 3)
                number = round(number + modifier, 3)
                damage.append(number)
            listitem.update({
                'level': damage
            })
        if "mDataValue" in i:
            listitem.update({
                'datavalue': translate.__getitem__(i['mDataValue']).lower()
            })
            if "apratio" in listitem['datavalue']:
                listitem.update({
                    'stat': "abilitypower"
                })
        if "mStat" in i:
            listitem.update({
                'stat': get_stat_name(i['mStat'])
            })
        if "mStatFormula" in i:
            listitem.update({
                'statType': "bonus"
            })
        if "mCoefficient" in i and "mStat" not in i:
            listitem.update({
                'stat': 'abilitypower'
            })
        if "mCoefficient" in i:
            listitem.update({
                'coefficient': round(i['mCoefficient'], 4)
            })
        if "mStartValue" in i:
            listitem.update({
                'startValue': round(i['mStartValue'], 3)
            })
        if "mEndValue" in i:
            listitem.update({
                'endValue': round(i['mEndValue'], 3)
            })
        if "mNumber" in i:
            listitem.update({
                'number': round(i['mNumber'], 3)
            })
        if "epicness" in i:
            listitem.update({
                'epicness': "LEGENDARY"
            })
        if "mSubparts" in i:
            listitem.update({
                'subparts': create_damage_list(i['mSubparts'])
            })
        if "mSubpart" in i:
            damage_list = create_damage_list(i['mSubpart'])
            if damage_list != []:
                listitem.update(damage_list[0])
        if "mPart1" in i:
            listitem.update({
                'part1': create_damage_list(i['mPart1'])
            })
        if "mPart2" in i:
            listitem.update({
                'part2': create_damage_list(i['mPart2'])
            })
        if listitem != {}:
            totaldamagetooltip.append(listitem)
    return totaldamagetooltip


def get_calculation(ability_bin):
    calculation = {}
    if "{50f145c0}" in ability_bin:
        calculation = create_damage_list(ability_bin['{50f145c0}'])
    if "mFormulaParts" in ability_bin:
        calculation['formula'] = create_damage_list(
            ability_bin['mFormulaParts'])
        if "mMultiplier" in ability_bin:
            calculation['multiplier'] = get_multiplier(
                ability_bin['mMultiplier'])
    if "mModifiedGameCalculation" in ability_bin:
        calculation = {
            'modifiedCalculation': "",
            'multiplier': {}
        }
        calculation.update({
            'modifiedCalculation': translate.__getitem__(ability_bin['mModifiedGameCalculation']).lower()
        })
        calculation['multiplier'].update(
            get_multiplier(ability_bin['mMultiplier']))
    return calculation


def get_multiplier(multiplier):
    dictionary = {}
    for j in multiplier:
        if j == "mBreakpoints":
            dictionary.update({
                j[1:].lower(): create_damage_list(multiplier[j])
            })
        elif j == "mNumber":
            dictionary.update({
                j[1:].lower(): round(multiplier[j], 3)
            })
        elif "part" in j.lower():
            dictionary.update({
                j[1:].lower(): create_damage_list(multiplier[j])
            })
        elif "mDataValue" in j:
            dictionary.update({
                j[1:].lower(): translate.__getitem__(multiplier[j]).lower()
            })
        else:
            dictionary.update({
                j[1:].lower(): translate.__getitem__(multiplier[j])
            })
    return dictionary
