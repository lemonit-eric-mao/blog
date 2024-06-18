---
title: 'SCP 迁移docker镜像，自动填写密码'
date: '2019-11-19T08:59:04+00:00'
status: publish
permalink: /2019/11/19/scp-%e8%bf%81%e7%a7%bbdocker%e9%95%9c%e5%83%8f%ef%bc%8c%e8%87%aa%e5%8a%a8%e5%a1%ab%e5%86%99%e5%af%86%e7%a0%81
author: 毛巳煜
excerpt: ''
type: post
id: 5136
category:
    - Shell
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
##### 前置条件

- 需要安装 **`yum install -y expect`**
- **`spawn`** ：后面跟具体要执行的命令
- **`expect`** ：定义字符内容用于匹配上面spawn后面执行命令的返回内容
- **`send`** ：如果spawn后面运行命令的返回内容，匹配expect上面定义的。就发送send定义的内容到上面（相当于输入了密码）。

##### save\_images.sh

```ruby
cat > save_images.sh 
```