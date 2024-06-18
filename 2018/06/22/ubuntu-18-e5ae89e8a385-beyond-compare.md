---
title: 'Ubuntu 18 安装 Beyond Compare'
date: '2018-06-22T16:04:03+00:00'
status: publish
permalink: /2018/06/22/ubuntu-18-%e5%ae%89%e8%a3%85-beyond-compare
author: 毛巳煜
excerpt: ''
type: post
id: 2178
category:
    - Ubuntu
tag: []
post_format: []
hestia_layout_select:
    - default
---
##### [Beyond Compare 官网地址](http://www.scootersoftware.com/download.php "官网地址")

### 下载

```
<pre data-language="">```ruby
mao-siyu@pc:/mnt/1TB/download$ wget http://www.scootersoftware.com/bcompare-4.2.5.23088_amd64.deb

```
```

### 安装 Beyond Compare

```
<pre data-language="">```ruby
mao-siyu@pc:/mnt/1TB/download$ sudo dpkg -i bcompare-4.2.5.23088_amd64.deb

```
```

### 如果需要安装依赖

```
<pre data-language="">```ruby
mao-siyu@pc:/mnt/1TB/download$ sudo apt-get -f -y install

```
```