---
title: '安装 Jupyter'
date: '2023-10-27T06:59:33+00:00'
status: private
permalink: /2023/10/27/%e5%ae%89%e8%a3%85-jupyter
author: 毛巳煜
excerpt: ''
type: post
id: 10418
category:
    - Python
tag: []
post_format: []
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
hestia_layout_select:
    - sidebar-right
---
**[安装conda](http://www.dev-share.top/2023/10/26/%e5%ae%89%e8%a3%85miniconda/ "安装conda")**
-----------------------------------------------------------------------------------------

- - - - - -

- **[官方网站](https://jupyter.org/install "官方网站")**
- 创建工作环境
  
  ```bash
  (base) [cloud@gpuServer1 (15:17:54) ~]
  └─# conda create -n worker_env python=3.10
  
  
  ```
- 激活环境 ```bash
  (base) [cloud@gpuServer1 (15:17:54) ~]
  └─# conda activate worker_env
  
  
  ```
- 安装jupyter ```bash
  # 如果期望指定安装源请使用 `-c conda-forge`
  (worker_env) [cloud@gpuServer1 (15:17:54) ~]
  └─# conda install jupyterlab -c conda-forge
  
  
  ```
- 汉化语言包(可选) ```bash
  (worker_env) [cloud@gpuServer1 (15:17:54) ~]
  └─# conda install jupyterlab-language-pack-zh-cn -c conda-forge
  
  ```
- 设置密码(新开一个shell) ```bash
  (worker_env) [cloud@gpuServer1 (15:17:54) ~]
  └─# jupyter server password
  
  ```
- 测试启动jupyter ```bash
  (worker_env) [cloud@gpuServer1 (15:17:54) ~]
  └─$ jupyter lab --ip 192.168.101.65
  
  ## 如果是(root用户)
  (worker_env) [cloud@gpuServer1 (15:17:54) ~]
  └─# jupyter lab --ip 192.168.101.65 --allow-root
  
  
  ```
  
  ![](http://qiniu.dev-share.top/image/LLM/LangChain01.png)
  
  ![](http://qiniu.dev-share.top/image/LLM/LangChain02.png)