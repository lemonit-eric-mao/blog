---
title: "Python 写文件"
date: "2019-05-29"
categories: 
  - "python"
---

##### 例子一

```python
#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

class GetFastDFSFile(object):

  def __init__(self):
    self.output_path = './output.txt'

  def read_file_full_path(self, src_dir):
     # 如果输入的文件已经存在，则先删除文件
     if os.path.exists(self.output_path):
        os.remove(self.output_path)

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
          content = os.path.join(dirpath, filename)
          self.save_path(content)

  def save_path(self, content):
    with open(self.output_path, 'a') as f:
        f.write(content + '\n')
        f.close()

if __name__ == '__main__':
    __this = GetFastDFSFile()
    # 启动程序
    __this.read_file_full_path('../deploy/')
```

##### 例子二

```python
#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import time

# 注意：input() 和 raw_input() 这两个函数均能接收 字符串 ，但 raw_input() 直接读取控制台的输入（任何类型的输入它都可以接收）。
# 而对于 input() ，它希望能够读取一个合法的 python 表达式，即你输入字符串的时候必须使用引号将它括起来，否则它会引发一个 SyntaxError 。
# 除非对 input() 有特别需要，否则一般情况下我们都是推荐使用 raw_input() 来与用户交互。
# 注意：python3 里 input() 默认接收到的是 str 类型。
# 获取控制台输入
version = raw_input('Enter your version: ')

# 动态生成版本号
newVersion = time.strftime('v%y%m%d-%H%M%S')

# 如果输入为空
if version:
    newVersion=version

# 定义项目名称集合
projects = [
    {'name': '120-innovent-innoventpos', 'version': newVersion, 'port': '20120'},
    {'name': '005-paas-system', 'version': newVersion, 'port': '20005'},
    {'name': '021-paas-sftp', 'version': newVersion, 'port': '20021'},
]

# 打开文件
file = open('build-app-images.py', 'w')

# 向文件中写入数据
file.write("import os\n\n")
file.write("os.system('rm -f /home/deploy/images/jar/app/*.jar')\n\n")
for obj in projects:
    str= []
    temp = "os.system('echo \"######## {0} ########\"')\n".format(obj['name'])
    str.append(temp)
    temp = "os.system('ln -f /home/deploy/kube_deploy/{0}/{0}.jar /home/deploy/images/jar/app/{0}.jar')\n".format(obj['name'])
    str.append(temp)
    temp = "os.system('docker build -t sinoeyes.io/library/{0}-app:{2} --build-arg file={3}.jar --build-arg port={1} /home/deploy/images/jar/app')\n".format(obj['name'][4:], obj['port'], obj['version'],obj['name'])
    str.append(temp)
    temp = "os.system('docker push sinoeyes.io/library/{0}-app:{1}')\n".format(obj['name'][4:], obj['version'])
    str.append(temp)
    str.append('\n')
    file.write(''.join(str))
file.write("os.system('rm -f /home/deploy/images/jar/app/*.jar')\n")

# 关闭文件
file.close()
```
