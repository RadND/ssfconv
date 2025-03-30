import sys, shutil
from pathlib import Path
from .translation import _
import argparse
from .extract.ssf import extract_ssf
from .convert import convert


def add_parser_unpack(subparsers: argparse._SubParsersAction):
    parser = subparsers.add_parser("unpack", help=_("Unpack skin"))
    parser.add_argument("src", type=Path, help=_("Skin file"))
    parser.add_argument(
        "dest",
        type=Path,
        help=_("Output folder name, default is same as Skin file name"),
        nargs="?",
        default=None,
    )
    parser.add_argument(
        "-t",
        "--type",
        help=_(
            "Format of skin to be unpack",
        ),
        default="ssf",
        choices=["ssf"],
    )
    parser.add_argument(
        "-f",
        "--force",
        help=_("Delete if output path already exist"),
        action="store_true",
    )
    parser.set_defaults(func=unpack)


def unpack(args):
    if args.dest == None:
        args.dest = args.src.with_suffix("")

    if not args.src.exists():
        sys.stderr.write(_("Input path %s not exist\n") % args.src)
        return 1
    if not args.src.is_file():
        sys.stderr.write(_("Input path %s is not file\n") % args.src)
        return 1
    if args.dest.exists():
        if args.force:
            if args.dest.is_dir():
                shutil.rmtree(args.dest)
            else:
                args.dest.unlink()
        else:
            sys.stderr.write(_("Output path  %s already exist\n") % args.dest)
            return 1
    else:
        args.dest.mkdir()

    return extract_ssf(args.src, args.dest)


def add_parser_convert(subparsers: argparse._SubParsersAction):
    parser = subparsers.add_parser("convert", help=_("Convert skin file"))
    parser.add_argument("src", type=Path, help=_("Input folder"))
    # parser.add_argument(
    #     "dest", help="输出文件夹，默认与输入文件夹相同", nargs="?", default=None
    # )
    parser.add_argument(
        "-t",
        "--type",
        help=_("Output skin type"),
        default="fcitx5",
        choices=["fcitx", "fcitx5"],
    )
    # parser.add_argument(
    #     "-f", "--force", help="强制覆盖输出文件夹的内容", action="store_true"
    # )
    parser.add_argument(
        "-i",
        "--install",
        help=_("Install the convert result to it's default install location"),
        action="store_true",
    )
    parser.set_defaults(func=conv)


def conv(args):
    if not args.src.exists():
        sys.stderr.write(_("Input path %s not exist\n") % args.src)
        return 1
    if not args.src.is_dir():
        sys.stderr.write(_("Input path %s is not folder\n") % args.src)
        return 1

    args.dest = args.src
    if args.dest.exists():
        # if not args.force:
        #     sys.stderr.write("输出文件（夹） %s 已存在\n" % args.dest)
        # return 1
        pass
    else:
        args.dest.mkdir()

    err = convert(args)
    exit(err)


def main():
    parser = argparse.ArgumentParser(prog="ssfconv")
    # parser.add_argument("--foo", action="store_true", help="foo help")
    subparsers = parser.add_subparsers()

    add_parser_unpack(subparsers)
    add_parser_convert(subparsers)

    # print(parser.parse_args(["a", "12"]))
    args = parser.parse_args()
    args.func(args)
