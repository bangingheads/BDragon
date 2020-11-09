import utils
import constants


def get_latest_ddragon_version():
    versions = utils.download_json(
        constants.ddragon_url + "/api/versions.json", use_cache=False)
    versions = [v for v in versions if "_" not in v]
    return versions[0]


def get_ddragon_version(patch):
    versions = utils.download_json(
        constants.ddragon_url + "/api/versions.json", use_cache=False)
    versions = [v for v in versions if "_" not in v]
    for v in versions:
        if v.startswith(patch):
            return v
    return versions[0]


def get_latest_cdragon_version():
    versionstring = utils.download_json(
        constants.cdragon_url + "/latest/content-metadata.json", use_cache=False)['version']
    split = versionstring.split(".")
    return f"{split[0]}.{split[1]}"


def get_cdragon_version(patch):
    versions = utils.download_json(constants.cdragon_url + "/json/", use_cache=False)
    for v in versions:
        if patch == v['name']:
            return v['name']
    raise Exception('Invalid patch specified')

def get_cdragon_pbe_version():
    return utils.download_json(
        constants.cdragon_url + "/pbe/content-metadata.json", use_cache=False)['version']
