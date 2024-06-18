---
title: '.editorconfig 格式化文件'
date: '2017-11-16T16:34:46+00:00'
status: publish
permalink: /2017/11/16/editorconfig-%e6%a0%bc%e5%bc%8f%e5%8c%96%e6%96%87%e4%bb%b6
author: 毛巳煜
excerpt: ''
type: post
id: 543
category:
    - 开发工具
tag: []
post_format: []
---
```
<pre class="line-numbers prism-highlight" data-start="1">```null
root = true

[*]
charset = utf-8
indent_style = space
indent_size = 4
end_of_line = lf
insert_final_newline = false
trim_trailing_whitespace = true

```
```

#### 在webstrom 使用格式化功能时, webstrom会优先查找当前项目根录中的这个文件, 按照这个文件中的配置进行格式化代码, 如果项目中没有这个文件, webstrom 会使用自己默认的格式 进行格式化代码