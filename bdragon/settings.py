import argparse

import version

args = []
patch = {}
production = True
tarball = False


def init():
    global patch
    global production
    global tarball
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-patch", "-p", help="Generate DDragon from specific patch", default="latest")

    parser.add_argument(
        "--force", help="Forces download regardless if patch is already downloaded", action="store_true")
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
    if args.force:
        production = False
    if args.tarball:
        tarball = True
