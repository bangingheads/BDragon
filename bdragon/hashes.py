from fnvhash import fnv1a_32
import os
import re
import sys

from cdragontoolbox.rstfile import RstFile
import download
import settings
import utils


def find_hashes():
    hashes = {}
    rst = RstFile(download.download_cdragon_rstfile("en_US"))
    for x in rst.entries:
        if type(rst[x]) is not str:
            continue
        for f in re.findall(r'\@(.*?)\@', rst[x]):
            string = f.split("*")[0]
            hashes.update({
                string: create_hash(string)
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
