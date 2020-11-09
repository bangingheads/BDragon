import math
import os
import re

import download
import utils
import settings


import translate


def create_item_json(cdragon_language, ddragon_language, path):
    # Using DDragon info for basic, groups, and tree as these don't seem to be in files anywhere
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
        if "mItemDataAvailability" not in item_bin or ("{2e97ceab}" not in item_bin['mItemDataAvailability'] and "mForceLoad" not in item_bin['mItemDataAvailability'] and "mInStore" not in item_bin['mItemDataAvailability']):
            continue
        cdragon_item = [d for d in cdragon_items if d['id']
                        == item_bin['itemID']][0]
        id = str(item_bin['itemID'])

        items['data'][id] = {
            'name': translate.t(ddragon_language, item_bin['mDisplayName']),
            'description': translate.t(ddragon_language, item_bin['mItemDataClient']['mDescription']),
            'colloq': translate.t(ddragon_language, "game_item_colloquialism_" + id),
            'plaintext': translate.t(ddragon_language, "game_item_plaintext_" + id),
        }
        if "maxStack" in item_bin and item_bin['maxStack'] != 1:
            items['data'][id]['stacks'] = item_bin['maxStack']

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
            'total': calculate_item_price(cdragon_items_bin, item_bin) if "price" in item_bin else 0,
            'sell': round_half_up(calculate_item_price(cdragon_items_bin, item_bin) * (item_bin['sellBackModifier'] if 'sellBackModifier' in item_bin else 0.7)) if "price" in item_bin else 0,
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
            if "Mod" in i and "Mode" not in i and "Modifier" not in i:
                if i[0] == "m":
                    items['data'][id]['stats'][capitalize(
                        i[1:])] = round(item_bin[i], 3)
                else:
                    items['data'][id]['stats'][capitalize(
                        i)] = round(item_bin[i], 3)

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
    price = item_bin['price']
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
    return 0
