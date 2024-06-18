---
title: 'Node.js 应用node-rsa 实现公钥加密私钥解密'
date: '2018-04-10T21:26:28+00:00'
status: publish
permalink: /2018/04/10/node-js-%e5%ba%94%e7%94%a8node-rsa-%e5%ae%9e%e7%8e%b0%e5%85%ac%e9%92%a5%e5%8a%a0%e5%af%86%e7%a7%81%e9%92%a5%e8%a7%a3%e5%af%86
author: 毛巳煜
excerpt: ''
type: post
id: 2065
category:
    - 网络基础
tag: []
post_format: []
hestia_layout_select:
    - default
---
### 在linux系统中 使用 openssl 生成私钥、公钥

```
<pre class="line-numbers prism-highlight" data-start="1">```ruby
# 生成RSA私钥
[root@zhujiwu mao_siyu]# openssl genrsa -out rsa_private_key.pem 1024
Generating RSA private key, 1024 bit long modulus
..................++++++
......++++++
e is 65537 (0x10001)
[root@zhujiwu mao_siyu]#

# 使用RSA私钥 生成RSA公钥
[root@zhujiwu mao_siyu]# openssl rsa -in rsa_private_key.pem -pubout -out rsa_pubwp_key.pem
writing RSA key
[root@zhujiwu mao_siyu]# ll
-rw-r--r--  1 root root  891 4月  10 21:01 rsa_private_key.pem
-rw-r--r--  1 root root  272 4月  10 21:03 rsa_pubwp_key.pem
[root@zhujiwu mao_siyu]#

```
```

**将公钥与私钥存入到项目的 ssl文件夹中**

### 项目目录

```
<pre class="line-numbers prism-highlight" data-start="1">```null
.
│  package.json
│  test.js
└─ssl
        README.md
        rsa_private_key.pem
        rsa_pubwp_key.pem

```
```

### test.js

```
<pre class="line-numbers prism-highlight" data-start="1">```ruby
const NodeRSA = require('node-rsa');
const fs = require('fs');

// 共享密钥
const shareKey = '！@#￥%……&*_shareKey';

// 公钥加密
const publicKey = new NodeRSA(fs.readFileSync('ssl/rsa_pubwp_key.pem'));
const encrypted = publicKey.encrypt(shareKey, 'base64');
console.log(`加密后的共享密钥: <span class="katex math inline">{encrypted}`);

// 私钥解密
const privateKey = new NodeRSA(fs.readFileSync('ssl/rsa_private_key.pem'));
const decrypted = privateKey.decrypt(encrypted, 'utf8');
console.log(`解密后的共享密钥:</span>{decrypted}`);

```
```

### package.json

```
<pre class="line-numbers prism-highlight" data-start="1">```json
{
  "name": "rsa-test",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "start": "node test.js"
  },
  "author": "",
  "license": "ISC",
  "dependencies": {
    "node-rsa": "^0.4.2"
  }
}

```
```

### 总结

**`共享密钥`的含义是指对数据的加解密只使用一把共同的密钥;  
前后端正常情况下都用 共享密钥来进行加解密，因为共享密钥进行加解密速度快，缺点是很容易被抓包拦截获取到密钥;  
所以根据前人的经验又对共享密钥的传输做了更高级加密，使用RSA 非对称加密算法来对共享密钥在进行二次加密，防止在客户端在与服务端交互过程中数据被抓包拦截获取;**