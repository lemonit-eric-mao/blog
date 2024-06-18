---
title: "Go语言 构建 web 服务器"
date: "2020-09-26"
categories: 
  - "go语言"
---

###### **[项目地址](https://gitee.com/eric-mao/go-web-server "项目地址")**

* * *

###### 项目结构

```ruby
go-web-server
│
├─pkgs                      # 下载的依赖包，默认放在它下面; Module GOPATH 一定要指定在pkgs上，否则找不到下载的依赖包
│  └─pkg
│      ├─mod
│      └─......
│
├─src
│   ├─ common
│   └─database              # 自定义的数据库连接文件
│           InfluxDB.go
│           MySQL.go
│
│  .gitignore
│  config.yaml              # 数据库相关配置信息
│  go.mod
│  go.sum
│  main.go                  # 程序入口
└─ README.md

```

* * *

###### config.yaml

```yaml
influxdb:
  host: 127.0.0.1
  port: 8060
  dbname: MyInfluxDB
  username: root
  password: 123456

mysql:
  host: 127.0.0.1
  port: 3306
  dbname: MySQLDB
  username: root
  password: 123456

```

* * *

###### InfluxDB.go

```go
package database

/**
 * 这里的代码采用简化的方式编写
 */
import (
    "gopkg.in/yaml.v3"
    "os"
)

/**
 * 定义与yaml文件中属性，相同层级的结构对象
 * influxdb:
 *   host: 127.0.0.1
 *   port: 8060
 *   dbname: MyInfluxDB
 *   username: root
 *   password: 123456
 */
type (
    InfluxDB struct {
        InfluxDBEntity InfluxDBEntity `yaml:"influxdb"`
    }

    InfluxDBEntity struct {
        UserName  string `yaml:"username"`
        Password  string `yaml:"password"`
        DataBases string `yaml:"dbname"`
        Host      string `yaml:"host"`
        Port      string `yaml:"port"`
    }
)

/**
 * 读取 InfluxDB 配置
 * 返回 InfluxDB 结构对象
 */
func GetInfluxDB(filepath string) *InfluxDB {

    // 初始化结构对象
    influxdb := new(InfluxDB)
    // 打开读取文件内容, 并忽略异常
    yamlFile, _ := os.Open(filepath)
    // 简写，解析文件内容到 influx结构对象中
    yaml.NewDecoder(yamlFile).Decode(influxdb)
    return influxdb
}

```

* * *

###### MySQL.go

```go
package database

/**
 * 这里的代码采用拆分详解的方式编写
 */
import (
    "gopkg.in/yaml.v3"
    "os"
)

/**
 * 定义与yaml文件中属性，相同层级的结构对象
 * mysql:
 *   host: 127.0.0.1
 *   port: 3306
 *   dbname: MySQLDB
 *   username: root
 *   password: 123456
 */
type MySQL struct {
    MySQLEntity MySQLEntity `yaml:"mysql"`
}
type MySQLEntity struct {
    UserName  string `yaml:"username"`
    Password  string `yaml:"password"`
    DataBases string `yaml:"dbname"`
    Host      string `yaml:"host"`
    Port      string `yaml:"port"`
}

/**
 * 读取 MySQL 配置
 * 返回 MySQL 结构对象
 */
func GetMySQL(filepath string) *MySQL {

    // 初始化结构对象
    mysql := &MySQL{}
    // 打开读取文件内容
    yamlFile, err := os.Open(filepath)
    // 如果读取文件失败
    if err != nil {
        return nil
    }
    // 解析文件内容
    var decoder = yaml.NewDecoder(yamlFile)
    // 将解析后的文件内容，保存到结构对象中
    decoder.Decode(mysql)

    return mysql
}

```

* * *

###### main.go

```go
package main

import (
    "encoding/json"
    "fmt"
    "go-web-server/src/database"
    "net/http"
)

/**
 * 程序入口
 */
func main() {

    router()
}

/**
 * 定义路由
 */
func router() {

    // 拦截根目录下("/mysql")请求
    http.HandleFunc("/influx", func(writer http.ResponseWriter, request *http.Request) {
        // 获取配置文件内容
        var influx = database.GetInfluxDB("./config.yaml")
        // 将结构对象转为 json对象， _下划线在go中表示忽略
        jsons, _ := json.Marshal(influx.InfluxDBEntity)
        // 返回影响体
        fmt.Fprintf(writer, string(jsons))
    })

    // 拦截根目录下("/mysql")请求
    http.HandleFunc("/mysql", func(writer http.ResponseWriter, request *http.Request) {
        // 获取配置文件内容
        var mysql = database.GetMySQL("./config.yaml")
        // 将结构对象转为 json对象， _下划线在go中表示忽略
        jsons, _ := json.Marshal(mysql.MySQLEntity)
        // 返回影响体
        fmt.Fprintf(writer, string(jsons))
    })

    // 开始监听
    fmt.Println("http://127.0.0.1:8066/influx")
    fmt.Println("http://127.0.0.1:8066/mysql")
    http.ListenAndServe("127.0.0.1:8066", nil)
}

```

* * *

###### 访问

```ruby
curl http://127.0.0.1:8066/influx
{"UserName":"root","Password":"123456","DataBases":"MyInfluxDB","Host":"127.0.0.1","Port":"8060"}


curl http://127.0.0.1:8066/mysql
{"UserName":"root","Password":"123456","DataBases":"MySQLDB","Host":"127.0.0.1","Port":"3306"}

```

* * *

* * *

* * *
