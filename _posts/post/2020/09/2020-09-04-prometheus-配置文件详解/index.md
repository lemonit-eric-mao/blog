---
title: "Prometheus 配置文件详解"
date: "2020-09-04"
categories: 
  - "linux服务器"
---

###### **[原文链接](https://www.cnblogs.com/liujiliang/p/10080849.html "原文链接")**

```yaml
# 全局配置
global:
  scrape_interval:     15s   # 多久 收集一次 数据
  evaluation_interval: 30s   # 多久 评估一次 规则
  scrape_timeout:      10s   # 每次 收集数据的 超时时间

  # 当Prometheus和外部系统(联邦, 远程存储, Alertmanager)通信的时候，添加标签到任意的时间序列或者报警
  external_labels:
    monitor: codelab
    foo:     bar

# 规则文件, 可以使用通配符
rule_files:
- "first.rules"
- "my/*.rules"

# 远程写入功能相关的设置
remote_write:
  - url: http://remote1/push
    write_relabel_configs:
    - source_labels: [__name__]
      regex:         expensive.*
      action:        drop
  - url: http://remote2/push

# 远程读取相关功能的设置
remote_read:
  - url: http://remote1/read
    read_recent: true
  - url: http://remote3/read
    read_recent: false
    required_matchers:
      job: special

# 收集数据 配置 列表
scrape_configs:
- job_name: prometheus  # 必须配置, 自动附加的job labels, 必须唯一

  honor_labels: true   # 标签冲突, true 为以抓取的数据为准 并 忽略 服务器中的, false 为 通过重命名来解决冲突
  # scrape_interval is defined by the configured global (15s).
  # scrape_timeout is defined by the global default (10s).

  metrics_path:     '/metrics'
  # scheme defaults to 'http'.


  # 文件服务发现配置 列表
  file_sd_configs:
    - files:  # 从这些文件中提取目标
      - foo/*.slow.json
      - foo/*.slow.yml
      - single/file.yml
      refresh_interval: 10m  # 刷新文件的 时间间隔
    - files:
      - bar/*.yaml


  # 使用job名作为label的 静态配置目录 的 列表
  static_configs:
  - targets: ['localhost:9090', 'localhost:9191']
    labels:
      my:   label
      your: label


  # 目标节点 重新打标签 的配置 列表.  重新标记是一个功能强大的工具，可以在抓取目标之前动态重写目标的标签集。 可以配置多个，按照先后顺序应用
  relabel_configs:
  - source_labels: [job, __meta_dns_name]   # 从现有的标签中选择源标签, 最后会被 替换， 保持， 丢弃
    regex:         (.*)some-[regex]  # 正则表达式, 将会提取source_labels中匹配的值
    target_label:  job   # 在替换动作中将结果值写入的标签.
    replacement:   foo-${1}  # 如果正则表达匹配, 那么替换值. 可以使用正则表达中的 捕获组
    # action defaults to 'replace'
  - source_labels: [abc]  # 将abc标签的内容复制到cde标签中
    target_label:  cde
  - replacement:   static
    target_label:  abc
  - regex:
    replacement:   static
    target_label:  abc

  bearer_token_file: valid_token_file  # 可选的, bearer token 文件的信息


- job_name: service-x

  # HTTP basic 认证信息
  basic_auth:
    username: admin_name
    password: "multiline\nmysecret\ntest"

  scrape_interval: 50s  # 对于该job, 多久收集一次数据
  scrape_timeout:  5s

  sample_limit: 1000  # 每次 收集 样本数据的限制. 0 为不限制

  metrics_path: /my_path  # 从目标 获取数据的 HTTP 路径
  scheme: https  # 配置用于请求的协议方案


  # DNS 服务发现 配置列表
  dns_sd_configs:
  - refresh_interval: 15s
    names:  # 要查询的DNS域名列表
    - first.dns.address.domain.com
    - second.dns.address.domain.com
  - names:
    - first.dns.address.domain.com
    # refresh_interval defaults to 30s.


  # 目标节点 重新打标签 的配置 列表
  relabel_configs:
  - source_labels: [job]
    regex:         (.*)some-[regex]
    action:        drop
  - source_labels: [__address__]
    modulus:       8
    target_label:  __tmp_hash
    action:        hashmod
  - source_labels: [__tmp_hash]
    regex:         1
    action:        keep
  - action:        labelmap
    regex:         1
  - action:        labeldrop
    regex:         d
  - action:        labelkeep
    regex:         k


  # metric 重新打标签的 配置列表
  metric_relabel_configs:
  - source_labels: [__name__]
    regex:         expensive_metric.*
    action:        drop


- job_name: service-y

  # consul 服务发现 配置列表
  consul_sd_configs:
  - server: 'localhost:1234'  # consul API 地址
    token: mysecret
    services: ['nginx', 'cache', 'mysql']  # 被检索目标的 服务 列表. 如果不定义那么 所有 服务 都会被 收集
    scheme: https
    tls_config:
      ca_file: valid_ca_file
      cert_file: valid_cert_file
      key_file:  valid_key_file
      insecure_skip_verify: false

  relabel_configs:
  - source_labels: [__meta_sd_consul_tags]
    separator:     ','
    regex:         label:([^=]+)=([^,]+)
    target_label:  ${1}
    replacement:   ${2}

- job_name: service-z

  # 收集 数据的 TLS 设置
  tls_config:
    cert_file: valid_cert_file
    key_file: valid_key_file

  bearer_token: mysecret

- job_name: service-kubernetes

  # kubernetes 服务 发现 列表
  kubernetes_sd_configs:
  - role: endpoints   # 必须写, 必须是endpoints, service, pod, node, 或者 ingress
    api_server: 'https://localhost:1234'

    basic_auth:  # HTTP basic 认证信息
      username: 'myusername'
      password: 'mysecret'

- job_name: service-kubernetes-namespaces

  kubernetes_sd_configs:
  - role: endpoints  # 应该被发现的 kubernetes 对象 实体
    api_server: 'https://localhost:1234'  # API Server的地址
    namespaces:  # 可选的命名空间发现, 如果省略 那么所有的命名空间都会被使用
      names:
        - default

- job_name: service-marathon
  # Marathon 服务发现 列表
  marathon_sd_configs:
  - servers:
    - 'https://marathon.example.com:443'

    tls_config:
      cert_file: valid_cert_file
      key_file: valid_key_file

- job_name: service-ec2
  ec2_sd_configs:
    - region: us-east-1
      access_key: access
      secret_key: mysecret
      profile: profile

- job_name: service-azure
  azure_sd_configs:
    - subscription_id: 11AAAA11-A11A-111A-A111-1111A1111A11
      tenant_id: BBBB222B-B2B2-2B22-B222-2BB2222BB2B2
      client_id: 333333CC-3C33-3333-CCC3-33C3CCCCC33C
      client_secret: mysecret
      port: 9100

- job_name: service-nerve
  nerve_sd_configs:
    - servers:
      - localhost
      paths:
      - /monitoring

- job_name: 0123service-xxx
  metrics_path: /metrics
  static_configs:
    - targets:
      - localhost:9090

- job_name: 測試
  metrics_path: /metrics
  static_configs:
    - targets:
      - localhost:9090

- job_name: service-triton
  triton_sd_configs:
  - account: 'testAccount'
    dns_suffix: 'triton.example.com'
    endpoint: 'triton.example.com'
    port: 9163
    refresh_interval: 1m
    version: 1
    tls_config:
      cert_file: testdata/valid_cert_file
      key_file: testdata/valid_key_file

# Alertmanager相关的配置
alerting:
  alertmanagers:
  - scheme: https
    static_configs:
    - targets:
      - "1.2.3.4:9093"
      - "1.2.3.5:9093"
      - "1.2.3.6:9093"
```

* * *

* * *

* * *

# **Prometheus 联邦配置示例**

#### **Prometheus的数据库（TSDB）：**

1. Prometheus 包含一个内置的时间序列数据库（TSDB），用于存储和查询监控数据。
2. TSDB 具有高效的存储引擎，可以处理大量时间序列数据。
3. 它支持数据自动保留策略，可配置保留多长时间的历史数据。
4. TSDB 使用标签（labels）来标识和区分不同的时间序列数据。

#### **Prometheus联邦（Federation）：**

1. Prometheus 联邦是一种机制，允许多个 Prometheus 服务器之间共享和查询监控数据。
2. 联邦通过使用 `/federate` 路径从其他 Prometheus 服务器获取数据来实现。
3. 联邦使得集中化监控和分布式监控变得更加容易，不同地点或组织的 Prometheus 服务器可以共享数据。
4. 在联邦设置中，Prometheus 服务器可以充当目标服务器（提供数据）或源服务器（获取数据）。
5. 联邦允许跨不同 Prometheus 服务器进行复杂的查询和分析操作。

#### **Prometheus.yaml**

```yaml
tee ./prometheus/config/prometheus.yml << ERIC

# 全局配置
global:
  scrape_interval:     15s   # 多久 采集一次 数据
  evaluation_interval: 30s   # 多久 评估一次 规则
  scrape_timeout:      10s   # 每次 收集数据的 超时时间

scrape_configs:
  - job_name: 'federate'
    scrape_interval: 15s              # 采集时间间隔为每15秒一次

    honor_labels: true                # 保留原始标签信息，有助于标识监控数据的来源

    metrics_path: '/federate'         # 使用/federate路径从目标服务器获取监控指标数据

    params:
      'match[]':
        - '{job=~".+"}'               # 匹配所有 job 标签值的正则表达式

    static_configs:
      - targets:
        - 'source-prometheus-1:9090'  # 配置三个目标服务器，从这些服务器获取监控数据
        - 'source-prometheus-2:9090'
        - 'source-prometheus-3:9090'

ERIC

```

**测试**

```bash
# curl 'http://source-prometheus-1:9090/federate?match[]={job=~".+"}'
curl http://source-prometheus-1:9090/federate?match[]=%7Bjob%3D%22nvidia-gpu%22%7D

```

* * *

* * *

* * *
