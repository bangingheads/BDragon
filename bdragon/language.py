import os

import download
import settings
import utils


def create_language_json(lang, path):
    # Returning Latest DDragon unless we can figure out how to merge trans.json files to match

    ddragon_language = download.download_versioned_ddragon_language(lang)
    language = {
        "type": "language",
        "version": settings.patch['json'],
        "data": ddragon_language['data'],
    }
    utils.save_json(language, os.path.join(path, "language.json"))
    return language
