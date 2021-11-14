自己有这么一个需求，我想批量在照片显示相机，光圈，iso以及快门信息。
因为要经常用到，那为什么不自己写个脚本来实现，说干就干。

- 适用python版本：python3.5+
- 请提前装好[思源字体](https://github.com/adobe-fonts/source-han-sans)(可**免费商用**)，可选字体[霞婺文楷](https://github.com/lxgw/LxgwWenKai)(可**免费商用**)
- 源码：[image_tools](https://github.com/RRRoger/image_tools)

## Features

- 使用Python Click命令行交互更又好
- 自动识别文字颜色
- TODO
  - GUI
  - 自定义放上下左右
  - 多线性
  - ...


##  Exif 介绍

**Exif**: Exif（Exchangeable image file format）是专门为数码相机的照片设定的，可以记录数码照片的属性信息和拍摄数据。
Exif信息是镶嵌在 JPEG/TIFF 图像文件格式内的一组拍摄参数，它就好像是傻瓜相机的日期打印功能一样，只不过 Exif信息所记录的资讯更为详尽和完备。
手机上查看 **Exif**我使用的是**Exif Viewer Lite**这款App。
如下图，能够看到照片的光圈、快门、iso，甚至当时拍摄的位置等信息。

<img src="https://camo.githubusercontent.com/e05cbce6cf25be47cd1b593d4116634dc42d0bdc5925c2c4f8b4dd958a5ebcee/68747470733a2f2f63646e2e6a7364656c6976722e6e65742f67682f69686174656265616e732f696d61676573406d61696e2f696d672f576563686174494d47323036332e6a706567" style="zoom:50%;" />

## 安装python库

```bash
ExifRead==2.3.1
click==7.1.2
Pillow==8.0.1
rich==10.13.0
```

## 读取EXIF信息

- 使用第三方库 **exifread**

```python
with open(source_path, 'rb') as f:
    tags = exifread.process_file(f)
```

- **tags**信息对照

| Tag Name             | Description | Note                          |
| -------------------- | ----------- | ----------------------------- |
| Image Make           | 相机品牌    |                               |
| Image Model          | 相机型号    |                               |
| EXIF ExposureTime    | 快门        |                               |
| EXIF FocalLength     | 使用焦段    |                               |
| EXIF FNumber         | 光圈        | 显示7/5<br/>需要手动处理成1.4 |
| EXIF ISOSpeedRatings | iso         |                               |
| EXIF LensModel       | 镜头信息    |                               |
| ...                  | ...         |                               |

## 批量写入Exif到图片里


```bash
cd image_tools/batch_insert_exif

# for help
python run -h

# demo
python run.py -p ~/Desktop/test_img -font LXGWWenKai-Bold.ttf -q 30
```

- **python run -h**

```bash
Usage: run.py [OPTIONS]

Options:
  -h, --help                * * * * * * * * * * * * * * * * * * * * * * * * *
                            批量写入照片Exif信息
                            
                            Author: Roger;
                            Python Version: python 3.7+;
                            Python Libraries:
                                click: https://click-docs-zh-cn.readthedocs.io/zh/latest/
                                exifread: https://pypi.org/project/ExifRead/
                                Pillow: https://pillow.readthedocs.io/en/stable/
                                Rich: https://rich.readthedocs.io/en/stable/
                            * * * * * * * * * * * * * * * * * * * * * * * * *
  -p, --images-dir TEXT     修改处理的图片路径  [required]
  -q, --quality INTEGER     图像质量(0, 95), 默认: 50
  -fs, --font-size INTEGER  字体大小, 默认: 80
  -font, --font TEXT        选择字体, 默认: SourceHanSansCN-Normal.otf
```

- 根据照片亮度自动识别文字颜色, 以下是代码片段

```python
# 先提取照片左上角的一块区域，我这里取的是左上角的1/6
# 使用PIL的函数获取这块区域的平均亮度
# 如果小于等于128则图片比较暗，适合给白色文字
# 如果大于128则图片比较亮，适合给黑色文字

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
```

## 处理后展示结果信息

<img src="https://cdn.jsdelivr.net/gh/ihatebeans/images@main/img/show_result.jpg" style="zoom:50%;" />

## 效果图展示

![](https://cdn.jsdelivr.net/gh/ihatebeans/images@main/img/DSC07784-4.JPG)

<img src="https://cdn.jsdelivr.net/gh/ihatebeans/images@main/img/DSC07404-7.JPG" style="zoom: 25%;" />

<img src="https://cdn.jsdelivr.net/gh/ihatebeans/images@main/img/DSC03930-1-2.JPG" alt="DSC03930-1-2" style="zoom:25%;" />

<img src="https://cdn.jsdelivr.net/gh/ihatebeans/images@main/img/DSC03857-41.JPG" alt="DSC03857-41" style="zoom:25%;" />

<img src="https://cdn.jsdelivr.net/gh/ihatebeans/images@main/img/DSC07228-1.JPG" alt="DSC07228-1" style="zoom:25%;" />

<img src="https://cdn.jsdelivr.net/gh/ihatebeans/images@main/img/DSC07318-18.JPG" alt="DSC07318-18" style="zoom:25%;" />

<img src="https://cdn.jsdelivr.net/gh/ihatebeans/images@main/img/DSC07502-16.JPG" alt="DSC07502-16" style="zoom:25%;" />

<img src="https://cdn.jsdelivr.net/gh/ihatebeans/images@main/img/DSCF6011-7.JPG" style="zoom:25%;" />

<img src="https://cdn.jsdelivr.net/gh/ihatebeans/images@main/img/DSCF6012-8.JPG" alt="DSCF6012-8" style="zoom:25%;" />