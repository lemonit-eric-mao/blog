---
title: '安装VS Code Web IDE'
date: '2021-10-08T09:24:48+00:00'
status: private
permalink: /2021/10/08/%e5%ae%89%e8%a3%85vs-code-web-ide
author: 毛巳煜
excerpt: ''
type: post
id: 7962
category:
    - 开发工具
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
---
docker-compose 安装Code-Server
----------------------------

**[官方github](https://github.com/cdr/code-server "官方github")**

- - - - - -

### 一、创建相关文件夹

```ruby
mkdir -p ./config/certs \
         ./config/project \
         ./config/offline-extensions

-------------------------------------------------------------
## 文件夹作用说明
#      # CodeServer 所有未安装的插件文件
#      - ./config/offline-extensions:<span class="katex math inline">HOME/offline-extensions

#      # CodeServer git clone 的项目
#      - ./config/project:</span>HOME/project

#      # CodeServer 的 https证书
#      - ./config/certs:$HOME/certs


```

### 二、将https证书 .pem .key 文件放到 `./config/certs`目录下。 将要离线安装的插件文件放到 `./config/offline-extensions`目录下。

- - - - - -

### 三、编写docker-compose文件

#### Http方式

```yaml
cat > docker-compose.yaml 
```

#### Https方式

```yaml
cat > docker-compose.yaml 
```

- - - - - -

###### 四、启动

```ruby
docker-compose up -d


```

- - - - - -

- - - - - -

- - - - - -

- - - - - -

- - - - - -

- - - - - -

##### Helm k8s 安装

###### **[官方github](https://github.com/cdr/code-server/tree/main/ci "官方github")**

###### **[官方网址](https://coder.com/docs/code-server/latest/helm "官方网址")**

```ruby
git clone https://github.com/cdr/code-server.git
cd code-server

helm upgrade --install code-server ci/helm-chart

```

- - - - - -

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

- - - - - -

###### 卸载

```ruby
helm -n nocalhost-test delete code-server

```

- - - - - -

- - - - - -

- - - - - -

###### **[插件扩展相关官方文档](https://github.com/cdr/code-server/blob/main/docs/FAQ.md#differences-compared-to-vs-code "插件扩展相关官方文档")**

###### **[添加Nocalhost插件](https://github.com/nocalhost/nocalhost-vscode-plugin/releases "添加Nocalhost插件")**

###### 汉化及其他插件

点击右侧的扩展图片，输入 **`chinese`** 下载简体中文语言包即可使用中文。

- - - - - -

- - - - - -

- - - - - -