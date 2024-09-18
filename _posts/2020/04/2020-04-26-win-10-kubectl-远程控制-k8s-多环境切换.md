---
title: "Win 10 kubectl 远程控制 K8S 多环境切换"
date: "2020-04-26"
categories: 
  - "非技术文档"
---

###### 前置条件

**[K8S多集群切换的前置条件](k8s-%e5%a4%9a%e9%9b%86%e7%be%a4%e5%88%87%e6%8d%a2 "K8S多集群切换的前置条件")**

* * *

* * *

* * *

###### 下载 kubectl

D盘创建文件夹 `D:\kubectl` 打开 **`cmd`**

```shell
wget -O D:\kubectl https://storage.googleapis.com/kubernetes-release/release/v1.20.4/bin/windows/amd64/kubectl.exe
```

* * *

###### k8s 切换环境 创建 `D:\kubectl\k8s.bat` 文件

```batch
@ECHO off
:: developer author Eric.mao

MKDIR %USERPROFILE%\.kube\

:: cd /d %~dp0 的意思就是cd /d D:\kubectl
:: %0代表批处理本身 D:\kubectl\k8s.bat
:: ~dp是变量扩充
:: d既是扩充到分区号 D:
:: p就是扩充到路径 \kubectl
:: dp就是扩充到分区号路径 D:\kubectl
:: 切换到当前执行的bat文件的所在目录
CD /d %~dp0

:: 防止乱码
CHCP 65001

:init
    ECHO.
    COLOR 2
    ECHO ***********菜单***********
    ECHO [0] DEV
    ECHO [1] UAT
    ECHO [2] PROD
    ECHO [9] 退出
    ECHO **************************

    SET /p param=请选择:
        IF /I %param%==0 GOTO dev
        IF /I %param%==1 GOTO uat
        IF /I %param%==2 GOTO prod
        IF /I %param%==99 EXIT

:dev
    copy /Y DEV-config %USERPROFILE%\.kube\config
    kubectl get nodes
    GOTO :EOF

:uat
    copy /Y UAT-config %USERPROFILE%\.kube\config
    kubectl get nodes
    GOTO :EOF

:prod
    copy /Y PROD-config %USERPROFILE%\.kube\config
    kubectl get nodes
    GOTO :EOF

```

* * *

###### 将目录加入到**系统环境变量** **`path`** 中

`D:\kubectl` 目录中内容

```shell
k8s.bat
kubectl.exe
# 以下三个文件为，不同K8S环境的 .kube/config 文件
DEV-config
UAT-config
PROD-config
```

* * *

###### 测试

```shell
Active code page: 65001

***********菜单***********
[0] DEV
[1] UAT
[2] PROD
[9] 退出
**************************
请选择:0
        1 file(s) copied.
NAME    STATUS   ROLES    AGE    VERSION
test1   Ready    master   6d8h   v1.13.0
test2   Ready    <none>   6d6h   v1.13.0
test3   Ready    <none>   6d6h   v1.13.0
test4   Ready    <none>   6d6h   v1.13.0
PS D:\kubectl>
```

* * *

* * *

* * *

###### 常见问题

**`Unable to connect to the server: dial tcp [::1]:8080: connectex: No connection could be made because the`**

```ruby
## 执行命令引发的异常
[root@master01 ~]# kubectl.exe get ns
Unable to connect to the server: dial tcp [::1]:8080: connectex: No connection could be made because the


## 查看 kubectl版本
[root@master01 ~]# kubectl.exe version
Client Version: version.Info{Major:"1", Minor:"20", GitVersion:"v1.20.4", GitCommit:"e87da0bd6e03ec3fea7933c4b5263d151aafd07c", GitTreeState:"clean", BuildDate:"2021-02-18T16:12:00Z", GoVersion:"go1.15.8", Compiler:"gc", Platform:"windows/amd64"}
###### 原来问题在这，这个问题通常是kubectl没有指定k8s集群的上下文
Unable to connect to the server: dial tcp [::1]:8080: connectex: No connection could be made because the target machine actively refused it.


## 确认问题，发现确实没有指定k8s集群的上下文
[root@master01 ~]# kubectl config get-contexts
CURRENT   NAME         CLUSTER          AUTHINFO   NAMESPACE
          cluster_01   15-184-cluster   eric.mao


## 处理问题
[root@master01 ~]# kubectl config use-context cluster_01
Switched to context "cluster_01".

## 再次查看
[root@master01 ~]# kubectl.exe config get-contexts
CURRENT   NAME         CLUSTER          AUTHINFO   NAMESPACE
*         cluster_01   15-184-cluster   eric.mao

## 再次查看
[root@master01 ~]# kubectl version
Client Version: version.Info{Major:"1", Minor:"20", GitVersion:"v1.20.4", GitCommit:"e87da0bd6e03ec3fea7933c4b5263d151aafd07c", GitTreeState:"clean", BuildDate:"2021-02-18T16:12:00Z", GoVersion:"go1.15.8", Compiler:"gc", Platform:"linux/amd64"}
Server Version: version.Info{Major:"1", Minor:"20", GitVersion:"v1.20.4", GitCommit:"e87da0bd6e03ec3fea7933c4b5263d151aafd07c", GitTreeState:"clean", BuildDate:"2021-02-18T16:03:00Z", GoVersion:"go1.15.8", Compiler:"gc", Platform:"linux/amd64"}
[root@master01 ~]#

```

* * *

* * *

* * *
