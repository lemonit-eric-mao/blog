---
title: "Linux系统 mount -t cifs 访问windows共享文件夹"
date: "2018-04-26"
categories: 
  - "linux服务器"
---

##### **mount是Linux下的一个命令，它可以将Windows分区作为Linux的一个“文件”挂接到Linux的一个空文件夹下，从而将Windows的分区和/mnt这个目录联系起来，因此我们只要访问这个文件夹，就相当于访问该分区了。**

`mount -t cifs -o username="本机电脑用户名",password="本机电脑密码" \\\\远程服务器IP/共享文件夹 /mnt/映射到本地的哪个文件夹`

#### 挂载

```ruby
mao-siyu@mao-siyu-PC:/mnt$ mkdir files
mao-siyu@mao-siyu-PC:/mnt$ sudo mount -t cifs -o username="mao-siyu",password="1asdfghjkl;'" \\\\10.32.156.158/files /mnt/files
```

#### 卸载

```ruby
mao-siyu@mao-siyu-PC:/$ sudo umount /mnt/files
```
