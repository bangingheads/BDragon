import os
import tarfile

import settings
import utils

directory = os.path.dirname(os.path.realpath(__file__))


def create_tarball(path):
    """
    This function packages files into the .tar inside of a .tgz file structure that matches DDragon
    """
    create_manifest_json()
    create_manifest_js()
    with tarfile.open(os.path.join(path, 'dragontail-' + settings.patch['json'] + '.tar'), mode='w:gz') as archive:
        archive.add(os.path.join(path, "data"),
                    settings.patch['json'] + "/data")
        archive.add(os.path.join(path, "img"), settings.patch['json'] + "/img")
        archive.add(os.path.join(path, "images"), "img")
        archive.add(os.path.join(directory, "tarball/bg"), arcname="img/bg")
        archive.add(os.path.join(directory, "tarball/global"),
                    arcname="img/global")
        archive.add(os.path.join(directory, "tarball/manifest.json"),
                    arcname=f"lolpatch_{settings.patch['json']}/manifest.json")
        archive.add(os.path.join(directory, "tarball/manifest.js"),
                    arcname=f"lolpatch_{settings.patch['json']}/manifest.js")
        archive.add(os.path.join(directory, "tarball/dragonhead.js"),
                    arcname="dragonhead.js")
        archive.add(os.path.join(directory, "tarball/languages.js"),
                    arcname="languages.js")
        archive.add(os.path.join(directory, "tarball/languages.json"),
                    arcname="languages.json")

    if os.path.exists(os.path.join(path, f"dragontail-{settings.patch['json']}.tgz")):
        os.remove(os.path.join(
            path, f"dragontail-{settings.patch['json']}.tgz"))
    os.rename(os.path.join(path, f"dragontail-{settings.patch['json']}.tar"),
              os.path.join(path, f"dragontail-{settings.patch['json']}.tgz"))


def create_manifest_json():
    """
    Creates a manifest json file that matches DDragon's
    """
    json = {
        "n": {
            "item": settings.patch['json'],
            "rune": settings.patch['json'],
            "mastery": settings.patch['json'],
            "summoner": settings.patch['json'],
            "champion": settings.patch['json'],
            "profileicon": settings.patch['json'],
            "map": settings.patch['json'],
            "language": settings.patch['json'],
            "sticker": settings.patch['json'],
        },
        "v": settings.patch['json'],
        "l": "en_US",
        "cdn": None,
        "dd": settings.patch['json'],
        "lg": settings.patch['json'],
        "css": settings.patch['json'],
        "profileiconmax": 28,
    }
    utils.save_json(json, os.path.join(directory, "tarball/manifest.json"))


def create_manifest_js():
    """
    Creates a manifest js file based on the manifest json file already created
    """
    with open(os.path.join(directory, 'tarball/manifest.json')) as f:
        manifest = f.read()
    js = "Riot.DDragon.m=" + manifest
    with open(os.path.join(directory, 'tarball/manifest.js'), 'w') as f:
        f.write(js)
