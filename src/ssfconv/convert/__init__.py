from .out import ssf2fcitx, ssf2fcitx5
from pathlib import Path
import os, sys, shutil
import logging


def convert(args):
    install_dir = None
    # TODO refractor ssf2fcitx{5} get rid of os.path
    match args.type:
        case "fcitx5":
            err = ssf2fcitx5(args.src)
        case "fcitx":
            err = ssf2fcitx(args.src)
        case _:
            assert False
    if args.install:
        install(args)
    return err


default_skins_dir = {
    "fcitx5": "fcitx5/themes/",
    "fcitx": "fcitx/skin/",
}


def install(args):
    match args.type:
        case "fcitx5":
            install_dir = os.getenv("XDG_DATA_HOME", Path("~/.local/share").expanduser())
        case "fcitx":
            install_dir = os.getenv("XDG_CONFIG_HOME", Path("~/.config").expanduser())
        case _:
            assert False
    install_dir = Path(install_dir) / default_skins_dir[args.type]
    shutil.move(args.dest, install_dir)
