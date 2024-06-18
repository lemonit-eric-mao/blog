---
title: "安装VS Code Web IDE"
date: "2021-10-08"
categories: 
  - "开发工具"
---

## docker-compose 安装Code-Server

**[官方github](https://github.com/cdr/code-server "官方github")**

* * *

### 一、创建相关文件夹

```ruby
mkdir -p ./config/certs \
         ./config/project \
         ./config/offline-extensions

-------------------------------------------------------------
## 文件夹作用说明
#      # CodeServer 所有未安装的插件文件
#      - ./config/offline-extensions:$HOME/offline-extensions

#      # CodeServer git clone 的项目
#      - ./config/project:$HOME/project

#      # CodeServer 的 https证书
#      - ./config/certs:$HOME/certs

```

### 二、将https证书 .pem .key 文件放到 `./config/certs`目录下。 将要离线安装的插件文件放到 `./config/offline-extensions`目录下。

* * *

### 三、编写docker-compose文件

#### Http方式

```yaml
cat > docker-compose.yaml << ERIC
version: "3.6"
services:
  code-server:
    container_name: code-server
    image: codercom/code-server:4.13.0
    restart: always
    privileged: true
    user: root
    ports:
      - 8080:8080
    volumes:
      - ./config:\$HOME
      # 用来存放你的项目代码
      - ./config/project:/project
    environment:
      PASSWORD: 123456

ERIC

```

#### Https方式

```yaml
cat > docker-compose.yaml << ERIC
version: "3.6"
services:
  code-server:
    container_name: code-server
    image: codercom/code-server:4.13.0
    restart: always
    privileged: true
    user: root
    ports:
      - 443:8080
    volumes:
      - ./config:\$HOME
      # 用来存放你的项目代码
      - ./config/project:/project

    # 出于安全考量，Service workers 只能由 HTTPS 承载
    # 如果自己测试可以使用 127.0.0.1进行访问， 但是提供外部访问一定要使用https访问，而且不能使用自签名证书，它会导致某些插件不可用
    entrypoint: |
      /usr/bin/entrypoint.sh --bind-addr="0.0.0.0:8080" --cert="\$HOME/certs/devcloud.dhccloud.com.cn.pem"  --cert-key="\$HOME/certs/devcloud.dhccloud.com.cn.key"
    environment:
      PASSWORD: 123456

ERIC

```

* * *

###### 四、启动

```ruby
docker-compose up -d

```

* * *

* * *

* * *

* * *

* * *

* * *

##### Helm k8s 安装

###### **[官方github](https://github.com/cdr/code-server/tree/main/ci "官方github")**

###### **[官方网址](https://coder.com/docs/code-server/latest/helm "官方网址")**

```ruby
git clone https://github.com/cdr/code-server.git
cd code-server

helm upgrade --install code-server ci/helm-chart
```

* * *

###### 或者使用values.yaml文件安装

```ruby
git clone https://gitee.com/eric-mao/code-server.git
cp code-server/ci/helm-chart/values.yaml .

helm upgrade --install code-server code-server/ci/helm-chart
    --set image.repository="172.16.15.183/library/codercom/code-server:4.3.0"
    --set persistence.enabled=false # 是否启用持久化
    -f values.yaml
    -n nocalhost-test

## 获取登录密码
echo $(kubectl get secret --namespace nocalhost-test code-server -o jsonpath="{.data.password}" | base64 --decode)

```

* * *

###### 卸载

```ruby
helm -n nocalhost-test delete code-server
```

* * *

* * *

* * *

###### **[插件扩展相关官方文档](https://github.com/cdr/code-server/blob/main/docs/FAQ.md#differences-compared-to-vs-code "插件扩展相关官方文档")**

###### **[添加Nocalhost插件](https://github.com/nocalhost/nocalhost-vscode-plugin/releases "添加Nocalhost插件")**

###### 汉化及其他插件

点击右侧的扩展图片，输入 **`chinese`** 下载简体中文语言包即可使用中文。

* * *

* * *

* * *
