---
title: "CentOS 7 搭建ntp时钟服务器"
date: "2017-11-16"
categories: 
  - "centos"
---

###### ntp `服务端`叫 **`ntpd`**

```ruby
yum -y install ntpd

systemctl start ntpd

```

> - 使用服务端同步时间不是立即同步，但它会根据自己本身的设定，进行自动同步，只需要将 **`互联网 ntpd 服务器`地址**添加到 **`/etc/ntp.conf`** 配置文件中

* * *

###### ntpd服务端自动同步工作原理

```ruby
             [  互联网 ntpd 服务器  ]
                  ^           ^
                --|-----------|--
    [ 主机1 ntpd服务端 ]   [ 主机2 ntpd服务端 ]

```

* * *

* * *

* * *

###### ntp `客户端`叫 **`ntpdate`**

```ruby
yum -y install ntpdate

systemctl start ntpdate

```

###### ntpdate 同步 ntpd

`ntpdate 指定ntpd的IP地址`

```ruby
ntpdate 192.168.20.91
```

`或者指定互联网的 ntpd服务器`

```ruby
ntpdate ntp.aliyun.com
```

> - 使用客户端同步时间是会立即同步的，但必须要 **手动执行`ntpdate`** 命令，或者写定时任务同步才行

* * *

###### **ntpdate** 手动同步工作原理

```ruby
          [  互联网 ntpd服务器  ]
              ^             ^
            --|-------------|--
   [ 主机1 ntpdate ]   [ 主机2 ntpdate ]

```

* * *

* * *

* * *
