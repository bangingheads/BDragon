from fnvhash import fnv1a_32
import os
import re
import sys

from cdragontoolbox.rstfile import RstFile
import champion
import download
import item
import settings


def find_hashes():
    hashes = {}
    # Get hashes from all RST strings
    rst = RstFile(download.download_cdragon_rstfile("en_US"))
    for x in rst.entries:
        if type(rst[x]) is not str:
            continue
        for f in re.findall(r'\@(.*?)\@', rst[x]):
            string = f.split("*")[0]
            hashes.update({
                string: create_hash(string)
            })
    # Get hashes from datavalues in champions
    champions = champion.create_championfull_json(
        "default", "en_US", capitalization=True)
    for _, data in champions['data'].items():
        for x in data['spells']:
            if x['datavalues'] != {}:
                for y in x['datavalues']:
                    hashes.update({
                        y: create_hash(y)
                    })
        if data['passive']['datavalues'] != {}:
            for y in data['passive']['datavalues']:
                hashes.update({
                    y: create_hash(y)
                })
    # Get hashes from datavalues in items
    items = item.create_item_json(
        "default", "en_US", f"{settings.files}/{settings.patch['json']}/data/en_US", capitalization=True)
    for _, data in items['data'].items():
        if "datavalues" in data and data['datavalues'] != {}:
            for y in data['datavalues']:
                hashes.update({
                    y: create_hash(y)
                })

    # Get hashes from ddragon item groups
    items = download.download_versioned_ddragon_items("en_US")
    for x in items['groups']:
        hashes.update({
            x['id']: create_hash(x['id'])
        })

    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "guessedhashes.txt"), "a+") as file_object:
        for x in hashes:
            file_object.write(hashes[x] + " " + x + "\n")
    sys.exit("DONE")


def create_hash(string):
    string = str.encode(string.lower())
    hash_string = hex(fnv1a_32(string))[2:]
    while len(hash_string) < 8:
        hash_string = "0" + hash_string
    return hash_string


def sort_hashes():
    hashes = {}
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "hashes.txt")) as f:
        for line in f:
            (key, value) = line.rstrip().split(" ", 1)
            hashes[value] = key
    hashes = dict(sorted(hashes.items()))
    os.remove(os.path.join(os.path.dirname(
        os.path.realpath(__file__)), "hashes.txt"))
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "hashes.txt"), "a+") as f:
        for x in hashes:
            f.write(hashes[x] + " " + x + "\n")
