# 图片处理工具

> 整理图片处理工具

## 1. 获取图片exif信息

- 使用第三方库

```bash
$ pip install exifread
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
|                      |             |                           |
|                      |             |                           |
|                      |             |                           |

## 2. 批量写入exif信息到图片里

- 使用第三方库

```bash
$ pip install PIL
```

- 效果

![](./images/after_exif_setting/DSC05247-21.JPG)

![](./images/after_exif_setting/IMG_9325.JPG)


