---
title: "Python 获取系统环境变量"
date: "2019-07-13"
categories: 
  - "python"
---

##### 获取系统环境变量

```
一、os.environ['环境变量名称']
二、os.getenv('环境变量名称')
```

##### 设置系统环境变量

```
一、os.environ['环境变量名称']='环境变量值'
二、os.putenv('环境变量名称', '环境变量值')
```

##### 获取 git-runner 运行时内置的环境变量

```ruby
[root@k8s-master script]# pwd
/home/gitlab-runner/script/
[root@k8s-master script]# cat > build.py << eric
#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

# $CI_PROJECT_NAME
print(os.environ['CI_PROJECT_NAME'])
# $CI_COMMIT_TAG
print(os.environ['CI_COMMIT_TAG'])
eric
[root@k8s-master script]#
```

##### .gitlab-ci.yml

```yaml
# 创建一个名为初始化的任务
init:
  # 要执行的脚本
  script:
    # 初始化Node.js项目的依赖
    - /home/gitlab-runner/script/build.py
  # 告诉 Runner 这个名为init的任务，只在打tag的时候执行
  only:
    - tags
  # GitLab CI有三个默认阶段：1构建(build)、2测试(test)、3部署(deploy)。
  # 告诉 Runner 这个名为init的任务，只在测试阶段执行
  stage: build
  # 告诉 Runner 我们应用哪个标签
  tags:
    - tag-nodejs
```
