---
title: 'Python 批量下载文件'
date: '2020-01-04T10:33:38+00:00'
status: private
permalink: /2020/01/04/python-%e6%89%b9%e9%87%8f%e4%b8%8b%e8%bd%bd%e6%96%87%e4%bb%b6
author: 毛巳煜
excerpt: ''
type: post
id: 5213
category:
    - Python
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
##### **批量下载 .ts文件，并转为mp4格式**

**ts起始位置**: **https://baidu.com/20190601/c2AoIFQG/800kb/hls/do2TIa5981`000`.ts**  
**ts结束位置**: **https://baidu.com/20190601/c2AoIFQG/800kb/hls/do2TIa5981`2773`.ts**

```python
#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2020/01/04 17:39
# @Author  : Eric.Mao
# @FileName: batch_download.py
# @Software: PyCharm
# @Blog    ：http://www.dev-share.top

import os
import urllib.request


class DownloadFile(object):

    # 下载
    def download(self, url):
        filename = os.path.basename(url)
        data = urllib.request.urlopen(url)
        with open('download/%s' % filename, 'wb') as f:
            f.write(data.read())
            f.close()

    # 初始化
    def init(self):
        # 如果文件夹不存在
        dist_dir = 'download/'
        if not os.path.exists(dist_dir):
            os.makedirs(dist_dir)

        # 循环下载 https://lajiao-bo.com/ .ts视频文件
        for i in range(0, 2773):
            num  = str(i).zfill(3)
            self.download('https://baidu.com/20190601/c2AoIFQG/800kb/hls/do2TIa5981%s.ts' % num)


if __name__ == '__main__':
    __this = DownloadFile()
    # 启动程序
    __this.init()
    # win7 系统合并成一个.ts文件
    os.system('copy /b download\\*.ts new.ts')
    # 转换后的文件如果播放速度太快，使用 狸窝全能视频转换器，转为 .mp4格式
    # 转换器下载链接：https://pan.baidu.com/s/1eJv-507RGxBZi24GhF6m7Q 提取码：onkc


```