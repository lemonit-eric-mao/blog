---
title: 'Go 集成 RabbitMQ 客户端'
date: '2022-06-06T09:29:23+00:00'
status: publish
permalink: /2022/06/06/go-%e9%9b%86%e6%88%90-rabbitmq-%e5%ae%a2%e6%88%b7%e7%ab%af
author: 毛巳煜
excerpt: ''
type: post
id: 8715
category:
    - Go
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
---
##### 前置资料

**[理解 RabbitMQ 工作原理](http://www.dev-share.top/2022/09/09/%e7%90%86%e8%a7%a3-rabbitmq-%e5%b7%a5%e4%bd%9c%e5%8e%9f%e7%90%86/ "理解 RabbitMQ 工作原理")**

- - - - - -

##### 使用Go语言操作 RabbitMQ 客户端

> MQ 客户端分为两种：**推送者**、**接收者**

**[安装RabbitMQ服务端](http://www.dev-share.top/2020/02/09/docker-compose-%e5%ae%89%e8%a3%85-rabbitmq/ "安装RabbitMQ服务端")**

- - - - - -

##### **持久化**

**持久化要注意`3`个部分**

1. **队列持久化** 在声明队列配置，见`CreateQueue()`方法
2. **消息持久化** 在推送消息时配置，见`PublishMessageQueue()`方法
3. **在容器中持久化**  
  3.1 改docker-compsoe的配置 `hostname: eric_os`  
  3.2 路径映射 `./data:/var/lib/rabbitmq`

- - - - - -

###### connectmq.go 统一链接配置

```go
package rabbitmq_queue

import (
    "fmt"
    amqp "github.com/rabbitmq/amqp091-go"
    "iris-server-mq/commons/tools"
    "os"
)

type RabbitMQ struct {
    conn *amqp.Connection // 连接成功后的MQ对象
    ch   *amqp.Channel    // 通道
}

var mqURI string

// NewRabbitMQ 初始化MQ
func NewRabbitMQ() *RabbitMQ {

    // 使用环境变量配置，方便容器化
    uri := fmt.Sprintf("amqp://%s:%s@%s:%s/%s",
        os.Getenv("MQ_USER"),
        os.Getenv("MQ_PASSWORD"),
        os.Getenv("MQ_HOST"),
        os.Getenv("MQ_PORT"),
        os.Getenv("MQ_VHOST"),
    )

    // 创建连接
    conn, err := amqp.Dial(uri)
    tools.FailOnError(err, "操作失败，未链接到RabbitMQ")
    return &RabbitMQ{
        conn: conn,
    }
}

// CreateChannel 建立通道
func (mq *RabbitMQ) CreateChannel() {
    // 建立通道
    ch, err := mq.conn.Channel()
    tools.FailOnError(err, "操作失败，不能开启一个通道")
    mq.ch = ch
}

// CloseRabbitMQ 关闭链接
func (mq *RabbitMQ) CloseRabbitMQ() {

    mq.ch.Close()
    mq.conn.Close()
}

// ----------------------------------------------------------

// CreateQueue 声明队列
func (mq *RabbitMQ) CreateQueue() {

    // 声明队列 （名称和类型需要与存在的队列保持一致）
    _, err := mq.ch.QueueDeclare(
        "message-queue",
        true,  // durable 开启队列持久化
        false, // auto-deleted
        false, // internal
        false, // no-wait
        nil,
    )
    tools.FailOnError(err, "")
}


```

- - - - - -

###### producer.go 生产者

```go
// 发布消息，生产者

package rabbitmq_queue

import (
    "fmt"
    amqp "github.com/rabbitmq/amqp091-go"
    "iris-server-mq/commons/tools"
)

// PublishMessageQueue 发布消息到消息队列
func (mq *RabbitMQ) PublishMessageQueue() {

    message := fmt.Sprint(tools.Now(), " --=> 您有新的【Queue】消息，请注意查收！")

    // 发布消息到指定的消息队列
    err := mq.ch.Publish(
        "",              // exchange
        "message-queue", // routing key （根据使用的交换机类型可选择的是否需要routing key），如果不选择交换机，该参数为消息队列名称
        false,           // mandatory
        false,           // immediate
        amqp.Publishing{
            DeliveryMode: 2, // 消息持久化
            ContentType:  "text/plain",
            Body:         []byte(message),
        },
    )
    tools.FailOnError(err, "")
}


```

- - - - - -

###### consumer.go 消费者

```go
// 订阅消息，消费者

package rabbitmq_queue

import (
    "iris-server-mq/commons/tools"
    "log"
    "time"
)

func (mq *RabbitMQ) ConsumeMessage() {
    // 创建消费者并消费指定消息队列中的消息
    msgs, err := mq.ch.Consume(
        "message-queue", // message-queue
        "",              // consumer
        false,           // autoAck 设置为非自动确认(可根据需求自己选择)
        false,           // exclusive
        false,           // no-local
        false,           // no-wait
        nil,             // args
    )
    tools.FailOnError(err, "")

    // 获取消息队列中的消息
    forever := make(chan bool)
    go func() {
        for d := range msgs {
            // 延迟6秒在进行消费
            time.Sleep(6e9)
            log.Printf("收到消息: %s", d.Body)
            // 手动回复ack
            d.Ack(false)
        }
    }()
    log.Printf(" [消费者] 正在等待消息... ")
    
```

- - - - - -

###### main\_test.go 测试类

```go
package main

import (
    "github.com/kataras/iris/v12"
    "iris-server-mq/commons/mq/rabbitmq_queue"
    "iris-server-mq/commons/tools"
    "os"
)

func init() {
    // 数据库环境变量(构建时删除)
    os.Setenv("MQ_USER", "mao_siyu")
    os.Setenv("MQ_PASSWORD", "******")
    os.Setenv("MQ_HOST", "eric.rabbitmq.com")
    os.Setenv("MQ_PORT", "5672")
    os.Setenv("MQ_VHOST", "eric_vhost")
}

func main() {
    app := iris.Default()

    mq := rabbitmq_queue.NewRabbitMQ()
    mq.CreateChannel()
    mq.CreateQueue()
    // 向【Queue】推送消息
    go tools.SetInterval(2e9, func() {
        go mq.PublishMessageQueue()
    })
    // 从【Queue】中消费消息，内置定时器每6秒消费一次
    go mq.ConsumeMessage()

    // 启动服务
    app.Listen(":8080")
}


```

- - - - - -

- - - - - -

- - - - - -

###### **[项目地址](https://gitee.com/eric-mao/iris-server-mq "项目地址")**

- - - - - -

- - - - - -

- - - - - -