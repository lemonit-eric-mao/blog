---
title: "Python 根据项目名称生成docker-compose 文件"
date: "2019-11-20"
categories: 
  - "python"
---

##### 前置条件

├─configs ├─dist ├─template └─tools

* * *

##### 配置文件 configs/config.yaml

```yaml
# 生成的根目录
dist:
  # 最终生成的文件夹
  paas:
    # 最终生成的项目
    - project_name: 009-paas-metadata
      main_class: "com.sinoeyes.PaasMetaDataApplication"
    - project_name: 012-paas-gensdk
      main_class: "com.sinoeyes.GensdkApplication"
      version: "1.0.1"
    - project_name: 013-paas-comet
      main_class: "com.sinoeyes.comet.PaasCometApplication"

  hengrui:
    - project_name: 601-hengrui-hengrui
      main_class: "com.sinoeyes.web.HengruiLoginMainApplication"
    - project_name: 602-hengrui-web
      main_class: "com.sinoeyes.web.HengruiWebApplication"

default:
  jvm_opts: "-server -Xms128m -Xmx512m"
  version: "1.0.0"
  main_class: ""
```

##### 模板文件 template/docker-compose.yml

```yml
  ${project_name}:
    container_name: ${project_name}
    image: sinoeyes.io/dev2/${image_name}:${version}
    restart: always
    network_mode: host
    volumes:
      - ../logs/${project_name}:/var/log/apps
      - ../config/logback-spring.xml:/opt/logback-spring.xml
    environment:
      - JVM_OPTS=${jvm_opts}
      - spring.cloud.config.uri=http://config-server:20001
      - spring.cloud.config.profile=prd2
      - user.timezone=GMT+08
      - mainClass=${main_class}
    ports:
      - ${port}:${port}
```

##### 工具文件 tools/tool\_yaml.py

```python
#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2019/11/20 17:34
# @Author  : Eric.Mao
# @FileName: tool_yaml.py
# @Software: PyCharm
# @Blog    : https://www.lemonit.cn

import yaml
import os
import shutil
from string import Template


# 解析yaml文件
def get_apps_yaml_info(target_config_yaml):
    # 加载配置文件
    yaml_file = open(target_config_yaml)

    # YAML 5.1版本后弃用了yaml.load(file)这个用法，因为觉得很不安全
    # 5.1版本之后就修改了需要指定Loader，
    # 通过默认加载​​器（FullLoader）禁止执行任意函数，该load函数也变得更加安全
    # https://github.com/yaml/pyyaml/wiki/PyYAML-yaml.load(input)-Deprecation#footnotes
    # 解析配置文件
    doc = yaml.load(yaml_file, Loader=yaml.FullLoader)
    # doc = yaml.load(yaml_file)
    yaml_file.close()
    # 补全每一条信息的 默认设置
    for project_group in doc['dist']:
        for project in doc['dist'][project_group]:
            # 有限使用特殊的配置，否则使用默认配置
            project['jvm_opts'] = (project.has_key('jvm_opts') and project['jvm_opts'] or doc['default']['jvm_opts'])
            project['version'] = (project.has_key('version') and project['version'] or doc['default']['version'])
            project['main_class'] = (project.has_key('main_class') and project['main_class'] or doc['default']['main_class'])
    return doc


# 递归删除一个目录以及目录内的所有内容
def del_file(srcfile):
    if os.path.exists(srcfile):
        shutil.rmtree(srcfile)


# 将生成的文件内容保存到本地
def save_file(dist_dir, file_name, content):
    # 如果文件夹不存在
    if not os.path.exists(dist_dir):
        os.makedirs(dist_dir)
    #
    file = os.path.join(dist_dir, file_name)
    with open(file, 'a+') as f:
        f.write(content)
        f.close()


# 实现字符串模板转换,tpl为模板路径，data为组装数据
def get_template_data(tpl, data):
    with open(tpl) as f:
        content = f.read()
        tmp = Template(content)
        str = tmp.substitute(data)
        return str
```

##### 入口文件 k8s\_2\_compose.py

```python
#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2019/11/20 17:06
# @Author  : Eric.Mao
# @FileName: k8s_2_compose.py
# @Software: PyCharm
# @Blog    : https://www.lemonit.cn

from tools.tool_yaml import *


class K8s2Compose(object):
    def __init__(self):
        self.configs = get_apps_yaml_info("configs/config.yaml")
        self.dist_dir = "dist/"

    # 生成docker-compose 相关文件
    def generate_docker_compose(self):

        # 删除已经存在的文件
        del_file(self.dist_dir)
        # 生成docker-compose文件头
        save_file(self.dist_dir, 'docker-compose.yml', 'version: "3"\nservices:')

        for project_group in self.configs['dist']:
            for data in self.configs['dist'][project_group]:
                # 获取项目名
                project_name = data['project_name']
                # 截取项目名
                data['image_name'] = project_name[4:]
                # 拼接端口号
                data['port'] = '20' + project_name[0:3]

                # 模板填充
                new_template = get_template_data("template/docker-compose.yml", data)

                # 生成新的文件
                save_file(self.dist_dir, 'docker-compose.yml', new_template)


if __name__ == '__main__':
    # 初始化
    __this = K8s2Compose()
    # 启动程序
    __this.generate_docker_compose()

```
