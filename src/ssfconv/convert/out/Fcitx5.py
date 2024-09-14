from ssfconv.convert.image_operation import *
from ssfconv.convert.ini_ssf_operation import *

def makeConfFromSsf(ssf):
    skin = CaseSensitiveConfigParser(allow_no_value = True)

    skin['Metadata'] = {
        # 皮肤名称
        'Name': ssf['General']['skin_name'],

        # 皮肤版本
        'Version': ssf['General']['skin_version'],

        # 皮肤作者
        'Author': ssf['General']['skin_author'],

        # 描述
        'Description': ssf['General']['skin_info'],

        # 用 DPI 缩放
        'ScaleWithDPI': 'False',
    }
    return skin


def ssf2fcitx5(skin_dir):
    """
        转换为 fcitx5 格式
        将解压后的 ssf 皮肤，在里面创建出 theme.conf
    """

    ssfw = SsfIniWrapper(skin_dir)
    ssf=ssfw.getRawIni() 

    skin=makeConfFromSsf(ssf)

    # 根据里面所有的图片，根据所设置的拉伸区域确定合适的背景色
    def findBackgroundColor():
        for key in (('Scheme_V1','pic'),
                    ('Scheme_V2','pinyin_pic'),
                    ('Scheme_V2','zhongwen_pic'),
                    ('Scheme_H1','pic'),
                    ('Scheme_H2','pinyin_pic'),
                    ('Scheme_H2','zhongwen_pic'),
                    ):
            # 排除不存在的键值
            image_name = ssfw.get_image_config(key[0], key[1])
            if not image_name : continue

            # 排除区域不存在
            h_str = ssfw.try_get_value(key[0], key[1][:-3] + 'layout_horizontal')
            if not h_str : continue
            v_str = ssfw.try_get_value(key[0], key[1][:-3] + 'layout_vertical')
            if not v_str : continue

            # 得出区域
            h = h_str.split(',')
            v = v_str.split(',')
            if len(h) != 3 or len(v) != 3: continue

            # 排除平铺模式（筛选出是拉伸区域）
            #if int(h[0]) != 0 or int(v[0]) != 0:
            #    continue

            return getImageAvg(skin_dir + os.sep + image_name,
                        (int(h[1]),
                         -int(h[2]),
                         int(v[1]),
                         -int(v[2])))
        else:
            return (0, 0, 0)

    # 输入框（pre_edit）输入的拼音颜色
    input_color = colorConv(ssf['Display']['pinyin_color'])

    # 列表中第一个词的颜色
    first_color = colorConv(ssf['Display']['zhongwen_first_color'])

    # 列表中其他词的颜色
    other_color = colorConv(ssf['Display']['zhongwen_color'])

    # 根据里面所有的图片，根据所设置的拉伸区域确定合适的背景色
    back_color = findBackgroundColor()

    # 字体大小（像素）
    font_size = int(ssf['Display']['font_size'])

    skin['InputPanel'] = {
        # 字体及其大小
        'Font': 'Sans %d' % font_size,

        # 非选中候选字颜色
        'NormalColor': '#%02x%02x%02x' % other_color,

        # 选中候选字颜色
        'HighlightCandidateColor': '#%02x%02x%02x' % first_color,

        # 高亮前景颜色(back_color输入字符颜色)
        'HighlightColor': '#%02x%02x%02x' % input_color,

        # 输入字符背景颜色
        'HighlightBackgroundColor': '#%02x%02x%02x' % back_color,

        #
        'Spacing': 3,
    }

    # 输入框背景图
    input_bar_image = ssfw.get_image_config('Scheme_H1', 'pic')
    input_bar_image_size = getImageSize(skin_dir + os.sep + input_bar_image)

    # 水平拉升区域
    lh = ssfw.try_get_value('Scheme_H1', 'layout_horizontal')
    if lh:
        lh = tuple(map(lambda s:int(s), lh.split(',')))
    else:
        lh = (0, 2, 2)

    # 垂直拉升区域
    lv = ssfw.try_get_value('Scheme_H1', 'layout_vertical')
    if lv:
        lv = tuple(map(lambda s:int(s), lv.split(',')))
    else:
        lv = (0, 2, 2)

    # 拼音边距
    pinyin_marge = ssfw.try_get_value('Scheme_H1', 'pinyin_marge')
    if pinyin_marge:
        pinyin_marge = tuple(map(lambda s:int(s), pinyin_marge.split(',')))
    else:
        assert False

    # 候选词边距
    zhongwen_marge = ssfw.try_get_value('Scheme_H1', 'zhongwen_marge')
    if zhongwen_marge:
        zhongwen_marge = tuple(map(lambda s:int(s), zhongwen_marge.split(',')))
    else:
        assert False

    # 分隔符长度
    sep = 1 if ssfw.try_get_value('Scheme_H1', 'separator') else 0

    # 恒等式：
    #   输入的拼音下方到候选词上方的距离：
    #     pinyin_marge[1] + sep + zhongwen_marge[0] = TextMargin.Bottom + TextMargin.Top
    #   输入的拼音上方到上方边界的距离：
    #     pinyin_marge[0] = ContentMargin.Top + TextMargin.Top
    #   候选词下方到下方边界的距离：
    #     zhongwen_marge[1] = ContentMargin.Bottom + TextMargin.Bottom
    #
    #
    #   这是四元一次方程组，由于只有三个方程，那么随便确定其中一个即可解得其它未知数。
    #     增加的方程：
    #       TextMargin.Bottom = (pinyin_marge[1] + sep + zhongwen_marge[0]) // 2

    distant_pinyin_zhongwen = pinyin_marge[1] + sep + zhongwen_marge[0]

    # 解得：
    TextMargin_Bottom = distant_pinyin_zhongwen // 2
    TextMargin_Top = distant_pinyin_zhongwen - TextMargin_Bottom
    ContentMargin_Top = pinyin_marge[0] - TextMargin_Top
    #ContentMargin_Bottom = zhongwen_marge[1] - TextMargin_Bottom
    ContentMargin_Bottom = input_bar_image_size[1] - \
            ContentMargin_Top - TextMargin_Top - font_size - TextMargin_Bottom - \
            TextMargin_Top - font_size - TextMargin_Bottom

    TextMargin_Top_Left = 5
    TextMargin_Top_Right = 5

    # 文字边距
    skin['InputPanel/TextMargin'] = {
        'Left': TextMargin_Top_Left,
        'Right': TextMargin_Top_Right,
        'Top': TextMargin_Top,
        'Bottom': TextMargin_Bottom,
    }

    # 输入框内容边距
    skin['InputPanel/ContentMargin'] = {
        'Left': max(pinyin_marge[2], zhongwen_marge[2]) - TextMargin_Top_Left,
        'Right': max(pinyin_marge[3], zhongwen_marge[3]) - TextMargin_Top_Right,
        'Top': ContentMargin_Top,
        'Bottom': ContentMargin_Bottom,
    }

    # 输入框背景图
    skin['InputPanel/Background'] = {
        'Image': input_bar_image,
    }

    # 输入框背景图的拉升区域
    skin['InputPanel/Background/Margin'] = {
        'Left': lh[1],
        'Right': lh[2],
        'Top': lv[1],
        'Bottom': lv[2],
    }


    # 绘制高亮的纯色图片
    # menu_highlight_color = rgbDistMax(first_color, input_color, other_color, back_color)
    Image.new('RGBA', (38,23), (0,0,0,0)).save(skin_dir + os.sep + 'highlight.png')

    # 高亮背景
    skin['InputPanel/Highlight'] = {
        'Image': 'highlight.png',
    }
    # 高亮背景边距
    skin['InputPanel/Highlight/Margin'] = {
        'Left': 5,
        'Right': 5,
        'Top': 5,
        'Bottom': 5,
    }


    # 绘制 prev.png 和 next.png 颜色为 '%d %d %d' % other_color
    savePolygon((16,24), ((5,6),(5,18),(11,12)), other_color, skin_dir + os.sep + 'next.png')
    savePolygon((16,24), ((11,6),(11,18),(5,12)), other_color, skin_dir + os.sep + 'prev.png')


    # 前一页的箭头
    skin['InputPanel/PrevPage'] = {
        'Image': 'prev.png',
    }
    skin['InputPanel/PrevPage/ClickMargin'] = {
        'Left': 5,
        'Right': 5,
        'Top': 4,
        'Bottom': 4,
    }
    # 后一页的箭头
    skin['InputPanel/NextPage'] = {
        'Image': 'next.png',
    }
    skin['InputPanel/NextPage/ClickMargin'] = {
        'Left': 5,
        'Right': 5,
        'Top': 4,
        'Bottom': 4,
    }

    # 竖排合窗口设置
    Scheme_V1_pic = ssfw.try_get_value('Scheme_V1', 'pic')

    # 水平拉升区域
    lh = ssfw.try_get_value('Scheme_V1', 'layout_horizontal')
    if lh:
        lh = tuple(map(lambda s:int(s), lh.split(',')))
    else:
        lh = None

    # 垂直拉升区域
    lv = ssfw.try_get_value('Scheme_V1', 'layout_vertical')
    if lv:
        lv = tuple(map(lambda s:int(s), lv.split(',')))
    else:
        lv = None

    # 拼音边距
    pinyin_marge = ssfw.try_get_value('Scheme_V1', 'pinyin_marge')
    if pinyin_marge:
        pinyin_marge = tuple(map(lambda s:int(s), pinyin_marge.split(',')))
    else:
        pinyin_marge = None

    # 候选词边距
    zhongwen_marge = ssfw.try_get_value('Scheme_V1', 'zhongwen_marge')
    if zhongwen_marge:
        zhongwen_marge = tuple(map(lambda s:int(s), zhongwen_marge.split(',')))
    else:
        zhongwen_marge = None

    if Scheme_V1_pic and lh and lv and pinyin_marge and zhongwen_marge:
        # 背景图片
        skin['Menu/Background'] = {
            'Image': Scheme_V1_pic,
        }

        # 背景图片拉升边距
        skin['Menu/Background/Margin'] = {
            'Left': lh[1],
            'Right': lh[2],
            'Top': lv[1],
            'Bottom': lv[2],
        }

        sep = 1 if ssfw.try_get_value('Scheme_V1', 'separator') else 0

        # 背景图片内容边距
        horizontal_margin = min(zhongwen_marge[2], zhongwen_marge[3])
        skin['Menu/ContentMargin'] = {
            # 左边距
            'Left': horizontal_margin,

            # 右边距
            'Right': horizontal_margin,

            # 上边距
            'Top': pinyin_marge[0] + pinyin_marge[1] + sep + zhongwen_marge[0],

            # 下边距
            'Bottom': zhongwen_marge[1],
        }
    else:
        # 构建纯色背景

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

        # 背景图片
        skin['Menu/Background'] = {
            'Image': 'menu.png',
        }

        # 背景图片拉升边距
        skin['Menu/Background/Margin'] = {
            'Left': 20,
            'Right': 20,
            'Top': 20,
            'Bottom': 20,
        }

        # 背景图片内容边距
        skin['Menu/ContentMargin'] = {
            # 左边距
            'Left': 8,

            # 右边距
            'Right': 8,

            # 上边距
            'Top': 8,

            # 下边距
            'Bottom': 8,
        }

    # 绘制高亮的透明图片
    #menu_highlight_color = rgbDistMax((255,255,255), back_color, input_color, first_color, other_color)
    Image.new('RGBA', (38,23), (0,0,0,0)).save(skin_dir + os.sep + 'menu_highlight.png')

    # 高亮背景
    skin['Menu/Highlight'] = {
        'Image': 'menu_highlight.png',
    }
    # 高亮背景边距
    skin['Menu/Highlight/Margin'] = {
        'Left': 10,
        'Right': 10,
        'Top': 5,
        'Bottom': 5,
    }

    # 分隔符颜色
    skin['Menu/Separator'] = {
        'Color': '#%02x%02x%02x' % other_color,
    }

    # 用纯背景色构建出本主题的 radio.png
    img = Image.open(default_radio_img_bin)
    a = np.array(img)
    for i in range(len(a)):
        for j in range(len(a[0])):
            if a[i][j][3]:
                a[i][j][0] = other_color[0]
                a[i][j][1] = other_color[1]
                a[i][j][2] = other_color[2]
    img = Image.fromarray(a)
    img.save(skin_dir + os.sep + 'radio.png')

    # 复选框图片
    skin['Menu/CheckBox'] = {
        'Image': 'radio.png',
    }

    # 绘制箭头图片
    savePolygon((6,12), ((0,0),(6,6),(0,12)), other_color, skin_dir + os.sep + 'arrow.png')

    # 箭头图片
    skin['Menu/SubMenu'] = {
        'Image': 'arrow.png',
    }

    # 菜单文字项边距
    skin['Menu/TextMargin'] = {
        # 左边距
        'Left': 5,

        # 右边距
        'Right': 5,

        # 上边距
        'Top': 5,

        # 下边距
        'Bottom': 5,
    }

    skin.write(open(skin_dir + os.sep + 'theme.conf', 'w', encoding="utf-8"), False)
    return 0
