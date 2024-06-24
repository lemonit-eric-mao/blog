---
title: "Ubuntu 安装五笔输入法"
date: "2017-11-16"
categories: 
  - "ubuntu"
---

```bash
# 第一步：缷载ibus
sudo apt remove ibus
sudo apt autoremove
# 重启ubuntu

# 第二步：安装fcitx五笔拼音
sudo apt update && \
sudo apt install fcitx && \
sudo apt install fcitx-table-wbpy

```
