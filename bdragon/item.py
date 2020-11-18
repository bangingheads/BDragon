import math
import os
import re

import download
import utils
import settings
import translate


def create_item_json(cdragon_language, ddragon_language, path):
    # Using DDragon info for basic, groups, and tree as we don't have all the hashes to build these
    ddragon_items = download.download_versioned_ddragon_items(ddragon_language)

    cdragon_items_bin = download.download_versioned_cdragon_items_bin()
    cdragon_items = download.download_versioned_cdragon_items(cdragon_language)
    cdragon_maps = download.download_versioned_cdragon_map_summary(
        cdragon_language)
    maps = {}
    for i in cdragon_maps:
        maps[i['id']] = i['mapStringId']
    items = {
        'type': 'item',
        'version': settings.patch['json'],
        'basic': ddragon_items['basic'],
        'data': {},
        'groups': ddragon_items['groups'],
        'tree': ddragon_items['tree'],
    }

    items["data"] = {}
    for x in cdragon_items_bin:
        item_bin = cdragon_items_bin[x]
        if ("mItemDataAvailability" not in item_bin or ("{2e97ceab}" not in item_bin['mItemDataAvailability'] and "mForceLoad" not in item_bin['mItemDataAvailability'] and "mInStore" not in item_bin['mItemDataAvailability'])) and ("mItemModifiers" not in item_bin or "{1fb38586}" not in item_bin['mItemModifiers']):
            continue
        cdragon_item = [d for d in cdragon_items if d['id']
                        == item_bin['itemID']][0]
        id = str(item_bin['itemID'])

        items['data'][id] = {
            'name': sanitize(translate.t(ddragon_language, item_bin['mDisplayName'])),
            'description': "",
            "sanitizedDescription": "",
            'colloq': translate.t(ddragon_language, "game_item_colloquialism_" + id),
            'plaintext': translate.t(ddragon_language, "game_item_plaintext_" + id),
            'epicness': ""
        }
        try:  # Use description in client if exists
            items['data'][id]['description'] = cdragon_item['description']
        except KeyError:
            items['data'][id]['description'] = translate.t(ddragon_language,
                                                           item_bin['mItemDataClient']['mDescription'])
        if "GeneratedTip" in items['data'][id]['description']:
            items['data'][id]['description'] = translate.t(
                ddragon_language, items['data'][id]['description'])
        items['data'][id]['sanitizedDescription'] = sanitize(
            items['data'][id]['description'])
        if "maxStack" in item_bin and item_bin['maxStack'] != 1:
            items['data'][id]['stacks'] = item_bin['maxStack']

        if "specialRecipe" in item_bin:
            items['data'][id]['specialRecipe'] = item_bin['specialRecipe']
        if "recipeItemLinks" in item_bin:
            items['data'][id]['from'] = []
            for item_from in item_bin['recipeItemLinks']:
                items['data'][id]['from'].append(
                    str(cdragon_items_bin[item_from]['itemID']))

        if "mItemDataAvailability" in item_bin and "mHidefromAll" in item_bin['mItemDataAvailability']:
            items['data'][id]['hideFromAll'] = True

        if "mItemDataAvailability" in item_bin and "mInStore" not in item_bin['mItemDataAvailability']:
            items['data'][id]['inStore'] = False

        if "mItemDataBuild" in item_bin:
            items['data'][id]['into'] = []
            for into in item_bin['mItemDataBuild']['itemLinks']:
                items['data'][id]['into'].append(
                    str(cdragon_items_bin[into]['itemID']))

        items['data'][id]['image'] = {
            'full': str(id) + ".png",
        }

        items['data'][id]['gold'] = {
            'base': item_bin['price'] if "price" in item_bin else 0,
            'purchasable': True if "mItemDataAvailability" in item_bin and "mInStore" in item_bin['mItemDataAvailability'] else False,
            'total': calculate_item_price(cdragon_items_bin, item_bin) if "price" in item_bin or "Items/ItemGroups/OrnnItems" in item_bin['mItemGroups'] else 0,
            'sell': round_half_up(calculate_item_price(cdragon_items_bin, item_bin) * (item_bin['sellBackModifier'] if 'sellBackModifier' in item_bin else 0.7)) if "price" in item_bin or "Items/ItemGroups/OrnnItems" in item_bin['mItemGroups'] else 0,
        }

        # Categories not in game files
        try:
            items['data'][id]['tags'] = cdragon_item['categories']
        except KeyError:
            items['data'][id]['tags'] = []

        items['data'][id]['maps'] = {}
        for i in maps:
            if 'mMapStringIdInclusions' in item_bin and maps[i] in item_bin['mMapStringIdInclusions']:
                items['data'][id]['maps'][i] = True
            else:
                items['data'][id]['maps'][i] = False

        items['data'][id]['stats'] = {}
        for i in item_bin:
            original = i
            if "{" in i:
                i = translate.__getitem__(i)
            if "Mod" in i and "Mode" not in i and "Modifier" not in i:
                if i[0] == "m":
                    items['data'][id]['stats'][capitalize(
                        i[1:])] = round(item_bin[original], 3)
                else:
                    items['data'][id]['stats'][capitalize(
                        i)] = round(item_bin[original], 3)

        if 'mEffectAmount' in item_bin:
            items['data'][id]['effect'] = {}
            index = 1
            for effect in item_bin['mEffectAmount']:
                effect_string = "Effect" + str(index) + "Amount"
                items['data'][id]['effect'][effect_string] = utils.remove_trailing_zeros(
                    effect)
                index += 1
        if 'from' in items['data'][id]:
            items['data'][id]['depth'] = len(items['data'][id]['from'])

        if 'consumed' in item_bin:
            items['data'][id]['consumed'] = True
        if 'usableInStore' in item_bin:
            items['data'][id]['consumeOnFull'] = True

        if "mRequiredAlly" in item_bin:
            items['data'][id]['requiredAlly'] = item_bin['mRequiredAlly']
        # Patch 10.23+ Fix
        elif "Items/ItemGroups/OrnnItems" in item_bin['mItemGroups']:
            items['data'][id]['requiredAlly'] = "Ornn"

        if "mRequiredChampion" in item_bin:
            items['data'][id]['requiredChampion'] = item_bin['mRequiredChampion']

        items['data'][id]['group'] = []
        for i in item_bin['mItemGroups']:
            if "{" in i:
                group = translate.__getitem__(i)
                if "{" not in group:
                    items['data'][id]['group'].append(group.split("/")[-1])
            else:
                items['data'][id]['group'].append(i.split("/")[-1])
        if "mDataValues" in item_bin:
            items['data'][id]['datavalues'] = {}
            for i in item_bin['mDataValues']:
                items['data'][id]['datavalues'].update({
                    i['mName']: round(i['mValue'], 3) if "mValue" in i else 0
                })
        if settings.patch['ddragon'] > "10.22.1":
            if "Boots" in items['data'][id]['group']:
                items['data'][id]['epicness'] = "BOOTS"
            elif "Consumable" in items['data'][id]['group'] or "Consumable" in items['data'][id]['tags']:
                items['data'][id]['epicness'] = "CONSUMABLE"
            elif "Trinket" in items['data'][id]['group'] or "Trinket" in items['data'][id]['tags']:
                items['data'][id]['epicness'] = "TRINKET"
            elif "from" not in items['data'][id] and "specialRecipe" not in items['data'][id] and "GuardianItems" not in items['data'][id]['group']:
                if "epicness" in item_bin and item_bin['epicness'] == 1:
                    items['data'][id]['epicness'] = "STARTER"
                else:
                    items['data'][id]['epicness'] = "BASIC"
            elif "epicness" in item_bin and item_bin['epicness'] == 4:
                items['data'][id]['epicness'] = "EPIC"
            elif "epicness" in item_bin and item_bin['epicness'] == 5 or "GuardianItems" in items['data'][id]['group']:
                items['data'][id]['epicness'] = "LEGENDARY"
            elif "epicness" in item_bin and item_bin['epicness'] == 6:
                items['data'][id]['epicness'] = "MYTHIC"
        else:
            del items['data'][id]['epicness']
    # Remove inactive items from the into and from
    for item in items['data']:
        if "into" in items['data'][item]:
            items['data'][item]['into'] = [
                x for x in items['data'][item]['into'] if x in items['data']]
            if len(items['data'][item]['into']) == 0:
                del items['data'][item]['into']
        if "from" in items['data'][item]:
            items['data'][item]['from'] = [
                x for x in items['data'][item]['from'] if x in items['data']]
            if len(items['data'][item]['from']) == 0:
                del items['data'][item]['from']

    # Calculate actual depth
    for item in items['data']:
        if "from" in items['data'][item]:
            depth = 2
            for builds_from in items['data'][item]['from']:
                if "from" in items['data'][builds_from]:
                    if depth < 3:
                        depth = 3
                    for builds_from2 in items['data'][builds_from]['from']:
                        if "from" in items['data'][builds_from2]:
                            depth = 4
            items['data'][item]['depth'] = depth

    items['data'] = {key: items['data'][key]
                     for key in sorted(items['data'].keys())}

    utils.save_json(
        items, os.path.join(path, "item.json"))
    return items


def get_item_bin(item, cdragon_items_bin):
    for x in cdragon_items_bin:
        if str(cdragon_items_bin[x]['itemID']) == str(item):
            return cdragon_items_bin[x]
    return {}


def add_sprite_info(lang, path):
    data = utils.load_json(os.path.join(path, "spriter_output.json"))
    items = utils.load_json(os.path.join(
        path, f"data/{lang}/item.json"))
    for item in items['data']:
        try:
            items['data'][item]['image'].update({
                'sprite': data['result']['item'][item]['regular']['texture'] + ".png",
                'group': "item",
                'x': data['result']['item'][item]['regular']['x'],
                'y': data['result']['item'][item]['regular']['y'],
                'w': data['result']['item'][item]['regular']['width'],
                'h': data['result']['item'][item]['regular']['height'],
            })
        except KeyError:
            print("Failed to add sprite of item: " + item)
    utils.save_json(items, os.path.join(path, f"data/{lang}/item.json"))
    return


def capitalize(key):
    return re.sub('([a-zA-Z])', lambda x: x.groups()[0].upper(), key, 1)


def round_half_up(val):
    if (float(val) % 1) >= 0.499:
        x = math.ceil(val)
    else:
        x = round(val)
    return x


def calculate_item_price(cdragon_item_bin, item_bin):
    price = item_bin['price'] if "price" in item_bin else 0
    if "recipeItemLinks" in item_bin:
        for x in item_bin['recipeItemLinks']:
            price = price + \
                (cdragon_item_bin[x]['price']
                 if "price" in cdragon_item_bin[x] else 0)
            if "recipeItemLinks" in cdragon_item_bin[x]:
                for y in cdragon_item_bin[x]['recipeItemLinks']:
                    price = price + \
                        (cdragon_item_bin[y]['price']
                         if "price" in cdragon_item_bin[y] else 0)
                    if "recipeItemLinks" in cdragon_item_bin[y]:
                        for z in cdragon_item_bin[y]['recipeItemLinks']:
                            price = price + \
                                (cdragon_item_bin[z]['price']
                                 if "price" in cdragon_item_bin[z] else 0)
        return price
    return price


def sanitize(text):
    """
    Remove html tags from a string
    Removes strings wrapped in %s
    Adds periods to br and li tags
    Fixes spacing
    """
    text = text.replace("<br>", ".")
    text = text.replace(" <li>", ".")
    clean = re.compile('<.*?>')
    clean_text = re.sub(clean, '', text)
    clean = re.compile(r'\%[^\s]+\%')
    clean_text = re.sub(clean, '', clean_text)
    clean_text = clean_text.replace("  ", " ")
    clean_text = clean_text.replace(". .", ".")
    periods = re.compile(r'\.{2,}')
    clean_text = re.sub(periods, '.', clean_text)
    if clean_text != "" and (clean_text[0] == " " or clean_text[0] == "."):
        clean_text = clean_text[1:]
    clean_text = re.sub(r'(?<=[.,])(?=[^\s\d])', r' ', clean_text)
    return clean_text
