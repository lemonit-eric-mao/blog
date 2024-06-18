---
title: "Git 常用命令 切换版本 切换分支"
date: "2018-04-28"
categories: 
  - "开发工具"
---

#### 下载`git lfs`

```bash
# 下载 git lfs
wget https://github.com/git-lfs/git-lfs/releases/download/v3.5.1/git-lfs-linux-amd64-v3.5.1.tar.gz
tar -axvf git-lfs-linux-amd64-v3.5.1.tar.gz && cd git-lfs-3.5.1
# 安装 git lfs
sh install.sh
```

**下载大文件**

```bash
# 下载大模型
git lfs install
git clone https://huggingface.co/THUDM/chatglm3-6b-128k

# 如果下载失败尝试断点续传
# git lfs fetch --all 是获取所有分支 LFS 对象
# git lfs fetch 通常只获取当前分支的 LFS 对象就足够了
cd chatglm3-6b-128k && git lfs fetch

```

* * *

* * *

* * *

#### 切换版本

```bash
git log 查看历时提交版本`
`git reset --hard 提交版本的ID`
`git push -f -u origin 分支名
# 查看历时版本信息
mao-siyu@mao-siyu-PC:~/文档/code/dlfc-cms/dlfc-cms-api$ git log

commit 07d74082c27cfdb6fd5d7fcb46a5ce1316bf57fb
Author: mao_siyu 
Date:   Thu Apr 26 17:11:43 2018 +0800

    将sql改为本地编写

commit c97ae531a554e97dca79d962ccd6aa42db4d1b06
Author: mao_siyu 
Date:   Thu Apr 26 14:57:41 2018 +0800

    添加控制层与逻辑层代码

mao-siyu@mao-siyu-PC:~/文档/code/dlfc-cms/dlfc-cms-api$

# 切换分支
mao-siyu@mao-siyu-PC:~/文档/code/dlfc-cms/dlfc-cms-api$ git reset --hard c97ae531a554e97dca79d962ccd6aa42db4d1b06
HEAD 现在位于 c97ae53 修改service引用包

# 把修改推到远程服务器
mao-siyu@mao-siyu-PC:~/文档/code/dlfc-cms/dlfc-cms-api$ git push -f -u origin master
Username for 'http://10.32.156.113:7990': maosiyu
Password for 'http://maosiyu@10.32.156.113:7990':
Total 0 (delta 0), reused 0 (delta 0)
To http://10.32.156.113:7990/scm/dlfcsorc/dlfc-cms.git
 + 426743d...c97ae53 master -> master (forced update)
分支 master 设置为跟踪来自 origin 的远程分支 master。
mao-siyu@mao-siyu-PC:~/文档/code/dlfc-cms/dlfc-cms-api$
```

#### 创建分支

```bash
# 查看本地分支
mao-siyu@pc:/mnt/1TB/devProject/bqhx-member$ git branch
* master
# 查看本地和远程分支
mao-siyu@pc:/mnt/1TB/devProject/bqhx-member$ git branch -a
* master
  remotes/origin/HEAD -> origin/master
  remotes/origin/master
# 创建新的分支 命名 member_0.2
mao-siyu@pc:/mnt/1TB/devProject/bqhx-member$ git branch member_0.2
# 创建新的远程分支 并将本地代码提交到新的远程分支
mao-siyu@pc:/mnt/1TB/devProject/bqhx-member$ git push origin member_0.2
Total 0 (delta 0), reused 0 (delta 0)
To 192.168.1.100:/home/library/bqhx-member.git
 * [new branch]      member_0.2 -> member_0.2
# 查看本地分支
mao-siyu@pc:/mnt/1TB/devProject/bqhx-member$ git branch
* master
  member_0.2
# 查看本地和远程分支
mao-siyu@pc:/mnt/1TB/devProject/bqhx-member$ git branch -a
* master
  member_0.2
  remotes/origin/HEAD -> origin/master
  remotes/origin/master
  remotes/origin/member_0.2
mao-siyu@pc:/mnt/1TB/devProject/bqhx-member$
```

#### 切换分支

```
切换本地分支 git checkout 本地分支名
```

##### git checkout 适用场景

```bash
# 查看本地分支与远程分支
mao-siyu@pc:/mnt/1TB/devProject/bqhx-member$ git branch -a
* master
  member_0.2
  remotes/origin/HEAD -> origin/master
  remotes/origin/master
  remotes/origin/member_0.2
# 切换本地分支
mao-siyu@pc:/mnt/1TB/devProject/bqhx-member$ git checkout member_0.2
切换到分支 'member_0.2'
# 查看本地分支与远程分支
mao-siyu@pc:/mnt/1TB/devProject/bqhx-member$ git branch -a
  master
* member_0.2
  remotes/origin/HEAD -> origin/master
  remotes/origin/master
  remotes/origin/member_0.2
mao-siyu@pc:/mnt/1TB/devProject/bqhx-member$

# 建立远程跟踪(新创建的分支, 首次提交数据需要这一步)
mao-siyu@pc:/mnt/1TB/devProject/bqhx-member$ git status
位于分支 member_0.2
尚未暂存以备提交的变更：
  （使用 "git add <文件>..." 更新要提交的内容）
  （使用 "git checkout -- <文件>..." 丢弃工作区的改动）

        修改：     assets/network.js

修改尚未加入提交（使用 "git add" 和/或 "git commit -a"）
mao-siyu@pc:/mnt/1TB/devProject/bqhx-member$ git add .
mao-siyu@pc:/mnt/1TB/devProject/bqhx-member$ git commit -m 'modify ip port'
[member_0.2 52c64db] modify ip port
 1 file changed, 2 insertions(+), 2 deletions(-)
mao-siyu@pc:/mnt/1TB/devProject/bqhx-member$ git status
位于分支 member_0.2
无文件要提交，干净的工作区
mao-siyu@pc:/mnt/1TB/devProject/bqhx-member$ git push
fatal: 当前分支 member_0.2 没有对应的上游分支。
为推送当前分支并建立与远程上游的跟踪，使用

    git push --set-upstream origin member_0.2

mao-siyu@pc:/mnt/1TB/devProject/bqhx-member$ git push --set-upstream origin member_0.2
mao_siyu@192.168.1.100's password:
对象计数中: 4, 完成.
Delta compression using up to 8 threads.
压缩对象中: 100% (4/4), 完成.
写入对象中: 100% (4/4), 368 bytes | 368.00 KiB/s, 完成.
Total 4 (delta 3), reused 0 (delta 0)
To 192.168.1.100:/home/library/bqhx-member.git
   cf32128..52c64db  member_0.2 -> member_0.2
分支 'member_0.2' 设置为跟踪来自 'origin' 的远程分支 'member_0.2'。
mao-siyu@pc:/mnt/1TB/devProject/bqhx-member$
```

```
下载远程分支 并在本地创建新的分支 git checkout -b 本地分支名 origin/远程分支名
```

##### git checkout -b 适用场景

```bash
# 查看本地分支与远程分支
mao-siyu@pc:/mnt/1TB/devProject/bqhx-member/bqhx-member-manage$ git branch -a
* master
  remotes/origin/HEAD -> origin/master
  remotes/origin/master
  remotes/origin/member_1
# 从远程拉取一个新分支 并在本地创建一个新分支
mao-siyu@pc:/mnt/1TB/devProject/bqhx-member/bqhx-member-manage$ git checkout -b member_1 origin/member_1
分支 'member_1' 设置为跟踪来自 'origin' 的远程分支 'member_1'。
切换到一个新分支 'member_1'
mao-siyu@pc:/mnt/1TB/devProject/bqhx-member/bqhx-member-manage$ git branch -a
  master
* member_1
  remotes/origin/HEAD -> origin/master
  remotes/origin/master
  remotes/origin/member_1
mao-siyu@pc:/mnt/1TB/devProject/bqhx-member/bqhx-member-manage$
```

#### 删除分支

```bash
# 查看
mao-siyu@pc:/mnt/1TB/devProject/bqhx-member$ git branch -a
* master
  member_0.2
  remotes/origin/HEAD -> origin/master
  remotes/origin/master
  remotes/origin/member_0.2
# 删除本地分支
mao-siyu@pc:/mnt/1TB/devProject/bqhx-member$ git branch -d member_0.2
error: 分支 'member_0.2' 没有完全合并。
如果您确认要删除它，执行 'git branch -D member_0.2'。
# 强制删除本地分支
mao-siyu@pc:/mnt/1TB/devProject/bqhx-member$ git branch -D member_0.2
已删除分支 member_0.2（曾为 938ff53）。
mao-siyu@pc:/mnt/1TB/devProject/bqhx-member$ git branch -a
* master
  remotes/origin/HEAD -> origin/master
  remotes/origin/master
  remotes/origin/member_0.2

# 删除远程分支 索引
mao-siyu@pc:/mnt/1TB/devProject/bqhx-member$ git branch -r -d origin/member_0.2
已删除远程跟踪分支 origin/member_0.2（曾为 ce7cd19）。
# 删除远程分支
mao-siyu@pc:/mnt/1TB/devProject/bqhx-member$ git push origin :member_0.2
mao-siyu@pc:/mnt/1TB/devProject/bqhx-member$ git branch -a
* master
  remotes/origin/HEAD -> origin/master
  remotes/origin/master
mao-siyu@pc:/mnt/1TB/devProject/bqhx-member$
```

# 将分支合并到 master

```bash
# 切换到主分支
mao-siyu@pc:/mnt/1TB/devProject/bqhx-member$ git checkout master
切换到分支 'master'
您的分支与上游分支 'origin/master' 一致。
# 查看
mao-siyu@pc:/mnt/1TB/devProject/bqhx-member$ git branch -a
* master
  member_0.2
  remotes/origin/HEAD -> origin/master
  remotes/origin/master
  remotes/origin/member_0.2
# 将分支合并到 master
mao-siyu@pc:/mnt/1TB/devProject/bqhx-member$ git merge member_0.2
更新 cf32128..2d4e333
Fast-forward
 assets/network.js        |   4 +--
 components/Heads.vue     |  25 +++++++++++++----
 components/MenuSlide.vue |  20 +++++++------
 nuxt.config.js           |   2 +-
 pages/adminEdit.vue      |  13 +++++----
 pages/adminList.vue      |   1 +
 pages/createPlate.vue    |   6 ++--
 pages/createStore.vue    |  17 ++++++------
 pages/editPassword.vue   |   2 +-
 pages/levelList.vue      |   6 ++--
 pages/mEdit.vue          |   2 +-
 pages/mbrList.vue        |   6 +++-
 pages/minsert.vue        |   2 +-
 pages/personalInfo.vue   |  81 +++++++++++++++++++++++++++++++++++++++++++++++++++++
 pages/plateEdit.vue      | 100 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 pages/plateList.vue      |  66 ++-----------------------------------------
 pages/storeEdit.vue      | 194 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 pages/storeList.vue      | 134 ++++++----------------------------------------------------------------------------------
 static/boqi.ico          | Bin 0 -> 1082 bytes
 static/favicon.ico       | Bin 1150 -> 0 bytes
 static/images/1.png      | Bin 143681 -> 0 bytes
 static/images/person.png | Bin 0 -> 1547 bytes
 22 files changed, 451 insertions(+), 230 deletions(-)
 create mode 100644 pages/personalInfo.vue
 create mode 100644 pages/plateEdit.vue
 create mode 100644 pages/storeEdit.vue
 create mode 100644 static/boqi.ico
 delete mode 100644 static/favicon.ico
 delete mode 100644 static/images/1.png
 create mode 100644 static/images/person.png
mao-siyu@pc:/mnt/1TB/devProject/bqhx-member$
```
