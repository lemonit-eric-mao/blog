---
title: '使用 docker-compose 安装 Prometheus+Alertmanager+Grafana'
date: '2019-06-25T02:45:50+00:00'
status: publish
permalink: /2019/06/25/%e4%bd%bf%e7%94%a8-docker-compose-%e5%ae%89%e8%a3%85-prometheusalertmanagergrafana
author: 毛巳煜
excerpt: ''
type: post
id: 4902
category:
    - ELK
    - prometheus
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
post_views_count:
    - '0'
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
---
###### [安装 docker-compose](http://www.dev-share.top/2019/06/12/%E5%AE%89%E8%A3%85-docker-compose/ "安装 docker-compose")

###### [grafana 官网](https://grafana.com "grafana 官网")

有的时候官方下载连接会失败，所以这里选择docker镜像来进行安装部署，被墙的头晕

##### 准备

```ruby
[root@k8s-master ~]# mkdir -p /home/monitor/prometheus/config/rules
[root@k8s-master ~]# mkdir -p /home/monitor/grafana/config

```

##### 步骤

1. 部署 Prometheus
2. 部署 Alertmanager
3. 与 Prometheus 建立连接
4. 使用 Prometheus 配置报警规则

##### 1.创建 docker-compose.yaml 配置文件

```ruby
[root@k8s-master monitor]# pwd
/home/monitor
[root@k8s-master monitor]# cat > docker-compose.yaml 
```

##### 2.添加告警模块配置文件 alertmanager.yml

```ruby
[root@k8s-master config]# pwd
/home/monitor/prometheus/config
[root@k8s-master config]# cat > alertmanager.yml 
```

##### 3.配置 普罗米修斯配置文件 prometheus.yml

```ruby
[root@k8s-master config]# pwd
/home/monitor/prometheus/config
[root@k8s-master config]# cat > prometheus.yml \` to any timeseries scraped from this config.
  - job_name: 'prometheus'
    # metrics_path defaults to '/metrics'
    # scheme defaults to 'http'.
    static_configs:
      - targets: ['k8s.dev-share.top:9090']

  # 后期追加mysql监控
  - job_name: 'uat-mysql'
    static_configs:
      - targets: ['k8s.dev-share.top:9104']

  # 后期追加机器监控
  - job_name: 'node-monitor'
    static_configs:
      # 因为阿里云有安全组策略，所以这里使用了外网域名
      - targets: ['k8s.dev-share.top:9100']
ERIC

[root@k8s-master config]#

```

##### 4.添加 普罗米修斯 告警规则文件 mysql-rules.yml (mysql相关的监控规则)

```ruby
[root@k8s-master rules]# pwd
/home/monitor/prometheus/config/rules
[root@k8s-master rules]# cat > mysql-rules.yml  Graph 里面查到的，这个说法是可以获取到被监控的mysql在线的数据; 等于0为离线
      expr: up{instance="k8s.dev-share.top:9104",job="mysql"} == 0
      #for: 30s
      for: 5s
      annotations:
        summary: "MySql离线监控告警 : {{.instance}}"
        description: "MySql离线监控告警 : {{.instance}}"
        custom: "mysql"

    - alert: 'Prometheus 离线监控告警'
      # 等于0时，将触发告警
      expr: up{instance="k8s.dev-share.top:9090",job="prometheus"} == 0
      for: 30s
      annotations:
        summary: "Prometheus 离线监控告警 : {{.instance}}"
        description: "Prometheus 离线监控告警 : {{.instance}}"
        custom: "prometheus"
ERIC

[root@k8s-master rules]#

```

##### 5.添加grafana配置文件 grafana.ini

```ruby
[root@dev10 config]# pwd
/home/monitor/grafana/config
[root@dev10 config]# cat > grafana.ini 
```

##### 6.启动

```ruby
[root@k8s-master monitor]# pwd
/home/monitor
[root@k8s-master monitor]# docker-compose up -d
Creating network "monitor_default" with the default driver
Creating alertmanager ... done
Creating prometheus   ... done
Creating grafana      ... done
[root@k8s-master monitor]#
# 如果启动后，有挂载盘权限问题，解决如下：虽然此方法并不好，暂时还没有更好的办法
[root@k8s-master home]# chmod -R 777 monitor/

```

**总结，alertmanager 是给 prometheus 本身的alert用的，它是用来告警后触发邮件;**

**而我们现在使用 Grafana 是在Grafana 的监控面板中 Alerts选项直接可以配置的告警语句的，告警的查询语句可以去 prometheus web页面 --&gt; Graph中 查询**

`所以在部署使用的时候不要弄混, Alertmanager 与 grafana 中的 alert 它俩没有任何关系`

- - - - - -

- - - - - -

- - - - - -

##### Grafana 关联 普罗米修斯

**Configuration** --&gt; **Data Sources** --&gt; **Add data source** --&gt; **Prometheus**

**配置 Prometheus**

<table><thead><tr><th>**key**</th><th>**value**</th></tr></thead><tbody><tr><td>Name：</td><td>Prometheus</td></tr><tr><td>URL：</td><td>http://k8s.dev-share.top:`9090`</td></tr><tr><td>Access：</td><td>Server(Default)</td></tr><tr><td>Whitelisted Cookies：</td><td>Prometheus</td></tr><tr><td>HTTP Method：</td><td>GET</td></tr></tbody></table>

- - - - - -

##### 常用的grafana面板

K8S 监控面板 ID: 7532  
MySQL 监控面板 ID: 7362  
Blackbox 监控面板 ID: 9965  
node 监控面板 ID: 9894

- - - - - -

##### Grafana 安装插件 饼图

```ruby
[root@k8s-master monitor]# docker exec grafana grafana-cli plugins install grafana-piechart-panel

[root@k8s-master monitor]# docker-compose restart grafana

```

- - - - - -

##### Grafana 添加报警接收者

**Alerting** --&gt; **Notification channels** --&gt; **Add channel**

- - - - - -

##### 普罗米修斯热更新

**`注意`**：Only POST or PUT requests allowed 只允许 POST 或 PUT 请求

```ruby
[root@k8s-master ~]# curl -X POST http://k8s.dev-share.top:9090/-/reload

```