# 图片处理工具

[![](https://img.shields.io/badge/version-python3.5+-green?style=flat-square)](https://www.python.org/downloads/)
[![GitHub last commit](https://img.shields.io/github/stars/RRRoger/image_tools.svg?style=flat-square)](https://github.com/RRRoger/image_tools)
[![GitHub issues](https://img.shields.io/github/issues/RRRoger/image_tools.svg?style=flat-square)](https://github.com/RRRoger/image_tools/issues)
[![GitHub last commit](https://img.shields.io/github/last-commit/RRRoger/image_tools.svg?style=flat-square)](https://github.com/RRRoger/image_tools/commits/master)
[![GitHub](https://img.shields.io/github/license/mashape/apistatus.svg?style=flat-square)](https://github.com/RRRoger/image_tools/blob/master/LICENSE)

> 整理图片处理工具
>
> - 请提前装好[思源字体](https://source.typekit.com/source-han-serif/cn/)(可**免费商用**)
>   - [https://source.typekit.com/source-han-serif/cn/](https://source.typekit.com/source-han-serif/cn/)
> - 安装依赖的python库
>   - `pip install -r requirements.txt`


## 1. 获取图片exif信息

> 参考链接: https://www.biaodianfu.com/exif-python.html
> Exif（Exchangeable image file format）是专门为数码相机的照片设定的，可以记录数码照片的属性信息和拍摄数据。
> Exif信息是镶嵌在 JPEG/TIFF 图像文件格式内的一组拍摄参数，它就好像是傻瓜相机的日期打印功能一样，只不过 Exif信息所记录的资讯更为详尽和完备。

- 使用第三方库 `exifread`

```bash
$ pip install exifread
```

- Function

```python
with open(source_path, 'rb') as f:
    tags = exifread.process_file(f)
```

- `tags`信息对照

| Tag Name             | Description | Note                      |
| -------------------- | ----------- | ------------------------- |
| Image Make           | 相机品牌    |                           |
| Image Model          | 相机型号    |                           |
| EXIF ExposureTime    | 快门        |                           |
| EXIF FocalLength     | 使用焦段    |                           |
| EXIF FNumber         | 光圈        | 显示7/5,需要手动处理成1.4 |
| EXIF ISOSpeedRatings | iso         |                           |
| EXIF LensModel       | 镜头信息    |                           |

## 2. 批量写入exif信息到图片里

- 使用第三方库 `Pillow`

```bash
$ pip install Pillow
```

- ***根据图片亮度自动识别出插入的字体颜色***

- **命令**:

```bash
cd image_tools/batch_insert_exif
# for help
python run -h

# demo
python run.py -p  /Users/chenpeng/Pictures/test_write_exif
```

​    

- 处理后效果

![](./images/after_exif_setting/DSC05247-21.JPG)

![](./images/after_exif_setting/IMG_9468.JPG)

