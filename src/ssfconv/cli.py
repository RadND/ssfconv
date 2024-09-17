#!/usr/bin/env python3
# -*- encoding:utf-8 -*-
import argparse
import os, sys, shutil
from .extract.ssf import extract_ssf
from .convert import convert


def conv():
    parser = argparse.ArgumentParser(description="皮肤文件转换")
    parser.add_argument("src", help="输入文件夹")
    # parser.add_argument(
    #     "dest", help="输出文件夹，默认与输入文件夹相同", nargs="?", default=None
    # )
    parser.add_argument(
        "-t",
        "--type",
        help="输出文件（夹）格式，默认 fcitx5",
        default="fcitx5",
        choices=["fcitx", "fcitx5"],
    )
    # parser.add_argument(
    #     "-f", "--force", help="强制覆盖输出文件夹的内容", action="store_true"
    # )
    parser.add_argument(
        "-i",
        "--install",
        help="将转换结果移动到该格式皮肤的默认位置",
        action="store_true",
    )
    args = parser.parse_args()

    if not os.path.exists(args.src):
        sys.stderr.write("输入文件（夹） %s 不存在\n" % args.src)
        return 1
    if not os.path.isdir(args.src):
        sys.stderr.write("%s 不是文件夹 \n" % args.src)
        return 1

    args.dest = args.src
    if os.path.exists(args.dest):
        # if not args.force:
        #     sys.stderr.write("输出文件（夹） %s 已存在\n" % args.dest)
        # return 1
        pass
    else:
        os.mkdir(args.dest)

    err = convert(args)
    exit(err)


def unpackage():
    parser = argparse.ArgumentParser(description="皮肤文件解压")
    parser.add_argument("src", help="皮肤文件名")
    parser.add_argument(
        "dest", help="输出文件夹名，默认与皮肤文件名相同", nargs="?", default=None
    )
    parser.add_argument(
        "-t",
        "--type",
        help="要解压的皮肤格式，默认 ssf",
        default="ssf",
        choices=["ssf"],
    )
    parser.add_argument(
        "-f",
        "--force",
        help="若输出文件（夹）名称已被占用，强制删除",
        action="store_true",
    )
    args = parser.parse_args()

    if args.dest == None:
        args.dest = os.path.splitext(args.src)[0]

    if not os.path.exists(args.src):
        sys.stderr.write("输入 %s 不存在\n" % args.src)
        return 1
    if not os.path.isfile(args.src):
        sys.stderr.write("输入 %s 不是文件\n" % args.src)
        return 1
    if os.path.exists(args.dest):
        if args.force:
            if os.path.isdir(args.dest):
                shutil.rmtree(args.dest)
            else:
                os.remove(args.dest)
        else:
            sys.stderr.write("输出文件（夹） %s 已存在\n" % args.dest)
            return 1
    else:
        os.mkdir(args.dest)

    return extract_ssf(args.src, args.dest)


def package():
    assert False
    if args.zip:
        file_list = os.listdir(skin_dir)
        with zipfile.ZipFile(args.dest, "w") as zf:
            for file in file_list:
                zf.write(skin_dir + os.sep + file, file)
        shutil.rmtree(tmp_dir)
        err = 0
    return
