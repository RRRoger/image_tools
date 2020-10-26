# -*- coding: utf-8 -*-
 
import exifread
import os
from PIL import ImageFont, ImageDraw, Image

FONT                = "SourceHanSansCN-Normal.otf" # 思源字体
QUALITY             = 30  # 导出图片质量
FONT_SIZE           = 80  # 字体大小
FONT_COLOR          = (0, 0, 0)  # 字体颜色
START_POSITION      = (50, 50)  # 字体起始位置
IMAGE_SUFFIX        = ['jpeg', 'jpg']  # 图片格式列表
BLACK_DIR_LIST      = []  # 不参与处理的目录

# 显示文本信息
SHOW_TEXT = u"""
相机: %(camera)s
镜头: %(lens)s
光圈: %(aperture)s
快门: %(shutterspeed)s
iso: %(iso)s
"""

def format_aperture(val):
    """ get image's aperture info: return float """
    val = str(val)
    nums = val.split('/')
    if len(nums) > 1:
        return float(nums[0]) / float(nums[1])
    else:
        return val


def check_is_image(f_name):
    " if the file is an image return True  "
    for suffix in IMAGE_SUFFIX:
        if f_name.lower().endswith("." + suffix):
            return True
    return False


def check_white_or_black(image):
    """ 判断图片给白字还是给黑字 """
    image.getcolors()
    rgb_start = image.getcolors()[0]
    rgb_end = image.getcolors()[-1]
    rgb_start_color,rgb_end_color = rgb_start[1],rgb_end[1]
    rgb_start_int,rgb_end_int = rgb_start[0],rgb_end[0]

    print(rgb_start,rgb_end)
    if rgb_start_int > rgb_end_int:
        if rgb_start_color == 0 or rgb_start_color == (0, 0, 0):
            return "White"
        else:
            return "Black"
    else:
        if rgb_start_color == 255 or rgb_start_color == (255, 255, 255):
            return "Black"
        else:
            return "White"    


def get_exif_info(tags):
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
        "camera": "%s %s" % (brand, model),
        "lens": lens,
        "aperture": aperture,
        "shutterspeed": shutterspeed,
        "iso": iso,
    }


def do_write(source, dest, font_name=None, font_size=40, quality=50):
    
    print("********** Write EXIF: %s ************" % dest)

    with open(source, 'rb') as f:
        tags = exifread.process_file(f)
        exif_info = get_exif_info(tags)

    show_text = SHOW_TEXT % exif_info

    image = Image.open(source)
    draw = ImageDraw.Draw(image)

    if font_name:
        font = ImageFont.truetype(font_name, font_size, encoding="unic")
    else:
        font = None

    

    draw.text(START_POSITION, show_text, FONT_COLOR, font=font)
    image.save(dest, quality=quality)


if __name__ == '__main__':

    # source = "/Users/chenpeng/Desktop/WechatIMG23064.jpeg"
    # dest = "/Users/chenpeng/Desktop/WechatIMG23064999.jpeg"
    # do_write(source, dest, font_name=FONT, font_size=FONT_SIZE, quality=QUALITY)

    dir_path = "/Users/chenpeng/Pictures/test_write_exif"
    dir_after = os.path.join(dir_path, 'AFTER')

    try:
        os.mkdir(dir_after)
    except OSError:
        pass

    print("************* Start *************")

    for i,j,k in os.walk(dir_path):
        # print(i, j, k)

        # 忽略AFTER目录;以及其他目录
        if i in [dir_after] + BLACK_DIR_LIST:
            continue

        for f_name in k:

            # 判断文件是否是图片
            if not check_is_image(f_name): continue

            f_path = os.path.join(dir_path, f_name)  # 源文件路径
            dest_path = os.path.join(dir_after, f_name)  # 目标文件路径

            # 处理函数
            do_write(f_path, dest_path, font_name=FONT, font_size=FONT_SIZE, quality=QUALITY)

    print("************* End *************")




