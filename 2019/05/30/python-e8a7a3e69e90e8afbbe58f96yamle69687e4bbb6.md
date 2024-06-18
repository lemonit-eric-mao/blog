---
title: 'Python 解析读取yaml文件'
date: '2019-05-30T07:48:06+00:00'
status: publish
permalink: /2019/05/30/python-%e8%a7%a3%e6%9e%90%e8%af%bb%e5%8f%96yaml%e6%96%87%e4%bb%b6
author: 毛巳煜
excerpt: ''
type: post
id: 4710
category:
    - Python
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
##### app.py

```python
#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import time
import yaml
from string import Template

# 工具方法：将文件以字符串的形式进行读取，并使用模板进行解析
def read_template_data(path, data):
    with open(path) as file:
        # 将文件一次读取为字符串
        content = file.read()
        # 如果没有要解析的数据将直接返回文件内容
        if not data:
            return content

        # 将字符串加入模板
        tmp = Template(content)
        # 让数据与模板进行映射
        str = tmp.safe_substitute(data)
        # 关闭文件
        file.close()
        return str


# 控制台获取版本号
def get_version():
    # 注意：input() 和 raw_input() 这两个函数均能接收 字符串 ，但 raw_input() 直接读取控制台的输入（任何类型的输入它都可以接收）。
    # 而对于 input() ，它希望能够读取一个合法的 python 表达式，即你输入字符串的时候必须使用引号将它括起来，否则它会引发一个 SyntaxError 。
    # 除非对 input() 有特别需要，否则一般情况下我们都是推荐使用 raw_input() 来与用户交互。
    # 注意：python3 里 input() 默认接收到的是 str 类型。
    # 获取控制台输入
    version = raw_input('Enter your version: ')
    # 如果输入为空
    if version:
        return version
    return time.strftime('v%y%m%d-%H%M%S')


# 获取版本号
v = get_version()

# 读取配置文件
dict = open('config/app-config.yaml')
# 使用yaml模块, 解析配置文件为字典数据
# YAML 5.1版本后弃用了yaml.load(file)这个用法，因为觉得很不安全
# 5.1版本之后就修改了需要指定Loader，
# 通过默认加载器（FullLoader）禁止执行任意函数，该load函数也变得更加安全
# https://github.com/yaml/pyyaml/wiki/PyYAML-yaml.load(input)-Deprecation#footnotes
config = yaml.load(dict, Loader=yaml.FullLoader)

for proj in config['projects']:
    # 如果字典中的key不存在
    if not proj.has_key('replicas'):
        proj['replicas'] = config['default']['replicas']
    # 如果字典中的key不存在
    if not proj.has_key('jvm_opt'):
        proj['jvm_opt'] = config['default']['jvm_opt']

    # 运行时加入版本号
    proj['version'] = v
    # 加入镜像名
    proj['image'] = 'sinoeyes.io/library/' + proj['service_id']
    # 生成新的文件，如果文件存在就覆盖
    file = open(proj['service_id'] + '.yaml', 'w+')
    # 调用模板映射数据方法
    result = read_template_data('template/app-deploy-template.yaml', proj)
    # 写文件
    file.write(result)
    # 关闭文件
    file.close()

```

##### app-config.yaml

```yaml
projects:
  - service_id: 003-paas-static
    port: 20003
  - service_id: 004-paas-login
    port: 20004
  - service_id: 005-paas-system
    port: 20005
  - service_id: 007-paas-filesystem
    port: 20007
  - service_id: 008-paas-platform
    port: 20008
  - service_id: 009-paas-metadata
    port: 20009
    replicas: 1
  - service_id: 012-paas-gensdk
    port: 20012
  - service_id: 013-paas-comet
    port: 20013
  - service_id: 015-paas-logs
    port: 20015
  - service_id: 018-paas-share
    port: 20018
  - service_id: 020-paas-position
    port: 20020
  - service_id: 021-paas-sftp
    port: 20021
  - service_id: 022-paas-msgimpexp
    port: 20022
    jvm_opt: "-server -Xms512m -Xmx1524m"
  - service_id: 023-paas-workflow
    port: 20023
  - service_id: 201-hrbm-hrbmweb
    port: 20201
    jvm_opt: "-server -Xms512m -Xmx1024m"
  - service_id: 202-hrbm-hrbmlogin
    port: 20202
    jvm_opt: "-server -Xms32m -Xmx32m"
  - service_id: 220-hrbm-hrbmpos
    port: 20220
  - service_id: 101-innovent-innoventweb
    port: 20101
    replicas: 1
  - service_id: 120-innovent-innoventpos
    port: 20120
default:
  replicas: 1
  jvm_opt: "-server -Xms128m -Xmx512m"

```

##### app-deploy-template.yaml

```yaml
#Deployment
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: <span class="katex math inline">{service_id}-deploy
  namespace: paas-app
  labels:
    name:</span>{service_id}-deploy
spec:
  replicas: <span class="katex math inline">{replicas}
  template:
    metadata:
      labels:
        name:</span>{service_id}-pod
    spec:
      terminationGracePeriodSeconds: 1  #k8s正确、优雅地关闭应用，等待时间30秒
      hostAliases:
        - ip: 172.160.180.33
          hostnames:
            - "dev11"
            - "mysql"
        - ip: 172.160.180.34
          hostnames:
            - "dev12"
        - ip: 172.160.180.35
          hostnames:
            - "dev13"

        - ip: 172.160.180.36
          hostnames:
            - "dev14"
        - ip: 172.160.180.37
          hostnames:
            - "dev15"
            - "config-server"
            - "service-proxy"
      containers:
        - name: "app"
          image: <span class="katex math inline">{image}-app:</span>{version}
          imagePullPolicy: Always
          ports:
            - containerPort: <span class="katex math inline">{port}
          env:
            - name: JavaOption
              value:</span>{jvm_opt}
            - name: mainClass
              value: ${main_class}

```