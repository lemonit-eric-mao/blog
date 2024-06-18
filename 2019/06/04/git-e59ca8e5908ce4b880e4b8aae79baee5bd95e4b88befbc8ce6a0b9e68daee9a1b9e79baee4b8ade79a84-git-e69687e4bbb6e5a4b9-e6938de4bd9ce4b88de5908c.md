---
title: 'Git 在同一个目录下，根据项目中的 .git/文件夹 操作不同的项目'
date: '2019-06-04T03:12:16+00:00'
status: publish
permalink: /2019/06/04/git-%e5%9c%a8%e5%90%8c%e4%b8%80%e4%b8%aa%e7%9b%ae%e5%bd%95%e4%b8%8b%ef%bc%8c%e6%a0%b9%e6%8d%ae%e9%a1%b9%e7%9b%ae%e4%b8%ad%e7%9a%84-git-%e6%96%87%e4%bb%b6%e5%a4%b9-%e6%93%8d%e4%bd%9c%e4%b8%8d%e5%90%8c
author: 毛巳煜
excerpt: ''
type: post
id: 4736
category:
    - Git
    - Linux服务器
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
```bash
#!/bin/bash

# 使用此脚本前 需要配置 gitlab ssh免密

read -p "请输入要创建的分支名: " BRANCH_NAME

if [ ! -n "<span class="katex math inline">{BRANCH_NAME}" ];
then
  echo '分支名不能为空！'
  exit
fi

# gitlab地址
gitlab_addr="172.160.180.8"

# gitlab 组名/项目名
project_names=(
    xiaohaigui/smartpad
    xiaohaigui/new_smartpad
)

# 批量创建分支
for name in</span>{project_names[@]};
do
    # 克隆项目
    git clone git@<span class="katex math inline">{gitlab_addr}:</span>{name}.git
    # 在同一个目录下，根据项目中的 .git/文件夹 操作不同的项目
    # 创建新的分支 (使用 #*/ 截取组名后面的项目名)
    git --git-dir=<span class="katex math inline">{name#*/}/.git --work-tree=</span>{name#*/} branch <span class="katex math inline">{BRANCH_NAME}
    # 将新分支推到远程
    git --git-dir=</span>{name#*/}/.git --work-tree=<span class="katex math inline">{name#*/} push origin</span>{BRANCH_NAME}
    # 查看创建结果
    git --git-dir=<span class="katex math inline">{name#*/}/.git --work-tree=</span>{name#*/} branch -a
    echo '================'
done


```