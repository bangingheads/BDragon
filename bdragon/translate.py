import i18n
import os
import re

from cdragontoolbox.rstfile import RstFile
import __main__
import download
import utils


def t(language, translation):
    """
    Translates RST strings to Regional Strings using i18n as a cache as parsing RST delays load by a lot to retrieve simple things that are used many times
    """
    i18n.set('locale', language)
    if translation == i18n.t(translation):
        rst = RstFile(download.download_cdragon_rstfile(language))
        try:
            name = rst.__getitem__(translation)
        except Exception:
            print("DIDNT FIND: " + translation)
            name = ""
        i18n.add_translation(translation, name, locale=language)
        return name
    return i18n.t(translation)


def __getitem__(hash):
    """
    Gets an item from the hashes.txt file if it exists, as CDragon is missing some hashes we create our own
    """
    if "{" not in str(hash):
        return hash
    if os.path.exists(os.path.join(os.path.dirname(os.path.realpath(__file__)), "trans/hashes.txt")):
        stripped_hash = re.findall(r'{(.+?)}', hash)[0]
        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "trans/hashes.txt")) as search:
            for line in search:
                if stripped_hash in line:
                    print("FOUND: " + line.split(" ", 1)[-1].rstrip())
                    return line.split(" ", 1)[-1].rstrip()
    print("FAILED TO FIND HASH: " + stripped_hash)
    return hash  # Unknown Hash
