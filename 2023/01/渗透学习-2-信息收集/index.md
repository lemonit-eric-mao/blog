---
title: "渗透学习-2. 信息收集"
date: "2023-01-15"
categories: 
  - "非技术文档"
---

# 信息收集-常用工具

## dnsenum

- > - 为什么要使用`dnsenum`?
    >     - `dns` 信息会暴露很多的服务信息，往往一个渗透测试项目就是从一个域名开始的，拿到一个域名后，也往往是先通过 `dns` 信息收集的方式获得目标更多的信息。
    >         
    >     - 所以掌握 `dns` 信息收集的工具是渗透测试者必须的。
    >         
    >         - 通过 `dns` 信息，我们可以获取到 `ip` 地址，根据 `IP` 地址可以获取同网段其他 `ip` 地址，而这些 `ip` 地址后面就能获取到开放的端口号，然后通过开发的端口号可以获取到背后跑的是什么服务。
    >         - 通过 `dns` 信息还能获取到一些子域名信息，获取到 `dns` 域名注册信息，甚至可能对 `dns` 服务器做区域传输，把整个目标后面的信息全部获取到。
    >         - `dnsenum` 就是一款用于收集 `dns` 信息的工具，这款工具通过`字典爆破`、`搜索引擎`、`whois 查询`、`区域传输`等手段用于获取域名背后的 `dns 信息`。
    >     - `dnsenum` 在默认情况下会综合查询给定域名后面的 `A 记录`、`NS 记录`、`MX 记录`、`bind 版本信息`以及尝试做区域传输，最后使用默认的字典做 `dns` 信息的爆破。
    >         - 当查询到 `C 类地址`的时候还会做`反向的域名查询`，以`发现更多的域名`。
    >         - 默认的字典文件所在位置是：`/usr/share/dnsenum/dns.txt`
    >             
    >         - `dnsenum` 是多线程 `perl` 脚本，用于枚举域的 `DNS` 信息并发现不连续的 `ip` 地址。
    >             
    >         - 可以用它进行如下操作：
    >             
    >             1. 获取主机记录（A 记录）
    >             2. 获取域名服务器
    >             3. 获取 `MX` 记录
    >             4. 在域名服务器上执行 `axfr` 查询并获取绑定版本
    >             5. 通过 Google 抓取获取额外的域名和子域（`Google query="allinurl:-www site:domain"`）
    >             6. 通过字典文件进行暴力破解子域，也可以对具有 `NS` 记录的子域执行递归查询
    >             7. 计算 `C 类网络地址范围`并对其进行 `whois` 查询
    >             8. 在 `netrange（C 类或者 whois netrange）`上执行反向查找
    >             9. 将 `ip-blocks` 写入 `domain_ips.txt` 文件
    > - **该程序对渗透测试人员、【`道德黑客`】和【`取证专家`】很有用。它还可以【用于`安全测试`】。**
    >     
    > - 接下来，以 `https://www.12306.cn` 网站为例
    >     
    
- ```shell
    ┌──(root㉿kali)-[~]
    └─# dnsenum 12306.cn
    
    
    dnsenum VERSION:1.2.6
    
    ----- 12306.cn   -----
    
    
    # 域名解析后的相关信息如下
    
    # 获取域名对应的【主机地址】信息
    #   可以看出，当前Web服务器，使用了负载均衡技术，如下，一个域名对应了多IP地址
    Host's addresses:
    __________________
    
    12306.cn.wsglb0.com.                     60       IN    A        113.6.77.27    # 黑龙江省绥化市 联通
    12306.cn.wsglb0.com.                     60       IN    A        222.163.80.15  # 吉林省四平市 联通
    12306.cn.wsglb0.com.                     60       IN    A        175.23.174.51  # 吉林省通化市 联通
    
    
    # 获取【Name Servers】信息
    Name Servers:
    ______________
    
    ins1.zdnscloud.com.                      3573     IN    A        27.221.63.3    # 山东省青岛市 联通
    ins1.zdnscloud.com.                      3573     IN    A        119.167.244.44 # 山东省青岛市 联通
    vns1.zdnscloud.biz.                      20920    IN    A        203.99.22.3    # 北京市
    vns1.zdnscloud.biz.                      20920    IN    A        203.99.23.3    # 北京市
    dns1.zdnscloud.info.                     3174     IN    A        114.67.16.205  # 广东省广州市 电信
    dns1.zdnscloud.info.                     3174     IN    A        114.67.16.206  # 广东省广州市 电信
    cns1.zdnscloud.net.                      2299     IN    A        42.62.2.24     # 北京市 电信&联通
    cns1.zdnscloud.net.                      2299     IN    A        42.62.2.29     # 北京市 电信&联通
    
    
    # 二级域名相关的【邮箱】信息
    Mail (MX) Servers:
    ___________________
    
    mail.12306.cn.                           21600    IN    A        117.10.116.6   # 天津市 联通
    
    
    # 在【Name Servers】上执行 【AXFR (DNS 区域传输)】 查询并获取 BIND 版本
    Trying Zone Transfers and getting Bind Versions:
    _________________________________________________
    
    
    Trying Zone Transfer for 12306.cn on ins1.zdnscloud.com ...
    AXFR record query failed: corrupt packet
    
    Trying Zone Transfer for 12306.cn on vns1.zdnscloud.biz ...
    AXFR record query failed: corrupt packet
    
    Trying Zone Transfer for 12306.cn on dns1.zdnscloud.info ...
    AXFR record query failed: corrupt packet
    
    Trying Zone Transfer for 12306.cn on cns1.zdnscloud.net ...
    AXFR record query failed: corrupt packet
    
    
    # 使用【字典爆破】获取域名传输的漏洞，这个过程通常会很长
    Brute forcing with /usr/share/dnsenum/dns.txt:
    _______________________________________________
    
    mail.12306.cn.                           21600    IN    A        117.10.116.6
    mobile.12306.cn.                         2131     IN    CNAME    mobile.12306.cn.lxdns.com.
    mobile.12306.cn.lxdns.com.               60       IN    A        218.7.198.13
    mobile.12306.cn.lxdns.com.               60       IN    A        122.143.28.12
    mobile.12306.cn.lxdns.com.               60       IN    A        58.244.182.23
    mobile.12306.cn.lxdns.com.               60       IN    A        122.143.28.11
    mobile.12306.cn.lxdns.com.               60       IN    A        218.7.198.254
    mobile.12306.cn.lxdns.com.               60       IN    A        139.215.227.118
    search.12306.cn.                         3600     IN    CNAME    search.12306.cn.wsglb0.com.
    search.12306.cn.wsglb0.com.              60       IN    A        175.23.174.51
    search.12306.cn.wsglb0.com.              60       IN    A        222.163.80.15
    search.12306.cn.wsglb0.com.              60       IN    A        113.6.77.27
    www.12306.cn.                            21168    IN    CNAME    www.12306.cn.lxdns.com.
    www.12306.cn.lxdns.com.                  60       IN    A        218.7.198.13
    www.12306.cn.lxdns.com.                  60       IN    A        218.7.198.254
    www.12306.cn.lxdns.com.                  60       IN    A        139.215.227.118
    www.12306.cn.lxdns.com.                  60       IN    A        122.143.28.12
    www.12306.cn.lxdns.com.                  60       IN    A        122.143.28.11
    
    
    # 计算 C 类域网络范围并对它们执行 whois 查询
    12306.cn class C netranges:
    ____________________________
    
     117.10.116.0/24
    
    
    # 对 netranges（C 类或/和 whois netranges）执行【DNS地址反向查找】来获取更多的域名信息
    Performing reverse lookup on 256 ip addresses:
    _______________________________________________
    
    
    0 results out of 256 IP addresses.
    
    
    # 将【ip-blocks】写入【domain_ips.txt】文件
    12306.cn ip blocks:
    ____________________
    
    
    done.
    
    ┌──(root㉿kali)-[~]
    └─#
    
    ```
    

## whois

- > - 查看域名注册信息
    > - 接下来，以 `https://www.12306.cn` 网站为例
    
- ```shell
    ┌──(root㉿kali)-[~]
    └─# whois 12306.cn
    
    
    Domain Name: 12306.cn
    ROID: 20030310s10001s00012731-cn
    Domain Status: ok
    Registrant: 中国铁道科学研究院集团有限公司
    Registrant Contact Email: 13501238352@139.com
    Sponsoring Registrar: 北京中科三方网络技术有限公司
    Name Server: cns1.zdnscloud.net
    Name Server: dns1.zdnscloud.info
    Name Server: ins1.zdnscloud.com
    Name Server: vns1.zdnscloud.biz
    Registration Time: 2003-03-10 18:50:16
    Expiration Time: 2029-01-13 14:16:31
    DNSSEC: unsigned
    
    ┌──(root㉿kali)-[~]
    └─#
    
    ```
    

## nslookup

- > - `DNS`解析工具
    > - 接下来，以 `https://www.12306.cn` 网站使用的其中一个`DMS`为例
    
- ```shell
    ┌──(root㉿kali)-[~]
    └─# nslookup 12306.cn
    
    
    # 我自己使用的【DNS服务器】地址
    Server:         8.8.8.8
    Address:        8.8.8.8#53
    
    # 这是解析【12306.cn】域名时，用到的每一跳的【DNS服务器名】与【DNS服务器IP地址】
    Non-authoritative answer:
    12306.cn        canonical name = 12306.cn.wsglb0.com.
    Name:   12306.cn.wsglb0.com
    Address: 222.163.80.15
    Name:   12306.cn.wsglb0.com
    Address: 113.6.77.27
    Name:   12306.cn.wsglb0.com
    Address: 175.23.174.51
    
    ```
    

## dig

- > - 常用参数
    >     - `+noall` 什么都不输出
    >     - `+answer` 只显示answer信息
    >     - `any` 显示更多信息
    >     - `-x` 反向解析
    >     - `+trace` DNS追踪
    > - 正向解析 `dig @dns服务器地址 要解析的域名`
    > - 反向解析 `dig -x dns服务器地址`
    > - 接下来，以 `https://www.12306.cn` 网站使用的其中一个`DMS`为例
    
- **正向解析**
    
    - 默认用法
        
    - ```shell
        ┌──(root㉿kali)-[~]
        └─# dig @8.8.8.8 12306.cn
        
        
        ; <<>> DiG 9.18.8-1-Debian <<>> @8.8.8.8 12306.cn
        ; (1 server found)
        ;; global options: +cmd
        ;; Got answer:
        ;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 9731
        ;; flags: qr rd ra; QUERY: 1, ANSWER: 4, AUTHORITY: 0, ADDITIONAL: 1
        
        ;; OPT PSEUDOSECTION:
        ; EDNS: version: 0, flags:; udp: 512
        ;; QUESTION SECTION:
        ;12306.cn.                      IN      A
        
        ;; ANSWER SECTION:
        12306.cn.               3153    IN      CNAME   12306.cn.wsglb0.com.
        12306.cn.wsglb0.com.    60      IN      A       175.23.174.51
        12306.cn.wsglb0.com.    60      IN      A       113.6.77.27
        12306.cn.wsglb0.com.    60      IN      A       222.163.80.15
        
        ;; Query time: 72 msec
        ;; SERVER: 8.8.8.8#53(8.8.8.8) (UDP)
        ;; WHEN: Sun Jan 15 16:53:11 CST 2023
        ;; MSG SIZE  rcvd: 118
        
        
        ┌──(root㉿kali)-[~]
        └─#
        
        ```
        
    - 添加参数 `+noall` `+answer`
        
    - ```shell
        ┌──(root㉿kali)-[~]
        └─# dig +noall +answer @8.8.8.8 12306.cn
        12306.cn.               3600    IN      CNAME   12306.cn.wsglb0.com.
        12306.cn.wsglb0.com.    60      IN      A       113.6.77.27
        12306.cn.wsglb0.com.    60      IN      A       222.163.80.15
        12306.cn.wsglb0.com.    60      IN      A       175.23.174.51
        
        ```
        
    - 添加参数 `+noall` `+answer` `any`
        
    - ```shell
        ┌──(root㉿kali)-[~]
        └─# dig +noall +answer @8.8.8.8 12306.cn any
        12306.cn.               3600    IN      NS      vns1.zdnscloud.biz.
        12306.cn.               3600    IN      NS      ins1.zdnscloud.com.
        12306.cn.               3600    IN      NS      dns1.zdnscloud.info.
        12306.cn.               3600    IN      NS      cns1.zdnscloud.net.
        12306.cn.               3600    IN      CNAME   12306.cn.wsglb0.com.
        12306.cn.               3600    IN      SOA     cns1.zdnscloud.net. mail.knet.cn. 137 3600 3600 3600 900
        12306.cn.               21600   IN      MX      10 mail.12306.cn.
        12306.cn.               3600    IN      TXT     "v=spf1 ip4:124.127.44.251 ip4:114.251.18.38 ip4:61.232.5.39 ip4:124.127.44.247 ip4:114.251.18.30 ip4:61.232.5.30 ip4:123.151.17.4 ip4:111.33.90.4 ip4:117.10.116.4 -all"
        
        ```
        
- **`DNS`反向解析**
    
    - 默认用法
        
    - ```shell
        ┌──(root㉿kali)-[~]
        └─# dig -x 8.8.8.8
        
        ; <<>> DiG 9.18.8-1-Debian <<>> -x 8.8.8.8
        ;; global options: +cmd
        ;; Got answer:
        ;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 15000
        ;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1
        
        ;; OPT PSEUDOSECTION:
        ; EDNS: version: 0, flags:; udp: 512
        ;; QUESTION SECTION:
        ;8.8.8.8.in-addr.arpa.          IN      PTR
        
        ;; ANSWER SECTION:
        8.8.8.8.in-addr.arpa.   20806   IN      PTR     dns.google.
        
        ;; Query time: 60 msec
        ;; SERVER: 8.8.8.8#53(8.8.8.8) (UDP)
        ;; WHEN: Sun Jan 15 17:07:20 CST 2023
        ;; MSG SIZE  rcvd: 73
        
        
        ┌──(root㉿kali)-[~]
        └─#
        
        ```
        
    - 添加参数 `+noall` `+answer`
        
    - ```shell
        ┌──(root㉿kali)-[~]
        └─# dig +noall +answer -x 8.8.8.8
        8.8.8.8.in-addr.arpa.   21149   IN      PTR     dns.google.
        
        ┌──(root㉿kali)-[~]
        └─#
        ```
