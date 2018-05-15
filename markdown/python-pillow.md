title: 使用Python将两张照片透明重叠
date: 2015-09-30 13:19:26
categories:
- Python
tags:
- Python
- Pillow
- 图片处理
---

透明重叠最主要用的是`Image.blend`方法(详情请看第二个代码块), 第一个代码块主要是将多个图片剪切到一张大图, 然后用这张大图和另外一张非剪切的大图进行透明重叠， 主要`Image.blend`方法第三个参数是相对于第一张图片透明度。 


```python
# -*- coding: utf-8 -*-
'''
File Name: merge.py
Author: JackeyGao
mail: junqi.gao@shuyun.com
Created Time: 一  6/ 1 13:27:49 2015
'''

from __future__ import division
import os
import math
import Image

def image_resize(img, size=(4, 3)):
    """调整图片大小
    """
    try:
        if img.mode not in ('L', 'RGB'):
            img = img.convert('RGB')
        img = img.resize(size)
    except Exception, e:
        pass
    return img

def image_merge(images, output_dir='output', output_name='merge.jpg', \
                restriction_max_width=None, restriction_max_height=None):
    """垂直合并多张图片
    images - 要合并的图片路径列表
    ouput_dir - 输出路径
    output_name - 输出文件名
    restriction_max_width - 限制合并后的图片最大宽度，如果超过将等比缩小
    restriction_max_height - 限制合并后的图片最大高度，如果超过将等比缩小
    """
    x_number = 10 if len(images) >= 5 else len(images)
    y_number = int(math.ceil(len(images) / x_number))
    total_height = 0
    # 计算合成后图片的宽度（以最宽的为准）和高度
    for img_path in images:
        if os.path.exists(img_path):
            img = Image.open(img_path)
            img = img.resize((712, 960))
            width, height = img.size

            max_width = width * x_number
            total_height = height * y_number

    # 产生一张空白图
    new_img = Image.new('RGB', (max_width, total_height), 255)
    # 合并
    x = y = n = 0
    for img_path in images:
        if os.path.exists(img_path):
            img = Image.open(img_path)
            img = img.resize((712, 960))
            width, height = img.size
            print width, height
            new_img.paste(img, (x, y))

            n += 1
            if n % x_number == 0:
                y += height
                x = 0
            else:
                x += width



    if restriction_max_width and max_width >= restriction_max_width:
        # 如果宽带超过限制
        # 等比例缩小
        ratio = restriction_max_height / float(max_width)
        max_width = restriction_max_width
        total_height = int(total_height * ratio)
        new_img = image_resize(new_img, size=(max_width, total_height))

    if restriction_max_height and total_height >= restriction_max_height:
        # 如果高度超过限制
        # 等比例缩小
        ratio = restriction_max_height / float(total_height)
        max_width = int(max_width * ratio)
        total_height = restriction_max_height
        new_img = image_resize(new_img, size=(max_width, total_height))

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    save_path = '%s/%s' % (output_dir, output_name)
    new_img.save(save_path)
    return save_path

if __name__ == '__main__':
    import os
    image_files = [ "input/%s" % f for f in os.listdir("input/") if f.endswith("pg") ]

    image_files = image_files * 4

    image_merge(images=image_files)
```

将两张背景图重叠

```python
import Image
img = Image.open("bg.jpeg")
img2 = Image.open("merge.jpg")
merge = Image.blend(img, img2, 0.3)
merge.save("my.jpg")
```

