import os
import json
import requests


def download_json(url: str, use_cache: bool = True):
    directory = os.path.dirname(os.path.realpath(__file__))
    fn = os.path.join(directory, "__cache__")
    if not os.path.exists(fn):
        os.mkdir(fn)
    url2 = url.replace(":", "")
    fn = os.path.join(fn, url2.replace("/", "@"))

    if use_cache and os.path.exists(fn):
        with open(fn) as f:
            j = json.load(f)
    else:
        try:
            page = requests.get(url)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        j = page.json()
        if use_cache:
            with open(fn, "w") as f:
                json.dump(j, f)
    return j


def download_image(url: str, use_cache: bool = True):
    directory = os.path.dirname(os.path.realpath(__file__))
    fn = os.path.join(directory, "__cache__")
    if not os.path.exists(fn):
        os.mkdir(fn)
    url2 = url.replace(":", "")
    fn = os.path.join(fn, url2.replace("/", "@"))

    if use_cache and os.path.exists(fn):
        with open(fn, "rb") as f:
            j = f.read()
    else:
        try:
            image = requests.get(url)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        j = image.content
        if use_cache:
            with open(fn, "wb") as f:
                f.write(j)
    return j


def download_file(url: str, use_cache: bool = True):
    directory = os.path.dirname(os.path.realpath(__file__))
    fn = os.path.join(directory, "__cache__")
    if not os.path.exists(fn):
        os.mkdir(fn)
    url2 = url.replace(":", "")
    fn = os.path.join(fn, url2.replace("/", "@"))

    if use_cache and os.path.exists(fn):
        return fn
    else:
        try:
            image = requests.get(url)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        j = image.content
        if use_cache:
            with open(fn, "wb") as f:
                f.write(j)
        return fn


def save_json(data, filename):
    def set_default(obj):
        if isinstance(obj, set):
            return list(obj)
        raise TypeError(
            f"Cannot serialize object of type: {type(obj)} ... {obj}")

    sdata = json.dumps(data, indent=2, default=set_default)
    with open(filename, "w") as of:
        of.write(sdata)
    with open(filename, "r") as f:
        sdata = f.read()
        sdata = sdata.replace("\u00a0", " ")
        sdata = sdata.replace("\u300d", " ")
        sdata = sdata.replace("\u300c", " ")
        sdata = sdata.replace("\u00ba", " ")
        sdata = sdata.replace("\xa0", " ")
    with open(filename, "w") as of:
        of.write(sdata)


def remove_trailing_zeros(x):
    return str(round(x, 3)).rstrip('0').rstrip('.')


def load_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)
