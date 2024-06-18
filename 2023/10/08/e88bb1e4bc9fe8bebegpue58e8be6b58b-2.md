---
title: 英伟达GPU压测
date: '2023-10-08T08:29:19+00:00'
status: private
permalink: /2023/10/08/%e8%8b%b1%e4%bc%9f%e8%be%begpu%e5%8e%8b%e6%b5%8b-2
author: 毛巳煜
excerpt: ''
type: post
id: 10339
category:
    - C
    - 人工智能
tag: []
post_format: []
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
hestia_layout_select:
    - sidebar-right
---
前置条件
----

#### 安装 `NVIDIA GRID GPU` 驱动

```bash
(base) [cloud@New-test1 (18:18:43) /mnt/data/Nvidia]
└─<span class="katex math inline">ll
-rwxrwxrwx  1 cloud cloud  419982787 11月  6 10:12 NVIDIA-Linux-x86_64-525.125.06-grid.run*

(base) [cloud@New-test1 (18:18:44) /mnt/data/Nvidia]
└─</span> sudo ./NVIDIA-Linux-x86_64-525.125.06-grid.run


```

#### 卸载 `NVIDIA GRID GPU` 驱动

```bash
sudo ./NVIDIA-Linux-x86_64-525.125.06-grid.run --uninstall


```

- - - - - -

> [CUDA](https://www.nvidia.cn/geforce/technologies/cuda/technology/ "CUDA") 是 NVIDIA 发明的一种并行计算平台和编程模型。  
>  因此要先安装CUDA才能进行编程  
>  [NVIDIA 计算能力对照表](https://developer.nvidia.com/cuda-gpus "NVIDIA 计算能力对照表")

#### 安装CUDA

```bash
(base) [cloud@New-test1 (18:24:01) /mnt/data/Nvidia/CUDA]
└─<span class="katex math inline">ll
-rwxrwxrwx 1 root  root  4207617207  1月 28  2023 cuda_12.0.1_525.85.12_linux.run*
-rwxrwxrwx 1 cloud cloud 4245586997  2月 23  2023 cuda_12.1.0_530.30.02_linux.run*
-rwxrwxrwx 1 cloud cloud 4360403711 10月 16 14:54 cuda_12.3.0_545.23.06_linux.run*


(base) [cloud@New-test1 (18:24:02) /mnt/data/Nvidia/CUDA]
└─</span> sudo ./cuda_12.1.0_530.30.02_linux.run

┌──────────────────────────────────────────────────────────────────────────────┐
│  End User License Agreement                                                  │
│  --------------------------                                                  │
│                                                                              │
│  NVIDIA Software License Agreement and CUDA Supplement to                    │
│  Software License Agreement. Last updated: October 8, 2021                   │
│                                                                              │
│  The CUDA Toolkit End User License Agreement applies to the                  │
│  NVIDIA CUDA Toolkit, the NVIDIA CUDA Samples, the NVIDIA                    │
│  Display Driver, NVIDIA Nsight tools (Visual Studio Edition),                │
│  and the associated documentation on CUDA APIs, programming                  │
│  model and development tools. If you do not agree with the                   │
│  terms and conditions of the license agreement, then do not                  │
│  download or use the software.                                               │
│                                                                              │
│  Last updated: October 8, 2021.                                              │
│                                                                              │
│                                                                              │
│  Preface                                                                     │
│  -------                                                                     │
│                                                                              │
│──────────────────────────────────────────────────────────────────────────────│
│ Do you accept the above EULA? (accept/decline/quit):                         │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
# 输入：accept

# 下一步
┌──────────────────────────────────────────────────────────────────────────────┐
│ CUDA Installer                                                               │
│# - [X] Driver                                                                │
│#      [X] 530.30.02                                                          │
│ - [ ] Driver                                                                 │
│      [ ] 530.30.02                                                           │
│ + [X] CUDA Toolkit 12.1                                                      │
│   [X] CUDA Demo Suite 12.1                                                   │
│   [X] CUDA Documentation 12.1                                                │
│ - [ ] Kernel Objects                                                         │
│      [ ] nvidia-fs                                                           │
│   Options                                                                    │
│   Install                                                                    │
│                                                                              │
│                                                                              │
│                                                                              │
│                                                                              │
│                                                                              │
│                                                                              │
│                                                                              │
│                                                                              │
│                                                                              │
│                                                                              │
│                                                                              │
│                                                                              │
│ Up/Down: Move | Left/Right: Expand | 'Enter': Select | 'A': Advanced options │
└──────────────────────────────────────────────────────────────────────────────┘
# 不勾选默认的驱动
# 选择Install安装

===========
= Summary =
===========

Driver:   Not Selected
Toolkit:  Installed in /usr/local/cuda-12.1/

Please make sure that
 -   PATH includes /usr/local/cuda-12.1/bin
 -   LD_LIBRARY_PATH includes /usr/local/cuda-12.1/lib64, or, add /usr/local/cuda-12.1/lib64 to /etc/ld.so.conf and run ldconfig as root


## 添加环境变量
(base) [cloud@New-test1 (18:24:01) /mnt/data/Nvidia/CUDA]
└─<span class="katex math inline">vim /etc/profile

# ......
export PATH=/usr/local/cuda-12.1/bin</span>{PATH:+:<span class="katex math inline">{PATH}}
export LD_LIBRARY_PATH=/usr/local/cuda-12.1/lib64</span>{LD_LIBRARY_PATH:+:<span class="katex math inline">{LD_LIBRARY_PATH}}


## 重启终端-查看
(base) [cloud@New-test1 (18:40:07) ~]
└─</span> nvcc -V
nvcc: NVIDIA (R) Cuda compiler driver
Copyright (c) 2005-2023 NVIDIA Corporation
Built on Tue_Feb__7_19:32:13_PST_2023
Cuda compilation tools, release 12.1, V12.1.66
Build cuda_12.1.r12.1/compiler.32415258_0



```

#### 卸载CUDA

```bash
(base) [cloud@New-test1 (18:41:09) /usr/local/cuda-12.1/bin]
└─<span class="katex math inline">ll | grep uninstall
-rwxr-xr-x  1 root root  1046898 11月 24 18:31 cuda-uninstaller*


## 执行卸载
(base) [cloud@New-test1 (18:41:19) /usr/local/cuda-12.1/bin]
└─</span> sudo ./cuda-uninstaller

┌──────────────────────────────────────────────────────────────────────────────┐
│ CUDA Uninstaller                                                             │
│   [ ] CUDA_Demo_Suite_12.1                                                   │
│   [ ] CUDA_Toolkit_12.1                                                      │
│   [ ] CUDA_Documentation_12.1                                                │
│   Done                                                                       │
│                                                                              │
│                                                                              │
│                                                                              │
│                                                                              │
│                                                                              │
│                                                                              │
│                                                                              │
│                                                                              │
│                                                                              │
│                                                                              │
│                                                                              │
│                                                                              │
│                                                                              │
│                                                                              │
│                                                                              │
│                                                                              │
│                                                                              │
│ Up/Down: Move | 'Enter': Select                                              │
└──────────────────────────────────────────────────────────────────────────────┘


```

- - - - - -

- - - - - -

- - - - - -

GPU信息
-----

```bash
test2:~$ nvidia-smi
Sun Oct  8 16:29:42 2023
+---------------------------------------------------------------------------------------+
| NVIDIA-SMI 530.30.02              Driver Version: 530.30.02    CUDA Version: 12.1     |
|-----------------------------------------+----------------------+----------------------+
| GPU  Name                  Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf            Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|                                         |                      |               MIG M. |
|=========================================+======================+======================|
|   0  NVIDIA A100 80GB PCIe           On | 00000000:0B:00.0 Off |                    0 |
| N/A   42C    P0               44W / 300W|      5MiB / 81920MiB |      0%      Default |
|                                         |                      |             Disabled |
+-----------------------------------------+----------------------+----------------------+
|   1  NVIDIA A100 80GB PCIe           On | 00000000:14:00.0 Off |                    0 |
| N/A   38C    P0               46W / 300W|      5MiB / 81920MiB |      0%      Default |
|                                         |                      |             Disabled |
+-----------------------------------------+----------------------+----------------------+

+---------------------------------------------------------------------------------------+
| Processes:                                                                            |
|  GPU   GI   CI        PID   Type   Process name                            GPU Memory |
|        ID   ID                                                             Usage      |
|=======================================================================================|
|    0   N/A  N/A      4536      G   /usr/lib/xorg/Xorg                            4MiB |
|    1   N/A  N/A      4536      G   /usr/lib/xorg/Xorg                            4MiB |
+---------------------------------------------------------------------------------------+


```

- - - - - -

编写测试程序，`vector_add.cu`
----------------------

```cpp
#include <iostream>
#include <cuda_runtime.h>
#include <chrono>
#include <cstdlib>

__global__ void vectorAdd(float *a, float *b, float *c, int numElements) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i  <device_index>" = numDevices) {
        std::cerr >>(d_a, d_b, d_c, numElements);
        cudaDeviceSynchronize();

        auto end_time = std::chrono::high_resolution_clock::now();
        auto duration = std::chrono::duration_cast<:chrono::seconds>(end_time - start_time);

        if (duration.count() >= duration_seconds) {
            break;
        }
    }

    std::cout </:chrono::seconds></device_index></cstdlib></chrono></cuda_runtime.h></iostream>
```

#### 编译执行

```bash
nvcc -o vector_add vector_add.cu

## ./vector_add  
./vector_add 60 0

```

- - - - - -

### **查看效果**

```bash
test2:~$ nvidia-smi
Sun Oct  8 16:27:05 2023
+---------------------------------------------------------------------------------------+
| NVIDIA-SMI 530.30.02              Driver Version: 530.30.02    CUDA Version: 12.1     |
|-----------------------------------------+----------------------+----------------------+
| GPU  Name                  Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf            Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|                                         |                      |               MIG M. |
|=========================================+======================+======================|
|   0  NVIDIA A100 80GB PCIe           On | 00000000:0B:00.0 Off |                    0 |
| N/A   46C    P0               71W / 300W|    423MiB / 81920MiB |     38%      Default |
|                                         |                      |             Disabled |
+-----------------------------------------+----------------------+----------------------+
|   1  NVIDIA A100 80GB PCIe           On | 00000000:14:00.0 Off |                    0 |
| N/A   41C    P0               46W / 300W|      7MiB / 81920MiB |      0%      Default |
|                                         |                      |             Disabled |
+-----------------------------------------+----------------------+----------------------+

+---------------------------------------------------------------------------------------+
| Processes:                                                                            |
|  GPU   GI   CI        PID   Type   Process name                            GPU Memory |
|        ID   ID                                                             Usage      |
|=======================================================================================|
|    0   N/A  N/A      4536      G   /usr/lib/xorg/Xorg                            4MiB |
|    0   N/A  N/A    650154      C   ./vector_add                                416MiB |
|    1   N/A  N/A      4536      G   /usr/lib/xorg/Xorg                            4MiB |
+---------------------------------------------------------------------------------------+


```

- - - - - -