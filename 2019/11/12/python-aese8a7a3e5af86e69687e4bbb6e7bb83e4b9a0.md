---
title: 'Python AES解密文件(练习)'
date: '2019-11-12T06:38:34+00:00'
status: publish
permalink: /2019/11/12/python-aes%e8%a7%a3%e5%af%86%e6%96%87%e4%bb%b6%e7%bb%83%e4%b9%a0
author: 毛巳煜
excerpt: ''
type: post
id: 5121
category:
    - Python
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
##### 依赖插件

```ruby
pip install pycryptodome

```

##### AESDecrypt.py

```python
#!/usr/bin/python
# -*- coding: utf-8 -*-

# 使用方法：
# 1 初次使用先双击执行 AESDecrypt.py
# 2 将要解密的文件放到 src/ 目录下
# 3 双击执行 AESDecrypt.py后，解密文件会生成到 dist/ 目录下

from Crypto.Cipher import AES
import os


class AESDecrypt(object):
    def __init__(self):
        self.input = './decrypt/src/'
        self.output = './decrypt/dist/'
        key = 'akpYd2SiNx17MV9V'.encode('utf-8')
        mode = AES.MODE_ECB
        self.cryptor = AES.new(key, mode)

    def decrypt(self, src_dir):
        for dirpath, dirnames, filenames in os.walk(src_dir):
            # 获取完整文件路径
            for filename in filenames:
                full_path = os.path.join(dirpath, filename)
                # print(full_path)
                old_file = open(full_path, "rb")
                cipher_text = old_file.read()
                plain_text = self.cryptor.decrypt(cipher_text)
                new_file = open(os.path.join(self.output, filename), "wb")
                new_file.write(plain_text)
                new_file.close()
                old_file.close()


if __name__ == '__main__':
    __this = AESDecrypt()
    # 创建输入路径
    if not os.path.exists(__this.input):
        os.makedirs(__this.input)
    if not os.path.exists(__this.output):
        os.makedirs(__this.output)

    # 启动程序
    __this.decrypt(__this.input)

```