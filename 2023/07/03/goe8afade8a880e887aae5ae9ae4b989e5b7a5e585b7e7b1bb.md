---
title: Go语言自定义工具类
date: '2023-07-03T08:16:10+00:00'
status: private
permalink: /2023/07/03/go%e8%af%ad%e8%a8%80%e8%87%aa%e5%ae%9a%e4%b9%89%e5%b7%a5%e5%85%b7%e7%b1%bb
author: 毛巳煜
excerpt: ''
type: post
id: 10091
category:
    - Go
tag: []
post_format: []
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
hestia_layout_select:
    - sidebar-right
---
### go语言定时器

```go
// SetInterval 自定义，定时器工具
/**
func main() {
    chanStop := tools.SetInterval(3e9, func() {})

    // 等待10秒
    time.Sleep(10e9)
    // 关闭定时器
    chanStop 
```

- - - - - -

- - - - - -

- - - - - -

### **go语言控制台输出彩色日志**

```go
package main

import "fmt"

const (
    Reset  = "\033[0m"
    Black  = "\033[30m"
    Red    = "\033[31m"
    Green  = "\033[32m"
    Yellow = "\033[33m"
    Blue   = "\033[34m"
    Purple = "\033[35m"
    Cyan   = "\033[36m"
    White  = "\033[37m"

    Bold       = "\033[1m"
    Underline  = "\033[4m"
    Background = "\033[7m"
)

var colors = map[int]string{
    0: Black,
    1: Red,
    2: Green,
    3: Yellow,
    4: Blue,
    5: Purple,
    6: Cyan,
    7: White,
    8: Bold,
    9: Background,
}

func main() {
    for i := 0; i 
```

- - - - - -

- - - - - -

- - - - - -

### 自定义logger

> `/commons/logger/logger.go`  
>  使用方法：`logger.Infof("%s 版本 %s 安装成功", "release.Name", "release.Chart.Metadata.Version")`

```go
/**
 * 2023-07-03
 * siyu.mao
 */
package logger

import (
    "fmt"
    "log"
    "os"
)

const (
    Reset  = "\033[0m"
    Black  = "\033[30m"
    Red    = "\033[31m"
    Green  = "\033[32m"
    Yellow = "\033[33m"
    Blue   = "\033[34m"
    Purple = "\033[35m"
    Cyan   = "\033[36m"
    White  = "\033[37m"

    Bold       = "\033[1m"
    Underline  = "\033[4m"
    Background = "\033[7m"
)

type LogLevel int

const (
    LogError LogLevel = iota
    LogInfo
    LogWarning
    LogDebug
)

var LogLevelNames = []string{"ERROR", "INFO", "WARNING", "DEBUG"}

var logLevel LogLevel

func init() {
    // TODO: 设置日志工具级别
    os.Setenv("LOG_LEVEL", "DEBUG")
    setLogLevelFromEnv()
}

func setLogLevel(level LogLevel) {
    logLevel = level
}

func setLogLevelFromEnv() {
    logLevelStr := os.Getenv("LOG_LEVEL")
    if logLevelStr == "" {
        setLogLevel(LogInfo)
        return
    }
    switch logLevelStr {
    case "ERROR":
        setLogLevel(LogError)
    case "INFO":
        setLogLevel(LogInfo)
    case "WARNING":
        setLogLevel(LogWarning)
    case "DEBUG":
        setLogLevel(LogDebug)
    default:
        setLogLevel(LogInfo)
    }
}

func logf(color string, level LogLevel, format string, v ...interface{}) {
    if level 
```

> 调整日志级别需要通过修改操作系统的环境变量来实现，如：  
>  Windows 系统：
> 
> ```bash
> set LOG_LEVEL="ERROR"
> go run main.go
> 
> ```
> 
>  Linux 系统：
> 
> ```bash
> export LOG_LEVEL="ERROR"
> go run main.go
> 
> ```

- - - - - -

- - - - - -

- - - - - -