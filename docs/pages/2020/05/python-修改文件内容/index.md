---
title: "Python 修改文件内容"
date: "2020-05-12"
categories: 
  - "python"
---

###### AlterFile.py 修改文件，写法

```python
#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/12 16:04
# @Author  : Eric.Mao
# @FileName: AlterFile.py
# @Software: PyCharm
# @Blog    ：http://dev-share.top


import sys
import os

# 强制转码
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)


class AlterFile(object):

    # 初始化
    # 文件路径, 旧内容, 新内容
    def alter(self, filepath, old_str, new_str):
        temp_data = ""
        # 读文件
        with open(filepath, "r") as f:
            for line in f:
                if old_str in line:
                    # 修改替换
                    line = line.replace(old_str, new_str)
                temp_data += line
        # 重新写入
        with open(filepath, "w") as f:
            f.write(temp_data)

    # 获取指定目录所有文件全路径
    def read_files(self, src_dir):
        for dir_path, dir_names, filenames in os.walk(src_dir):
            # 获取完整文件路径
            for filename in filenames:
                full_path = os.path.join(dir_path, filename)
                # 只处理yaml文件
                if full_path.endswith('.yaml'):
                    print (full_path)
                    # 批量替换
                    self.alter(full_path, "paas-app-hrbm", "paas-app-eric")


# 定义入口函数
def main():
    __this = AlterFile()
    # 读取指定目录下所有文件
    __this.read_files("F:/test")


if __name__ == '__main__':
    main()

```
