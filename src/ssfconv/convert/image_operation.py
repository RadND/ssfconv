from PIL import Image, ImageDraw
import numpy as np


def getImageAvg(image_path, area=(0, 0, 0, 0)):
    """
    获取图片的像素平均值
        image_path 图片的路径
        aria 是需要求的平均值的区域，默认整幅图
            格式 area = (x1,x2,y1,y2)
            当 x2 或 y2 为零表示最大值直到边界
                        为负时表示距离最大边界多少的坐标
    返回 (r,g,b) 三元组
    """

    file = Image.open(image_path)
    size = file.size

    # 确定区域
    x1 = area[0] % size[0]
    x2 = area[1] % size[0]
    y1 = area[2] % size[1]
    y2 = area[3] % size[1]
    if x2 == 0:
        x2 = size[0]
    if y2 == 0:
        y2 = size[1]

    if x1 > x2:
        t = x1
        x1 = x2
        x2 = t
    if y1 > y2:
        t = y1
        y1 = y2
        y2 = t
    if x1 == x2:
        if x2 != size[0]:
            x2 += 1
        else:
            x1 -= 1
    if y1 == y2:
        if y2 != size[1]:
            y2 += 1
        else:
            y1 -= 1

    # 算出区域内所有像素点的平均值
    img = np.asarray(file)
    r = g = b = 0
    count = 0
    """
    NOTE https://github.com/fkxxyz/ssfconv/issues/20
    此处会溢出，不影响最终结果，问题不大
    """
    if img.shape[2] == 4:
        for y in range(y1, y2):
            for x in range(x1, x2):
                if img[y][x][3] > 0:
                    r += img[y][x][0]
                    g += img[y][x][1]
                    b += img[y][x][2]
                    count += 1
    else:
        for y in range(y1, y2):
            for x in range(x1, x2):
                r += img[y][x][0]
                g += img[y][x][1]
                b += img[y][x][2]
                count += 1
    if count == 0:
        count = 1
    r //= count
    g //= count
    b //= count
    return (r, g, b)


# 获取图片大小的函数
def getImageSize(image_file):
    size = Image.open(image_file).size
    assert size[0] > 0 and size[0] < 65536 and size[1] > 0 and size[1] < 65536
    return size


# 保存一个多边形到文件
def savePolygon(size, points, color, out_file):
    img = Image.new("RGBA", size)
    draw = ImageDraw.Draw(img)
    draw.polygon(points, fill=color)
    img.save(out_file)


def rgbDistSqure(c1, c2):
    """
    简单的计算两个颜色之间的距离
    """
    dr = c1[0] - c2[0]
    dg = c1[1] - c2[1]
    db = c1[2] - c2[2]
    return dr * dr + dg * dg + db * db


def rgbDistMax(color, *colors):
    """
    求 colors 中与 color 的距离最大的颜色
    """
    max_dist = 0
    max_dist_color = colors[0]
    for c in colors:
        # basic-colormath 的距离计算方法更精确，但这一切值得吗
        cur_dist = rgbDistSqure(color, c)
        if max_dist < cur_dist:
            max_dist = cur_dist
            max_dist_color = c
    return max_dist_color
