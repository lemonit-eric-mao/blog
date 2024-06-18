---
title: "Java 常见问题"
date: "2020-02-26"
categories: 
  - "spring-boot"
---

###### 使用jar命令

```ruby
jar --help
非法选项: -
用法: jar {ctxui}[vfmn0PMe] [jar-file] [manifest-file] [entry-point] [-C dir] files ...
选项:
    -c  创建新档案
    -t  列出档案目录
    -x  从档案中提取指定的 (或所有) 文件
    -u  更新现有档案
    -v  在标准输出中生成详细输出
    -f  指定档案文件名
    -m  包含指定清单文件中的清单信息
    -n  创建新档案后执行 Pack200 规范化
    -e  为捆绑到可执行 jar 文件的独立应用程序
        指定应用程序入口点
    -0  仅存储; 不使用任何 ZIP 压缩
    -P  保留文件名中的前导 '/' (绝对路径) 和 ".." (父目录) 组件
    -M  不创建条目的清单文件
    -i  为指定的 jar 文件生成索引信息
    -C  更改为指定的目录并包含以下文件

如果任何文件为目录, 则对其进行递归处理。

清单文件名, 档案文件名和入口点名称的指定顺序与 'm', 'f' 和 'e' 标记的指定顺序相同。

示例 1: 将两个类文件归档到一个名为 classes.jar 的档案中:
       jar cvf classes.jar Foo.class Bar.class
示例 2: 使用现有的清单文件 'mymanifest' 并
           将 foo/ 目录中的所有文件归档到 'classes.jar' 中:
       jar cvfm classes.jar mymanifest -C foo/ .

```

* * *

* * *

* * *

###### 文件上传异常， `io.undertow.server.RequestTooBigException`

```ruby
2020-02-26 20:39:22.399 ERROR 2525 --- [  XNIO-1 task-6] c.y.c.c.exception.entity.ResultEntity    :
class org.springframework.http.converter.HttpMessageNotReadableException
null
500
I/O error while reading input message; nested exception is io.undertow.server.RequestTooBigException: UT000020: Connection terminated as request was larger than 10485760
org.springframework.web.servlet.mvc.method.annotation.AbstractMessageConverterMethodArgumentResolver.readWithMessageConverters(AbstractMessageConverterMethodArgumentResolver.java:217)
1582720762399
```

**修改如下文件解决 `application.yml`**

```yml
spring:
  # 设置上传文件大小限制
  servlet:
    multipart:
      # 最大文件大小。值可以使用后缀“MB”或“KB”分别表示兆字节或千字节。
      max-file-size: 100MB
      # 最大请求大小。值可以使用后缀“MB”或“KB”分别表示兆字节或千字节。
      max-request-size: 100MB
```

* * *

* * *

* * *
