---
title: "Python AES加密文件(练习)"
date: "2019-11-14"
categories: 
  - "python"
---

##### 依赖插件

```ruby
pip install pycryptodome
```

##### AESEncrypt.py

```python
#!/usr/bin/python
# -*- coding: utf-8 -*-

# 使用方法：
# 1 初次使用先双击执行 AESEncrypt.py
# 2 将要加密的文件放到 src/ 目录下
# 3 双击执行 AESEncrypt.py后，解密文件会生成到 dist/ 目录下

from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
import os


class AESEncrypt(object):
    def __init__(self):
        # 加密时需要补充位数
        self.BLOCK_SIZE = 64
        self.input = './encrypt/src/'
        self.output = './encrypt/dist/'
        key = 'akpYd2SiNx17MV9V'.encode('utf-8')
        mode = AES.MODE_ECB
        self.cryptor = AES.new(key, mode)

    def encrypt(self, src_dir):
        for dirpath, dirnames, filenames in os.walk(src_dir):
            # 获取完整文件路径
            for filename in filenames:
                full_path = os.path.join(dirpath, filename)
                # print(full_path)
                old_file = open(full_path, "rb")
                cipher_text = old_file.read()
                plain_text = self.cryptor.encrypt(pad(cipher_text, self.BLOCK_SIZE))
                new_file = open(os.path.join(self.output, filename), "wb")
                new_file.write(plain_text)
                new_file.close()
                old_file.close()


if __name__ == '__main__':
    __this = AESEncrypt()
    # 创建输入路径
    if not os.path.exists(__this.input):
        os.makedirs(__this.input)
    if not os.path.exists(__this.output):
        os.makedirs(__this.output)

    # 启动程序
    __this.encrypt(__this.input)
```
