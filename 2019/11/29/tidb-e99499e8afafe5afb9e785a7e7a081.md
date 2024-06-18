---
title: 'TiDB 错误对照码'
date: '2019-11-29T02:23:39+00:00'
status: publish
permalink: /2019/11/29/tidb-%e9%94%99%e8%af%af%e5%af%b9%e7%85%a7%e7%a0%81
author: 毛巳煜
excerpt: ''
type: post
id: 5163
category:
    - TiDB
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
###### [官方文档](https://pingcap.com/docs-cn/stable/reference/error-codes/#%E9%94%99%E8%AF%AF%E7%A0%81 "官方文档")

###### [MySQL 错误码对照表](http://www.dev-share.top/2019/11/28/mysql-%E9%94%99%E8%AF%AF%E7%A0%81%E5%AF%B9%E7%85%A7%E8%A1%A8/ "MySQL 错误码对照表")

<table><thead><tr><th align="center"><label style="width:60px">错误码</label></th><th align="left">**错误信息**</th><th align="left">**问题原因**</th></tr></thead><tbody><tr><td align="center">`8001`</td><td align="left">`空`</td><td align="left"> 请求使用的内存超过 TiDB 内存使用的阈值限制</td></tr><tr><td align="center">`8002`</td><td align="left">`空`</td><td align="left"> 带有 SELECT FOR UPDATE 语句的事务，在遇到写入冲突时，为保证一致性无法进行重试，事务将进行回滚并返回该错误</td></tr><tr><td align="center">`8003`</td><td align="left">`空`</td><td align="left"> ADMIN CHECK TABLE 命令在遇到行数据跟索引不一致的时候返回该错误</td></tr><tr><td align="center">`8004`</td><td align="left">`空`</td><td align="left"> 单个事务过大</td></tr><tr><td align="center">`8005`</td><td align="left">`Write Conflict, txnStartTS is stale`</td><td align="left"> 事务在 TiDB 中遇到了写入冲突; 可以检查 `tidb_disable_txn_auto_retry` 是否为 on, 如果是，将其设置为 off；  
`SET GLOBAL tidb_disable_txn_auto_retry = off;`开启自动重试  
 如已经是 off，将 `tidb_retry_limit` 调大到不再发生该错误。  
 **[事务自动重试及带来的异常](https://pingcap.com/docs-cn/stable/reference/transactions/transaction-isolation/#%E4%BA%8B%E5%8A%A1%E8%87%AA%E5%8A%A8%E9%87%8D%E8%AF%95%E5%8F%8A%E5%B8%A6%E6%9D%A5%E7%9A%84%E5%BC%82%E5%B8%B8 "事务自动重试及带来的异常")**</td></tr><tr><td align="center">`9001`</td><td align="left">`PD Server Timeout`</td><td align="left"> 请求 PD 超时，请检查 PD Server 状态/监控/日志以及 TiDB Server 与 PD Server 之间的网络;   
 这个报错一般是 TiDB 访问 PD 出了问题，TiDB 后台有个 worker 会不断地从 PD 查询 safepoint，如果超过 100s 查不成功就会报这个错   
 一般是因为 PD 磁盘操作过忙、反应过慢，或者 TiDB 和 PD 之间的网络有问题。</td></tr><tr><td align="center">`9002`</td><td align="left">`TiKV Server Timeout`</td><td align="left"> 请求 TiKV 超时，请检查 TiKV Server 状态/监控/日志以及 TiDB Server 与 TiKV Server 之间的网络;</td></tr><tr><td align="center">`9003`</td><td align="left">`TiKV Server is Busy`</td><td align="left"> TiKV 操作繁忙，一般出现在数据库负载比较高时，请检查 TiKV Server 状态/监控/日志;</td></tr><tr><td align="center">`9004`</td><td align="left">`Resolve Lock Timeout`</td><td align="left"> 清理锁超时，当数据库上承载的业务存在大量的事务冲突时，会遇到这种错误，请检查业务代码是否有锁争用;</td></tr><tr><td align="center">`9005`</td><td align="left">`Region is unavailable`</td><td align="left"> 访问的 Region 不可用，某个 Raft Group 不可用，如副本数目不足，出现在 TiKV 比较繁忙或者是 TiKV 节点停机的时候，请检查 TiKV Server 状态/监控/日志;</td></tr><tr><td align="center">`9006`</td><td align="left">`GC life time is shorter than transaction duration`</td><td align="left"> `GC Life Time` 间隔时间过短，长事务本应读到的数据可能被清理了，可使用如下命令增加 `GC Life Time`:   
 **`update mysql.tidb set variable_value='30m' where variable_name='tikv_gc_life_time';`**   
 其中 30m 代表仅清理 30 分钟前的数据，这可能会额外占用一定的存储空间。</td></tr><tr><td align="center">`9007`</td><td align="left">`Write Conflict`</td><td align="left"> 事务在 TiKV 中遇到了写入冲突，可以检查 `tidb_disable_txn_auto_retry` 是否为 on。如是，将其设置为 off；如已经是 off，将 `tidb_retry_limit` 调大到不再发生该错误。;</td></tr><tr><td align="center">`2013`</td><td align="left">`Lost connection to MySQL server during query`</td><td align="left">log 中是否有 panic   
 dmesg 中是否有 oom，命令：`dmesg -T | grep -i oom`   
 长时间没有访问，也会收到这个报错，一般是 tcp 超时导致的，tcp 长时间不用, 会被操作系统 kill。</td></tr><tr><td align="center">`2003`</td><td align="left">`Can't connect to MySQL server on 'xxx.xxx.xxx.xx' (10061 "Unknown error")`</td><td align="left"> TiDB链接中断，  
 1 如果配置了内存限制，那么有可能是执行的SQl语句使用的内存过多，为了保护服务器不宕机，TiDB会杀死占用内存过多进程；  
 2 查看TiDB日志，确定进程中断的原因</td></tr><tr><td align="center">`1105`</td><td align="left">`other error: unknown error Wire Error(InvalidEnumValue(4004))`</td><td align="left"> 这类问题一般是 TiDB 和 TiKV 版本不匹配，在升级过程尽量一起升级，避免版本 mismatch。</td></tr><tr><td align="center">`1148`</td><td align="left">`the used command is not allowed with this TiDB version`</td><td align="left"> 这个问题是因为在执行 LOAD DATA LOCAL 语句的时候，MySQL 客户端不允许执行此语句（即 local\_infile 选项为 0）。   
 解决方法是在启动 MySQL 客户端时，用 `--local-infile=1` 选项。   
 具体启动指令类似：`mysql --local-infile=1 -u root -h 127.0.0.1 -P 4000`。   
 有些 MySQL 客户端需要设置而有些不需要设置，原因是不同版本的 MySQL 客户端对 `local-infile` 的默认值不同。</td></tr><tr><td align="center">`EOF`</td><td align="left">`空`</td><td align="left"> 当客户端或者 proxy 断开连接时，TiDB 不会立刻察觉连接已断开，而是等到开始往连接返回数据时，才发现连接已断开，此时日志会打印 EOF 错误。</td></tr></tbody></table>