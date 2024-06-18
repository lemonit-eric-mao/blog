---
title: 'Mono、.Net Core、.Net Framework 区别'
date: '2020-08-01T10:25:44+00:00'
status: publish
permalink: /2020/08/01/mono%e3%80%81-net-core%e3%80%81-net-framework-%e5%8c%ba%e5%88%ab
author: 毛巳煜
excerpt: ''
type: post
id: 5554
category:
    - 自学整理
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
views:
    - '8'
---
##### 区别在图中

![](http://res.mianshigee.com/upload/article/netcore.jpg)

从架构图中可以看到， **.NET Framework 、 .NET Core 、XAMARIN** 都是基于 `.NET STANDARD 库`的

- - - - - -

##### .NET Core 特点

- **跨平台**：是微软推出的最新的开源的，跨平台的框架，用它可以创建的应用可以运行在Windows、MAC、Linux上 。
- **开源**
- **部署灵活**： 可以在应用中包含 .NET Core 或并行安装它（用户或系统范围安装）。 **可搭配 `Docker` 容器使用**。

- - - - - -

##### .NET Framework

- 这个是我们现在经常用的，用这个可以创建windows应用程序还有web applications ，现在你可以用它创建Winform ，UWP ,wpf 等等相关的应用程序 ，web 方面就是Asp.net MVC
- **闭源**

- - - - - -

##### XAMARIN

- 主要用来构建APP的（包括IOS，Android Windows）主要用的是C#语言

- - - - - -

##### Mono

- Mono 通过 **`XAMARIN`** 产品支持 .NET Framework 应用模型（例如，Windows Forms）和其他应用模型（例如，Xamarin.iOS）的子集。而 **.NET Core** `不支持`这些内容。
- Mono 支持很多平台和 CPU。
- Mono 和 .NET Core 两者都使用 MIT 许可证，且都属于 .NET Foundation 项目。
- 最近几年，Mono 的 **`主要焦点是移动平台`** ，而 **.NET Core 的`焦点是云`工作负荷** 。

- - - - - -

##### **[ 如何选择？](https://docs.microsoft.com/zh-cn/dotnet/standard/choosing-core-framework-server " 如何选择？")**

###### **在以下情况，对服务器应用程序使用 .NET Core：**

- 用户有跨平台需求。
- 以微服务为目标。
- 使用 Docker 容器。
- 需要高性能和可扩展的系统。
- 需按应用程序提供并行的 .NET 版本。

###### **在以下情况，对服务器应用程序使用 .NET Framework ：**

- 应用当前使用 .NET Framework（建议扩展而不是迁移）。
- 应用使用不可用于 .NET Core 的第三方 .NET 库或 NuGet 包。
- 应用使用不可用于 .NET Core 的 .NET 技术。
- 应用使用不支持 .NET Core 的平台。 Windows、macOS 和 Linux 支持 .NET Core。

###### **开发移动端 使用 Mono**

- - - - - -

##### **[从 .NET Framework 移植到 .NET Core](https://docs.microsoft.com/zh-cn/dotnet/core/porting/ "从 .NET Framework 移植到 .NET Core")**

- - - - - -

- - - - - -

- - - - - -

###### 环境

k8s版本 1.16.6

docker 版本 19.03.12

- - - - - -

#### 尝试使用 .NET Core 镜像

docker hub 地址： https://hub.docker.com/\_/microsoft-dotnet-core

##### 预期

能够在 linux操作系统中，以 docker 容器运行

##### 测试 使用 docker 运行

```ruby
[root@master ~]# docker run -it --rm -p 30800:80 --name aspnetcore_sample mcr.microsoft.com/dotnet/core/samples:aspnetapp

```

##### 测试 web访问

```ruby
[root@master ~]# curl 11.11.11.27:30800 | grep -E "<h1.>.*"

    <h1 class="display-4">Welcome to .NET Core</h1>

[root@master ~]#

</h1.>
```

- - - - - -

##### 测试 使用 k8s 运行

##### 预期

能够在 linux操作系统 k8s 集群中运行

###### 创建命名空间

```ruby
kubectl create ns win-tools-ns

```

###### 创建 service yaml文件

```ruby
cat > win-svc.yaml 
```

###### 创建 deploy yaml文件

```ruby
cat > win-deploy.yaml 
```

###### 启动

```ruby
kubectl apply -f win-svc.yaml -f win-deploy.yaml

```

###### 测试 web访问

```ruby
[root@master ~]# curl 11.11.11.28:30800 | grep -E "<h1.>.*"

    <h1 class="display-4">Welcome to .NET Core</h1>

[root@master ~]#


[root@master ~]# curl 11.11.11.27:30800 | grep -E "<h1.>.*"

    <h1 class="display-4">Welcome to .NET Core</h1>

[root@master ~]#

</h1.></h1.>
```

- - - - - -

- - - - - -

- - - - - -

##### 尝试使用 Win IIS 镜像

##### 预期

能够在 linux操作系统中，以 docker 容器运行

###### https://hub.docker.com/\_/microsoft-windows-servercore-iis-insider/?tab=description

```ruby
[root@master win]# docker pull mcr.microsoft.com/windows/servercore/iis/insider:windowsservercore-10.0.19035.1
windowsservercore-10.0.19035.1: Pulling from windows/servercore/iis/insider
7705b4d2f0a3: Downloading
40a58c20f260: Pulling fs layer
384fcceebe2a: Pulling fs layer
c841a85b0bb4: Waiting
052e58d80275: Waiting
fa87dd837c31: Waiting
image operating system "windows" cannot be used on this platform
[root@master win]#

```

###### 结果**`不可行`**

###### 问题原因 https://stackoverflow.com/questions/52414844/docker-toolbox-image-operating-system-windows-cannot-be-used-on-this-platform

- - - - - -

- - - - - -

- - - - - -

##### 尝试使用 .NET Framework 镜像

##### 预期

能够在 linux操作系统中，以 docker 容器运行

###### https://hub.docker.com/\_/microsoft-dotnet-framework-aspnet

```ruby
[root@master win]# docker pull mcr.microsoft.com/dotnet/framework/aspnet:4.8
4.8: Pulling from dotnet/framework/aspnet
no matching manifest for linux/amd64 in the manifest list entries
[root@master win]#


```

```ruby
[root@master win]# docker pull mcr.microsoft.com/dotnet/framework/samples:aspnetapp
aspnetapp: Pulling from dotnet/framework/samples
no matching manifest for linux/amd64 in the manifest list entries
[root@master win]#

```

```ruby
[root@master win]# docker pull mcr.microsoft.com/dotnet/framework/samples:dotnetapp
dotnetapp: Pulling from dotnet/framework/samples
no matching manifest for linux/amd64 in the manifest list entries
[root@master win]#

```

```ruby
[root@master win]# docker pull mcr.microsoft.com/dotnet/framework/samples:wcfservice
wcfservice: Pulling from dotnet/framework/samples
no matching manifest for linux/amd64 in the manifest list entries
[root@master win]#

```

```ruby
[root@master win]# docker pull mcr.microsoft.com/dotnet/framework/samples:wcfclient
wcfclient: Pulling from dotnet/framework/samples
no matching manifest for linux/amd64 in the manifest list entries
[root@master win]#

```

###### 结果**`不可行`**

- - - - - -

- - - - - -

- - - - - -

- - - - - -

##### 打包 Docker 镜像

下载官网 Dockerfile: https://hub.docker.com/\_/microsoft-dotnet-core

- - - - - -

###### 查看 .net 项目目录

```ruby
[root@master publish]# ll
total 356
-rw-r--r--. 1 root root    162 Aug  2 14:17 appsettings.Development.json
-rw-r--r--. 1 root root    192 Aug  2 14:17 appsettings.json
-rw-r--r--. 1 root root    162 Aug  3 10:26 Dockerfile
-rw-r--r--. 1 root root 106546 Aug  2 14:43 NetDemo.deps.json
-rw-r--r--. 1 root root   9216 Aug  2 14:43 NetDemo.dll
-rw-r--r--. 1 root root 174592 Aug  2 14:43 NetDemo.exe
-rw-r--r--. 1 root root   1964 Aug  2 14:43 NetDemo.pdb
-rw-r--r--. 1 root root    224 Aug  2 14:30 NetDemo.runtimeconfig.json
-rw-r--r--. 1 root root  35840 Aug  2 14:43 NetDemo.Views.dll
-rw-r--r--. 1 root root   3724 Aug  2 14:43 NetDemo.Views.pdb
-rw-r--r--. 1 root root    551 Aug  2 14:43 web.config
drwxr-xr-x. 5 root root     57 Aug  2 14:43 wwwroot
[root@master publish]#

```

- - - - - -

###### 创建 Dockerfile

ASP.NET Core 运行时环境: https://hub.docker.com/\_/microsoft-dotnet-core-aspnet/

```ruby
cat > Dockerfile 
```

- - - - - -

###### 打包

```ruby
docker build -t dotnet-core:v1.0.0 .

[root@localhost publish]# docker images
REPOSITORY                              TAG                 IMAGE ID            CREATED             SIZE
dotnet-core                             v1.0.0              b806ae139698        7 seconds ago       194MB
[root@localhost publish]#

[root@localhost publish]# docker run -it --name dotnet-core --rm -p 5000:80 dotnet-core:v1.0.0

```

- - - - - -

###### 访问

curl http://192.168.20.91:5000

- - - - - -

- - - - - -

- - - - - -