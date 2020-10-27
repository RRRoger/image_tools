# -*- coding: utf-8 -*-
 
import exifread
import os
import sys
from PIL import ImageFont, ImageDraw, Image, ImageStat

FONT = "SourceHanSansCN-Normal.otf"                # 思源字体
QUALITY = 30                                       # 导出图片质量
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
iso: %(iso)s
"""

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
    try:
        os.mkdir(_path)
    except OSError:
        pass
    return _path


def check_is_image(f_name):
    """ if the file is an image return True  """
    for suffix in IMAGE_SUFFIX:
        if f_name.lower().endswith("." + suffix):
            return True
    return False


def get_exif_info(tags):
    """ 获取EXIF具体信息 """
    brand = tags.get('Image Make', '')  # 相机品牌
    model = tags.get('Image Model', '')  # 相机型号
    date = tags.get('Image DateTime', '')  # 拍摄时间
    shutterspeed = tags.get('EXIF ExposureTime', '')  # 快门
    focallength = tags.get('EXIF FocalLength', '')  # 使用焦段
    aperture = tags.get('EXIF FNumber', '')  # 光圈
    iso = tags.get('EXIF ISOSpeedRatings', '')  # iso
    lens = tags.get('EXIF LensModel', '')  # 镜头信息
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
    
    print("********** Insert EXIF Info: %s ************" % dest)

    with open(source, 'rb') as f:
        tags = exifread.process_file(f)
        exif_info = get_exif_info(tags)

    show_text = SHOW_TEXT % exif_info

    image = Image.open(source)
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
        font_color = FONT_COLOR

    draw.text(START_POSITION, show_text, font_color, font=font)
    image.save(dest, quality=quality)


def main(dir_path):
    dir_after = os.path.join(dir_path, DIR_AFTER)

    mkdir_safe(dir_after)

    print("************* Start *************")

    for root, dirs, files in os.walk(dir_path):
        
        # 忽略AFTER目录;以及其他自定义目录
        if root in [dir_after] + BLACK_DIR_LIST: continue

        for f_name in files:

            # 判断文件是否是图片
            if not check_is_image(f_name): continue

            f_path = os.path.join(dir_path, f_name)  # 源文件路径
            dest_path = os.path.join(dir_after, f_name)  # 目标文件路径

            # 调用处理图片函数
            do_write(f_path, dest_path, font_name=FONT, font_size=FONT_SIZE, quality=QUALITY)

    print("************* End *************")
    return "OK"


if __name__ == '__main__':
    dir_path = sys.argv[1]
    if dir_path == '/': raise OSError
    main(dir_path=dir_path)




