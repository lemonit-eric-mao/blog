---
title: ".editorconfig 格式化文件"
date: "2017-11-16"
categories: 
  - "开发工具"
---

```null
root = true

[*]
charset = utf-8
indent_style = space
indent_size = 4
end_of_line = lf
insert_final_newline = false
trim_trailing_whitespace = true
```

#### 在webstrom 使用格式化功能时, webstrom会优先查找当前项目根录中的这个文件, 按照这个文件中的配置进行格式化代码, 如果项目中没有这个文件, webstrom 会使用自己默认的格式 进行格式化代码
