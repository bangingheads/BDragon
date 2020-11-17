import i18n
import os
import re

from cdragontoolbox.rstfile import RstFile
import download
import hashes
import utils

rst = {}


def t(language, translation):
    """
    Translates RST strings to Regional Strings
    """
    global rst
    if language not in rst:
        rst[language] = RstFile(
            download.download_cdragon_rstfile(language))
    try:
        name = rst[language].__getitem__(translation)
    except Exception:
        print("DIDNT FIND: " + translation)
        name = ""
    return name


def __getitem__(hash):
    """
    Gets an item from the hashes.txt file if it  as well as guessedhashes.txt, as CDragon is missing some hashes we create our own
    """
    if "{" not in str(hash):
        return hash
    if os.path.exists(os.path.join(os.path.dirname(os.path.realpath(__file__)), "hashes.txt")):
        stripped_hash = re.findall(r'{(.+?)}', hash)[0]
        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "hashes.txt")) as search:
            for line in search:
                if stripped_hash in line:
                    print("FOUND: " + line.split(" ", 1)[-1].rstrip())
                    return line.split(" ", 1)[-1].rstrip()
    if os.path.exists(os.path.join(os.path.dirname(os.path.realpath(__file__)), "guessedhashes.txt")):
        stripped_hash = re.findall(r'{(.+?)}', hash)[0]
        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "guessedhashes.txt")) as search:
            for line in search:
                if stripped_hash in line:
                    print("USING GUESSED HASH: " +
                          line.split(" ", 1)[-1].rstrip())
                    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "hashes.txt"), "a+") as hash_list:
                        hash_list.write(line)
                    hashes.sort_hashes()
                    return line.split(" ", 1)[-1].rstrip()
    print("FAILED TO FIND HASH: " + stripped_hash)
    return hash  # Unknown Hash
