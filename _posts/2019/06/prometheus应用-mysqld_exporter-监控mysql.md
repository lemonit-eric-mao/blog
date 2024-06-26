---
title: "Prometheus应用 mysqld_exporter 监控Mysql"
date: "2019-06-21"
categories: 
  - "linux服务器"
---

### 添加 远程Mysql监控

[安装 Prometheus](http://www.dev-share.top/2019/06/25/%E4%BD%BF%E7%94%A8-docker-compose-%E5%AE%89%E8%A3%85-prometheusalertmanagergrafana/")

###### 在要监控的Mysql中创建一个账户为 普罗米修斯使用

```ruby
mysql> GRANT ALL PRIVILEGES ON *.* TO 'prometheus'@'%' IDENTIFIED BY 'prometheus1987' WITH GRANT OPTION;
Query OK, 0 rows affected, 1 warning (0.01 sec)
# 授权
mysql> GRANT SELECT ON *.* TO 'prometheus';
Query OK, 0 rows affected (0.01 sec)

mysql>
```

#### 使用 普罗米修斯 监控Mysql

#### `二进制安装方法`

###### 1.在普罗米修斯中添加 mysqld\_exporter ；它是用来连接Mysql的，然后在使用 普罗米修斯连接它

```ruby
[root@k8s-master prometheus]# wget https://github.com/prometheus/mysqld_exporter/releases/download/v0.10.0/mysqld_exporter-0.10.0.linux-amd64.tar.gz
[root@k8s-master prometheus]#
[root@k8s-master prometheus]# cd mysqld_exporter-0.10.0.linux-amd64
[root@k8s-master mysqld_exporter-0.10.0.linux-amd64]#
[root@k8s-master mysqld_exporter-0.10.0.linux-amd64]# ll
total 10196
-rw-rw-r-- 1 1000 1000    11325 Apr 25  2017 LICENSE
-rwxr-xr-x 1 1000 1000 10419174 Apr 25  2017 mysqld_exporter
-rw-rw-r-- 1 1000 1000       65 Apr 25  2017 NOTICE
[root@k8s-master mysqld_exporter-0.10.0.linux-amd64]#
```

##### 2.添加配置文件

```ruby
[root@k8s-master mysqld_exporter-0.10.0.linux-amd64]# cat > my.cnf << EOF

[client]
host=mysql.dev-share.top
port=3306
user=prometheus
password=prometheus1987
EOF
[root@k8s-master mysqld_exporter-0.10.0.linux-amd64]#
```

##### 3.mysqld\_exporter 启动

```ruby
[root@k8s-master mysqld_exporter-0.10.0.linux-amd64]# ./mysqld_exporter -config.my-cnf ./my.cnf
INFO[0000] Starting mysqld_exporter (version=0.10.0, branch=master, revision=80680068f15474f87847c8ee8f18a2939a26196a)  source="mysqld_exporter.go:460"
INFO[0000] Build context (go=go1.8.1, user=root@3b0154cd9e8e, date=20170425-11:24:12)  source="mysqld_exporter.go:461"
INFO[0000] Listening on :9104                            source="mysqld_exporter.go:479"
```

##### 4.修改 普罗米修斯配置文件，将mysql监控加入进去, 配置完成后重启普罗米修斯

```yaml
......
scrape_configs:
  # The job name is added as a label `job=<job_name>` to any timeseries scraped from this config.
  - job_name: 'prometheus'
    # metrics_path defaults to '/metrics'
    # scheme defaults to 'http'.
    static_configs:
      - targets: ['k8s.dev-share.top:9090']

  - job_name: 'mysql'
    static_configs:
        # 因为阿里云有安全组策略，所以这里使用了外网域名
      - targets: ['k8s.dev-share.top:9104']
```

##### 5.配置 grafana监控面板，并展示从 普罗米修斯获取到的数据

1. 从grafana官网搜索要使用的监控面板: https://grafana.com/dashboards
2. **Dashboards** --> **Manage** --> **Import** --> 在 (**Grafana.com Dashboard**) 中输入 查询到的面板id
3. 鼠标离开会自动显示加载面板的 Options
4. **Options** --> **prometheus** --> 选择我们之前配置好的 普罗米修斯就可以了
5. 其它的扩展就自己看着办了
6. 建议使用 **MySQL Overview** 监控面板， 因为这个面板支持同时监控多个MySQL数据库，并进行展示

* * *

* * *

#### `使用 docker 安装`

**`示例`**

```ruby
docker run -d --restart=always --name mysqld-exporter -p 9104:9104 -e DATA_SOURCE_NAME="user:password@(hostname:port)/database" prom/mysqld-exporter
```

```ruby
[root@k8s-master ~]# docker pull prom/mysqld-exporter
[root@k8s-master ~]#
[root@k8s-master ~]# docker run -d --restart always --name mysqld-exporter -p 9104:9104 -e DATA_SOURCE_NAME="prometheus:prometheus1987@(mysql.dev-share.top:3306)/resource_manage" prom/mysqld-exporter
```
