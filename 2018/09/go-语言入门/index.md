---
title: "GO 语言入门"
date: "2018-09-20"
categories: 
  - "go语言"
---

## 前置资料

**[下载开发工具](https://www.jetbrains.com/go/download/download-thanks.html "下载开发工具")**

**[常见问题](http://www.dev-share.top/2020/09/26/go-%e8%af%ad%e8%a8%80%e5%b8%b8%e8%a7%81%e9%97%ae%e9%a2%98/ "常见问题")**

**[Go 安装包下载-国内](https://studygolang.com/dl "Go 安装包下载-国内")**

**[Go 安装包下载](https://go.dev/dl/ "Go 安装包下载")**

* * *

## CentOS 7 中安装Golang

```ruby
## 官方地址
[root@Linux golang]# wget https://go.dev/dl/go1.20.3.linux-amd64.tar.gz
## 国内地址
[root@Linux golang]# wget https://studygolang.com/dl/golang/go1.20.3.linux-amd64.tar.gz

## 解压到本地环境变量
[root@Linux golang]# tar -zxvf go1.20.3.linux-amd64.tar.gz -C /usr/local

## 配置环境变量
cat >> ~/.bash_profile << ERIC
# golang env config
export GO111MODULE=on
export GOROOT=/usr/local/go
export PATH=\$PATH:\$GOROOT/bin:\$GOPATH/bin
ERIC

## 刷新环境变量
[root@Linux golang]# source ~/.bash_profile

## 查看Go 版本
[root@Linux golang]# go version
go version go1.20.3 linux/amd64

```

* * *

## go mod 命令介绍

> - `go mod` 它的作用就像是 **Node.js**项目中的 **package.json**
>     
> - 使用命令 **go mod init `你的项目名`**， 如执行命令：`go mod init flexi-build`， 这将会在当前项目中自动创建一个**go.mod**文件内容如下：
>     

```shell
[root@centos-04 (20:10:21) /data/siyu.mao/go]
└─# mkdir flexi-build && cd flexi-build && go mod init flexi-build
go: creating new go.mod: module flexi-build


[root@centos-04 (20:11:39) /data/siyu.mao/go/flexi-build]
└─# cat go.mod
module flexi-build

go 1.20

```

```go
Usage:

        go mod <command> [arguments]

The commands are:

    download    download modules to local cache               将模块下载到本地缓存
    edit        edit go.mod from tools or scripts             从工具或脚本编辑go.mod
    graph       print module requirement graph                输出项目依赖
    init        initialize new module in current directory    初始化一个项目
    tidy        add missing and remove unused modules         添加缺少的模块并删除未使用的模块
    vendor      make vendored copy of dependencies            制作依赖项的副本
    verify      verify dependencies have expected content     验证依赖项是否具有预期的内容
    why         explain why packages or modules are needed    解释为什么需要软件包或模块

Use "go help mod <command>" for more information about a command.

```

* * *

## go get -u 命令介绍

`go get` 命令将获取列在 `go.mod` 文件（Go 模块文件）中的包的最新版本或将包更新为最新版本。

`-u` 标志代表 "update"，它告诉 `go get` 命令即使现有版本已满足 `go.mod` 文件中指定的版本约束，也要更新包。

* * *

## 构建第一个 web服务器 go-web-server

```ruby
[root@controller ~]# mkdir go-web-server

# 添加包代理
[root@controller ~]# go env -w GOPROXY=https://goproxy.cn

# 创建 go.mod文件
[root@controller ~]# go mod init go-web-server

# 创建 go入口文件
[root@controller ~]# cat > go-web-server/main.go << ERIC

package main

import (
    "fmt"
    "net/http"
)

func main() {
    // 拦截根目录下("/")请求
    http.HandleFunc("/", func(writer http.ResponseWriter, request *http.Request) {
        // 返回影响体
        fmt.Fprintf(writer, "Hello World !")
    })
    // 开始监听
    http.ListenAndServe("127.0.0.1:8066", nil)
}

ERIC

# 测试访问
[root@controller ~]# curl 127.0.0.1:8066
Hello World !

```

**逐行来解读这个程序：**

- `package main`：声明了 main.go 所在的包，Go 语言中使用包来组织代码。一般一个文件夹即一个包，包内可以暴露类型或方法供其他包使用。但 main包是特殊的存在，可以没有实际的main文件夹。
- `import "fmt"`：fmt 是 Go 语言的一个标准库/包，用来处理标准输入输出。
- `func main`：main 函数是整个程序的入口，main 函数所在的包名也必须为 main。
- `fmt.Println("......")`：调用 fmt 包的 Println 方法

**go run main.go，其实是 2 步：**

- `go build main.go`：编译成二进制可执行程序
- `./main`：执行该程序

* * *

## 1\. 了解并使用，标准库启动Web服务

Go语言内置了 net/http库，封装了HTTP网络编程的基础的接口，我们实现的Gee Web 框架便是基于net/http的。我们接下来通过一个例子，简单介绍下这个库的使用。

```go
package main

import (
    "fmt"
    "net/http"
)

/**
 * 配置http请求监听
 */
func testHttpHandle() {

    // 监听请求路径为： "/"
    http.HandleFunc("/", func(writer http.ResponseWriter, request *http.Request) {
        fmt.Fprintf(writer, "URL.Path = %q \n", request.URL.Path)
    })

    // 监听请求路径为： "/hello"
    http.HandleFunc("/hello", func(writer http.ResponseWriter, request *http.Request) {
        for k, v := range request.Header {
            // fmt.Printf， 是把格式字符串输出到标准输出（一般是屏幕，可以重定向）
            // fmt.Sprintf，是把格式字符串输出到指定字符串中
            // fmt.Fprintf，是把格式字符串输出到指定文件设备中
            fmt.Fprintf(writer, "Header[%q] = %q\n", k, v)
        }
    })

    // 启动http服务
    http.ListenAndServe("0.0.0.0:8080", nil)

}

func main() {
    testHttpHandle()
}

```

* * *

## 2\. 以实现http.Handler接口的方式拦截所有http请求

Handler是一个接口，需要实现方法 ServeHTTP ，也就是说，只要传入任何实现了 ServerHTTP 接口的实例，所有的HTTP请求，就都交给了该实例处理了。

```go
package main

import (
    "fmt"
    "net/http"
)


// 我们定义了一个空的结构体Engine，实现了方法ServeHTTP。
type Engine struct{}

// 实现Engine结构的ServeHTTP方法
func (engine *Engine) ServeHTTP(writer http.ResponseWriter, request *http.Request) {

    switch request.URL.Path {
    case "/":
        fmt.Fprintf(writer, "URL.Path = %q \n", request.URL.Path)
    case "/hello":
        for k, v := range request.Header {
            // fmt.Printf， 是把格式字符串输出到标准输出（一般是屏幕，可以重定向）
            // fmt.Sprintf，是把格式字符串输出到指定字符串中
            // fmt.Fprintf，是把格式字符串输出到指定文件设备中
            fmt.Fprintf(writer, "Header[%q] = %q \n", k, v)
        }
    default:
        fmt.Fprintf(writer, "404 NOT FOUND: %s \n", request.URL)
    }
}

func main() {
    engine := new(Engine)
    http.ListenAndServe("0.0.0.0:8080", engine)
}

```

- 我们定义了一个空的结构体Engine，实现了方法ServeHTTP。这个方法有2个参数，第二个参数是 Request ，该对象包含了该HTTP请求的所有的信息，比如请求地址、Header和Body等信息；第一个参数是 ResponseWriter ，利用 ResponseWriter 可以构造针对该请求的响应。
    
- 在 main 函数中，我们给 ListenAndServe 方法的第二个参数传入了刚才创建的engine实例。至此，我们走出了实现Web框架的第一步，即，将所有的HTTP请求转向了我们自己的处理逻辑。还记得吗，在实现Engine之前，我们调用 http.HandleFunc 实现了路由和Handler的映射，也就是只能针对具体的路由写处理逻辑。比如/hello。但是在实现Engine之后，我们拦截了所有的HTTP请求，拥有了统一的控制入口。在这里我们可以自由定义路由映射的规则，也可以统一添加一些处理逻辑，例如日志、异常处理等。
    
- 代码的运行结果与之前的是一致的。
    

* * *

## 深入学习

**[Go 语言学习笔记](http://www.dev-share.top/2022/03/16/go-%e8%af%ad%e8%a8%80%e5%ad%a6%e4%b9%a0%e7%ac%94%e8%ae%b0/ "Go 语言学习笔记")**
