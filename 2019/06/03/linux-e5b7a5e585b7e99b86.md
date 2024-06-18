---
title: 'Linux 工具集'
date: '2019-06-03T07:54:48+00:00'
status: publish
permalink: /2019/06/03/linux-%e5%b7%a5%e5%85%b7%e9%9b%86
author: 毛巳煜
excerpt: ''
type: post
id: 4724
category:
    - Linux服务器
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
enclosure:
    - "http://qiniu.dev-share.top/rpm/htop-3.0.5-1.el8.x86_64.rpm\r\n145804\r\napplication/vnd.apple.pages\r\n"
    - "http://qiniu.dev-share.top/rpm/htop-2.2.0-3.el7.x86_64.rpm\r\n105672\r\napplication/vnd.apple.pages\r\n"
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
---
> `logrotate`是一个Linux系统内置的工具，用于管理日志文件。它的主要功能是定期轮转日志文件，以防止它们变得过大，节省磁盘空间并确保系统正常运行。  
>  在`/etc/logrotate.d/`目录中添加配置文件，系统会自动执行。

```bash
## 配置日志轮转
sudo tee /etc/logrotate.d/028-nohup 
```

**参数解释**

```bash
# 日志文件的路径，这里是示例路径
/mnt/data/0.2.8-Langchain-Chatchat/nohup.out {
    # 使用 root 用户执行 logrotate 任务
    su root root

    # 每天执行一次轮转
    daily

    # 保留最近 7 个轮转后的日志文件
    rotate 7

    # 对轮转后的日志文件进行压缩
    compress

    # 如果轮转后的日志文件不存在，则创建一个空文件
    create

    # 在日志文件名后添加日期扩展，形式如：nohup.out-20211211
    dateext

    # 如果日志文件缺失也不报错
    missingok

    # 如果日志文件为空则不轮转
    notifempty

    # 不创建空日志文件
    nocreate

    # 复制并截断原始日志文件，而不是重命名或删除
    copytruncate
}


```

- - - - - -

- - - - - -

- - - - - -

常用工具一次性安装
---------

```shell
yum install -y epel-release jq htop tree vim wget net-tools tcpdump httpd-tools iptraf nc bind-utils lm_sensors

```

- - - - - -

- - - - - -

- - - - - -

#### **终端输出彩色日志**

```ruby
cat > color.sh 
```

- - - - - -

- - - - - -

- - - - - -

##### **arp 工具**

如何查看网络环境是否支持ARP 广播或 ARP 代理？  
您可以通过以下方式来检查网络环境是否支持 ARP 广播或 ARP 代理：

> 使用 ping 命令：在 Kubernetes 集群内的一个节点上执行以下命令：
> 
> ```shell
> ping -b 255.255.255.255
> 
> ```
> 
>  如果命令可以成功执行并收到响应，则表示网络支持广播，因为该命令发送的是广播包。

- - - - - -

> 使用 arp 命令：在 Kubernetes 集群内的一个节点上执行以下命令：
> 
> ```shell
> yum install -y net-tools
> 
> arp -a
> 
> ```
> 
>  如果命令可以列出本地网络中的其他设备的 MAC 地址，则表示网络支持 ARP 协议，因为该命令使用 ARP 协议获取网络中的设备信息。

- - - - - -

> 使用 tcpdump 命令：在 Kubernetes 集群内的一个节点上执行以下命令：
> 
> ```shell
> yum install -y tcpdump
> 
> tcpdump -i <interface_name> arp
> </interface_name>
> ```
> 
>  其中，<interface_name> 是本地网络接口的名称，例如 eth0、enp3s0 等。如果命令可以输出 ARP 请求和响应信息，则表示网络支持 ARP 协议和广播。 </interface_name>

- - - - - -

**常用命令**

```shell
arp -a [<hostname>]        ：显示ARP缓存，如果指定了主机名，则只显示该主机的缓存。
arp -d <host>              ：从ARP缓存中删除指定的条目。
arp -s <host> <hwaddr>     ：向ARP缓存中添加一个静态条目，指定主机IP地址和对应的MAC地址。
arp -f [<filename>]        ：从指定文件中读取条目并添加到ARP缓存中。
arp -i <if>                ：指定使用的网络接口。
arp -n                     ：显示IP和MAC地址的数值形式，不使用名称解析。
arp -v                     ：显示详细信息，通常包括IP地址、MAC地址、类型和接口信息等。
arp -H <hw>                ：指定硬件地址类型，默认为ether，也就是以太网地址。
arp -A/-p/--protocol       ：指定协议族，默认为IPv4。
arp -e/-E                  ：以默认（Linux）或替代（BSD）风格显示所有主机的ARP缓存。
arp -D/--use-device        ：从指定的设备中读取MAC地址，并添加到ARP缓存中。
</hw></if></filename></hwaddr></host></host></hostname>
```

> 需要注意的是，这些选项和用法可能在不同的操作系统和版本中略有差异。建议在具体使用时，查看对应系统的文档或手册。

- - - - - -

- - - - - -

- - - - - -

##### **AB 压测工具**

```shell
## 直接安装
yum install -y httpd-tools


## 七牛云下载安装
wget http://qiniu.dev-share.top/file/httpd-tools.tar && tar -xvf httpd-tools.tar && rpm -ivh *.rpm

```

**测试**  
**ab -n `请求次数` -c `并发数` `URL`/**

```shell
ab -n 100 -c 10 http://www.baidu.com/

```

**参数说明**

```shell
-n  即requests，用于指定压力测试总共的执行次数。
-c  即concurrency，用于指定的并发数。
-t  即timelimit，等待响应的最大时间(单位：秒)。
-b  即windowsize，TCP发送/接收的缓冲大小(单位：字节)。
-p  即postfile，发送POST请求时需要上传的文件，此外还必须设置-T参数。
-u  即putfile，发送PUT请求时需要上传的文件，此外还必须设置-T参数。
-T  即content-type，用于设置Content-Type请求头信息，例如：application/x-www-form-urlencoded，默认值为text/plain。
-v  即verbosity，指定打印帮助信息的冗余级别。
-w  以HTML表格形式打印结果。
-i  使用HEAD请求代替GET请求。
-x  插入字符串作为table标签的属性。
-y  插入字符串作为tr标签的属性。
-z  插入字符串作为td标签的属性。
-C  添加cookie信息，例如："Apache=1234"(可以重复该参数选项以添加多个)。
-H  添加任意的请求头，例如："Accept-Encoding: gzip"，请求头将会添加在现有的多个请求头之后(可以重复该参数选项以添加多个)。
-A  添加一个基本的网络认证信息，用户名和密码之间用英文冒号隔开。
-P  添加一个基本的代理认证信息，用户名和密码之间用英文冒号隔开。
-X  指定使用的和端口号，例如:"126.10.10.3:88"。
-V  打印版本号并退出。
-k  使用HTTP的KeepAlive特性。
-d  不显示百分比。
-S  不显示预估和警告信息。
-g  输出结果信息到gnuplot格式的文件中。
-e  输出结果信息到CSV格式的文件中。
-r  指定接收到错误信息时不退出程序。
-h  显示用法信息，其实就是ab -help。

```

- - - - - -

- - - - - -

- - - - - -

##### **iptraf** Linux 网络监控（抓包）工具

```shell
## 安装
sudo apt install bmon

```

**使用**

```shell
## 直接用
bmon

```

- - - - - -

- - - - - -

- - - - - -

##### **nc** 查看端口是否可用

```ruby
## 安装
yum install -y nc


# 模拟测试
## node1 开启端口监听
nc -l 8301

## node2 测试链接
nc -v 10.18.7.0 8301


```

- - - - - -

###### 常见问题

ip地址能 ping通， 但是 nc端口不通如：

```ruby
dial tcp 10.18.7.0:8301: connect: no route to host


## 通常这种问题是 iptables 规则没有清理干净/乱了
## 刷新iptables
iptables --flush
iptables -tnat --flush


```

- - - - - -

- - - - - -

- - - - - -

##### **`k9s`[官方github](https://github.com/derailed/k9s/tags "官方github")**

```ruby
## 官方安装
wget https://github.com/derailed/k9s/releases/download/v0.25.18/k9s_Linux_x86_64.tar.gz \
     && tar -zxvf k9s_Linux_x86_64.tar.gz \
     && mv k9s /usr/local/bin/ \
     && k9s version



## 七牛云安装
wget http://qiniu.dev-share.top/tools/k9s_Linux_x86_64.tar.gz \
     && tar -zxvf k9s_Linux_x86_64.tar.gz \
     && mv k9s /usr/local/bin/ \
     && k9s version

## 使用
k9s


```

- - - - - -

- - - - - -

- - - - - -

##### **`nslookup`**

```ruby
## 安装
yum install -y bind-utils

```

**nslookup 域名 \[指定DNS\_SERVER\]**

```ruby
[root@master01 new_test]# nslookup www.dev-share.top 10.96.0.10
Server:         10.96.0.10
Address:        10.96.0.10#53

Non-authoritative answer:
Name:   www.dev-share.top
Address: 1.15.104.19




[root@master01 new_test]# nslookup www.dev-share.top
Server:         192.168.100.4
Address:        192.168.100.4#53

Non-authoritative answer:
Name:   www.dev-share.top
Address: 1.15.104.19


```

- - - - - -

- - - - - -

- - - - - -

##### **`dig`**

```ruby
## 安装
yum install -y bind-utils

```

dig 的其中一个查询格式为：

> dig \[@server\] \[-p {port}\] \[name\]

例如：`dig @127.0.0.1 -p 8600` 是指定 `8600` 端口作为 `DNS` 服务查询的端口；name 名称则表示要指定查询的资源名称。 **注: `DNS端口`通常默认为`53`**

- - - - - -

###### 通过 DNS 查询 Consul 服务信息

前面已经注册了 web 服务，那么 如何通过 Consul 的 DNS 接口(8600端口)查询 web 服务的信息？  
可在在默认主机上执行：

```ruby
## 关于 dig 命令，前面已经讲解了，web.service.consul 就是 [name] 部分。 Consul 会将注册的服务名称加上 .service.consul 做为命名。
dig @127.0.0.1 -p 8600 web.service.consul

```

- - - - - -

- - - - - -

- - - - - -

##### Linux **`jq`** 工具将Json字符串对象化

###### [安装](https://stedolan.github.io/jq/download/ "安装")

```shell
yum install -y epel-release && yum install -y jq

```

```shell
┌──(root@k8s1-master 13:49:10) - [/data/siyu.mao/white_list]
└─# echo '{"A":1, "next":{"B":2,"C":3}}, "D":4' | jq '{"数据重组":.next}'
{
  "数据重组": {
    "B": 2,
    "C": 3
  }
}


```

- - - - - -

```ruby
## 要解析的Json字符串
[root@master01 consul]# kubectl get secrets -n dhc-consul consul-bootstrap-acl-token -o json | jq
{
  "apiVersion": "v1",
  "data": {
    "token": "ZTljMjYyOTctMjM1MC0yYjAyLTk2ZjMtN2JjZTA3MDM5MTAw"
  },
  "kind": "Secret",
  "metadata": {
    "creationTimestamp": "2021-07-12T03:37:13Z",
    "managedFields": [
      {
        "apiVersion": "v1",
        "fieldsType": "FieldsV1",
        "fieldsV1": {
          "f:data": {
            ".": {},
            "f:token": {}
          },
          "f:type": {}
        },
        "manager": "consul-k8s",
        "operation": "Update",
        "time": "2021-07-12T03:37:13Z"
      }
    ],
    "name": "consul-bootstrap-acl-token",
    "namespace": "dhc-consul",
    "resourceVersion": "7229917",
    "uid": "c25c2d88-dca3-48eb-b78f-2b72d9121738"
  },
  "type": "Opaque"
}
[root@master01 consul]#

```

- - - - - -

```ruby
## 获取 .data.token的值
[root@master01 consul]# kubectl get secrets -n dhc-consul consul-bootstrap-acl-token -o json | jq '.data.token'
"ZTljMjYyOTctMjM1MC0yYjAyLTk2ZjMtN2JjZTA3MDM5MTAw"
[root@master01 consul]#


## 获取 .data.token不带双引号的值
[root@master01 consul]# kubectl get secrets -n dhc-consul consul-bootstrap-acl-token -o json | jq -r '.data.token'
ZTljMjYyOTctMjM1MC0yYjAyLTk2ZjMtN2JjZTA3MDM5MTAw
[root@master01 consul]#


## 对字符串进行解码
[root@master01 consul]# kubectl get secrets -n dhc-consul consul-bootstrap-acl-token -o json | jq -r '.data.token' | base64 -d
e9c26297-2350-2b02-96f3-7bce07039100
[root@master01 consul]#


```

- - - - - -

- - - - - -

- - - - - -

###### **[官网](https://asciinema.org/ "官网")**

###### **[Github地址](https://github.com/asciinema/asciinema-player/releases "Github地址")**

###### **[官方安装文档](https://asciinema.org/docs/installation#installing-on-linux "官方安装文档")**

- - - - - -

###### 安装终端录制工具

```ruby
yum -y install asciinema

## 如果 No package asciinema available. 找不到安装包，执行如下代码，将会从企业版Linux库配置包中安装扩展包
yum install epel-release

```

- - - - - -

###### 开始录制终端，并将文件生成到本地，生成剧本

```ruby
[root@mao-controllor ~]# asciinema rec demo.json
~ Asciicast recording started.
~ Hit Ctrl-D or type "exit" to finish.
[root@mao-controllor ~]# kubectl get nodes
NAME       STATUS   ROLES    AGE   VERSION
master01   Ready    master   47d   v1.16.6
worker01   Ready    <none>   47d   v1.16.6
worker02   Ready    <none>   47d   v1.16.6
worker03   Ready    <none>   47d   v1.16.6
[root@mao-controllor ~]#
</none></none></none>
```

- - - - - -

###### 退出

**随时按 `Ctrl-D` 完成录制**

```ruby
[root@mao-controllor ~]# exit
~ Asciicast recording finished.
[root@mao-controllor ~]#

[root@mao-controllor ~]# ll
demo.json
[root@mao-controllor ~]#

```

- - - - - -

###### 在终端回放

```ruby
[root@mao-controllor ~]# asciinema play demo.json

```

- - - - - -

###### **[在HTML5中播放 Demo](http://qiniu.dev-share.top/asciinema-player/asciinema-demo.html "在HTML5中播放 Demo")**

```
<pre data-language="HTML">```markup



    <link href="http://qiniu.dev-share.top/asciinema-player/3.0.0/asciinema-player.css" rel="stylesheet" type="text/css"></link>
    <style>
        div {
            width: 800px;
            height: 600px;
        }
    </style>



<h3>第一种用法</h3>
<div id="demo1"></div>


<h3>第二种用法</h3>
<div id="demo2"></div>


<h3>第三种用法</h3>
<div id="demo3"></div>

<script src="http://qiniu.dev-share.top/asciinema-player/3.0.0/asciinema-player.min.js"></script>
<script>
    let data = {
        "version": 1,
        "width": 204,
        "height": 59,
        "duration": 38.012932,
        "command": null,
        "title": null,
        "env": {
            "TERM": "xterm",
            "SHELL": "/bin/bash"
        },
        "stdout": [
            [ 0.070082, "\u001b]0;root@mao-controllor:~\u0007\u001b[?1034h[root@mao-controllor ~]# " ],
            [ 0.218946, "k" ], [ 0.130072, "u" ], [ 0.028884, "b" ], [ 0.160006, "e" ], [ 0.161009, "c" ], [ 0.163124, "t" ], [ 0.163124, "l" ],
            [ 0.487628, "g" ], [ 0.100941, "e" ], [ 0.087018, "t" ], [ 0.106371, " " ],
            [ 0.598573, "n" ], [ 0.098913, "o" ], [ 0.056102, "d" ], [ 0.163915, "e" ], [ 0.152781, "s" ], [ 0.551071, "\r\n" ],
            [ 0.305454, "NAME       STATUS   ROLES    AGE   VERSION\r\nmaster01   Ready    master   47d   v1.16.6\r\nworker01   Ready    <none>   47d   v1.16.6\r\nworker02   Ready    <none>   47d   v1.16.6\r\nworker03   Ready    <none>   47d   v1.16.6\r\n" ],
            [ 0.716233, "\u001b]0;root@mao-controllor:~\u0007\u001b[?1034h[root@mao-controllor ~]# " ], [ 1.716233 ]
        ]
    }

    <!--&#31532;&#19968;&#31181;&#29992;&#27861;-->
    AsciinemaPlayer.create("http://qiniu.dev-share.top/asciinema-player/demo.cast", document.getElementById('demo1'));
    <!--&#31532;&#20108;&#31181;&#29992;&#27861;-->
    AsciinemaPlayer.create("http://qiniu.dev-share.top/asciinema-player/demo.json", document.getElementById('demo2'));
    <!--&#31532;&#19977;&#31181;&#29992;&#27861;-->
    AsciinemaPlayer.create({data: data}, document.getElementById('demo3'));
</script>





```
```

- - - - - -

- - - - - -

- - - - - -

##### 查看 CPU 温度 (虚拟机看不了)

```ruby
[root@test1 ~]# yum install -y lm_sensors

# 如下可见我的 CPU 温度很高
[root@test1 ~]# sensors
coretemp-isa-0000
Adapter: ISA adapter
Package id 0:  +98.0°C  (high = +86.0°C, crit = +100.0°C)
Core 0:        +97.0°C  (high = +86.0°C, crit = +100.0°C)
Core 1:        +97.0°C  (high = +86.0°C, crit = +100.0°C)
Core 2:        +98.0°C  (high = +86.0°C, crit = +100.0°C)
Core 3:        +97.0°C  (high = +86.0°C, crit = +100.0°C)
Core 4:        +98.0°C  (high = +86.0°C, crit = +100.0°C)
Core 5:        +96.0°C  (high = +86.0°C, crit = +100.0°C)
Core 6:        +96.0°C  (high = +86.0°C, crit = +100.0°C)
Core 7:        +95.0°C  (high = +86.0°C, crit = +100.0°C)

nvme-pci-0200
Adapter: PCI adapter
Composite:    +54.9°C  (low  = -273.1°C, high = +80.8°C)
                       (crit = +80.8°C)
Sensor 1:     +54.9°C  (low  = -273.1°C, high = +65261.8°C)
Sensor 2:     +61.9°C  (low  = -273.1°C, high = +65261.8°C)

[root@test1 ~]#

```

- - - - - -

- - - - - -

- - - - - -

##### MyCLI

**[官网](https://www.mycli.net/install "官网")**  
**[官网Github](https://github.com/dbcli/mycli#rhel-centos "官网Github")**

```ruby
# 安装依赖
yum -y install gcc libffi-devel python-devel openssl-devel


# 安装依赖
yum install -y python3-pip


## 安装 Python3
wget https://www.python.org/ftp/python/3.10.0/Python-3.10.0.tgz && tar -zxvf Python-3.10.0.tgz
pushd ./Python-3.10.0
./configure --prefix=/usr/local/python3 && make && make install
ln -s /usr/local/python3/bin/python3 /usr/bin/python3
ln -s /usr/local/python3/bin/pip3 /usr/bin/pip3
alternatives --install /usr/bin/python python /usr/bin/python2 0
alternatives --install /usr/bin/python python /usr/bin/python3 1
echo 2 | alternatives --config python
python -V
popd


## 安装 mycli
pip3 install --upgrade pip
pip3 install cryptography==36.0.2
pip3 install mycli==1.24.1

## 切回 Python2
echo 1 | alternatives --config python

## 查看版本
mycli -V


```

- - - - - -

- - - - - -

- - - - - -

#### alias \[别名\]=\[指令名称\]

##### 新增别名

```ruby
alias anode='node --harmony'

```

##### 列出所有别名只输入 **alias**

```ruby
mao-siyu@mao-siyu-PC:~/文档/code/koa-example<span class="katex math inline">alias
alias anode='node --harmony'
alias la='ls -A'
alias ll='ls -alF'
alias ls='ls --color=auto'
alias node='node --harmony'
mao-siyu@mao-siyu-PC:~/文档/code/koa-example</span>

```

##### 删除别名 unalias \[别名\]

```ruby
mao-siyu@mao-siyu-PC:~/文档/code/koa-example<span class="katex math inline">unalias node
mao-siyu@mao-siyu-PC:~/文档/code/koa-example</span> alias
alias anode='node --harmony'
alias la='ls -A'
alias ll='ls -alF'
alias ls='ls --color=auto'
mao-siyu@mao-siyu-PC:~/文档/code/koa-example$

```

- - - - - -

- - - - - -

- - - - - -

##### 模糊查找器

###### 安装 fzf (Fuzzy finder)

**[指南](https://keelii.com/2018/08/12/fuzzy-finder-full-guide/ "指南")**  
**下载**

```ruby
git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf

```

**安装/卸载**

```ruby
~/.fzf/install

~/.fzf/uninstall

```

**加入环境变量，让界面更好看**

```ruby
cat >> ~/.bashrc 
```

`使用 cd /home/** 按tab键`

```ruby
[root@test1 ~]# cd /home/**

```

`使用 vim /home/** 按tab键`

```ruby
[root@test1 ~]# vim /home/**

```

- - - - - -

- - - - - -

- - - - - -

##### iftop 查看网络状态

```ruby
[root@k8s-master deploy]# yum install -y iftop
[root@k8s-master deploy]#
[root@k8s-master deploy]# iftop

```

- - - - - -

- - - - - -

- - - - - -

##### 简单自定义美化终端

```shell
## 临时
export PS1="[\[\033[01;36m\]\u\[\033[35m\]@\[\033[01;32m\]\h\[\033[00m\] (\[\033[01;33m\]\t\[\033[00m\]) \033[01;34m\]\w\[\033[00m\]] \n└─\\$ "

## 永久
cat >> ~/.bashrc 
```

##### kali风格美化终端

```shell
## 临时
export PS1="\n┌──(\[\033[01;36m\]\u\[\033[35m\]㉿\[\033[01;32m\]\h\[\033[00m\] \[\033[01;33m\]\t\[\033[00m\]) - [\033[01;34m\]\w\[\033[00m\]] \n└─\\$ "

## 永久
cat >> ~/.bashrc 
```

##### 美化终端

1. 安装基础环境 zsh

```ruby
[root@k8s-master ~]# yum install -y zsh

```

2. 安装 oh-my-zsh

```ruby
[root@k8s-master ~]# wget https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh -O - | sh

```

3. 卸载 oh-my-zsh

```ruby
[root@k8s-master ~]# wget https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/uninstall.sh -O - | sh

```

4. 更换zsh皮肤  
  https://github.com/robbyrussell/oh-my-zsh/wiki/Themes

```ruby
[root@test1 ~ ]$ vim ~/.zshrc
#ZSH_THEME="robbyrussell"
ZSH_THEME="gianu"
或
ZSH_THEME="agnoster"

```

- - - - - -

- - - - - -

- - - - - -

[ccat下载地址](https://github.com/jingweno/ccat/releases "ccat下载地址")

###### 让 cat亮起来

```ruby
[root@k8s-master deploy]#
[root@k8s-master deploy]# mkdir donwload
[root@k8s-master deploy]#
[root@k8s-master deploy]# cd donwload/
# 下载 ccat
[root@k8s-master donwload]#  wget https://github.com/jingweno/ccat/releases/download/v1.1.0/linux-amd64-1.1.0.tar.gz
[root@k8s-master ~]#
[root@k8s-master donwload]# tar -zxvf linux-amd64-1.1.0.tar.gz
[root@k8s-master donwload]# cd linux-amd64-1.1.0
# 将ccat保存到 cat所在的目录下
[root@k8s-master linux-amd64-1.1.0]# cp ccat /bin/
# 将ccat配置加入到所有用户
[root@k8s-master ~]# cat >> /etc/bashrc 
```

- - - - - -

- - - - - -

- - - - - -

##### 进程监控 htop

**rpm包安装**： http://rpmfind.net/linux/rpm2html/search.php?query=htop(x86-64)&amp;submit=Search+...&amp;system=epel&amp;arch=

```ruby
## CentOS 8
wget http://qiniu.dev-share.top/rpm/htop-3.0.5-1.el8.x86_64.rpm
rpm -ivh htop-3.0.5-1.el8.x86_64.rpm


## CentOS 7
wget http://qiniu.dev-share.top/rpm/htop-2.2.0-3.el7.x86_64.rpm
rpm -ivh htop-2.2.0-3.el7.x86_64.rpm


```

- - - - - -

###### 或者直接yum装

```ruby
## yum 安装
yum -y install epel-release && yum -y install htop

```

**参数详解：**

<table><thead><tr><th>参数</th><th>说明</th></tr></thead><tbody><tr><td>**`PID`**</td><td>进行的标识号</td></tr><tr><td>**`USER`**</td><td>运行此进程的用户</td></tr><tr><td>**`PRI`**</td><td>进程的优先级</td></tr><tr><td>**`NI`**</td><td>进程的优先级别值，默认的为0，可以进行调整</td></tr><tr><td>**`VIRT`**</td><td>进程占用的虚拟内存值   
 **`VIRT`：virtual memory usage**   
 1. 进程“需要的”虚拟内存大小，包括进程使用的库、代码、数据等   
 2. 假如进程申请100m的内存，但实际只使用了10m，那么它会增长100m，而不是实际的使用</td></tr><tr><td>**`RES`**</td><td>进程占用的物理内存值   
 **`RES`：resident memory usage 常驻内存**   
 1. 进程当前使用的内存大小，但不包括swap out   
 2. 包含其他进程的共享   
 3. 如果申请100m的内存，实际使用10m，它只增长10m，与VIRT相反   
 4. 关于库占用内存的情况，它只统计加载的库文件所占内存大小</td></tr><tr><td>**`SHR`**</td><td>进程占用的共享内存值   
 **`SHR`：shared memory**   
 1. 除了自身进程的共享内存，也包括其他进程的共享内存   
 2. 虽然进程只使用了几个共享库的函数，但它包含了整个共享库的大小   
 3. 计算某个进程所占的物理内存大小公式：RES – SHR   
 4. swap out后，它将会降下来</td></tr><tr><td>**`S`**</td><td>进程的运行状况，R表示正在运行、S表示休眠，等待唤醒、Z表示僵死状态</td></tr><tr><td>**`%CPU`**</td><td>该进程占用的CPU使用率</td></tr><tr><td>**`%MEM`**</td><td>该进程占用的物理内存和总内存的百分比</td></tr><tr><td>**`TIME+`**</td><td>该进程启动后占用的总的CPU时间</td></tr><tr><td>**`COMMAND`**</td><td>进程启动的启动命令名称</td></tr></tbody></table>

- - - - - -

- - - - - -

- - - - - -

##### pip

```ruby
# 安装
[root@dev18 ~]# yum -y install python2-pip -i https://pypi.douban.com/simple
[root@dev18 ~]#
# 使用
[root@dev18 ~]# pip install ansible
# 使用国内镜像
[root@dev18 ~]# pip install ansible -i https://pypi.douban.com/simple

```

- - - - - -

- - - - - -

- - - - - -

##### yum 常用命令

- 列出所有`未安装`与`已安装`的软件包，使用 @区分 `有@符`为已经安装，`没有@符`为未安装  
  `yum list`
- 安装软件包  
  `yum install -y 软件包名称`
- 删除软件包  
  `yum remove -y 软件包名称`
- 列出所有可更新的软件包  
  `yum list updates`
- 列出所有已安装的软件包  
  `yum list installed`
- 列出所有已安装但不在 Yum Repository 内的软件包  
  `yum list extras`

- - - - - -

- - - - - -

- - - - - -

##### zip

**压缩**

```ruby
[root@test3 ~]# zip -r 你的文件夹.zip 你的文件夹/

```

**解压**

```ruby
[root@test3 ~]# unzip -O CP936 你的zip文件.zip
Archive:  你的zip文件.zip
  inflating: 2018年5月24日.xlsx
  inflating: 2018年5月24日.xlsx
mao-siyu@pc:/mnt/1TB/docment$

```

- - - - - -

**`加密`压缩**

```ruby
[root@cloudserver deploy]# zip -rP '123&456' k8s-1.16.6-offline-setup-External-etcd.zip k8s-1.16.6-offline-setup-External-etcd/

```

**`解密`解压**

```ruby
[root@cloudserver deploy]# unzip k8s-1.16.6-offline-setup-External-etcd.zip
Archive:  k8s-1.16.6-offline-setup-External-etcd.zip
k8s-1.16.6-offline-setup-External-etcd/offline_setup/inventory.ini password: # 输入密码即可

# 或者
[root@cloudserver deploy]# unzip -P '123&456' k8s-1.16.6-offline-setup-External-etcd.zip

```

###### **`注意`: 使用windows系统加密的文件， 在`Linux解密解压是不行的`**

- - - - - -

- - - - - -

- - - - - -

##### lftp 客户端

**安装**

```ruby
[root@dev1 ~]# yum install -y lftp

```

###### 格式

```ruby
#登录到ftp--法1
lftp (ftp://)user:password@site:21  #ftp://可以省略，默认21端口可以省略

#登录到ftp--法2
lftp (ftp://)user@site:port   #这种方式回车后，系统提示输入密码


#登录到sftp---法1
lftp sftp://user:password@site:22  #如果是默认端口22，可以省略，如果不是就必须填写端口号

#登录到sftp---法2
lftp sftp://user@password:port

```

###### 用法

**查看要上传的文件**

```ruby
[root@dev1 ~]# ll
总用量 20933620
-rw-------. 1 root root 858723328 2月  26 12:09 006-eck-1.0.0.tar
-rw-------. 1 root root 858772992 2月  26 12:09 007-em-1.0.0.tar
-rw-------. 1 root root 845254144 2月  27 11:53 804-ean-1.0.0.tar
-rw-------. 1 root root 849477632 2月  27 11:55 806-ta-1.0.0.tar
[root@dev1 ~]#

```

**登录**  
`用户名`： eric  
`密码`： eric&amp;123 加双引号是为了解决密码中的特殊字符  
`FTP地址`： www.dev-share.top  
`端口`： 21

```ruby
[root@dev1 ~]# lftp eric:'eric&123'@www.dev-share.top:21
lftp eric@www.dev-share.top:~>
lftp eric@www.dev-share.top:~>
lftp eric@www.dev-share.top:~>
lftp eric@www.dev-share.top:/> cd /software/eric/
lftp eric@www.dev-share.top:/software/eric>
lftp eric@www.dev-share.top:/software/eric>
lftp eric@www.dev-share.top:/software/eric>
# 将本地当前目录中的所有tar文件，上传到 FTP服务器中的 /software/eric/ 目录下
lftp eric@www.dev-share.top:/software/eric> mput *.tar

```

- - - - - -

- - - - - -

- - - - - -

###### ethtool 网络管理工具

`ethtool 网卡`

```ruby
[root@test ~]# ethtool ens160
Settings for ens160:
        Supported ports: [ TP ]
        Supported link modes:   1000baseT/Full
                                10000baseT/Full
        Supported pause frame use: No
        Supports auto-negotiation: No
        Supported FEC modes: Not reported
        Advertised link modes:  Not reported
        Advertised pause frame use: No
        Advertised auto-negotiation: No
        Advertised FEC modes: Not reported
        Speed: 10000Mb/s
        Duplex: Full
        Port: Twisted Pair
        PHYAD: 0
        Transceiver: internal
        Auto-negotiation: off
        MDI-X: Unknown
        Supports Wake-on: uag
        Wake-on: d
        Link detected: yes
[root@test ~]#

```

**查看是否为万兆网卡**

```ruby
[root@test ~]# ethtool ens160 | grep Speed
        Speed: 10000Mb/s
[root@test ~]#

```

- - - - - -

- - - - - -

- - - - - -

###### Ubuntu 将命令发送到多个SSH会话工具

```ruby
sudo apt install terminator

```

- - - - - -

- - - - - -

- - - - - -

###### yumdownloader 工具 将 rpm下载到本地

```ruby
# 安装工具
yum -y install yum-utils

# 说明
yumdownloader
--resolve # 如果有依赖，会下载所有依赖
--downloadonly # 只下载不安装
--downloaddir= # 下载路径
ansible # 要下载的工具

# 使用 yumdownloader 下载 docker 离线包
yumdownloader --resolve --downloadonly --downloaddir=$PWD docker-ce-20.10.6-3.el7

# 离线安装
rpm -ivh --force --nodeps *.rpm

```

- - - - - -

- - - - - -

- - - - - -

###### tree

```ruby
yum -y install tree

```

```
-A 使用ASNI绘图字符显示树状图而非以ASCII字符组合。

-C 在文件和目录清单加上色彩，便于区分各种类型。

-d 显示目录名称而非内容。

-D 列出文件或目录的更改时间。

-f 在每个文件或目录之前，显示完整的相对路径名称。

-F 在执行文件，目录，Socket，符号连接，管道名称名称，各自加上"*","/","=","@","|"号。

-g 列出文件或目录的所属群组名称，没有对应的名称时，则显示群组识别码。

-i 不以阶梯状列出文件或目录名称。

-I 不显示符合范本样式的文件或目录名称。

-l 如遇到性质为符号连接的目录，直接列出该连接所指向的原始目录。

-n 不在文件和目录清单加上色彩。

-N 直接列出文件和目录名称，包括控制字符。

-p 列出权限标示。

-P 只显示符合范本样式的文件或目录名称。

-q 用"?"号取代控制字符，列出文件和目录名称。

-s 列出文件或目录大小。

-t 用文件和目录的更改时间排序。

-u 列出文件或目录的拥有者名称，没有对应的名称时，则显示用户识别码。

-x 将范围局限在现行的文件系统中，若指定目录下的某些子目录，其存放于另一个文件系统上，则将该子目录予以排除在寻找范围外。

```

- - - - - -

- - - - - -

- - - - - -