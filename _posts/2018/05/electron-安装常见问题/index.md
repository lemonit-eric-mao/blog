---
title: "electron 安装常见问题"
date: "2018-05-17"
categories: 
  - "ubuntu"
---

### libgconf-2.so.4 No such file or directory

```ruby
mao-siyu@pc:/$ electron
/usr/lib/node_modules/electron/dist/electron: error while loading shared libraries: libgconf-2.so.4: cannot open shared object file: No such file or directory
mao-siyu@pc:/$
```

##### 解决方案 执行下面的命令

```ruby
mao-siyu@pc:/$ sudo apt-get install libgconf-2-4
```
