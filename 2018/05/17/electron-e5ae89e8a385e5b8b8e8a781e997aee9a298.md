---
title: 'electron 安装常见问题'
date: '2018-05-17T10:43:38+00:00'
status: publish
permalink: /2018/05/17/electron-%e5%ae%89%e8%a3%85%e5%b8%b8%e8%a7%81%e9%97%ae%e9%a2%98
author: 毛巳煜
excerpt: ''
type: post
id: 2111
category:
    - Ubuntu
tag: []
post_format: []
hestia_layout_select:
    - default
---
### libgconf-2.so.4 No such file or directory

```
<pre data-language="">```ruby
mao-siyu@pc:/<span class="katex math inline">electron
/usr/lib/node_modules/electron/dist/electron: error while loading shared libraries: libgconf-2.so.4: cannot open shared object file: No such file or directory
mao-siyu@pc:/</span>

```
```

##### 解决方案 执行下面的命令

```
<pre data-language="">```ruby
mao-siyu@pc:/$ sudo apt-get install libgconf-2-4

```
```