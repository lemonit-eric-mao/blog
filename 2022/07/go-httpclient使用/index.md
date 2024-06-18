---
title: "Go HttpClient使用"
date: "2022-07-15"
categories: 
  - "go语言"
---

###### **示例 HttpClient 向三方应用发起API调用**

```go
func HttpClient(method string, url string, payload io.Reader) []byte {

    // 1. 构建Request请求对象
    req, _ := http.NewRequest(method, url, payload)
    // 2. 配置请求头
    req.Header.Add("Content-Type", "application/json")

    // 3. 忽略 https 证书验证
    transport := &http.Transport{
        TLSClientConfig: &tls.Config{InsecureSkipVerify: true},
    }

    // 4. 初始化 http.Client 对象
    client := &http.Client{Transport: transport}

    // 5. 向三方应用发起请求
    res, _ := client.Do(req)
    defer res.Body.Close()

    // 6. 读取返回的结果
    body, _ := ioutil.ReadAll(res.Body)

    return body
}

```

* * *

###### **示例 HttpClient`BasicAuth` 向三方应用发起API调用**

```go
func HttpClientBasicAuth(method string, url, Username, Password string, payload io.Reader) []byte {

    // 1. 构建Request请求对象
    req, _ := http.NewRequest(method, url, payload)

    // 2. 配置请求头
    req.Header.Add("Content-Type", "application/json")
    // 2.1 设置用户名密码
    req.SetBasicAuth(Username, Password)

    // 3. 忽略 https 证书验证
    transport := &http.Transport{
        TLSClientConfig: &tls.Config{InsecureSkipVerify: true},
    }

    // 4. 初始化 http.Client 对象
    client := &http.Client{Transport: transport}

    // 5. 向三方应用发起请求
    res, _ := client.Do(req)
    defer res.Body.Close()

    // 6. 读取返回的结果
    body, _ := ioutil.ReadAll(res.Body)

    return body
}

```

* * *

* * *

* * *

* * *

* * *

* * *

##### 实际应用

###### **nettool.go** 封装网络工具类

```go
package tools

import (
    "crypto/tls"
    "io"
    "io/ioutil"
    "net/http"
)

type NetTool struct {
    client *http.Client
}

// NewHttpClient
// 1. 初始化网络工具
func NewHttpClient() *NetTool {

    transport := &http.Transport{
        TLSClientConfig: &tls.Config{InsecureSkipVerify: true},
    }

    return &NetTool{
        client: &http.Client{Transport: transport},
    }
}

// Post
// 2.1 POST 请求封装
func (n *NetTool) Post(url string, payload io.Reader) []byte {

    // 1. 构建Request请求对象
    req, err := http.NewRequest("POST", url, payload)
    if err != nil {
        panic(err.Error())
    }

    // 2. 配置请求头
    req.Header.Add("Content-Type", "application/json")

    // 3. 发送请求
    body := n.Send(req)

    return body
}

// PostBasicAuth
// 2.2 POST 请求封装
func (n *NetTool) PostBasicAuth(url, Username, Password string, payload io.Reader) []byte {

    // 1. 构建Request请求对象
    req, err := http.NewRequest("POST", url, payload)
    if err != nil {
        panic(err.Error())
    }

    // 2. 配置请求头
    req.Header.Add("Content-Type", "application/json")
    // 2.1 设置用户名密码
    req.SetBasicAuth(Username, Password)

    // 3. 发送请求
    body := n.Send(req)

    return body
}

// Get
// 2.3 GET 请求封装
func (n *NetTool) Get(url string) []byte {
    // 1. 构建Request请求对象
    req, err := http.NewRequest("GET", url, nil)
    if err != nil {
        panic(err.Error())
    }

    // 2. 配置请求头
    //req.Header.Add("Content-Type", "application/json")

    // 3. 发送请求
    body := n.Send(req)

    return body
}

// GetBasicAuth
// 2.4 GET 请求封装
func (n *NetTool) GetBasicAuth(url, Username, Password string, payload io.Reader) []byte {
    // 1. 构建Request请求对象
    req, err := http.NewRequest("GET", url, payload)
    if err != nil {
        panic(err.Error())
    }

    // 2. 配置请求头
    req.Header.Add("Content-Type", "application/json")
    // 2.1 设置用户名密码
    req.SetBasicAuth(Username, Password)

    // 3. 发送请求
    body := n.Send(req)

    return body
}

// Send
// 3. 发送请求，并获得返回结果
func (n *NetTool) Send(req *http.Request) []byte {
    res, err := n.client.Do(req)
    if err != nil {
        panic(err.Error())
    }
    defer res.Body.Close()

    body, err := ioutil.ReadAll(res.Body)
    if err != nil {
        panic(err.Error())
    }

    return body
}

```

* * *

###### **attackIpRes.go** 实体类接收查询结果

```go
package hfish

type AttackIpRes struct {
    ResponseCode int    `json:"response_code"`
    VerboseMsg   string `json:"verbose_msg"`
    Data         AttackData
}

type AttackData struct {
    AttackIp []string `json:"attack_ip"`
}

```

* * *

###### **hfish.go** 测试类实际使用

```go
package service

import (
    "encoding/json"
    "fmt"
    "iris-server-transfer-server/commons/tools"
    "iris-server-transfer-server/src/model/vo/hfish"
    "os"
    "strconv"
    "strings"
)

type HFishService struct {
}

func NewHFishService() *HFishService {
    return &HFishService{}
}

// ------------------------ 蜜罐 REST API ------------------------

// QueryHFishIpList
// 查询HFish所有数据
func (a *HFishService) QueryHFishIpList() *hfish.AttackIpRes {

    url := fmt.Sprintf("%s/api/v1/attack/ip?api_key=%s", os.Getenv("H_FISH_URL"), os.Getenv("H_FISH_API_KEY"))
    starTime, _ := strconv.Atoi(os.Getenv("H_FISH_START_TIME"))
    endTime, _ := strconv.Atoi(os.Getenv("H_FISH_END_TIME"))
    s := fmt.Sprintf(`{
        "start_time": %d,
        "end_time": %d,
        "intranet": -1,
        "source": 0,
        "threat_label": [
            "Scanner",
            "IDC",
            "Spam"
        ]
    }`, starTime, endTime)
    // 请求参数
    payload := strings.NewReader(s)

    body := tools.NewHttpClient().Post(url, payload)

    // 将结果转为对象
    result := &hfish.AttackIpRes{}
    json.Unmarshal(body, &result)

    return result
}

```

* * *

* * *

* * *

### **[项目地址](https://gitee.com/eric-mao/iris-server-transfer-server "项目地址")**
