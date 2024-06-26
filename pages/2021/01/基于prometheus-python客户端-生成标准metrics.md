---
title: "基于Prometheus Python客户端 生成标准Metrics"
date: "2021-01-07"
categories: 
  - "prometheus"
  - "python"
---

###### **[Prometheus官方指定客户端](https://prometheus.io/docs/instrumenting/clientlibs/#client-libraries "Prometheus官方指定客户端")**

###### **[Python Prometheus客户端](https://github.com/prometheus/client_python "Python Prometheus客户端")**

* * *

**实现思路：**

1. 获取 **`VMware vSphere`** 信息
2. 将vSphere信息转为 **`Prometheus Metrics`** 格式的数据
3. 搭建Web服务器提供 **`Metrics`** 数据的获取

* * *

* * *

* * *

###### **1** 创建客户端，获取VMware信息

```python
#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2021/01/13 11:28
# @Author  : Eric.Mao
# @FileName: vm_connect.py
# @Software: PyCharm
# @Blog    : http://www.dev-share.top/

# https://zhuanlan.zhihu.com/p/58120047
# 用于注册程序退出时的回调函数
import atexit
import ssl

from pyVim import connect


# 链接VMware, 获取所有信息
class VMConnect(object):

    def __init__(self, host, port, user, pwd, ssl_context):
        if ssl_context is None:
            # 配置ssl
            ssl_context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
            ssl_context.verify_mode = ssl.CERT_NONE

        # 连接到vCenter
        self.service_instance = connect.SmartConnect(
            host=host,
            port=port,
            user=user,
            pwd=pwd,
            sslContext=ssl_context)

        # 注册程序退出时的回调
        atexit.register(connect.Disconnect, self.service_instance)
        # 获取vCenter链接信息
        self.content = self.service_instance.RetrieveContent()

    # vCenter 所有对象信息
    #     view_type 数据中心对象类型：[vim.Datacenter]
    #     view_type 集群对象类型：[vim.ClusterComputeResource]
    #     view_type 宿主机对象类型：[vim.HostSystem]
    #     view_type 虚拟机对象：[vim.VirtualMachine]
    def get_all_objs(self, view_type):
        # 根据对象类型获取这一类型的所有对象
        container = self.content.viewManager.CreateContainerView(self.content.rootFolder, view_type, True)
        return container.view

    # vCenter 指定对象信息
    #     view_type 数据中心对象类型：[vim.Datacenter]
    #     view_type 集群对象类型：[vim.ClusterComputeResource]
    #     view_type 宿主机对象类型：[vim.HostSystem]
    #     view_type 虚拟机对象：[vim.VirtualMachine]
    #     name 对象名称
    def get_obj_by_name(self, view_type, name):
        # 根据对象类型获取这一类型的所有对象
        container = self.content.viewManager.CreateContainerView(self.content.rootFolder, view_type, True)
        for view in container.view:
            if view.name == name:
                return view

# if __name__ == '__main__':
#     # VMConnect()
#     vm_connect = VMConnect(
#         host="192.168.20.20",
#         port=443,
#         user="username",
#         pwd="passwd",
#         ssl_context=None)
#     # 打印信息
#     print(vm_connect.get_all_objs([vim.ClusterComputeResource]))

```

* * *

###### **2** 搭建Web服务器 Flask

`将VMware信息转换为 metrics，提供 metrics 的Web服务器`

```python
#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2021/01/13 09:04
# @Author  : Eric.Mao
# @FileName: app.py
# @Software: PyCharm
# @Blog    : http://www.dev-share.top/

import os

from flask import Flask, Response
from prometheus_client import Counter, Gauge, CollectorRegistry, generate_latest
from pyVmomi import vim

from vmware_exporter.vm_connect import VMConnect

app = Flask(__name__)
# 将多个指标类型数据注册到起，统一返回
registry = CollectorRegistry()

"""
Prometheus 提供四种指标类型, 分别为 Counter, Gauge, Histogram, Summary。
    Counter 指标只增不减，可以用来代表处理的请求数量，处理的任务数量等。
    Gauge 指标可增可减，例如，并发请求数量，cpu 占用率等。
    Histogram 用于统计样本数值落在不同的桶（buckets）里面的数量。例如，统计应用程序的响应时间，可以使用 histogram 指标类型。
    Summary 和 histogram 类型类似，可用于统计数据的分布情况。

.inc() 作用累加
.set() 作用只赋值

"""

# 定义metrics数据格式
# Counter('Counter 名称', 'Counter 的描述', 'registry=将多个指标类型数据注册到起，统一返回')
# 用法 counter.inc(1)
counter = Counter('vmware_counter', 'vmware counter data', registry=registry)

# 定义metrics数据格式
# Gauge('Gauge 名称', 'Gauge 的描述', 'Gauge 的标签', 'registry=将多个指标类型数据注册到起，统一返回')
# 用法 gauge.labels('0.0.0.0').set(0)
gauge = Gauge('vmware_gauge', 'vmware gauge data', ['vmware_name', 'vmware_ip', 'vmware_power_state'], registry=registry)

@app.route('/metrics')
def get_metrics():
    # 添加 Counter 测试数据
    counter.inc(1)

    #  添加 Gauge 测试数据
    for child in vm_connect.get_all_objs([vim.VirtualMachine]):
        summary = child.summary
        gauge.labels(summary.config.name, summary.guest.ipAddress, summary.runtime.powerState).inc(0)

    # 统一返回
    return Response(generate_latest(registry), mimetype='text/plain')


# 程序首页
@app.route('/')
def index():
    html = """<html>
               <head><title>CN VMware Exporter</title></head>
               <body>
               <h1>VMware Exporter</h1>
               <p><a href="/metrics">Metrics</a></p>
               <p><a href="/health">Health</a></p>
               </body>
               </html>"""
    return Response(html, mimetype='text/html')


# Web服务器运行状态
@app.route('/health')
def health():
    string = "Service is UP"
    return Response(string, mimetype='text/plain')


if __name__ == '__main__':
    os.environ.setdefault('VSPHERE_HOST', '192.168.20.20')
    os.environ.setdefault('VSPHERE_PORT', '443')
    os.environ.setdefault('VSPHERE_USER', 'username')
    os.environ.setdefault('VSPHERE_PASSWORD', 'passwd')

    vm_connect = VMConnect(
        host=os.environ.get('VSPHERE_HOST'),
        port=os.environ.get('VSPHERE_PORT'),
        user=os.environ.get('VSPHERE_USER'),
        pwd=os.environ.get('VSPHERE_PASSWORD'),
        ssl_context=None)

    # 启动web服务器
    app.run(host='0.0.0.0', port=9293, debug=False)

```

* * *

* * *

* * *

###### 分解：

```python
gauge = Gauge('gauge_cluster_info', '描述-测试数据', ['cluster_name', 'cluster_ip'], registry=registry)
gauge.labels('DHC_CLOUD', '0.0.0.1').set(75.23)
gauge.labels('DHC_MGMT', '0.0.0.2').set(12.58)
```

| Element(理解为 **`Key`** ) | **`Value`** |
| --- | --- |
| gauge.labels(标签内容1, 标签内容2, ......) | .set(动态值) |
| `不要放动态值`否则会出现很多**Element** | 对应的值 |
| **以下是生成后的 metrics数据格式** |  |
| gauge\_cluster\_info{cluster\_name=`"DHC_CLOUD"`, cluster\_ip=`"0.0.0.1"`} | 75.23 |
| gauge\_cluster\_info{cluster\_name=`"DHC_MGMT"`, cluster\_ip=`"0.0.0.2"`} | 12.58 |

* * *

* * *

* * *

###### [程序源码打包成Docker镜像](https://gitee.com/eric-mao/cn-vmware/blob/master/Dockerfile "程序源码打包成Docker镜像")

* * *

* * *

* * *
