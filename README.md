# 简介

![gplv3](./gplv3-with-text-136x68.png) 

一个将皮肤从搜狗格式转换为 fcitx/fcitx5 格式的脚本，如果您在寻找“原生”的fcitx5皮肤，可以看[这里](https://github.com/topics/fcitx5-theme)

新开了仓库，因为作者的账号很久没有活动过，我所做的改动也很大：

1. 制成 python 包，用户不需要自己装依赖了
2. 重构，减少重复，将原先的脚本拆分为解包和转换两部分
3. 注册命令行程序、调整命令行参数、中文本地化
4. 由于使用了match case语法，python版本要求上升到3.10，如果想用旧版本python运行，请自行把相关代码改回长串 if elif （但这一切值得吗.jpg）

程序的目的没有变，所以原作者的[参考图像](https://www.fkxxyz.com/d/ssfconv)依然适用

# 安装
## 手动

clone或下载release

```shell
python -m venv venv_name
source venv_name/bin/activate
pip install .
```

## pip

[ ] 上传到 pypi

```shell
pip install ssfconv
```

# 使用

本包提供的命令行程序加 `-h` 参数就可以查看帮助

## 获取皮肤

可以从[搜狗的皮肤站](https://pinyin.sogou.com/skins/)下载自己喜欢的皮肤，得到ssf格式的文件，例如 【雨欣】蒲公英的思念.ssf

## 解包 ssf 皮肤

```shell
ssfunpack 【雨欣】蒲公英的思念.ssf
```

得到的文件夹可供 `ssfconv` 使用

## 转换为 fcitx 皮肤

```shell
ssfconv -t fcitx 【雨欣】蒲公英的思念
```

复制到用户皮肤目录

```shell
mkdir -p ~/.config/fcitx/skin/
cp -r 【雨欣】蒲公英的思念  ~/.config/fcitx/skin/
```

右键输入法托盘图表，选中皮肤，这款皮肤是不是出现在列表里了呢，尽情享用吧。

## 转换为 fcitx5 主题

```shell
ssfconv 【雨欣】蒲公英的思念
```

复制到用户主题目录

```shell
mkdir -p ~/.local/share/fcitx5/themes/
cp -r 【雨欣】蒲公英的思念  ~/.local/share/fcitx5/themes/
```

打开 fcitx5 的配置，附加组件标签，经典用户界面，点配置，在主题的下拉列表里，选择这款皮肤。

或者你也可以直接修改配置文件 ~/.config/fcitx5/conf/classicui.conf，将 Theme 的值改成这个皮肤的名称即可。

查看该皮肤在配置文件中的名称：

```shell
grep Name ~/.local/share/fcitx5/themes/【雨欣】蒲公英的思念/theme.conf
```

# 微调

转换得到的皮肤配置或多或少会有点瑕疵，其实调整它们并不困难，快去试试吧

# 已知缺陷

## fcitx5

- fcitx5 能够完美地像搜狗输入法一样调整，但是主题中所设置的字体是无效的，需要手动设置字体，经过 fkxxyz 反复实验，将字体设置为 "Sans 10" 似乎是大多数皮肤的最佳体验。
- 菜单字体颜色无法通过主题调整，只能为黑色高亮白色，所以在背景比较黑或者比较白的皮肤下，菜单可能体验不理想。
- 可能有皮肤转换效果不太好，欢迎提出 pr 改进。

## fcitx

- 因为 fcitx 的限制，输入框里只能对文字的外边距进行设置，无法像搜狗输入法一样任意调整坐标，导致部分皮肤只能在图片拉升和文件位置靠右来二选一的取舍。不过大多数皮肤都能挺不错的转换，只有少数皮肤实在是没办法了，只好用图片拉升代替（VOID001 是将文字调整到靠右，留了很多空白）。

# 致谢

前两位作者的仓库分别在
- https://github.com/fkxxyz/ssfconv
- https://github.com/VOID001/ssf2fcitx

前两位作者的账号都不活动，也许已经对系统美化不感兴趣了。不管怎样，我把他们写在了 `pyproject.toml` 中，在此对他们表示感谢。( •ᴗ• )

还要感谢 [`那些时光.ssf`](https://pinyin.sogou.com/d/skins/download.php?skin_id=344544) 的作者 szwjerry ，为了用上这个皮肤，我才接触到这个工具。

# 贡献征集
## 方格示意

需要一个调试工具，能依据转换后的皮肤配置文件在图片上划线，用以表明这个皮肤是怎样被拉伸的

考虑到这和转换的过程无关，更像是一个独立的程序

## 更多整理

转换部分的主函数仍然非常长，需要拆分，有部分固定的配置可以抽离出来以模板文件的形式存在

## IBus

```
GNOME桌面和非GNOME桌面的IBus采用了两个不同的前端。非GNOME桌面的IBus是项目自己本身基于GTK写的一个很简陋的前端，其使用GTK主题，根据我之前的研究，要实现搜狗那样的皮肤效果应该不太可能。GNOME在他们的GJS代码库里给IBus重写了一个前端，他们的前端可定制性更强，主要是使用CSS文件指定样式
@HollowMan6
```

仅靠转换程序做不到在 IBus 上实现搜狗这种美观的皮肤效果，看样子最有希望的办法是通过 GNOME Shell 扩展修改输入法前端，先行提供背景图片等素材的显示和拉伸/压缩的能力