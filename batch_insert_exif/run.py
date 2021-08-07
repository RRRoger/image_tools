# -*- coding: utf-8 -*-

"""
\b
* * * * * * * * * * * * * * * * * * * * * * * * *
批量写入照片Exif信息


\b 
Author: Roger;
Python Version: python 3.7+;
Python Libraries:
    click: https://click-docs-zh-cn.readthedocs.io/zh/latest/
    exifread: https://pypi.org/project/ExifRead/
    Pillow: https://pillow.readthedocs.io/en/stable/
* * * * * * * * * * * * * * * * * * * * * * * * *
"""

from PIL import ImageFont, ImageDraw, Image, ImageStat
import exifread
import os
import click
import piexif
import pickle
import copy

FONT = "SourceHanSansCN-Normal.otf"                # 思源字体
QUALITY = 50                                       # 导出图片质量
FONT_SIZE = 80                                     # 字体大小
FONT_DEFAULT_COLOR = (0, 0, 0)                     # 字体颜色
START_POSITION = (50, 50)                          # 字体起始位置
IMAGE_SUFFIX = ['jpeg', 'jpg']                     # 图片格式列表
BLACK_DIR_LIST = []                                # 不参与处理的目录
DIR_AFTER = 'AFTER'                                # 处理好的图片存放路径
COLOR_WHITE = (255, 255, 255)                      # 白色颜色色值
COLOR_BLACK = (0, 0, 0)                            # 黑色颜色色值


# 显示文本信息
SHOW_TEXT = u"""相机: %(camera)s
镜头: %(lens)s
光圈: %(aperture)s
快门: %(shutterspeed)s
iso: %(iso)s"""

def format_aperture(val):
    """
        get image's aperture info: return float
        获取图片光圈信息
    """
    val = str(val)
    nums = val.split('/')
    if len(nums) > 1:
        return float(nums[0]) / float(nums[1])
    else:
        return val


def mkdir_safe(_path):
    """make dir if exists then pass"""
    if not os.path.exists(_path):
        os.mkdir(_path)
    return _path


def check_is_image(f_name):
    """ if the file is an image return True  """
    for suffix in IMAGE_SUFFIX:
        if f_name.lower().endswith("." + suffix):
            return True
    return False


def get_exif_info(tags):
    """ 获取EXIF具体信息 """
    brand = tags.get('Image Make', '')                 # 相机品牌
    model = tags.get('Image Model', '')                # 相机型号
    date = tags.get('Image DateTime', '')              # 拍摄时间
    shutterspeed = tags.get('EXIF ExposureTime', '')   # 快门
    focallength = tags.get('EXIF FocalLength', '')     # 使用焦段
    aperture = tags.get('EXIF FNumber', '')            # 光圈
    iso = tags.get('EXIF ISOSpeedRatings', '')         # iso
    lens = tags.get('EXIF LensModel', '')              # 镜头信息
    aperture = format_aperture(aperture)

    return {
        "camera": "%s | %s" % (brand, model),
        "lens": lens,
        "aperture": aperture,
        "shutterspeed": shutterspeed,
        "iso": iso,
    }


def get_image_light_mean(img):
    """ 获取图片平均亮度 0~255 """
    im = img.convert('L')
    stat = ImageStat.Stat(im)
    return stat.mean[0]


def judge_font_color(img):
    """ 判断文字用白色还是黑色 """
    ratio = 1.0 / 6
    width, height = img.size

    # 获取图片的一块区域 left, top, right, bottom 逆时针
    crop_rectangle = (0, 0, width * ratio, height * ratio)
    cropped_im = img.crop(crop_rectangle)
    brightness = get_image_light_mean(cropped_im)

    # 如果小于128,则判断图片为暗的
    if brightness < 128:
        return "White"
    else:
        return "Black"


def do_write(source, dest, font_name=None, font_size=40, quality=50):
    
    print(f"[Writing]: {dest}")

    with open(source, 'rb') as f:
        tags = exifread.process_file(f)
        exif_info = get_exif_info(tags)

    show_text = SHOW_TEXT % exif_info

    image = Image.open(source)

    # TODO: keep exif info from src image
    # exif = image.getexif()
    color = judge_font_color(image)
    draw = ImageDraw.Draw(image)

    if font_name:
        font = ImageFont.truetype(font_name, font_size)
    else:
        font = None

    if color == 'Black':
        font_color = COLOR_BLACK
    elif color == 'White':
        font_color = COLOR_WHITE
    else:
        font_color = COLOR_WHITE

    draw.text(START_POSITION, show_text, font_color, font=font)
    image.save(dest, format='JPEG', subsampling=0, quality=quality)


help_c = __doc__
help_p = "修改处理的图片路径"
help_q = f"图像质量(0, 95), 默认: {QUALITY}"
help_fs = f"字体大小, 默认: {FONT_SIZE}"
help_font = f"选择字体, 默认: {FONT}"


@click.command()
@click.help_option("-h", "--help", help=help_c)
@click.option("-p", "--images-dir", "images_dir", help=help_p, type=str, required=True)
@click.option("-q", "--quality", "quality", help=help_q, type=int, required=False, default=QUALITY)
@click.option("-fs", "--font-size", "font_size", help=help_fs, type=int, required=False, default=FONT_SIZE)
@click.option("-font", "--font", "font_name", help=help_font, type=str, required=False, default=FONT)
def main(images_dir, quality, font_size, font_name):
    dir_after = os.path.join(images_dir, DIR_AFTER)
    mkdir_safe(dir_after)

    print("************* Start *************")

    fn_list = sorted([f for f in os.listdir(images_dir)])
    for _i, fn in enumerate(fn_list):        

        # 判断文件是否是图片
        if not check_is_image(fn): continue

        f_path = os.path.join(images_dir, fn)  # 源文件路径
        dest_path = os.path.join(dir_after, fn)  # 目标文件路径

        # 调用处理图片函数
        do_write(f_path, dest_path, font_name=font_name, font_size=font_size, quality=quality)

    print("************* End *************")
    return "OK"


if __name__ == '__main__':
    main()




