from .out import ssf2fcitx, ssf2fcitx5

import sys, os, shutil
import logging

default_skins_dir = {
    "fcitx5": "~/.local/share/fcitx5/themes/",
    "fcitx": "~/.config/fcitx/skin/",
}


def convert(args):
    match args.type:
        case "fcitx5":
            err = ssf2fcitx5(args.src)
        case "fcitx":
            err = ssf2fcitx(args.src)
        case _:
            assert False
    if args.install:
        skins_dir = os.path.expanduser(default_skins_dir[args.type])
        shutil.move(args.dest, skins_dir)
    return err
