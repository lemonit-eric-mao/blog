---
title: "Python 拼接Docker 路径"
date: "2019-10-12"
categories: 
  - "python"
---

##### 根据 docker inspect、 环境变量等信息，拼接路径

```python
#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2019/10/12 16:03
# @Author  : Eric.Mao
# @FileName: test.py
# @Software: PyCharm
# @Blog    ：https://www.lemonit.cn

import os
import re
import commands


class ReadFilePath(object):

    def __init__(self):
        self.output_path = './output.txt'

    def read_file_full_path(self, path, group_name, cname):
        if len(path) > 0:
            for dirpath, dirnames, filenames in os.walk(path):
                # 把与正则相匹配的字符串，根据正则进行分组
                paths = re.search(r'(.*)/%s/(.*)' % cname, dirpath)
                if paths is not None:
                  temp = paths.group(2)
                  for file in filenames:
                      if '-m' not in file:
                        fullpath = os.path.join(group_name, cname, temp, file)
                        self.save_path(fullpath)

    def save_path(self, content):
        with open(self.output_path, 'a') as f:
            f.write(content + '\n')
            f.close()

    def resouse(self):

        if os.path.exists(self.output_path):
            os.remove(self.output_path)

        (code, data) = commands.getstatusoutput("docker ps | grep storage | awk '{print $11}'")
        lists = data.split('\n')
        for cname in lists:
            (code1, path) = commands.getstatusoutput('docker inspect --format \'{{range .Mounts}}{{if eq "bind" .Type}}{{.Source}}{{print}}{{end}}{{end}}\' %s' % cname)
            (code2, data2) = commands.getstatusoutput('docker exec -it %s env | grep GROUP_NAME=' % cname)
            group_name = data2.replace('GROUP_NAME=', "").replace('\r', "")
            group_name = len(group_name) > 0 and group_name or "group1"
            self.read_file_full_path(path, group_name, cname)


if __name__ == '__main__':
    __this = ReadFilePath()
    # 启动程序
    __this.resouse()

```

##### format 命令解释

```ruby
# range迭代 需要 end结束符
# if判断  需要 end结束符
docker inspect --format '{{range 要迭代的对象}}{{if eq "bind" 要判断的属性}}{{要输出的属性值}}{{print}}{{end}}{{end}}' 容器名或容器ID
docker inspect --format '{{range .Mounts}}{{if eq "bind" .Type}}{{.Source}}{{print}}{{end}}{{end}}' storage2
```
