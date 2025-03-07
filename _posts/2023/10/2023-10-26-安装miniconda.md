---
title: "安装miniconda"
date: "2023-10-26"
categories: 
  - "python"
---

# Ubuntu/CentOS 安装conda

下载指定版本： https://repo.anaconda.com/miniconda/

下载最新版本： https://docs.conda.io/projects/miniconda/en/latest/

- ```bash
    mkdir -p ~/miniconda3
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
    bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
    rm -rf ~/miniconda3/miniconda.sh
    ```
    
- 或 使用七牛云下载
- ```bash
    ## 使用七牛云下载
    ### 安装到指定目录
    mkdir -p /data/miniconda3
    wget http://qiniu.dev-share.top/file/Miniconda3-py311_23.9.0-0-Linux-x86_64.sh -O /data/miniconda3/miniconda.sh
    bash /data/miniconda3/miniconda.sh -b -u -p /data/miniconda3
    rm -rf /data/miniconda3/miniconda.sh
    ```
    
    安装后，初始化新安装的 Miniconda。以下命令针对 bash 和 zsh shell 进行初始化：
    
- ```bash
    /data/miniconda3/bin/conda init bash
    /data/miniconda3/bin/conda init zsh
    ```
    
- **`重启终端`**
    

* * *

* * *

* * *

# 树莓派4b安装conda

> 因为我是64位的，所以我选择Linux-aarch64版本的下载： `注意`：目前大于4.9版本的miniconda不适配树莓派arm64架构操作系统，安装后无法正常使用！

- ```bash
    mkdir -p ~/miniconda3
    wget https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/Miniconda3-py37_4.9.2-Linux-aarch64.sh -O ~/miniconda3/miniconda.sh
    bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
    rm -rf ~/miniconda3/miniconda.sh
    ```
    

> 安装并激活环境

- ```bash
    ~/miniconda3/bin/conda init bash
    ~/miniconda3/bin/conda init zsh
    ```
    
    **`重启终端`**
    
    查看版本
    
- ```bash
    (base) siyu.mao@raspberrypi:~ $ conda -V
    conda 4.9.2
    ```
    

* * *

* * *

* * *

## 常用命令

- 创建环境
    
    ```bash
    conda create -n [你的环境名]
    ```
    
- 环境克隆
    
    ```bash
    conda create -n [你的环境名] --clone [已存在的环境名]
    ```
    
- 激活环境
    
    ```bash
    conda activate [你的环境名]
    ```
    
- 删除环境
    
    ```bash
    conda env remove -n [你的环境名]
    ```
    
- 查看下载源
    
    ```bash
    conda config --show channels
    ```
    
- 添加源
    
    ```bash
    conda config --add channels [源地址]
    ```
    
- 删除源
    
    ```bash
    conda config --remove channels [源地址]
    ```
    

* * *

* * *

* * *

### 检查环境安装的是否正确

```bash
## 查看默认环境
(base) [cloud@gpuServer1 (16:07:10) ~]
└─$ conda env list
# conda environments:
#
                         /data/oobabooga_linux/installer_files/conda
                         /data/oobabooga_linux/installer_files/env
base                  *  /home/cloud/miniconda3

## 查看pip所在的位置
(base) [cloud@gpuServer1 (16:07:19) ~]
└─$ which pip
/home/cloud/miniconda3/bin/pip                          ## 正确的路径




## 创建一个新环境
(base) [cloud@gpuServer1 (15:52:02) ~]
└─$ conda create -n LangChainLLM-POC python==3.10
## 查看
(base) [cloud@gpuServer1 (16:07:10) ~]
└─$ conda env list
# conda environments:
#
                         /data/oobabooga_linux/installer_files/conda
                         /data/oobabooga_linux/installer_files/env
base                  *  /home/cloud/miniconda3
LangChainLLM-POC         /home/cloud/miniconda3/envs/LangChainLLM-POC




## 切换环境
(base) [cloud@gpuServer1 (16:07:28) ~]
└─$ conda activate LangChainLLM-POC
## 查看pip所在的位置
(LangChainLLM-POC) [cloud@gpuServer1 (16:07:35) ~]
└─$ which pip
/home/cloud/miniconda3/envs/LangChainLLM-POC/bin/pip     ## 正确的路径

```

#### **可能出现的`问题`**

```bash
(base) [cloud@gpuServer1 (16:01:01) ~]
└─$ which pip
/home/cloud/.local/bin/pip

## 或

(LangChainLLM-POC) [cloud@gpuServer1 (16:01:01) ~]
└─$ which pip
/home/cloud/.local/bin/pip

(LangChainLLM-POC) [cloud@gpuServer1 (16:23:04) ~]
└─$ pip -V
pip 23.2.1 from /home/cloud/.local/lib/python3.10/site-packages/pip (python 3.10)

```

#### **解决办法**

> 删除用户本地的 `pip`

```bash
## 针对不同的空间删除不同的pip
(base) [cloud@gpuServer1 (16:01:01) ~]
└─$ mv /home/cloud/.local/bin/pip /home/cloud/.local/bin/pip_backup

## 针对不同的空间删除不同的pip
(LangChainLLM-POC) [cloud@gpuServer1 (16:23:04) ~]
└─$ rm -rf /home/cloud/.local/lib/python3.10/site-packages/pip

```

* * *

* * *

* * *

# 配置nexus代理服务器

```bash
## 添加代理服务器地址
##  --override-channels 只使用代理源，不使用其它源
conda create -n vllm-0.2.2 python==3.10.12 -c http://172.16.21.146:8081/repository/anaconda-proxy/main --override-channels

```

* * *

* * *

* * *

# Conda 环境迁移

## 常用命令

```bash
# 显示环境目录
conda config --show   envs_dirs
conda config --append envs_dirs /data/anaconda3/envs/
conda config --remove envs_dirs /data/anaconda3/envs/

# 显示环境根目录前缀
conda config --show root_prefix
conda config --set  root_prefix /home/cloud/anaconda3
```

## 原环境

```bash
(base) [cloud@AI (09:54:48) ~]
└─$ conda env list
# conda environments:
#
base                  *  /home/cloud/anaconda3
ai-0x01                  /home/cloud/anaconda3/envs/ai-0x01


# 查看环境前缀
(base) [cloud@AI (09:59:13) ~]
└─$ conda config --show root_prefix
root_prefix: /home/cloud/anaconda3

```

## 切换与迁移

```bash
## 切换环境目录
conda config --set  root_prefix /data/anaconda3


## 切换环境
(base) [cloud@AI (10:00:33) ~]
└─$ conda env list
# conda environments:
#
base                  *  /data/anaconda3
                         /home/cloud/anaconda3
                         /home/cloud/anaconda3/envs/ai-0x01


## 查看环境目录
(base) [cloud@AI (10:14:53) ~]
└─$ conda config --show   envs_dirs
envs_dirs:
  - /data/anaconda3/envs      # 第一行的是默认环境目录
  - /home/cloud/.conda/envs


## 迁移
(base) [cloud@AI (10:03:26) ~]
└─$ conda create -n ai-0x01 --clone /home/cloud/anaconda3/envs/ai-0x01



## 查看
(base) [cloud@AI (10:15:45) ~]
└─$ conda env list
# conda environments:
#
base                  *  /data/anaconda3                         # 注意这只改变了默认的下载目录
ai-0x01                  /data/anaconda3/envs/ai-0x01
                         /home/cloud/anaconda3                   # conda的源文件还在这里，要想改变根目录，需要重新安装conda并在安装时指定安装目录
                         /home/cloud/anaconda3/envs/ai-0x01

```
