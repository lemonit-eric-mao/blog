---
title: "Python 执行文件 传参"
date: "2019-05-31"
categories: 
  - "python"
---

##### 执行文件传参

```python
#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
# 脚本路径，基本上第一位永远是脚本的路径
print sys.argv[0]
# 参数以空格做分隔 参数一
print sys.argv[1]
# 参数二
print sys.argv[2]
# 退出系统
sys.exit(1)
```

##### argparse 执行文件传参

```python
#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import argparse
import time

parser = argparse.ArgumentParser(description='帮助文档')
parser.add_argument('-v', type=str, default=time.strftime('v%y%m%d-%H%M%S'), help='如果不指定此参数，默认动态生成版本号')
parser.add_argument('-name', type=str, default='all', help='选择要编译的项目名称')
# 获取转换后的参数
args = parser.parse_args()

print args.v
print args.name
# 退出系统
sys.exit(1)
```
