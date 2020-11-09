# BananaDragon Static Data

A tool to generate more accurate and timely DDragon-esque files from CDragon game & client files.

## Dependencies

To install dependencies, run:

```
pip install -r requirements.txt
```

As BDragon uses [CDTB](https://github.com/CommunityDragon/CDTB), these include CDTB's requirements.

## Command Line Running

You can use the command line to explain parameters `python3 bdragon -h`

Example parameters:

```python
#download current patch files
python3 bdragon

#download pbe files
python3 bdragon -p pbe

#download pbe files and create a tarball
python3 bdragon -p pbe --tarball

#download 10.20 files for only en_US
python3 bdragon -p 10.20 -l en_US
```

## Sprite Sheets

This project uses a modified version of [Querijin's DragonSpriter](https://github.com/Querijn/DragonSpriter). Binaries for Linux and Windows are included in the repository. If you would like to compile these files yourself you can download and compile from [my forked repository](https://github.com/bangingheads/DragonSpriter) and replace the respective file in the bdragon folder.

## Files

Files are generated into the `files/{patch}` directory in the main directory. `data` contains all the data jsons (cdn/patch/data), `img` contains all the versioned images of the patch (cdn/patch/img), `images` contains all the unversioned images of the patch (cdn/img)

## Contributing

The best way to contribute is to fork the repository and create a Pull Request. All Pull Requests are welcome but please make sure you are only effecting the code you plan to as every small change can have a big impact parsing files.

## CDN

As hosting your own ddragon data is not always viable, I also host the data at [https://ddragon.bangingheads.net/cdn/](https://ddragon.bangingheads.net/cdn/)

This includes all ddragon resources like the [versions api](https://ddragon.bangingheads.net/api/versions.json).

Although no downtime is expected, this CDN is provided as a best effort service. If you require high amounts of bandwidth from the CDN, I ask that you download the tarball and host it yourself.

## Thank You

A special shoutout to the CommunityDragon team, this project is not possible without them, they work hard and for free for the community and I hope everyone can thank them for that.

A thank you to Querijin for his making of the sprite sheet maker as it saved time in building the project.
