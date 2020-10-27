# -*- coding: utf-8 -*-

from PIL import Image, ImageStat
import math
im = Image.open("image_tools/test_insert_exif/IMG_9477.JPG")
from ..base_tools.time_cost import time_cost
# 测试获取一块区域的图片
# 测试图片的平均亮度


@time_cost
def get_image_light_mean(img):
    im = img.convert('L')
    stat = ImageStat.Stat(im)
    return stat.mean[0]

@time_cost
def get_image_light_rms(img):
    im = img.convert('L')
    stat = ImageStat.Stat(im)
    return stat.rms[0]

@time_cost
def get_image_light_mean_sqrt(img):
    stat = ImageStat.Stat(img)
    r, g, b = stat.mean
    return math.sqrt(0.241 * (r ** 2) + 0.691 * (g ** 2) + 0.068 * (b ** 2))

@time_cost
def get_image_light_rms_sqrt(img):
    stat = ImageStat.Stat(img)
    r, g, b = stat.rms
    return math.sqrt(0.241 * (r ** 2) + 0.691 * (g ** 2) + 0.068 * (b ** 2))

@time_cost
def get_image_light_gs(img):
    stat = ImageStat.Stat(img)
    gs = (math.sqrt(0.241 * (r ** 2) + 0.691 * (g ** 2) + 0.068 * (b ** 2))
          for r, g, b in img.getdata())
    return sum(gs) / stat.count[0]


if __name__ == '__main__':

    width, height = im.size
    # left, top, right, bottom 逆时针
    crop_rectangle = (0, 0, width / 6, height / 6)
    cropped_im = im.crop(crop_rectangle)

    print("get_image_light_mean", get_image_light_mean(cropped_im))

    print("get_image_light_rms", get_image_light_rms(cropped_im))

    print("get_image_light_mean_sqrt", get_image_light_mean_sqrt(cropped_im))

    print("get_image_light_rms_sqrt", get_image_light_rms_sqrt(cropped_im))

    print("get_image_light_gs", get_image_light_gs(cropped_im))


