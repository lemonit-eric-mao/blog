---
title: "GitLab-CI 持续集成 生产案例"
date: "2019-07-10"
categories: 
  - "git"
---

##### 自动部署时，要保证所有被 gitlab-runner 操作的项目或文件，都在 gitlab-runner用户目录下，这样省去很多麻烦

##### 项目目录结构

```ruby
promotion-platform-web
│  .gitlab-ci.yml
│  Dockerfile               # 将当前项目 打包成docker镜像的配置文件
│  package.json
│  README.md
│
├─deploy-k8s                # 存放属于当前项目的 k8s 配置文件
│      namespace.yaml
│      service.yaml
│      deployment.yaml
│
├─dist-server               # 用来部署 dist 程序
│  │  .editorconfig
│  │  .gitignore
│  │  app.js
│  │  package.json
│  │  README.md
│  │
│  ├─bin
│  │      www
│  │
│  ├─dist
│  ├─exception-log
│  │      ExceptionLog.js
│  │
│  └─routes
│          index.js
│
├─public
│
│  ......
│
└─src
    ......

```

* * *

##### Dockerfile

```ruby
# This file is a template, and might need editing before it works on your project.
FROM node:12.18.2-alpine AS base-image
# 工作目录
WORKDIR /usr/src/app/

# ARG NODE_ENV
# ENV NODE_ENV $NODE_ENV

# 将dist-server服务器， 复制到工作目录
COPY ./dist-server /usr/src/app/

RUN npm cache verify && npm install -S

# 将 .dist/目录中内容， 复制到工作目录下的 dist/目录中
COPY ./dist /usr/src/app/dist/

CMD [ "npm", "start" ]

# replace this with your application's default port
EXPOSE 8066

```

* * *

##### .gitlab-ci.yml

```yaml
# 创建一个名为 my_tag 的任务
my_tag:

    # 要执行的脚本
    script:
        - yarn cache clean && yarn
        # 打包程序
        - yarn build
        - cp -rp /home/gitlab-runner/deploy/dist-server/ .
        - cp -rp ./dist/ ./dist-server/
        # 构建镜像
        - pushd dist-server
        - envsubst < Dockerfile | docker build -t harbor.software.com/library/${CI_PROJECT_NAME}:${CI_COMMIT_TAG} -f - .
        - popd
        # 先确定 docker 已经登录到 harbor库
        - docker login harbor.software.com -u admin -p Harbor12345
        # 上传到Harbor私有仓库
        - docker push harbor.software.com/library/${CI_PROJECT_NAME}:${CI_COMMIT_TAG}

        # 将k8s的yaml文件，上传到基于Harbor的Helm Charts私有仓库， 并且版本与Docker镜像保持一致
        # http://192.168.20.93/chartrepo    chartrepo为关键字
        - helm repo add harbor-repo http://harbor.software.com/chartrepo/dev/ --username admin --password Harbor12345

        # 将准备好的 helm chart模板复制到工作目录， 进行构建
        # 参考 自定义-helm-chart包：  http://www.dev-share.top/2021/06/11/%e8%87%aa%e5%ae%9a%e4%b9%89-helm-chart%e5%8c%85/
        - cp -rp /home/gitlab-runner/deploy/build_helm_charts/${CI_PROJECT_NAME} .
        # 推送到Harbor
        - helm push ${CI_PROJECT_NAME} harbor-repo --version=${CI_COMMIT_TAG}

        # 更新 helm仓库
        - helm repo update
        # 拉取helm chart包
        - helm pull harbor-repo/${CI_PROJECT_NAME} --version ${CI_COMMIT_TAG} --username admin --password Harbor12345
        # 离线解包
        - helm template ${CI_PROJECT_NAME} ./${CI_PROJECT_NAME}-${CI_COMMIT_TAG}.tgz --output-dir .
            --namespace uat-mssp
            --set image.repository=harbor.software.com/library/${CI_PROJECT_NAME}
            --set image.tag=${CI_COMMIT_TAG}
            --set deployment.serverIp=172.16.15.184
            --set deployment.serverPort=30002
        # 在k8s上运行
        - kubectl apply -R -f ${CI_PROJECT_NAME}/templates/


    # 构建完成后，删除空镜像
    after_script:
        - docker system prune -f

    # 告诉 Runner 这个名为 my_tag 的任务，只在 新建tag 的时候执行
    only:
        - tags

    stage: build

    # 告诉 Runner 我们应用哪个标签。 如果不写会报错：(此作业被卡住，因为没有任何该项目指定标签的 runner 在线)
    tags:
        - devops
```

* * *

##### package.json

```json
{
  "name": "promotion-platform-web",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "vue-cli-service serve",
    "build": "vue-cli-service build",
    "lint": "vue-cli-service lint"
  },
  "dependencies": {
    "axios": "^0.19.2",
    "core-js": "^3.6.4",
    "element-ui": "^2.13.0",
    "moment": "^2.24.0",
    "vue": "^2.6.10",
    "vue-qriously": "^1.1.1",
    "vue-router": "^3.0.3",
    "xlsx": "^0.15.5"
  },
  "devDependencies": {
    "@vue/cli-plugin-babel": "^4.2.2",
    "@vue/cli-service": "^4.2.2",
    "node-sass": "^4.9.0",
    "sass-loader": "^8.0.2",
    "vue-template-compiler": "^2.6.10"
  }
}

```

* * *

* * *

* * *

* * *

* * *

* * *

##### k8s 相关配置文件

###### namespace.yaml

```yaml
---
# 创建命名空间
kind: Namespace
apiVersion: v1
metadata:
    # 不可以使用 下划线
    name: promotion-platform
    labels:
        name: promotion-platform

```

* * *

###### service.yaml

```yaml
---
# 为部署的容器开放端口
# Service
kind: Service
apiVersion: v1
metadata:
    # 所属的命名空间
    namespace: promotion-platform
    # Service 名称
    name: service-${CI_PROJECT_NAME}
    # Service 标签
    labels:
        name: service-${CI_PROJECT_NAME}

# 容器的详细定义
spec:
    # 告诉 K8s Docker容器对外开放几个端口
    # 如果指定为 NodePort 则这个service的端口可以被外界访问
    type: NodePort
    ports:
        - name: http
          protocol: TCP
            # port 是service的端口
          port: 80
            # targetPort 是pod的端口
          targetPort: 8066
            # 可以被外网访问的端口
          nodePort: 30808

    # 选择 Pod的label名
    selector:
        # Pod的label名
        app: pod-${CI_PROJECT_NAME}
```

* * *

###### deployment.yaml

```yaml
---
# 创建要部署的容器
# 种类：告诉 k8s 下面这些配置的含义(常用的包括：Namespace, Deployment, Service)
kind: Deployment
# 版本号 规定格式 apps/* 必须这么写
apiVersion: apps/v1
# Deployment
metadata:
    # Deployment 的所属的命名空间
    namespace: promotion-platform
    # Deployment 名称
    name: deployment-${CI_PROJECT_NAME}

# 容器的详细定义
spec:
    # 告诉 K8s 启动几个节点
    replicas: 1
    # 滚动升级时，容器准备就绪时间最少为30s
    minReadySeconds: 30
    # 选择模板
    selector:
        # 根据模板的labels来选择
        matchLabels:
            # 选择下面模板中, Pod 的label名
            app: pod-${CI_PROJECT_NAME}

    # 定义 Pod模板
    template:
        metadata:
            # Pod模板的labels
            labels:
                # Pod的label名
                app: pod-${CI_PROJECT_NAME}
        spec:
            # k8s将会给应用发送SIGTERM信号，可以用来正确、优雅地关闭应用,默认为30秒
            terminationGracePeriodSeconds: 60
            # 告诉 k8s 根据设置的节点名称，将这个pod部署到哪个节点机器上（默认不指定，k8s会自动分配）; 因为 nodeName(节点的名称不可以重复，因此使用nodeName只能指定一台节点服务)
            # nodeName: k8s-node1
            # 告诉 k8s 根据设置的节点标签，将这个pod部署到哪个节点机器上（默认不指定，k8s会自动分配）; 因为 nodeLabels(节点的标签可以重复，因此使用nodeSelector是可以指定同一个标签的多个节点服务)
            # nodeSelector:
            # 配置 Docker容器
            containers:
                # Docker 容器名
                - name: ${CI_PROJECT_NAME}
                  # 告诉 K8s 要部署的 Docker 镜像名:Tag
                  image: harbor.software.com/library/${CI_PROJECT_NAME}:${CI_COMMIT_TAG}
#                  env:
#                  - name:
#                    value:
                  # 告诉 K8s 如果本地没有这个镜像
                  # 总是拉取 pull
                  imagePullPolicy: Always
                  # 只使用本地镜像，从不拉取
                  # imagePullPolicy: Never
                  # 默认值,本地有则使用本地镜像,不拉取
                  # imagePullPolicy: IfNotPresent
                  # 告诉 K8s Docker容器对外开放几个端口
                  ports:
                      - containerPort: 8066
                        protocol: TCP
```

* * *

* * *

* * *

* * *

* * *

* * *

* * *

* * *

* * *
