---
title: "Git 在同一个目录下，根据项目中的 .git/文件夹 操作不同的项目"
date: "2019-06-04"
categories: 
  - "git"
  - "linux服务器"
---

```bash
#!/bin/bash

# 使用此脚本前 需要配置 gitlab ssh免密

read -p "请输入要创建的分支名: " BRANCH_NAME

if [ ! -n "${BRANCH_NAME}" ];
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
for name in ${project_names[@]};
do
    # 克隆项目
    git clone git@${gitlab_addr}:${name}.git
    # 在同一个目录下，根据项目中的 .git/文件夹 操作不同的项目
    # 创建新的分支 (使用 #*/ 截取组名后面的项目名)
    git --git-dir=${name#*/}/.git --work-tree=${name#*/} branch ${BRANCH_NAME}
    # 将新分支推到远程
    git --git-dir=${name#*/}/.git --work-tree=${name#*/} push origin ${BRANCH_NAME}
    # 查看创建结果
    git --git-dir=${name#*/}/.git --work-tree=${name#*/} branch -a
    echo '================'
done

```
