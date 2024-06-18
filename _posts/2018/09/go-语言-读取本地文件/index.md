---
title: "GO 语言 读取本地文件"
date: "2018-09-20"
categories: 
  - "go语言"
---

###### wordpress 导出文件格式转换 AlterFile.go

```go
/**
 * 将 wordpress 博客 导出的xml文件中，HTML语法 格式为 markdown语法
 *
 * @date 2018-09-20
 * @author mao_siyu
 */
package main

import (
    "fmt"
    "io/ioutil"
    "strings"
)

/** 声明一个空字典 */
var dictionary map[string]string

/**
 * 读取XML文件
 *
 * return 字符串文本
 */
func readXmlFile(fileName string) string {

    // 读取文件
    b, err := ioutil.ReadFile(fileName)
    // 如果有错
    if err != nil {
        fmt.Println(err)
    }
    // 将流转为字符串
    xml := string(b)
    // strings.Replace 返回 xml 的副本，并将副本中的 old 字符串替换为 new 字符串
    // 替换次数为 n 次，如果 n 为 -1，则全部替换
    for key := range dictionary {
        xml = strings.Replace(xml, key, dictionary[key], -1)
    }
    return xml
}

/**
 * 向磁盘写入XML文件
 */
func writeXmlFile(srcFile string, fileName string) {

    d1 := []byte(srcFile)
    err := ioutil.WriteFile(fileName, d1, 0644)
    if err != nil {
        fmt.Println(err)
    }
}

/**
 * 填充字典
 */
func fillDictionary() {

    // 初始化 map
    dictionary = make(map[string]string)
    dictionary[`<pre class="prism-highlight line-numbers" data-start="1"><code class="language-null">`] = "```\n"
    dictionary[`<pre class="line-numbers prism-highlight" data-start="1"><code class="language-null">`] = "```\n"
    dictionary[`<pre><code class=" line-numbers">`] = "```\n"

}

/**
 * 入口
 */
func main() {

    // 填充字典
    fillDictionary()

    var fileName string
    //fmt.Println("Please input your full file path: ")
    //fmt.Scanln(&fileName)
    fileName = "F:/test/ln.xml"
    // 读取xml文件 并且进行格式化
    xml := readXmlFile(fileName)
    // 将html语法 替换成 markdown语法
    newFileName := strings.Replace(fileName, ".xml", "_markdown.xml", -1)
    // 将xml文件写入磁盘
    writeXmlFile(xml, newFileName)
    //
    fmt.Println("文件已生成：", newFileName)
    //fmt.Println("按回车键退出!")
    //fmt.Scanln()
}

```

* * *

###### 运行

```go
go run AlterFile.go
```

* * *

* * *

* * *
