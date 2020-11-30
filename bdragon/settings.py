import argparse
import os
import sys
import yaml

import constants
import hashes
import version

languages = {}
patch = {}
config = {}

directory = os.path.abspath(os.path.join(
    os.path.dirname(os.path.realpath(__file__)), ".."))

files = os.path.join(directory, "files")


def init():
    global config
    global languages
    global patch
    global tarball
    try:
        with open(os.path.join(directory, "config.yml"), "r") as ymlfile:
            config = yaml.load(ymlfile, yaml.Loader)
    except FileNotFoundError:
        sys.exit(
            "Please rename config_example.yml to config.yml. Reference README for more information")
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-patch", "-p", help="Generate DDragon from specific patch", default="latest")
    parser.add_argument(
        "-language", "-l", help="Generate DDragon for a specific language", default="all")
    parser.add_argument(
        "--force", help="Forces download regardless if patch is already downloaded", action="store_true")
    parser.add_argument(
        "--hashes", help="Uses a previously built champion json to find missing datavalue hashes", action="store_true")
    parser.add_argument(
        "--tarball", help="Creates a DDragon tarball in the patch directory", action="store_true")
    args = parser.parse_args()

    if args.patch == "latest":
        patch = {
            'ddragon': version.get_latest_ddragon_version(),
            'cdragon': version.get_latest_cdragon_version(),
            'json': version.get_latest_cdragon_version() + ".1",
        }
    elif args.patch == "pbe":
        patch = {
            'ddragon': version.get_latest_ddragon_version(),
            'cdragon': version.get_cdragon_version(args.patch),
            'json': "pbe",
        }
    else:
        patch = {
            'ddragon': version.get_ddragon_version(args.patch),
            'cdragon': version.get_cdragon_version(args.patch),
            'json': version.get_cdragon_version(args.patch) + ".1",
        }
    if args.language == "all":
        languages = constants.languages
    elif args.language in constants.languages:
        languages = {
            args.language: constants.languages[args.language]
        }
    else:
        sys.exit("Invalid language specified")
    if args.force:
        config['general']['production'] = False
    if args.tarball:
        tarball = True
    if args.hashes:
        hashes.find_hashes()
