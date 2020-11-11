from fnvhash import fnv1a_32
import os
import re
import sys

import settings
import utils


def find_hashes():
    hashes = {}
    championfull = utils.load_json(os.path.join(
        settings.files, settings.patch['json'] + "/data/en_US/championFull.json"))

    for champion in championfull['data']:
        for x in championfull['data'][champion]['spells']:
            if x['datavalues'] != {}:
                for y in x['datavalues']:
                    hashes.update({
                        y: create_hash(y)
                    })
            for f in re.findall(r'\{\{(.*?)\}\}', x['tooltip']):
                string = f.split("*")[0]
                string = string.replace(" ", "")
                hashes.update({
                    string: create_hash(string)
                })

    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "guessedhashes.txt"), "a+") as file_object:
        for x in hashes:
            file_object.write(hashes[x] + " " + x + "\n")
    sys.exit("DONE")


def create_hash(string):
    string = str.encode(string.lower())
    return hex(fnv1a_32(string))[2:]


def sort_hashes():
    hashes = {}
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "hashes.txt")) as f:
        for line in f:
            (key, value) = line.rstrip().split(" ", 1)
            hashes[value] = key
    hashes = dict(sorted(hashes.items()))
    os.remove(os.path.join(os.path.dirname(
        os.path.realpath(__file__)), "trans/hashes.txt"))
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "hashes.txt"), "a+") as f:
        for x in hashes:
            f.write(hashes[x] + " " + x + "\n")
