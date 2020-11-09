import os

import settings
import utils


def create_sticker_json(path):
    # This hasn't been included since 9.2.1, so we're not going to include it
    stickers = {
        "type": "sticker",
        "version": settings.patch['json'],
        "data": {},
    }
    utils.save_json(stickers, os.path.join(path, "sticker.json"))
    return stickers
