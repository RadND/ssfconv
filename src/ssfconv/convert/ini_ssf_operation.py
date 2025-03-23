from .CaseSensitiveConfigParser import CaseSensitiveConfigParser
from .image_operation import *
import io
from pathlib import Path
import sys


default_menu_img_bin = io.BytesIO(
    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00<\x00\x00\x00<\x08\x06\x00\x00\x00:\xfc\xd9r\x00\x00\x00\x04sBIT\x08\x08\x08\x08|\x08d\x88\x00\x00\x00\tpHYs\x00\x00\x1b\xaf\x00\x00\x1b\xaf\x01^\x1a\x91\x1c\x00\x00\x00\x19tEXtSoftware\x00www.inkscape.org\x9b\xee<\x1a\x00\x00\x01\xdaIDATh\x81\xed\x9b\xc1N\xdb@\x10@\xdf\x80\x15R\x08R\x10\xa4\x12\xbd\x84\x037\xbe\xa0\x9f\xd2/\xec'\xf0\t|\x04\x1c\xc8\t\t\x88\x9a\x127AHdz\x98\xdd\xd6\nI$\xa4\x10\xd8a\x9e\xb4\xb2\xec\xb5\xady\x1e{}\x99\x11U\xa5\x89\x88\xec\x02-@(\x1b\x05\x9eTu\xd2<(Y8\x89\x1e\x02\xfb@\x1b\x1f\xc2\x8f\xc0\x18\x18f\xf1\n\xfe\xc9\x1e\x03_\x81\x03\xe0\x0b>\x84\xa7\xc0/\xa0%\"7\xaa:\xa9\xd2\xe4!&\xfb\r\xe8\x01\x1d`\xeb]\xc2\\\x1f3\xa0\xc6\x92\x07\xf0\x04L\xaa\x94\xdd},\xb3=L\xfa\x18\xf8\x0e\xf41\xf9\x92\xa8\x81\x01p\x01\xdc\xa4cS\xe0\xb7\x88\xecV\xd8\x02\xd5\xc6\x9eD\x07\x93\xfd\x01\xecm>\xd6\xb5\xd0\x01\xce\x80\x13\xe0'\xf0\x80\xb9\xb5\x81V\x85}\xabyla\x99\xdd\x03\xae\x80.\xf6j\xe8\xfc]?(\xd9a\x04\x9cb.\x974\x1c\xab\x05\x17\xf5\xd3\xb6\x0b<o \xc8u\xa2X\xcc\xdd\xb4\xdf\x9f?a\xd1\xc2\x94\xbf\xd9\xd9\x1b\x05\xb5\tr\xec/\xd6\x9fU+q)\xaf\xf1\"\x96\xc6^\xfa\xaf\xe7\xd5\x84\xb0wB\xd8;!\xec\x9d\x10\xf6N\x08{'\x84\xbd\x13\xc2\xde\ta\xef\x84\xb0wB\xd8;!\xec\x9d\x10\xf6N\x08{'\x84\xbd\x13\xc2\xde\ta\xef\x84\xb0wB\xd8;!\xec\x9d\x10\xf6\xce*\xe1\x92\x0b\xc4\x97\xc6\xbeH\xb8^1W\n9\xf6z\xd9D\x93A\xda\x8e\x80m\xca\xca\xb4`1\x8f\xd2\xfe`\xfe\x84\n+\xc4\xccc\x86U\x92\x9f`\xf5\xc6\xa5r\x04\xfc\xc1\\r\xbd\xb7\x02\xba\x8de\xb9\x93Fn\xee\xb8\x06v\x80\xdc\xd2S\x125V\x14~\x8e\xb5\x00\x0c\xd3\xb8\x07\x86\x95\xaaNDd\x8cu\x7f\xe4\x86\x88\x87tQ\xc9\xe4&\x8f;\xccm\xdc\xecj\x19\xf2?\x93S\xfc\xb5\xf1\xdcb\x8e\x9f\xafQK>[+\xde_\xdfNz_\xa1?jm\x00\x00\x00\x00IEND\xaeB`\x82"
)
default_radio_img_bin = io.BytesIO(
    b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x18\x00\x00\x00\x18\x08\x06\x00\x00\x00\xe0w=\xf8\x00\x00\x00\tpHYs\x00\x00\r\xd7\x00\x00\r\xd7\x01B(\x9bx\x00\x00\x00\x19tEXtSoftware\x00www.inkscape.org\x9b\xee<\x1a\x00\x00\x00\x9dIDATH\x89\xed\x91\xc1\n\x830\x10Dg\x1a\xd0\x1f*\xbdfIoJ?\xb7-\xeda!G\xc1\x1fR\x88\xdb\x8b\xd2\x1e\x84\x08zk\xde1\xbb\x93\x07\xb3@\xa1P\xe0\xd6EUm\x9dsg\x00H)\xf5!\x84\xfba\x82\x18\xe3\xcb\xcc\x04@5?\r$\xd5{\xdf\xe4\xb2\xa7\xdc\x82\xaa\xb6f\xe6\x7f>\x07\x80\xda\xcc\xae1\xc6\xfd\x82\xb9\x96zeTM\xd3t\xd9-\xd8KV\x90R\xeaI\x8e+\xa3\x81d\x97\xcbo=\xf2\xc3\xcc\x02\xbeU\x8d\x00\xde"r;D0K\x9a\xa5s\x92\x9d\x88<\xb7f\x0b\x85\x7f\xe7\x03\xc2\x8b7\xa7\xab\xe8\x14\xb1\x00\x00\x00\x00IEND\xaeB`\x82'
)


class SsfIniWrapper:
    def __init__(self, skin_dir: Path):
        self.ssf = None
        self.skin_dir = skin_dir
        self.read_ssf_ini()

    def read_ssf_ini(self):
        """
        为了重复使用，不和init合并
        """
        skin_ini = self.skin_dir / "skin.ini"
        if not skin_ini.is_file():
            sys.stderr.write("找不到 skin.ini\n")
            return 1

        try:
            ssf_ini = CaseSensitiveConfigParser(allow_no_value=True)
            ssf_ini.read(skin_ini, encoding="utf-16")
        except:
            sys.stderr.write("读取 skin.ini 失败\n")
            return 2
        self.ssf = ssf_ini
        return

    def get_image_config(self, section, key, index=0):
        """
        获取图片文件名的函数（获取失败则返回空字符串）
        """
        image_name_list = self.ssf[section].get(key, "").split(",")
        if index < len(image_name_list):
            image_name = image_name_list[index]
            if (self.skin_dir / image_name).is_file():
                return image_name
        else:
            return ""

    def try_get_value(self, section, key):
        return self.ssf[section].get(key, "").strip()

    def getRawIni(self):
        # FIXME 允许写这个变量是坏主意，考虑使用私有变量或私有方法来暗示
        return self.ssf

    def findBackgroundColorBy(self, key):
        # 排除键值不存在
        image_name = self.get_image_config(key[0], key[1])
        if not image_name:
            return None

        # 排除区域不存在
        h_str = self.try_get_value(key[0], key[1][:-3] + "layout_horizontal")
        if not h_str:
            return None
        v_str = self.try_get_value(key[0], key[1][:-3] + "layout_vertical")
        if not v_str:
            return None

        # 得出区域
        h = h_str.split(",")
        v = v_str.split(",")
        if len(h) != 3 or len(v) != 3:
            return None

        # 排除平铺模式（筛选出是拉伸区域）
        # if int(h[0]) != 0 or int(v[0]) != 0:
        #    return None

        return getImageAvg(
            self.skin_dir / image_name,
            (int(h[1]), -int(h[2]), int(v[1]), -int(v[2])),
        )

    def findBackgroundColor(self):
        """
        根据里面所有的图片，根据所设置的拉伸区域确定合适的背景色
        不知道原作者为什么按顺序取到任意一张就完成
        """
        keys = (
            ("Scheme_V1", "pic"),
            ("Scheme_V2", "pinyin_pic"),
            ("Scheme_V2", "zhongwen_pic"),
            ("Scheme_H1", "pic"),
            ("Scheme_H2", "pinyin_pic"),
            ("Scheme_H2", "zhongwen_pic"),
        )
        for key in keys:
            avg_color = self.findBackgroundColorBy(key)
            if avg_color:
                return avg_color
        else:
            return (0, 0, 0)


# 将 skin.ini 的颜色转换成 (r,g,b) 三元组
def colorConv(ssf_color):
    color_int = int(ssf_color, 16)
    r = color_int % 256
    g = (color_int % 65536) // 256
    b = color_int // 65536
    return (r, g, b)
