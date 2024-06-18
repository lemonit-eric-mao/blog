---
title: 'CentOS 7 安装 Openssl-1.1.1g'
date: '2021-11-23T14:05:41+00:00'
status: publish
permalink: /2021/11/23/centos-7-%e5%ae%89%e8%a3%85-openssl-1-1-1g
author: 毛巳煜
excerpt: ''
type: post
id: 8165
category:
    - CentOS
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
###### 下载 openssl-1.1.1g

```ruby
wget https://www.openssl.org/source/openssl-1.1.1g.tar.gz --no-check-certificate

## 解压
tar -zxvf openssl-1.1.1g.tar.gz && cd openssl-1.1.1g
## 编译
./config --prefix=/usr/local/openssl
## 安装
make -j 16 && make install


mv /usr/bin/openssl /usr/bin/openssl.bak

## 添加软链
ln -sf /usr/local/openssl/bin/openssl /usr/bin/openssl
ln -s /usr/local/openssl/lib/libssl.so.1.1 /usr/lib64/libssl.so.1.1
ln -s /usr/local/openssl/lib/libcrypto.so.1.1 /usr/lib64/libcrypto.so.1.1

echo 'usr/local/openssl/lib' >> /etc/ld.so.conf

## 设置生效
ldconfig -v

openssl version
OpenSSL 1.1.1g  21 Apr 2020

```

- - - - - -

- - - - - -

- - - - - -