---
title: 'Prometheus应用 node_exporter 监控机器状态'
date: '2019-06-21T02:57:16+00:00'
status: publish
permalink: /2019/06/21/prometheus%e5%ba%94%e7%94%a8-node_exporter-%e7%9b%91%e6%8e%a7%e6%9c%ba%e5%99%a8%e7%8a%b6%e6%80%81
author: 毛巳煜
excerpt: ''
type: post
id: 4885
category:
    - Linux服务器
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
---
[安装 Prometheus](http://www.dev-share.top/2019/06/25/%e4%bd%bf%e7%94%a8-docker-compose-%e5%ae%89%e8%a3%85-prometheusalertmanagergrafana/ "安装 Prometheus")

为了熟悉Prometheus使用插件的方式，我们重复上面的流程在添加一个 `node_exporter` 监控模块

#### 在普罗米修斯中添加 node\_exporter

##### 1.docker 下载/安装/运行 普罗米修斯组件：node\_exporter

```ruby
[root@k8s-master ~]# docker pull prom/node-exporter:v1.6.1
[root@k8s-master ~]# docker run -d --name prometheus-node -p 9100:9100 prom/node-exporter:v1.6.1
[root@k8s-master ~]# docker ps | grep 9100
790b0c2331bf        prom/node-exporter                       "/bin/node_exporter"     5 seconds ago       Up 4 seconds            0.0.0.0:9100->9100/tcp                                             prometheus-node


```

##### 2.修改 普罗米修斯配置文件，将node\_exporter监控加入进去, 配置完成后重启普罗米修斯

```yaml
......
scrape_configs:
  # The job name is added as a label `job=<job_name>` to any timeseries scraped from this config.
  - job_name: 'prometheus'
    # metrics_path defaults to '/metrics'
    # scheme defaults to 'http'.
    static_configs:
      - targets: ['k8s.dev-share.top:9090']

  - job_name: 'node-exporter'
    static_configs:
        # 因为阿里云有安全组策略，所以这里使用了外网域名
      - targets: ['k8s.dev-share.top:9100']
</job_name>
```

##### 3.配置 grafana监控面板，并展示从 普罗米修斯获取到的数据

1. [从grafana官网搜索要使用的监控面板](https://grafana.com/dashboards "从grafana官网搜索要使用的监控面板")
2. 搜索 grafana node\_exporter监控面板 `Node Exporter 0.16 for Prometheus Monitoring display board` id: **9894**
3. **Dashboards** –&gt; **Manage** –&gt; **Import** –&gt; 在 (**Grafana.com Dashboard**) 中输入 **9894**
4. **Options** –&gt; **prometheus** –&gt; 选择 **Prometheus**

- - - - - -

- - - - - -

- - - - - -

二进制安装
=====

下载
--

```bash
wget https://github.com/prometheus/node_exporter/releases/download/v1.6.1/node_exporter-1.6.1.linux-amd64.tar.gz

tar xvfz node_exporter-1.6.1.linux-amd64.tar.gz

cd node_exporter-1.6.1.linux-amd64

sudo cp node_exporter /usr/local/bin/


```

启动
--

```bash
sudo tee /etc/systemd/system/node_exporter.service 
```

```bash
# 让 systemd 重新加载服务单元文件
sudo systemctl daemon-reload

# 让 "node_exporter" 开机自启动
sudo systemctl enable node_exporter

# 启动 "node_exporter" 服务
sudo systemctl start node_exporter


```

- - - - - -

- - - - - -

- - - - - -