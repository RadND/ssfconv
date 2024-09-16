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
        logging.debug(
            "os.pardir %s \n"
            + "args.dest %s \n"
            + "default_skins_dir[args.type] %s \n",
            os.pardir,
            args.dest,
            default_skins_dir[args.type],
        )
        # shutil.move(os.pardir + args.dest, default_skins_dir[args.type] + args.dest)
        pass
    return err
