---
title: 基于Langchain-Chatchat的大模型POC
date: '2023-10-11T05:59:41+00:00'
status: private
permalink: /2023/10/11/%e5%9f%ba%e4%ba%8elangchain-chatchat%e7%9a%84%e5%a4%a7%e6%a8%a1%e5%9e%8bpoc
author: 毛巳煜
excerpt: ''
type: post
id: 10346
category:
    - 人工智能
tag: []
post_format: []
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
hestia_layout_select:
    - sidebar-right
---
基于Langchain-Chatchat的大模型POC
===========================

[环境最低要求](https://github.com/chatchat-space/Langchain-Chatchat/tree/v0.2.5#%E7%8E%AF%E5%A2%83%E6%9C%80%E4%BD%8E%E8%A6%81%E6%B1%82)
---------------------------------------------------------------------------------------------------------------------------------

> - Python版本: &gt;= 3.8.5,
> - Cuda版本: &gt;= 11.7, 且能顺利安装Python

**[安装conda](http://www.dev-share.top/2023/10/26/%e5%ae%89%e8%a3%85miniconda/ "安装conda")**
-----------------------------------------------------------------------------------------

```bash
wget https://mirrors.bfsu.edu.cn/anaconda/archive/Anaconda3-2022.10-Linux-x86_64.sh --no-check-certificate | sudo bash


```

安装 git-lfs
==========

Ubuntu 20.x
-----------

```bash
# 1.添加packagecloud仓库
> curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash

# 2. 安装软件包
> sudo apt-get install git-lfs

# 3. 验证
> git lfs -v
git-lfs/3.4.0 (GitHub; linux amd64; go 1.20.6)

# 4. 开启lfs功能
> git lfs install
Git LFS initialized.


```

配置加速器（可选）建议使用VPN这样问题会少很多，这个下载器有可能丢文件
------------------------------------

> 加速器网站：https://aliendao.cn/

### 下载gpt2

```bash
git lfs install
git clone https://huggingface.co/gpt2

```

### 下载m3e-base

```bash
git lfs install
git clone https://huggingface.co/moka-ai/m3e-base

```

### 下载chatglm2-6b

```bash
git lfs install
git clone https://huggingface.co/THUDM/chatglm2-6b

```

- - - - - -

安装
==

ChatChat-0.2.8
==============

1. 创建conda环境 ```bash
  conda create -y -n 0.2.8 python==3.10.12 -c http://172.16.21.146:8081/repository/anaconda-proxy/main --override-channels
  
  
  conda activate 0.2.8
  
  
  ```
2. 下载必要依赖 ```bash
  (0.2.8) [root@AI (13:57:24) /data/0.2.8-Langchain-Chatchat]
  └─$ pip install -i http://172.16.21.146:8081/repository/pypi/simple  --trusted-host 172.16.21.146 --timeout 0 -r ./requirements.txt
  
  ```
3. 修改`vllm`和`fastchat`的源码，让`vllm`适配 `chatglm3-6b-32k`
  1. fastchat源码
  
  ```bash
  (0.2.8) [root@AI (15:31:01) ~]
  └─# pip show fschat
  
  Name: fschat
  Version: 0.2.33
  Summary: An open platform for training, serving, and evaluating large language model based chatbots.
  Home-page:
  Author:
  Author-email:
  License:
  Location: /root/anaconda3/envs/0.2.8/lib/python3.10/site-packages
  Requires: aiohttp, fastapi, httpx, markdown2, nh3, numpy, prompt-toolkit, pydantic, requests, rich, shortuuid, tiktoken, uvicorn
  Required-by:
  
  
  
  (0.2.8) [root@AI (13:57:24) /data/0.2.8-Langchain-Chatchat]
  └─$ vim vim /root/anaconda3/envs/0.2.8/lib/python3.10/site-packages/fastchat/serve/vllm_worker.py
  
  # 103行
  :103
  
  sampling_params = SamplingParams(
             n=1,
             temperature=temperature,
             top_p=top_p,
             use_beam_search=use_beam_search,
             #stop=list(stop),
             stop=[i for i in stop if i != ""], # 修改此处
             max_tokens=max_new_tokens,
             top_k=top_k,
             presence_penalty=presence_penalty,
             frequency_penalty=frequency_penalty,
             best_of=best_of,
         )
  
  
  ```
4. 基于`L40`的GPU参数调整`ChatChat`的`startup.py` vllm参数 ```python
  # 预留embedding空间，调大增加推理速度，过大会内存溢出
  args.gpu_memory_utilization = 0.90
  # worker并发数，调大增加并行处理速度，过大会导致程序变慢
  #args.limit_worker_concurrency = 5
  args.limit_worker_concurrency = 100
  # vllm worker的切分是tensor并行，这里填写显卡的数量
  args.num_gpus = 1
  
  ```
5. 基于`A100`的GPU参数调整`ChatChat`的`startup.py` vllm参数 ```python
  args.max_num_batched_tokens = None       # (默认：None) 一个批次中的最大令牌（tokens）数量，这个取决于你的显卡和大模型设置，设置太大显存会不够
  args.max_num_seqs = 512                  # (默认：256) 每次迭代的最大序列数量
  args.max_paddings = 256                  # (默认：256) 一个批次中的最大填充数量
  args.gpu_memory_utilization = 0.95       # (默认：0.90) GPU内存利用率，经过实际测试，设置为0.95更合适，要给知识库查询预留一些显存
  args.limit_worker_concurrency = 300      # (默认：5) 经过实际测试，无论单卡还是多卡，大于300或小于300推理速度都会变慢，只有300最合适
  args.num_gpus = 1                        # (默认：1) vllm worker的切分是tensor并行，这里填写显卡的数量；【可改为单机GPU卡数量】
  args.tensor_parallel_size = 1            # (默认：1) 张量并行大小；【与GPU卡数量相同】
  args.worker_use_ray = False              # (默认：False) 是否使用Ray作为worker
  
  ```
6. 修改配置文件

- 创建新的配置文件
  
  ```python
  (0.2.8) [root@AI (14:50:15) /data/0.2.8-Langchain-Chatchat]
  └─# python copy_config_example.py
  
  ```
- 修改数据库配置`vim configs/kb_config.py````python
  # 默认向量库/全文检索引擎类型。可选：faiss, milvus(离线) & zilliz(在线), pgvector,全文检索引擎es
  #DEFAULT_VS_TYPE = "faiss"
  DEFAULT_VS_TYPE = "milvus"
  
  # ......
  
  # 可选向量库类型及对应配置
  kbs_config = {
     "faiss": {
     },
     "milvus": {                               # 在这里修改milvus向量数据库配置
         "host": "127.0.0.1",
         "port": "19530",
         "user": "",
         "password": "",
         "secure": False,
     },
  
  # ......
  
  }
  
  
  ```
- 修改模型配置`vim configs/model_config.py````python
  import os
  
  # 可以指定一个绝对路径，统一存放所有的Embedding和LLM模型。
  # 每个模型可以是一个单独的目录，也可以是某个目录下的二级子目录。
  # 如果模型目录名称和 MODEL_PATH 中的 key 或 value 相同，程序会自动检测加载，无需修改 MODEL_PATH 中的路径。
  MODEL_ROOT_PATH = "/data/LLM"
  
  # 选用的 Embedding 名称
  EMBEDDING_MODEL = "bge-base-zh-v1.5"
  
  # Embedding 模型运行设备。设为"auto"会自动检测，也可手动设定为"cuda","mps","cpu"其中之一。
  EMBEDDING_DEVICE = "cuda"
  
  # ......
  
  
  # 要运行的 LLM 名称，可以包括本地模型和在线模型。列表中本地模型将在启动项目时全部加载。
  # 列表中第一个模型将作为 API 和 WEBUI 的默认模型。
  # 在这里，我们使用目前主流的两个离线模型，其中，chatglm3-6b 为默认加载模型。
  # 如果你的显存不足，可使用 Qwen-1_8B-Chat, 该模型 FP16 仅需 3.8G显存。
  #LLM_MODELS = ["chatglm3-6b", "zhipu-api", "openai-api"] # "Qwen-1_8B-Chat",
  LLM_MODELS = ["chatglm3-6b-32k"]
  
  # AgentLM模型的名称 (可以不指定，指定之后就锁定进入Agent之后的Chain的模型，不指定就是LLM_MODELS[0])
  Agent_MODEL = None
  
  # LLM 运行设备。设为"auto"会自动检测，也可手动设定为"cuda","mps","cpu"其中之一。
  LLM_DEVICE = "cuda"
  
  # ......
  
  # 在以下字典中修改属性值，以指定本地embedding模型存储位置。支持3种设置方法：
  # 1、将对应的值修改为模型绝对路径
  # 2、不修改此处的值（以 text2vec 为例）：
  #       2.1 如果{MODEL_ROOT_PATH}下存在如下任一子目录：
  #           - text2vec
  #           - GanymedeNil/text2vec-large-chinese
  #           - text2vec-large-chinese
  #       2.2 如果以上本地路径不存在，则使用huggingface模型
  MODEL_PATH = {
     "embed_model": {
         # ......
         "m3e-base": "moka-ai/m3e-base",
         "bge-large-zh": "BAAI/bge-large-zh",
         "bge-large-zh-v1.5": "BAAI/bge-large-zh-v1.5",
         # ......
     },
  
     "llm_model": {
         # ......
         "chatglm3-6b": "THUDM/chatglm3-6b",
         "chatglm3-6b-32k": "THUDM/chatglm3-6b-32k",
         "chatglm3-6b-base": "THUDM/chatglm3-6b-base",
         # ......
     }
  }
  
  
  VLLM_MODEL_DICT = {
     # ......
     "chatglm3-6b": "THUDM/chatglm3-6b",
     "chatglm3-6b-32k": "THUDM/chatglm3-6b-32k",
     # ......
  }
  
  
  ```
- 修改模型配置`vim configs/server_config.py````python
  # 各服务器默认绑定host。如改为"0.0.0.0"需要修改下方所有XX_SERVER的host
  # DEFAULT_BIND_HOST = "0.0.0.0" if sys.platform != "win32" else "127.0.0.1"
  DEFAULT_BIND_HOST = "172.198.11.13" if sys.platform != "win32" else "127.0.0.1"
  
  
  # fastchat model_worker server
  # 这些模型必须是在model_config.MODEL_PATH或ONLINE_MODEL中正确配置的。
  # 在启动startup.py时，可用通过`--model-name xxxx yyyy`指定模型，不指定则为LLM_MODELS
  FSCHAT_MODEL_WORKERS = {
     # 所有模型共用的默认配置，可在模型专项配置中进行覆盖。
     "default": {
         "host": DEFAULT_BIND_HOST,
         "port": 20002,
         "device": LLM_DEVICE,
         # False,'vllm',使用的推理加速框架,使用vllm如果出现HuggingFace通信问题，参见doc/FAQ
         # vllm对一些模型支持还不成熟，暂时默认关闭
         # fschat=0.2.33的代码有bug, 如需使用，源码修改fastchat.server.vllm_worker，
         # 将103行中sampling_params = SamplingParams的参数stop=list(stop)修改为stop= [i for i in stop if i!=""]
         #"infer_turbo": False,
         # 开启vllm加速
         "infer_turbo": "vllm",
  
  
         # ===========================以下暂时仅供参考=========================================================
  
         # model_worker多卡加载需要配置的参数
         # "gpus": None, # 使用的GPU，以str的格式指定，如"0,1"，如失效请使用CUDA_VISIBLE_DEVICES="0,1"等形式指定
         "num_gpus": 1, # 使用GPU的数量
         "max_gpu_memory": "80GiB", # 每个GPU占用的最大显存，根据显卡配置调整
  
         # 以下为model_worker非常用参数，可根据需要配置
         # "load_8bit": False, # 开启8bit量化
         # "cpu_offloading": None,
         # "gptq_ckpt": None,
         # "gptq_wbits": 16,
         # "gptq_groupsize": -1,
         # "gptq_act_order": False,
         # "awq_ckpt": None,
         # "awq_wbits": 16,
         # "awq_groupsize": -1,
         # "model_names": LLM_MODELS,
         # "conv_template": None,
         # "limit_worker_concurrency": 5,
         # "stream_interval": 2,
         # "no_register": False,
         # "embed_in_truncate": False,
  
         # 以下为vllm_worker配置参数,注意使用vllm必须有gpu，仅在Linux测试通过
  
         # tokenizer = model_path # 如果tokenizer与model_path不一致在此处添加
         # 'tokenizer_mode':'auto',
         # 'trust_remote_code':True,
         # 'download_dir':None,
         # 'load_format':'auto',
         # 'dtype':'auto',
         # 'seed':0,
         'worker_use_ray': False,             # (默认：False) 是否使用Ray作为worker
         # 'pipeline_parallel_size':1,
         'tensor_parallel_size':1,            # (默认：1) 张量并行大小；【与GPU卡数量相同】
         # 'block_size':16,
         # 'swap_space':4 , # GiB
         'gpu_memory_utilization': 0.95,      # (默认：0.90) GPU内存利用率，经过实际测试，设置为0.95更合适，要给知识库查询预留一些显存
         'max_num_batched_tokens': None,      # (默认：None) 一个批次中的最大令牌（tokens）数量，这个取决于你的显卡和大模型设置，设置太大显存会不够
         'max_num_seqs': 512,                 # (默认：256) 每次迭代的最大序列数量
         # 'disable_log_stats':False,
         # 'conv_template':None,
         'limit_worker_concurrency': 300,     # (默认：5) 经过实际测试，无论单卡还是多卡，大于300或小于300推理速度都会变慢，只有300最合适
         # 'no_register':False,
         'num_gpus': 1                        # (默认：1) vllm worker的切分是tensor并行，这里填写显卡的数量；【可改为单机GPU卡数量】
         # 'engine_use_ray': False,
         # 'disable_log_requests': False
  
     },
  }
  
  ```

- - - - - -

参数配置
====

<table><thead><tr><th>**知识库**</th><th>**参数**</th><th>说明</th></tr></thead><tbody><tr><td>温度</td><td>0.1</td><td>取值范围：0.00 ~ 1.00  
数值越大，模型的思维越具有创造性  
数值越小，模型的思维会更加的专注 在使用知识库实现检索生成时，如果模型本身不是太聪明，那么将数据调小效果会更好一些，  
例如：小学生与博士，博士的回答肯定要比小学生的回答更具有参考价值，所以我们会希望博士为我们思考  
而小学生虽然没有专业的回答，但他可以为我们做阅读，信息有人来判断。

</td></tr><tr><td>历史对话轮数</td><td>0</td><td>取值范围：没限制  
模型与我们对话时，它是否要考虑我们之前说的话，要考虑多少交流的内容，就是通过这个值来设置的。</td></tr><tr><td>匹配知识条数</td><td>1</td><td>取值范围：没限制  
从向量库中检索到的信息有很多条，我们希望让模型知道有几条信息，就是通过这个值来设置的。</td></tr><tr><td>知识匹配分数阈值</td><td>1</td><td>对向量库中检索到的信息再次进行过滤，最终的结果会传给大模型。  
较高的阈值会筛选掉一些分数较低的匹配，但也可能导致信息不足</td></tr><tr><td>重复惩罚参数</td><td>1.2</td><td></td></tr></tbody></table>

<table><thead><tr><th>**大模型**</th><th>**参数**</th><th>说明</th></tr></thead><tbody><tr><td>温度</td><td>0.7</td><td></td></tr><tr><td>历史对话轮数</td><td>10</td><td></td></tr><tr><td>重复惩罚参数</td><td>1.2</td><td></td></tr></tbody></table>