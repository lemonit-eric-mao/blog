---
title: "Python os.walk 读取文件"
date: "2019-10-10"
categories: 
  - "python"
---

##### read\_file\_path.py

```python
#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

class ReadFilePath(object):

  def __init__(self):
    print('init')

  def read_file_full_path(self, src_dir):
     for dirpath, dirnames, filenames in os.walk(src_dir):
        # 当前目录路径
        #print(dirpath)
        # 当前路径下所有子目录
        #print(dirnames)
        # 当前路径下所有非目录子文件
        #print(filenames)

        # 获取完整目录
        #for dirname in dirnames:
        #  print(os.path.join(dirpath, dirname))

        # 获取完整文件路径
        for filename in filenames:
          print(os.path.join(dirpath, filename))

if __name__ == '__main__':
    __this = ReadFilePath()
    # 启动程序
    __this.read_file_full_path('../deploy/')
```

##### 运行

```ruby
./read_file_path.py
```

##### 参数含义：

- dirpath：string，代表目录的路径；
- dirnames：list，包含了当前dirpath路径下所有的子目录名字（不包含目录路径）；
- filenames：list，包含了当前dirpath路径下所有的非目录子文件的名字（不包含目录路径）
