---
title: "GitLab CI/CD 配置 .gitlab-ci.yml"
date: "2019-06-14"
categories: 
  - "git"
---

###### 配置 .gitlab-ci.yml

将 `.gitlab-ci.yml` 文件加入到项目的根目录，Runner它会去读取这里面的配置 需求：whois项目是一个使用Node.js开发的服务器用来查询域名的，因此必须需要有node.js环境才能运行。

###### **注：`多阶段任务在执行过程中， 每个任务开始执行时， 都会将上一阶段执行的环境恢复成默认状态`**

```yaml
# 自定义环境变量， 此变量只在gitlab-runner中可用
variables:
  ## ENV_NAME: "ENV_VALUE"
  ENV_OPTIONS: "$ENV_OPTIONS"


# 设定任务执行顺序, 名称可以随意自定义
stages:
  # step: 1
  - build
  # step: 2
  - dev-share
  # step: 3
  - publish
  # step: 4
  - deploy

# 创建一个名为 build_dev 的任务
build_dev:
  # 告诉 Runner 这个名为 build_dev 的任务，在多任务共同执行时，它的执行顺序为 1
  stage: build
  # 要执行的脚本
  script:
    # 初始化Node.js项目的依赖
    - cnpm i
    # 执行脚本
    - sudo /home/runner/kubectl-get-pods.sh
  # 不允许失败后继续执行
  allow_failure: false
  # 告诉 Runner 这个名为 build_dev 的任务，只在 master 分支上执行
  only:
    - master
  # 告诉 Runner 我们应用哪个标签
  tags:
    - devops

# 创建一个名为 build_test 的任务
build_test:
  # 告诉 Runner 这个名为 build_test 的任务，在多任务共同执行时，它的执行顺序为 2
  stage: dev-share
  # 要执行的脚本
  script:
    - cnpm i
  # 不允许失败后继续执行
  allow_failure: false
  # 告诉 Runner 这个名为 build_test 的任务, 只在 除master 分支之外的其他分支的每次推送时执行
  except:
    - master
  # 告诉 Runner 我们应用哪个标签。 如果不写会报错：(此作业被卡住，因为没有任何该项目指定标签的 runner 在线)
  tags:
    - devops

# 创建一个名为 build_uat 的任务
build_uat:
  # 告诉 Runner 这个名为 build_uat 的任务，在多任务共同执行时，它的执行顺序为 3
  stage: publish
  # 要执行的脚本
  script:
    - cnpm i
  # 不允许失败后继续执行
  allow_failure: false
  # 告诉 Runner 这个名为 build_uat 的任务, 只在 除master 分支之外的其他分支的每次推送时执行
  only:
    - uat
  # 告诉 Runner 我们应用哪个标签。 如果不写会报错：(此作业被卡住，因为没有任何该项目指定标签的 runner 在线)
  tags:
    - devops

# 创建一个名为 build_tag 的任务
build_tag:
  # 告诉 Runner 这个名为 build_tag 的任务，在多任务共同执行时，它的执行顺序为 4
  stage: deploy
  # 要执行的脚本
  script:
    - cnpm i
  # 不允许失败后继续执行
  allow_failure: false
  # 告诉 Runner 这个名为 build_tag 的任务，只在 新建tag 的时候执行
  only:
    - tags
  # 告诉 Runner 我们应用哪个标签。 如果不写会报错：(此作业被卡住，因为没有任何该项目指定标签的 runner 在线)
  tags:
    - devops
```

##### 在gitlab-runner 中执行 .sh 脚本

前置条件: 1. gitlab-runner 与 k8s-master 安装在同一台主机 2. k8s-master 只有 root权限才可以使用 kubectl 命令 3. 希望使用 gitlab-runner用户来执行 kubectl 命令来操作 k8s-master

```ruby
# 在gitlab-runner用户下编写脚本
[gitlab-runner@master ~]#
# 编写测试脚本
[gitlab-runner@master ~]# cat > /home/gitlab-runner/kubectl-get-pods.sh << EOF
#!/bin/bash
kubectl get pods -A -o wide
EOF
# 授权
[gitlab-runner@master ~]# chmod -R 777 /home/gitlab-runner/kubectl-get-pods.sh
[gitlab-runner@master ~]# ll
total 8
drwxrwxr-x 3 gitlab-runner gitlab-runner 4096 Jun  5 16:10 builds
-rwxrwxrwx 1 gitlab-runner gitlab-runner   40 Jun  5 17:22 kubectl-get-pods.sh
[gitlab-runner@master ~]#
```

* * *

* * *

* * *

### 脚本中使用CURL

```yaml
variables:
  # 禁用 GitLab Runner 默认的代码克隆功能
  GIT_STRATEGY: none
  # gitops-agent 地址
  AGENT_URL: http://127.0.1.2:8080

stages:
  # 先拉取项目
  - git_clone
  # 再执行脚本
  - exec_agent

# 先拉取项目
git_clone:
  stage: git_clone
  only:
    - tags
  tags:
    - devops
  script:
    # 向远程agent发起工作请求
    - |
      response=$(curl -s -w "\n%{http_code}" -X POST -d '{
        "repoURL": "'$CI_REPOSITORY_URL'",
        "tag": "'$CI_COMMIT_TAG'"
      }' $AGENT_URL/api/clone)

      # 提取最后一行，即状态码
      statusCode=${response##*$'\n'}
      # 从响应中移除状态码部分
      responseData=${response%$statusCode}

      echo "$responseData"
      # 执行异常
      if [ "$statusCode" != "200" ]; then
        exit 1
      fi

# 再执行脚本
exec_agent:
  needs:
    - job: git_clone
  stage: exec_agent
  only:
    - tags
  tags:
    - devops
  script:
    # 向远程agent发起工作请求
    - |
      response=$(curl -s -w "\n%{http_code}" -X POST -d '{
        "scriptPath": "/script/start.bat",
        "tag": "'$CI_COMMIT_TAG'",
        "cmdType": "powershell"
      }' $AGENT_URL/api/exec)

      # 提取最后一行，即状态码
      statusCode=${response##*$'\n'}
      # 从响应中移除状态码部分
      responseData=${response%$statusCode}

      echo "$responseData"
      # 执行异常
      if [ "$statusCode" != "200" ]; then
        exit 1
      fi
```

**[GitOps Agent 项目地址](https://gitee.com/eric-mao/gitops-agent "GitOps Agent 项目地址")**

* * *

* * *

* * *

###### [GitLab CI/CD 预定义环境变量说明](https://docs.gitlab.com/ee/ci/variables/predefined_variables.html "GitLab CI/CD 预定义环境变量说明")
