---
title: "Git 如何忽略已经提交过的文件"
date: "2017-11-16"
categories: 
  - "git"
  - "开发工具"
---

###### 忽略合并 **.gitattributes**

`添加.gitattributes 目的： 合并时使用本地的.gitlab-ci.yml文件 注：只有两处分支都对.gitlab-ci.yml有修改，即有冲突时才会使用此规则。 merge=ours 我的理解是合并并且发生冲突时使用自己的.gitlab-ci.yml文件,若仅仅是一处修改，那么将正常合并【未冲突】，则不会触发此规则`

```ruby
echo '.gitlab-ci.yml merge=ours' > .gitattributes
# 设置driver 是否全局生效，酌情使用--global
git config --global merge.ours.driver true

root@192:/# git config --global --list
merge.ours.driver=true

###################

## 在docker中运行
[root@cloudserver gitlab]# docker exec -it gitlab-zh    git config --global merge.ours.driver true
[root@cloudserver gitlab]# docker exec -it gitlab-zh    git config --global --list
merge.ours.driver=true
[root@cloudserver gitlab]#

```

* * *

* * *

* * *

##### **Git 如何忽略已经提交过的文件?**

###### **git pull 代码时经常遇到的问题**

```ruby
mao-siyu@mao-siyu-PC:~/文档/code/bigdata/client$ git pull
error: Your local changes to the following files would be overwritten by merge:
        .idea/workspace.xml
Please, commit your changes or stash them before you can merge.
Aborting
mao-siyu@mao-siyu-PC:~/文档/code/bigdata/client$
```

###### **处理方法**

```ruby
mao-siyu@mao-siyu-PC:~/文档/code/bigdata/client$ git rm --cached .idea/workspace.xml
rm '.idea/workspace.xml'
mao-siyu@mao-siyu-PC:~/文档/code/bigdata/client$
```

###### **修改 .gitignore**

```ruby
# dependencies
node_modules

# logs
npm-debug.log

# Nuxt build
.nuxt

# Nuxt generate
dist

# idea/ all
.idea/
```

**最后 提交 .gitignore文件**

* * *

* * *

* * *
