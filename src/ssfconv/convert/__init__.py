from .out import ssf2fcitx, ssf2fcitx5


import sys
import os


def convert(args):
    match args.type:
        case "fcitx5":
            err = ssf2fcitx5(args.src)
        case "fcitx":
            err = ssf2fcitx(args.src)
        case _:
            assert False

    return err
