---
title: "Python 读取yaml文件"
date: "2019-05-30"
categories: 
  - "python"
---

##### 下载yaml解析器

https://yaml.org/

##### 下载python的yaml解析器

https://pyyaml.org/download/pyyaml/PyYAML-5.1.tar.gz 如果是windows系统 使用rar解压即可

```python
E:\download\PyYAML-5.1\PyYAML-5.1> python setup.py install
```

##### test.yaml

```yaml
name: Tom Smith
age: 37
spouse:
  name: Jane Smith
  age: 25
children:
  - name: Jimmy Smith
    age: 15
  - name1: Jenny Smith
    age1: 12
```

##### test.py

```python
#!/usr/bin/python
# -*- coding: utf-8 -*-
import yaml

# 打开文件
file = open('test.yaml')
# 解析文件内容
result = yaml.load(file)
# 控制台输出
print result
# 关闭文件
file.close()
```

##### 读取文件

```python
#!/usr/bin/python
# -*- coding: utf-8 -*-

def read_template_data(path, data):
    with open(path) as f:
        # 将文件一次读取为字符串
        content = f.read()
        # 将字符串加入模板
        tmp = Template(content)
        # 让数据与模板进行映射
        str = tmp.safe_substitute(data)
        return str
```

```python
#!/usr/bin/python
# -*- coding: utf-8 -*-

# 工具方法：将文件以字符串的形式进行读取，并使用模板进行解析
def read_template_data(path, data):
    with open(path) as file:
        # 将文件一次读取为字符串
        content = file.read()
        # 如果没有要解析的数据将直接返回文件内容
        if not data:
            return content

        # 将字符串加入模板
        tmp = Template(content)
        # 让数据与模板进行映射
        str = tmp.safe_substitute(data)
        return str
```

##### 控制台获取版本号

```python
#!/usr/bin/python
# -*- coding: utf-8 -*-

# 控制台获取版本号
def get_version():
    # 注意：input() 和 raw_input() 这两个函数均能接收 字符串 ，但 raw_input() 直接读取控制台的输入（任何类型的输入它都可以接收）。
    # 而对于 input() ，它希望能够读取一个合法的 python 表达式，即你输入字符串的时候必须使用引号将它括起来，否则它会引发一个 SyntaxError 。
    # 除非对 input() 有特别需要，否则一般情况下我们都是推荐使用 raw_input() 来与用户交互。
    # 注意：python3 里 input() 默认接收到的是 str 类型。
    # 获取控制台输入
    version = raw_input('Enter your version: ')
    # 如果输入为空
    if version:
        return version
    return time.strftime('v%y%m%d-%H%M%S')
```
