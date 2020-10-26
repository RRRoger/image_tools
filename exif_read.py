import exifread

def get_exif_info(tags):
    brand = tags['Image Make']  # 相机品牌
    model = tags['Image Model']  # 相机型号
    date = tags['Image DateTime']  # 拍摄时间
    shutterspeed = tags['EXIF ExposureTime']  # 快门
    focallength = tags['EXIF FocalLength']  # 使用焦段
    aperture = tags['EXIF FNumber']  # 光圈
    iso = tags['EXIF ISOSpeedRatings']  # iso
    lens = tags['EXIF LensModel']  # 镜头信息
    aperture = format_aperture(aperture)

    return {
        "camera": "%s %s" % (brand, model),
        "lens": lens,
        "aperture": aperture,
        "shutterspeed": shutterspeed,
        "iso": iso,
    }