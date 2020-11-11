from natsort import natsorted
import os
import requests
import shutil

import constants
import settings
import utils
import version

unv_path = "cdn/img"


def update_cdn():
    global unv_path
    if not os.path.exists(os.path.join(settings.config['cdn']['cdn_root'], "api")):
        os.makedirs(os.path.join(settings.config['cdn']['cdn_root'], "api"))
    if not os.path.exists(os.path.join(settings.config['cdn']['cdn_root'], "realms")):
        os.makedirs(os.path.join(settings.config['cdn']['cdn_root'], "realms"))
    if settings.patch['json'] == "pbe":
        unv_path = "cdn/img/pbe"
    create_cdn_patch()
    patches = create_version()
    update_symlink(patches)
    update_realms(patches)
    if settings.config['cloudflare']['purge_cloudflare'] == True:
        purge_cloudflare()


def create_cdn_patch():
    if not os.path.exists(os.path.join(settings.config['cdn']['cdn_root'], f"cdn/{settings.patch['json']}")):
        os.makedirs(os.path.join(
            settings.config['cdn']['cdn_root'], f"cdn/{settings.patch['json']}"))
    if os.path.exists(os.path.join(settings.config['cdn']['cdn_root'], f"cdn/{settings.patch['json']}/data")):
        shutil.rmtree(settings.config['cdn']['cdn_root'],
                      f"cdn/{settings.patch['json']}/data")
    shutil.copytree(os.path.join(settings.files, f"{settings.patch['json']}/data"), os.path.join(
        settings.config['cdn']['cdn_root'], f"cdn/{settings.patch['json']}/data"))
    if os.path.exists(os.path.join(settings.config['cdn']['cdn_root'], f"cdn/{settings.patch['json']}/img")):
        shutil.rmtree(settings.config['cdn']['cdn_root'],
                      f"cdn/{settings.patch['json']}/img")
    shutil.copytree(os.path.join(settings.files, f"{settings.patch['json']}/img"), os.path.join(
        settings.config['cdn']['cdn_root'], f"cdn/{settings.patch['json']}/img"))
    if settings.patch['json'] == version.get_latest_ddragon_version() or settings.patch['json'] == "pbe":
        if os.path.exists(os.path.join(settings.config['cdn']['cdn_root'], f"{unv_path}/champion")):
            shutil.rmtree(os.path.join(
                settings.config['cdn']['cdn_root'], f"{unv_path}/champion"))
        if os.path.exists(os.path.join(settings.config['cdn']['cdn_root'], f"{unv_path}/perk-images")):
            shutil.rmtree(os.path.join(
                settings.config['cdn']['cdn_root'], f"{unv_path}/perk-images"))
        shutil.copytree(os.path.join(settings.files, f"{settings.patch['json']}/images/champion"), os.path.join(
            settings.config['cdn']['cdn_root'], f"{unv_path}/champion"))
        shutil.copytree(os.path.join(settings.files, f"{settings.patch['json']}/images/perk-images"), os.path.join(
            settings.config['cdn']['cdn_root'], f"{unv_path}/perk-images"))
    if os.path.exists(os.path.join(settings.config['cdn']['cdn_root'], f"cdn/dragontail-{settings.patch['json']}.tgz")):
        os.remove(os.path.join(
            settings.config['cdn']['cdn_root'], f"cdn/dragontail-{settings.patch['json']}.tgz"))
    if settings.config['general']['tarball'] == True:
        shutil.copyfile(os.path.join(settings.files, f"{settings.patch['json']}/dragontail-{settings.patch['json']}.tgz"), os.path.join(
            settings.config['cdn']['cdn_root'], f"cdn/dragontail-{settings.patch['json']}.tgz"))


def create_version():
    patches = [f.path.split("/")[-1] for f in os.scandir(os.path.join(settings.config['cdn']['cdn_root'], "cdn"))
               if "latest" not in f.path and f.is_dir() and "img" not in f.path and "pbe" not in f.path]
    patches = natsorted(patches)
    patches.reverse()
    utils.save_json(patches, os.path.join(
        settings.config['cdn']['cdn_root'], "api/versions.json"))
    return patches


def update_symlink(patches):
    try:
        os.symlink(os.path.join(
            settings.config['cdn']['cdn_root'], f"cdn/{patches[0]}/"), os.path.join(settings.config['cdn']['cdn_root'], "cdn/latest"))
    except FileExistsError:
        os.remove(os.path.join(
            settings.config['cdn']['cdn_root'], "cdn/latest"))
        os.symlink(os.path.join(
            settings.config['cdn']['cdn_root'], f"cdn/{patches[0]}/"), os.path.join(settings.config['cdn']['cdn_root'], "cdn/latest"))


def update_realms(patches):
    for realm in constants.realms:
        json = {
            "n": {
                "item": patches[0],
                "rune": "7.23.1",
                "mastery": "7.23.1",
                "summoner": patches[0],
                "champion": patches[0],
                "profileicon": patches[0],
                "map": patches[0],
                "language": patches[0],
                "sticker": patches[0],
            },
            "v": patches[0],
            "l": constants.realms[realm],
            "cdn": settings.config['cdn']['cdn_url'],
            "dd": patches[0],
            "lg": patches[0],
            "css": patches[0],
            "profileiconmax": 28,
            "store": None,
        }
        utils.save_json(json, os.path.join(
            settings.config['cdn']['cdn_root'], f"realms/{realm}.json"))


def purge_cloudflare():
    url = "https://api.cloudflare.com/client/v4/zones/" + \
        settings.config['cloudflare']['cloudflare_zone_id'] + "/purge_cache"
    headers = {
        "X-Auth-Email": settings.config['cloudflare']['cloudflare_email'],
        "X-Auth-Key": settings.config['cloudflare']['cloudflare_auth_key'],
        "Content-Type": "application/json",
    }
    data = {
        "purge_everything": True,
    }

    requests.post(url, json=data, headers=headers)
