---
title: 脚本编写，自动部署程序
date: '2020-02-13T07:32:11+00:00'
status: private
permalink: /2020/02/13/%e8%84%9a%e6%9c%ac%e7%bc%96%e5%86%99%ef%bc%8c%e8%87%aa%e5%8a%a8%e9%83%a8%e7%bd%b2%e7%a8%8b%e5%ba%8f
author: 毛巳煜
excerpt: ''
type: post
id: 5255
category:
    - Python
    - Shell
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
###### 前置条件

dev1 172.16.30.207 程序部署机器  
dev2 172.16.30.208 程序构建机器

- - - - - -

###### dev2 机器中 构建程序脚本 publist.sh

```shell
#!/bin/bash

# 更新代码
git --git-dir=/home/project/yihui-mid-platform/.git --work-tree=/home/project/yihui-mid-platform pull

# 更新 dependencies
mvn -f /home/project/yihui-mid-platform/yihui-dependencies/pom.xml clean install -Dmaven.test.skip=true

# 在父工程打包
mvn -f /home/project/yihui-mid-platform/pom.xml clean install package -U -Dmaven.test.skip=true

for i in "<span class="katex math inline">@"; do
    # 把jar包传输到 dev1
    scp /home/project/yihui-mid-platform/</span>i/target/<span class="katex math inline">i-1.0.0.jar dev1:/home/deploy/app
    # 重启 dev1中的程序
    ssh dev1 /home/deploy/app/redeploy.py</span>i
done

```

- - - - - -

###### dev1 机器中重启程序脚本 redeploy.py

**路径：**`/home/deploy/app`

```python
#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2020/02/13 17:39
# @Author  : Eric.Mao
# @Software: PyCharm
# @Blog    ：http://www.dev-share.top

import os
import sys
os.chdir('/home/deploy/app/')


class ReDeploy(object):

    def __init__(self):
        print('redeploy ......')

    def run(self):
        jar_name = sys.argv[1]
        # 杀死程序
        os.system("kill -9 <span class="katex math inline">(/home/java/jdk1.8.0_241/bin/jps -l | grep %s | awk '{print</span>1}')" % jar_name)
        # 启动程序
        os.system('nohup /home/java/jdk1.8.0_241/bin/java -jar $(ls | grep %s*.jar) --spring.profiles.active=dev > %s.log &' % (jar_name, jar_name))


# 定义入口函数
def main():
    # 初始化
    __this = ReDeploy()
    # 启动程序
    __this.run()

if __name__ == '__main__':
    main()

```

- - - - - -

###### 测试

```ruby
[root@dev2 build]# ./publist.sh yihui-empi yihui-his

```