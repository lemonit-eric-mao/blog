---
title: 'Git 如何忽略已经提交过的文件'
date: '2017-11-16T16:37:58+00:00'
status: publish
permalink: /2017/11/16/git-%e5%a6%82%e4%bd%95%e5%bf%bd%e7%95%a5%e5%b7%b2%e7%bb%8f%e6%8f%90%e4%ba%a4%e8%bf%87%e7%9a%84%e6%96%87%e4%bb%b6
author: 毛巳煜
excerpt: ''
type: post
id: 551
category:
    - Git
    - 开发工具
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
###### 忽略合并 **.gitattributes**

`添加.gitattributes 目的： 合并时使用本地的.gitlab-ci.yml文件<br></br>注：只有两处分支都对.gitlab-ci.yml有修改，即有冲突时才会使用此规则。<br></br>merge=ours 我的理解是合并并且发生冲突时使用自己的.gitlab-ci.yml文件,若仅仅是一处修改，那么将正常合并【未冲突】，则不会触发此规则`

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

- - - - - -

- - - - - -

- - - - - -

##### **Git 如何忽略已经提交过的文件?**

###### **git pull 代码时经常遇到的问题**

```ruby
mao-siyu@mao-siyu-PC:~/文档/code/bigdata/client<span class="katex math inline">git pull
error: Your local changes to the following files would be overwritten by merge:
        .idea/workspace.xml
Please, commit your changes or stash them before you can merge.
Aborting
mao-siyu@mao-siyu-PC:~/文档/code/bigdata/client</span>

```

###### **处理方法**

```ruby
mao-siyu@mao-siyu-PC:~/文档/code/bigdata/client<span class="katex math inline">git rm --cached .idea/workspace.xml
rm '.idea/workspace.xml'
mao-siyu@mao-siyu-PC:~/文档/code/bigdata/client</span>

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

- - - - - -

- - - - - -

- - - - - -