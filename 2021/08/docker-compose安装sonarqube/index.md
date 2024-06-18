---
title: "docker-compose安装sonarqube"
date: "2021-08-11"
categories: 
  - "sonarqube"
---

**[官方github资料](https://github.com/SonarSource/sonarqube "官方github资料")**

**[官方文档](https://docs.sonarqube.org/latest/setup/install-server/ "官方文档")**

## SonarQube的集成思路

**搭建Gitlab** --> **搭建Gitlab-Runner** --> **Gitlab-Runner注册Gitlab** **搭建SonarQube** --> **获取Gitlab用户权限** --> **拉取Gitlab中的项目** **搭建SonarScannerCLI** --> **启动ScannerCLI时绑定SonarQube** --> **配置gitlab-ci.yaml添加SonarQube的触发条件**

## 注意事项

1. 目前最新版本, 已经`不再支持使用外部的ES`——官方意见。只使用内部嵌入式的ES。
2. SonarQube 9.0.x 与 GitLab的集成至少需要 `GitLab 11.7` 版。
3. 社区版不支持多分支的分析，只能分析主分支。从`Developer`版开始，才支持分析多个分支与并合并请求。 **`注意:` 只有社区版才能用，其它版本需要`许可证`**
4. SonarQube 9.0.x 版本至少需要 **`jdk11`** 否则执行失败
5. 如果当前项目使用jdk8， 与SonarQube版本不一致， 在非容器化`CI/CD`(gitlab-runner)情况下，需要提前做好版本切换功能。

### 汉化包安装

**[怎么获取历史版本的jar包](https://github.com/xuhuisheng/sonar-l10n-zh/issues/46 "怎么获取历史版本的jar包")** 原则上用sonarqube的应用市场，会自动匹配对应的插件版本。 然后，项目首页维护了一个兼容版本矩阵，也可以自己手工下载对应的版本放到extensions/plugin目录下，重启就可以用。 **[jar包下载地址](https://github.com/xuhuisheng/sonar-l10n-zh/releases "jar包下载地址")**

```ruby
## 七牛云下载
wget http://qiniu.dev-share.top/sonar-l10n-zh-plugin-9.0.jar

```

## 部署 sonarqube

```yaml
cat > docker-compose.yaml << ERIC
version: "3.1"
services:
  sonarqube:
    image: sonarqube:9.0.1-community
    container_name: sonarqube
    restart: always
    depends_on:
      - db
    environment:
      SONAR_JDBC_URL: jdbc:postgresql://db:5432/sonar
      SONAR_JDBC_USERNAME: sonar
      SONAR_JDBC_PASSWORD: sonar
    volumes:
      - sonarqube_data:/opt/sonarqube/data
      - sonarqube_extensions:/opt/sonarqube/extensions
      - sonarqube_logs:/opt/sonarqube/logs
    ports:
      - 9000:9000

  db:
    image: postgres:12
    container_name: postgres
    restart: always
    environment:
      POSTGRES_USER: sonar
      POSTGRES_PASSWORD: sonar
    volumes:
      - postgresql:/var/lib/postgresql
      - postgresql_data:/var/lib/postgresql/data

volumes:
  sonarqube_data:
  sonarqube_extensions:
  sonarqube_logs:
  postgresql:
  postgresql_data:

ERIC

```

### 运行

```ruby
## 启动
docker-compose up -d

## 汉化
docker exec -it sonarqube  wget -P /opt/sonarqube/extensions/plugins http://qiniu.dev-share.top/sonar-l10n-zh-plugin-9.0.jar

## 重启 sonarqube
docker-compose restart sonarqube

```

> - 127.0.0.1:9000
>     
> - 用户名: admin
>     
> - 密码: admin
> - 登录后自行修改

### 使用gitlab-ci自动化测试的相关配置

#### 1\. sonar 选项手工配置

- 第1步`创建令牌`
- 第2步有问题, 缺少一个`-Dsonar.java.binaries=target/classes`

#### 2\. 关键`.gitlab-ci.yml`配置

```yaml
stages:
  - sonar-check

## snoar检查， 它检查的是 class文件， 所以一定要有target/classes
my-sonar-check:
  stage: sonar-check
  allow_failure: false
  script:
    - echo 1 | sudo alternatives --config java && mvn clean package -U -D maven.test.skip=true
    - echo 2 | sudo alternatives --config java && mvn sonar:sonar
     -Dsonar.java.binaries=target/classes
     -Dsonar.host.url=http://172.16.15.182:9000
     -Dsonar.projectKey=mssp_mssp-service_AXtJzrB6RMuF87xHbp4p
     -Dsonar.login=321da8c28c92de6ca9d04a310eddc58fb46aa222
  only:
    - master
  tags:
    - sonarqube

```

## 常见问题

```ruby
sonarqube  | 2021.08.11 11:37:55 INFO  es[][o.e.b.BootstrapChecks] explicitly enforcing bootstrap checks
sonarqube  | ERROR: [1] bootstrap checks failed. You must address the points described in the following [1] lines before starting Elasticsearch.
sonarqube  | bootstrap check failure [1] of [1]: max virtual memory areas vm.max_map_count [65530] is too low, increase to at least [262144]
sonarqube  | ERROR: Elasticsearch did not exit normally - check the logs at /opt/sonarqube/logs/sonarqube.log

## 解决办法， 直接修改宿主机
cat >> /etc/sysctl.conf << ERIC

# BEGIN ES
vm.max_map_count = 262144
# END ES

ERIC


## 重启
sudo sysctl -p
```

## 绑定 gitlab详细文档

部署成功以后 **http://127.0.0.1`/documentation/analysis/gitlab-integration/`** 查看文档说明
