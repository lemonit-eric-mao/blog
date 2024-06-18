---
title: "Go 语言常见问题"
date: "2020-09-26"
categories: 
  - "go语言"
---

### Go 跨域

```go
import (
    "encoding/json"
    "github.com/lemonit-eric-mao/commons/logger"
    "net/http"
)

// Router 定义服务端路由
func Router() {
    // 任务路由
    http.HandleFunc("/server/test/add", corsMiddleware(handleAddTestTD))
    http.HandleFunc("/server/test/list", corsMiddleware(handleListTestTD))
}

func corsMiddleware(next http.HandlerFunc) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        // 设置允许跨域请求的响应头
        w.Header().Set("Access-Control-Allow-Origin", "*")
        w.Header().Set("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        // 允许跨域时，前端要求
        w.Header().Set("Access-Control-Allow-Headers", "Content-Type, satoken")

        if r.Method == http.MethodOptions {
            w.WriteHeader(http.StatusOK)
            return
        }

        next.ServeHTTP(w, r)
    }
}

// handleAddTestTD 处理添加请求
func handleAddTestTD(writer http.ResponseWriter, request *http.Request) {
    if request.Method != http.MethodPost {
        http.Error(writer, "只允许POST请求", http.StatusMethodNotAllowed)
        return
    }
    //
    //param := &TestTD{}
    //
    //err := json.NewDecoder(request.Body).Decode(param)
    //if err != nil {
    //    http.Error(writer, "解析JSON数据失败", http.StatusBadRequest)
    //    return
    //}
    //
    //InsertData()
    //// 添加
    //if err != nil {
    //    logger.Error(err)
    //    http.Error(writer, err.Error(), http.StatusBadRequest)
    //    return
    //}

    json.NewEncoder(writer).Encode(map[string]interface{}{})
}
```

* * *

* * *

* * *

### [Go语言编译的exe添加图标](https://juejin.cn/post/7217410854844448827 "Go语言编译的exe添加图标")

1. 准备图片，可以去下载ico图片，或者是其他格式转为ico
2. 命名为`main.ico`，进入到项目的目录
3. 创建一个空白文本文件`main.rc`，打开输入`IDI_ICON1 ICON "main.ico"`，保存关闭
4. 在项目目录执行命令 `windres -o main.syso main.rc`，此时生成了一个`main.syso`
5. 直接`go build`生成的exe就有图标了

* * *

* * *

* * *

### **`//go:embed` 将文件嵌入到可执行文件中**

**目录结构**

```bash
src
│
└─web
    │  router.go              # 代码在这里
    │
    ├─html
    │      index.html
    │      progress.html
    │      swimLane.html
    │      timeline.html
    │
    └─public
        │  favicon.ico
        │
        └─js
              ajax.js
              index.js
              progress.js
              swimLane.js
              timeline.js

```

**`router.go` 用法，将多个文件嵌入到文件系统**

```go
package web

import (
    "embed"
    "github.com/lemonit-eric-mao/commons/logger"
    "html/template"
    "net/http"
)

var templates *template.Template

// 使用 embed 包来实现, 将 HTML 和 JavaScript 文件嵌入到可执行文件中
// 【//go:embed】这是个特殊写法
// 把 public/ 文件夹下所有的内容（包括子文件夹中的内容）都嵌入到应用程序中。
var (
    //go:embed public/*
    EmbedPublic embed.FS
    //go:embed html/*
    EmbedHtml embed.FS
)

// Router 定义路由
func Router() {

    // EmbedPublic 是访问静态资源时用到的前缀如：http://172.16.15.208:8080/public/favicon.ico
    // 加载静态文件（使用 embed 包）
    fs := http.FileServer(http.FS(EmbedPublic))
    http.Handle("/", http.StripPrefix("/", fs))

    // 解析嵌入的 HTML 模板
    templates = template.Must(template.ParseFS(EmbedHtml, "html/*.html"))

    // Web端路由
    http.HandleFunc("/web/", handleIndex)
}

```

* * *

* * *

* * *

### **编译后运行，关闭GUI**

```go
[root@controller ~]# go build -ldflags "-s -w -H=windowsgui" -o StartTask.exe
```

**解释**

> - `go build -ldflags "-s -w -H=windowsgui" -o StartTask.exe`
>     - `-ldflags` 是 Go 编译器的一个标志，用于传递链接器选项（linker flags）。通过在编译时使用 `-s`、`-w` 和 `-H=windowsgui` 标志，可以实现以下效果：
>     - `-s` 削减了生成的可执行文件的符号表和调试信息，以减小文件大小并降低反编译的风险。
>         
>     - `-w` 禁用了 DWARF 调试信息的生成，进一步减小了可执行文件的大小，但也限制了详细的调试能力。
>         
>     - `-H=windowsgui` 在 Windows 系统上将可执行文件转换为 GUI 应用程序，避免了显示命令行窗口，从而实现隐藏 GUI 窗口的目的。
>         

* * *

* * *

* * *

### **如何将代码放在github上被引用？**

> 项目地址：https://github.com/lemonit-eric-mao/commons.git

```bash
# 项目目录
E:\GO-PROJECT\COMMONS
│  go.mod               # 将module的默认是指向本地的路径，改为指向公有仓库的路径(module github.com/lemonit-eric-mao/commons)
│
├─logger
│      logger.go        # 没有其实引用，不需要调整
│
└─tools
       devtool.go       # 其中引用了logger.go，也必须要使用公有仓库路径的引用( import "github.com/lemonit-eric-mao/commons/logger" )
```

* * *

###### **如何使用**

1. 首先在公有仓库中，需要打tag，tag的版本号，会做为使用时的引用版本
2. 如何引用？

```bash
## 命令行下载
go get github.com/lemonit-eric-mao/commons@v1.0.3

## 代码中引用
import "github.com/lemonit-eric-mao/commons/logger"

```

* * *

* * *

* * *

### **问题：当我执行 `go build -buildmode plugin` 命令时，它会出现以下错误：**

```ruby
E:\go-project\gitlab\kong-plugins-go-encrypt> go build -buildmode plugin .\plugins\go-log.go

-buildmode=plugin not supported on windows/amd64

```

**`-buildmode=plugin在windows/amd64`上不受支持** [目前插件仅在 Linux、FreeBSD 和 macOS 上受支持。](https://pkg.go.dev/plugin)

* * *

* * *

* * *

### **问题：`Golang verifying module: xxx: initializing sumdb.Client: reading tree note: malformed note`**

```ruby
go get: github.com/kataras/iris/v12@v12.1.8: verifying module: github.com/kataras/iris/v12@v12.1.8: initializing sumdb.Client: checking tree#10399623: Get "https://sum.golang.org/tile/8/2/000.p/158"
: dial tcp 142.251.42.241:443: connectex: A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected
host has failed to respond.

```

**[这个错误翻译过来就是 sumdb 校验异常](http://www.bubuko.com/infodetail-3642633.html "这个错误翻译过来就是 sumdb 校验异常")**

##### 解决方案

```ruby
## 关闭sumdb校验
go env -w GOSUMDB=off
```

* * *

* * *

* * *

### 启动程序时异常

```
go: updates to go.mod needed; to update it:
    go mod tidy

```

**如果已经设置了gomod环境，只需要更新mod依赖的modules，需要在命令行执行 `go mod tidy`**

* * *

* * *

* * *

### 用切片组成的切片

```go
package main

import "fmt"

func main() {

    // 定义数组常量
    arr := []int{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
    // index     0  1  2  3  4  5  6  7  8  9

    // 切片 a1
    a1 := arr[6:8]
    fmt.Println("a1的值:", a1, "    a1的长度", len(a1)) // a1的值: [7 8]          a1的长度 2
    // 切片 a2 （用切片组成的切片，拥有相同的元素，但是仍然指向相同的相关数组）
    a2 := a1[0:4]
    fmt.Println("a2的值:", a2, "    a2的长度", len(a2)) // a2的值: [7 8 9 10]     a2的长度 4

}

```

**[使用切片的注意事项-切片和垃圾回收](https://github.com/unknwon/the-way-to-go_ZH_CN/blob/master/eBook/07.6.md#768-%E5%88%87%E7%89%87%E5%92%8C%E5%9E%83%E5%9C%BE%E5%9B%9E%E6%94%B6 "使用切片的注意事项-切片和垃圾回收")**

* * *

* * *

* * *

### 异常

```go
package WordpressXmlFormat

import "fmt"

/**
 * 将 wordpress 博客 导出的xml文件 格式为 markdown
 */
func main() {
    fmt.Println("Hello, World!")
}
// 运行此代码会得到一个异常
runnerw.exe: CreateProcess failed with error 216:
Process finished with exit code 216
```

* * *

##### 原因 package 必须是 main; 方法名 也必须是 main

```go
package main

import "fmt"

/**
 * 将 wordpress 博客 导出的xml文件中，HTML语法 格式为 markdown语法
 */
func main() {
    fmt.Println("Hello, World!")
}
```

##### 编译成可执行文件

```go
go build 文件名
```

* * *

* * *

* * *

### 异常 引入自定义包失败

    **原因： 缺少 go.mod文件**     **创建后项目名以后需要执行 `go mod init` 项目名**

```ruby
go-web-server> go mod init
go: cannot determine module path for source directory G:\Test\go-web-server (outside GOPATH, module path must be specified)
Example usage:
        'go mod init example.com/m' to initialize a v0 or v1 module
        'go mod init example.com/m/v2' to initialize a v2 module

Run 'go help mod init' for more information.

##############################################
go-web-server> go mod init go-web-server
go: creating new go.mod: module go-web-server


```

* * *

* * *

* * *
