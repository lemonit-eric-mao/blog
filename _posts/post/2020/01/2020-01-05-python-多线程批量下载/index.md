---
title: "Python 多线程批量下载"
date: "2020-01-05"
categories: 
  - "python"
---

##### [Python 多线程参数资料](http://www.ruanyifeng.com/blog/2019/11/python-asyncio.html "Python 多线程参数资料")

* * *

###### 目录

```ruby
G: ts-ffmpeg
│  app.py
│  ffmpeg.exe
│  index-new.m3u8
│  index.m3u8
│  key.key
└  README.md
```

* * *

* * *

* * *

##### **`多线程下载`**

```python
#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2020/01/04 17:39
# @Author  : Eric.Mao
# @FileName: app.py
# @Software: PyCharm
# @Blog    ：http://www.dev-share.top

import os
import re
import time
import shutil
import aiohttp
import asyncio


class DownloadFile(object):

    def __init__(self):
        # 默认下载路径
        self.dist = './download/'
        # 要开启下载的线程数
        self.thread_num = 10
        # 存放要下载的ts文件的url
        self.urls = []
        # 存放修改后的index.m3u8文件
        self.index_local = []

    # 1 读取index.m3u8清单文件中的url
    #    path: 清单文件路径 (必须)
    #    url_prefix: 有些源视频地址没有url这里可以补充 (可选)
    def read_index_m3u8(self, path, url_prefix):
        with open(path, "r", encoding="utf-8") as r:
            # 一行一行读取
            line = r.readlines()
            for content in line:
                # 过滤出源视频地址，用来下载
                ts_url = content.replace("\n", "")
                if content.endswith(".ts\n"):
                    # 拼接要下载的ts文件的url
                    self.urls.append(f"{url_prefix}{ts_url}")
                    # 存放修改后的index.m3u8文件
                    # python 截取文件名 ts_url.split('/')[-1]
                    self.index_local.append(f"{self.dist}{ts_url.split('/')[-1]}")
                else:
                    # 过滤：如果有key，会自动修改key文件的位置
                    filter_ts_url = re.sub('URI=.*.', 'URI="./key.key"', ts_url)
                    # 存放修改后的index.m3u8文件
                    self.index_local.append(f"{filter_ts_url}")

    # 1.1 生成修改后的index.m3u8文件
    def create_index_local_m3u8(self):
        with open('./index_local.m3u8', 'w') as w:
            for content in self.index_local:
                w.write(f'{content}\n')
            w.close()

    # 2 链接URL
    async def get_content(self, link):
        async with aiohttp.ClientSession() as session:
            response = await session.get(link)
            content = await response.read()
            return content

    # 3 将文件下载到本地
    async def download(self, url):
        print('将文件下载到本地: %s' % url)
        filename = os.path.basename(url)
        with open(os.path.join(self.dist, filename), 'wb') as f:
            f.write(await self.get_content(url))
            f.close()

    # 创建文件夹
    def mkdir(self, dist_dir):
        # 如果文件夹不存在
        if not os.path.exists(dist_dir):
            os.makedirs(dist_dir)

    # 递归删除一个目录以及目录内的所有内容
    def rmdir(self, srcfile):
        if os.path.exists(srcfile):
            shutil.rmtree(srcfile)

    # 初始化
    def run(self):

        # 存放要异步执行的函数
        tasks = []
        # 将 self.urls 中的数据进行分批下载，默认一次下载 self.thread_num 个，少于 self.thread_num 个，就按照剩余的数量下载
        urls_len = len(self.urls)
        threads = urls_len > self.thread_num and self.thread_num or urls_len

        # 构建多个下载函数
        for i in range(0, threads):
            # 从前面取出数据， 取 self.thread_num 次， 构建下载函数
            url = self.urls.pop(0)
            # 构建下载函数
            tasks.append(self.download(url))

        # 获取事件循环 EventLoop
        loop = asyncio.get_event_loop()
        # 执行协同程序 coroutine； 多线程批量下载
        loop.run_until_complete(asyncio.wait(tasks))
        # 判断是否有未完成下载资源
        if len(self.urls) > 0:
            # 递归下载
            self.run()
        # 下载完成后关闭事件循环
        loop.close()


# 定义入口函数
def main():
    try:
        # 初始化
        __this = DownloadFile()

        # 为index.m3u8清单文件里面的视频链接添加访问地址
        print('为index.m3u8清单文件补充url')
        __this.read_index_m3u8('index.m3u8', 'https://ts6.hhmm0.com:9999')

        print('生成新的m3u8文件，将视频链接地址，指向本地')
        __this.create_index_local_m3u8()

        # 在当前项目目录，创建文件夹
        __this.mkdir(__this.dist)

        # 运行程序
        __this.run()
        print('Download Done!')

        # 解密、转换、合并
        os.system(f'ffmpeg -allowed_extensions ALL -i index_local.m3u8 -c copy {time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())}.mp4')
        print('Convert Done!')

    finally:
        print('删除download文件夹')
        # __this.rmdir(__this.dist)


if __name__ == '__main__':
    main()

```

* * *

* * *

* * *

###### **[项目地址](https://gitee.com/eric-mao/ts-ffmpeg "项目地址")**

* * *

* * *

* * *
