from ..image_operation import *
from ..ini_ssf_operation import *

#TODO 用pathlib 替换
import os

# 创建符号链接的函数（若存在则覆盖）
def symlinkF(src, dst):
    if os.path.isfile(dst):
        os.remove(dst)
    return os.symlink(src, dst)

def makeConfFromSsf(ssf):
    skin = CaseSensitiveConfigParser(allow_no_value = True)

    skin['SkinInfo'] = {
        # 皮肤名称
        'Name': ssf['General']['skin_name'],

        # 皮肤版本
        'Version': ssf['General']['skin_version'],

        # 皮肤作者
        'Author': ssf['General']['skin_author'],

        # 描述
        'Desc': ssf['General']['skin_info'],
    }
    return skin


def ssf2fcitx(skin_dir:str):
    """
        转换为 fcitx 格式
        将解压后的 ssf 皮肤，在里面创建出 fcitx_skin.conf
    """
    
    ssfw = SsfIniWrapper(Path(skin_dir))
    ssf=ssfw.getRawIni() 

    skin=makeConfFromSsf(ssf)

    # 输入框输入的拼音颜色
    input_color = colorConv(ssf['Display']['pinyin_color'])

    # 列表中第一个词的颜色
    first_color = colorConv(ssf['Display']['zhongwen_first_color'])

    # 列表中其他词的颜色
    other_color = colorConv(ssf['Display']['zhongwen_color'])

    # 根据里面所有的图片，根据所设置的拉伸区域确定合适的背景色
    back_color = ssfw.findBackgroundColor()

    # 字体大小（像素）
    font_size = int(ssf['Display']['font_size'])

    # 状态栏背景图
    static_bar_image = ssfw.get_image_config('StatusBar', 'pic')

    # 中/英文状态
    cn_status_image = ssfw.get_image_config('StatusBar', 'cn_en', 0)
    en_status_image = ssfw.get_image_config('StatusBar', 'cn_en', 1)

    # 全半角状态
    quan_status_image = ssfw.get_image_config('StatusBar', 'quan_ban', 0)
    ban_status_image = ssfw.get_image_config('StatusBar', 'quan_ban', 1)

    # 中/英文标点状态
    cn_p_status_image = ssfw.get_image_config('StatusBar', 'biaodian', 0)
    en_p_status_image = ssfw.get_image_config('StatusBar', 'biaodian', 1)

    # 繁/简状态
    simp_status_image = ssfw.get_image_config('StatusBar', 'fan_jian', 1)
    trad_status_image = ssfw.get_image_config('StatusBar', 'fan_jian', 0)

    # 虚拟键盘状态
    vk_inactive_status_image = ssfw.get_image_config('StatusBar', 'softkeyboard')
    for mouse_status in ('down','in','out','downing'):
        vk_active_status_image = ssfw.get_image_config('StatusBar', 'softkeyboard_' + mouse_status)
        if vk_active_status_image:
            break

    icons = (cn_status_image, simp_status_image, trad_status_image,
                  quan_status_image, ban_status_image,
                  cn_p_status_image, en_p_status_image,
                  vk_inactive_status_image, vk_active_status_image)

    # 求图标的前景色（任意一个即可）
    for image in icons:
        if image:
            icon_color = getImageAvg(Path(skin_dir) / image)
            break
    else:
        icon_color = other_color

    skin['SkinFont'] = {
        # 字体大小
        'FontSize': font_size,

        # 菜单字体大小
        'MenuFontSize': 14,

        # 字体大小遵守dpi设置
        'RespectDPI': 'False',

        # 提示信息颜色
        'TipColor': '%d %d %d' % first_color,

        # 输入信息颜色
        'InputColor': '%d %d %d' % other_color,

        # 候选词索引颜色
        'IndexColor': '%d %d %d' % other_color,

        # 第一候选词颜色
        'FirstCandColor': '%d %d %d' % first_color,

        # 用户词组颜色
        'UserPhraseColor': '%d %d %d' % first_color,

        # 码表提示颜色
        'CodeColor': '%d %d %d' % input_color,

        # 其他颜色
        'OtherColor': '%d %d %d' % other_color,

        # 活动菜单项颜色
        'ActiveMenuColor': '%d %d %d' % \
            rgbDistMax(other_color,
                first_color, input_color, back_color, icon_color),

        # 非活动菜单项颜色+状态栏图标文字颜色
        'InactiveMenuColor': '%d %d %d' % \
            rgbDistMax(back_color,
                first_color, input_color, other_color, icon_color),
    }

    # 创建中文拼音状态图 pinyin.png
    if cn_status_image:
        symlinkF(cn_status_image, skin_dir + os.sep + 'pinyin.png')

    # 创建全/半角状态图 fullwidth_active.png / fullwidth_inactive.png
    if quan_status_image:
        symlinkF(quan_status_image, skin_dir + os.sep + 'fullwidth_active.png')
    if ban_status_image:
        symlinkF(ban_status_image, skin_dir + os.sep + 'fullwidth_inactive.png')

    # 创建中/英文标点状态图 punc_active.png / punc_inactive.png
    if cn_p_status_image:
        symlinkF(cn_p_status_image, skin_dir + os.sep + 'punc_active.png')
    if en_p_status_image:
        symlinkF(en_p_status_image, skin_dir + os.sep + 'punc_inactive.png')

    # 创建繁/简状态图 chttrans_inactive.png / chttrans_active.png
    if simp_status_image:
        symlinkF(simp_status_image, skin_dir + os.sep + 'chttrans_inactive.png')
    if trad_status_image:
        symlinkF(trad_status_image, skin_dir + os.sep + 'chttrans_active.png')

    # 创建虚拟键盘状态图 vk_inactive.png / vk_active.png
    if vk_inactive_status_image:
        symlinkF(vk_inactive_status_image, skin_dir + os.sep + 'vk_inactive.png')
    if vk_active_status_image:
        symlinkF(vk_active_status_image, skin_dir + os.sep + 'vk_active.png')

    # 求搜狗状态栏上几个按钮的坐标的最值
    x_min = y_min = 65536
    x_max = y_max = 0
    for button in ('cn_en',
                   'biaodian',
                   'quan_ban',
                   'quan_shuang',
                   'fan_jian',
                   'softkeyboard',
                   'menu',
                   'sogousearch',
                   'passport',
                   'skinmanager'):
        display = ssfw.try_get_value('StatusBar', button + '_display')
        if display != '1': continue
        pos = ssfw.try_get_value('StatusBar', button + '_pos').split(',')
        if len(pos) != 2: continue

        # 取最值
        if int(pos[0]) < x_min: x_min = int(pos[0])
        if int(pos[1]) < y_min: y_min = int(pos[1])

        # 得到图标尺寸
        icon_image = ssfw.get_image_config('StatusBar', button, 0)
        if not icon_image: continue
        size = getImageSize(skin_dir + os.sep + icon_image)

        # 取最右值
        x = int(pos[0]) + size[0]
        if x > x_max: x_max = x

        y = int(pos[1]) + size[1]
        if y > y_max: y_max = y

    # 得出合适的右边距和下边距
    if static_bar_image:
        size = getImageSize(skin_dir + os.sep + static_bar_image)
        MarginRight = size[0] - x_max + 4
        MarginBottom = size[1] - y_max + 4
    else:
        MarginRight = 4
        MarginBottom = 4

    skin['SkinMainBar'] = {
        # 背景图片
        'BackImg': static_bar_image,

        # Logo图标
        'Logo': '',

        # 英文模式图标
        'Eng': en_status_image,

        # 激活状态输入法图标
        'Active': cn_status_image,

        # 左边距
        'MarginLeft': x_min+4,

        # 右边距
        'MarginRight': MarginRight,

        # 上边距
        'MarginTop': y_min+4,

        # 下边距
        'MarginBottom': MarginBottom,

        # 可点击区域的左边距
        #ClickMarginLeft=0
        # 可点击区域的右边距
        #ClickMarginRight=0
        # 可点击区域的上边距
        #ClickMarginTop=0
        # 可点击区域的下边距
        #ClickMarginBottom=0
        # 覆盖图片
        #Overlay=
        # 覆盖图片停靠位置
        # Available Value:
        # TopLeft
        # TopCenter
        # TopRight
        # CenterLeft
        # Center
        # CenterRight
        # BottomLeft
        # BottomCenter
        # BottomRight
        #OverlayDock=TopLeft
        # 覆盖图片 X 偏移
        #OverlayOffsetX=0
        # 覆盖图片 Y 偏移
        #OverlayOffsetY=0
        # 纵向填充规则
        # Available Value:
        # Copy
        # Resize
        #FillVertical=Resize
        # 横向填充规则
        # Available Value:
        # Copy
        # Resize
        #FillHorizontal=Resize
        # 使用自定的文本图标颜色
        # Available Value:
        # True False
        #UseCustomTextIconColor=True
        # 活动的文本图标颜色
        #ActiveTextIconColor=101 153 209
        # 非活动的文本图标颜色
        #InactiveTextIconColor=101 153 209
        # 特殊图标位置
        #Placement=
    }


    # 输入框背景图
    input_bar_image = ssfw.get_image_config('Scheme_H1', 'pic')
    input_bar_image_size = getImageSize(skin_dir + os.sep + input_bar_image)

    # 绘制 prev.png 和 next.png 颜色为 '%d %d %d' % other_color
    savePolygon((6,12), ((0,0),(6,6),(0,12)), other_color, skin_dir + os.sep + 'next.png')
    savePolygon((6,12), ((0,6),(6,0),(6,12)), other_color, skin_dir + os.sep + 'prev.png')

    # 水平边距
    lh = ssfw.try_get_value('Scheme_H1', 'layout_horizontal')
    if lh:
        lh = tuple(map(lambda s:int(s), ssf['Scheme_H1']['layout_horizontal'].split(',')))
    else:
        lh = (0, 0, 0)

    # 竖直边距
    pinyin_marge = ssfw.try_get_value('Scheme_H1', 'pinyin_marge')
    if pinyin_marge:
        pinyin_marge = tuple(map(lambda s:int(s), pinyin_marge.split(',')))
    else:
        assert False
    zhongwen_marge = ssfw.try_get_value('Scheme_H1', 'zhongwen_marge')
    if zhongwen_marge:
        zhongwen_marge = tuple(map(lambda s:int(s), zhongwen_marge.split(',')))
    else:
        assert False
    separator = ssfw.try_get_value('Scheme_H1', 'separator')
    sep = 1 if separator else 0
    InputPos = pinyin_marge[0] + font_size
    OutputPos = pinyin_marge[0] + pinyin_marge[1] + font_size + \
            sep + zhongwen_marge[0] + font_size
    MarginBottom = input_bar_image_size[1] - OutputPos
    if lh[1] - pinyin_marge[2] > 32:
        MarginLeft = pinyin_marge[2]
    else:
        MarginLeft = lh[1]

    skin['SkinInputBar'] = {
        # 背景图片
        'BackImg': input_bar_image,

        # 左边距
        'MarginLeft': MarginLeft,

        # 右边距
        'MarginRight': lh[2],

        # 上边距
        'MarginTop': 0,

        # 下边距
        'MarginBottom': MarginBottom,

        # 可点击区域的左边距
        #ClickMarginLeft=0
        # 可点击区域的右边距
        #ClickMarginRight=0
        # 可点击区域的上边距
        #ClickMarginTop=0
        # 可点击区域的下边距
        #ClickMarginBottom=0
        # 覆盖图片
        #Overlay=hangul.png
        # 覆盖图片停靠位置
        # Available Value:
        # TopLeft
        # TopCenter
        # TopRight
        # CenterLeft
        # Center
        # CenterRight
        # BottomLeft
        # BottomCenter
        # BottomRight
        #OverlayDock=TopRight
        # 覆盖图片 X 偏移
        #OverlayOffsetX=-26
        # 覆盖图片 Y 偏移
        #OverlayOffsetY=2

        # 光标颜色
        'CursorColor': '%d %d %d' % first_color,

        # 预编辑文本的位置或偏移
        'InputPos': InputPos,

        # 候选词表的位置或偏移
        'OutputPos': OutputPos,

        # 上一页图标
        'BackArrow': 'prev.png',

        # 下一页图标
        'ForwardArrow': 'next.png',

        # 上一页图标的横坐标
        'BackArrowX': lh[2] - lh[1] + 10,

        # 上一页图标的纵坐标
        'BackArrowY': pinyin_marge[0],

        # 下一页图标的横坐标
        'ForwardArrowX': lh[2] - lh[1],

        # 下一页图标的纵坐标
        'ForwardArrowY': pinyin_marge[0],

        # 纵向填充规则
        # Available Value:
        # Copy
        # Resize
        #FillVertical=Resize
        # 横向填充规则
        # Available Value:
        # Copy
        # Resize
        #FillHorizontal=Resize
    }

    # 使用系统默认的 active.png 和 inactive.png
    symlinkF('/usr/share/fcitx/skin/default/active.png',
               skin_dir + os.sep + 'active.png')
    symlinkF('/usr/share/fcitx/skin/default/inactive.png',
               skin_dir + os.sep + 'inactive.png')

    skin['SkinTrayIcon'] = {
        # 活动输入法图标
        'Active': 'active.png',

        # 非活动输入法图标
        'Inactive': 'inactive.png',
    }

    # 用纯背景色构建出本主题的 menu.png
    img = Image.open(default_menu_img_bin)
    a = np.array(img)
    for i in range(len(a)):
        for j in range(len(a[0])):
            if a[i][j][3]:
                a[i][j][0] = back_color[0]
                a[i][j][1] = back_color[1]
                a[i][j][2] = back_color[2]
    img = Image.fromarray(a)
    img.save(skin_dir + os.sep + 'menu.png')

    skin['SkinMenu'] = {
        # 背景图片
        'BackImg': 'menu.png',

        # 上边距
        'MarginTop': 8,

        # 下边距
        'MarginBottom': 8,

        # 左边距
        'MarginLeft': 8,

        # 右边距
        'MarginRight': 8,

        # 活动菜单项颜色
        'ActiveColor': '%d %d %d' % other_color,

        # 分隔线颜色
        'LineColor': '%d %d %d' % other_color,
    }

    skin['SkinKeyboard'] = {
        # 虚拟键盘图片
        #BackImg=keyboard.png

        # 软键盘按键文字颜色
        #'KeyColor': '%d %d %d' % first_color,
    }

    skin.write(open(skin_dir + os.sep + 'fcitx_skin.conf', 'w', encoding="utf-8"), False)
    return 0