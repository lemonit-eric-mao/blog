---
title: vLLM接入大模型
date: '2023-11-24T14:18:13+00:00'
status: private
permalink: /2023/11/24/vllm%e6%8e%a5%e5%85%a5%e5%a4%a7%e6%a8%a1%e5%9e%8b
author: 毛巳煜
excerpt: ''
type: post
id: 10540
category:
    - 人工智能
tag: []
post_format: []
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
hestia_layout_select:
    - sidebar-right
---
`vLLM`源码操作
==========

环境准备
----

```bash
## 下载vLLM源码
[cloud@New-test1 (11:16:34) /mnt/data/siyu.mao]
└─<span class="katex math inline">wget https://github.com/vllm-project/vllm/archive/refs/tags/v0.2.2.zip


## 创建conda环境
[cloud@New-test1 (11:19:36) /mnt/data/siyu.mao]
└─</span> conda create -n vllm-0.2.2 python==3.10.12 -c http://172.16.21.146:8081/repository/anaconda-proxy/main --override-channels


[cloud@New-test1 (11:19:36) /mnt/data/siyu.mao]
└─$ conda activate vllm-0.2.2


```

尝试运行
----

```bash
## 安装依赖
(vllm-0.2.2) [cloud@New-test1 (16:49:39) /mnt/data/siyu.mao/vllm-0.2.2]
└─<span class="katex math inline">pip install -i http://172.16.21.146:8081/repository/pypi/simple  --trusted-host 172.16.21.146 --timeout 0 -r ./requirements.txt


## 本地构建安装
(vllm-0.2.2) [cloud@New-test1 (17:23:08) /mnt/data/siyu.mao/vllm-0.2.2]
└─</span> pip install -i http://172.16.21.146:8081/repository/pypi/simple  --trusted-host 172.16.21.146 --timeout 0 vllm -e .


## 查看引用列表
(vllm-0.2.2) [cloud@New-test1 (19:04:33) /mnt/data/siyu.mao/vllm-0.2.2]
└─$ pip list | grep vllm
vllm                      0.2.2        /mnt/data/siyu.mao/vllm-0.2.2



```

### 准备测试

```python
(vllm-0.2.2) [cloud@New-test1 (19:16:08) /mnt/data/siyu.mao/vllm-0.2.2]
└─$ python
Python 3.10.12 (main, Jul  5 2023, 18:54:27) [GCC 11.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>


```

1. ```python
  # 引入所需的依赖包
  from vllm import LLM, SamplingParams
  
  ```
2. ```python
  # 加载大模型(这个过程会稍微慢一点)
  llm = LLM(model="/mnt/data/NewLLM/THUDM/chatglm3-6b-32k", trust_remote_code=True)
  
  ```
3. ```python
  # 配置模型推理参数
  sampling_params = SamplingParams(
     top_p=0.9,                # 在采样时，累积概率分布的最高概率。较高的值会增加更多的随机性。
     top_k=3,                  # 在采样时，只考虑累积概率分布中的前 k 个最高概率的标记。
     best_of=6,                # 在多次生成中选择最佳结果的次数，以提高生成文本的质量。
     repetition_penalty=1.2,   # 重复惩罚，惩罚生成与已生成文本中相似的标记的概率。较高的值减少生成文本中的重复。
     temperature=0.7,          # 温度参数，控制生成文本的随机性。较低的值使输出更加确定性，较高的值增加随机性。
     max_tokens=500            # 限制生成的长度，防止生成的文本过长。
  )
  
  ```
4. ```python
  # 编写提示模板
  prompts = [
     "你是谁？",
  ]
  
  ```
5. ```python
  # 让模型思考并反馈(推理生成)
  outputs = llm.generate(prompts, sampling_params)
  
  ```
6. ```python
  # 打印模型的反馈
  for output in outputs:
     prompt = output.prompt
     generated_text = output.outputs[0].text
     print(f"Prompt: {prompt!r}, Generated text: {generated_text!r}")
  
  
  # 输出
  Prompt: '你是谁？', Generated text: ' \n\n我是 QAGLM, 人工智能助手,很高兴为您服务！'
  
  
  ```

#### 信息解释

**采样参数：**

- `n`: 给定提示返回的输出序列数量。  
  作用：限定生成的输出序列数量为 `n`。  
  说明：生成模型将返回多个输出序列，用户可以从中选择。
- `best_of`: 从提示生成的输出序列数。从这些`best_of`序列中选择前`n`个序列返回。当`use_beam_search`为True时，将其视为波束宽度。默认情况下，`best_of`设置为`n`。  
  作用：控制生成多个序列后从中选择的候选数量。  
  说明：在生成多个序列后，用户可以选择从中返回最好的 `n` 个序列。
- `presence_penalty`: 基于生成文本中新标记是否出现而对其进行奖励或惩罚的浮点数。大于0的值鼓励模型使用新标记，小于0的值鼓励模型重复标记。  
  作用：根据生成文本中新标记的出现与否对模型进行奖励或惩罚。  
  说明：正值鼓励模型引入新标记，负值则鼓励模型重复使用标记。主要用于调整模型生成文本的多样性。
- `frequency_penalty`: 基于生成文本中新标记的频率而对其进行惩罚的浮点数。大于0的值鼓励模型使用新标记，小于0的值鼓励模型重复标记。  
  作用：根据生成文本中新标记的频率对模型进行奖励或惩罚。  
  说明：正值鼓励模型使用新标记，负值则鼓励模型重复使用标记。
- `repetition_penalty`: 控制生成文本中标记重复的程度的浮点数。大于1的值鼓励模型使用新标记，小于1的值鼓励模型重复标记。  
  作用：根据生成文本中标记的重复程度对模型进行奖励或惩罚。  
  说明：大于1的值鼓励模型引入新标记，小于1的值则鼓励模型重复使用标记。用于调整模型生成文本中标记的重复程度。
- `temperature`: 控制采样随机性的浮点数。较低的值使模型更加确定性，较高的值使模型更加随机。零表示贪婪采样。  
  作用：调整生成文本时的随机性。  
  说明：较低的值使生成更加确定，较高的值使生成更加随机，零表示贪婪采样。
- `top_p`: 控制要考虑的前几个标记的累积概率的浮点数。必须在(0, 1\]范围内。设置为1以考虑所有标记。  
  作用：指定累积概率阈值，用于确定生成文本时可考虑的标记。  
  说明：只考虑累积概率高于该阈值的标记。
- `top_k`: 控制要考虑的前几个标记的整数。设置为-1以考虑所有标记。  
  作用：限制生成文本时考虑的标记数量。  
  说明：只考虑概率最高的前 `top_k` 个标记。
- `min_p`: 表示相对于最可能标记的概率而考虑的标记的最小概率的浮点数。必须在\[0, 1\]范围内。设置为0以禁用此功能。  
  作用：设置生成文本时考虑的标记概率的最小阈值。  
  说明：只考虑概率相对较高的标记，阈值由 `min_p` 决定。
- `use_beam_search`: 是否使用波束搜索而不是采样。  
  作用：指定是否使用波束搜索算法生成文本。  
  说明：如果为True，模型将使用波束搜索，否则使用采样。
- `length_penalty`: 基于序列长度而对其进行惩罚的浮点数。用于波束搜索。  
  作用：根据生成序列的长度对波束搜索结果进行调整。  
  说明：长度惩罚用于平衡生成的序列长度，防止生成过短或过长的序列。
- `early_stopping`: 控制波束搜索的停止条件。接受以下值：`True`，生成停止时有`best_of`完整候选项；`False`，应用启发式并在很不可能找到更好的候选项时停止生成；`"never"`，只有在不能有更好的候选项时波束搜索过程才停止（标准波束搜索算法）。  
  作用：设置波束搜索的停止条件。  
  说明：根据条件控制波束搜索何时停止，可以选择在找到一定数量的候选项后停止。
- `stop`: 生成这些字符串时停止生成。返回的输出将不包含停止字符串。  
  作用：指定在生成文本中包含指定字符串时停止生成。  
  说明：生成的文本将在包含指定字符串时终止。
- `stop_token_ids`: 生成这些标记时停止生成。返回的输出将包含停止标记，除非停止标记是特殊标记。  
  作用：指定在生成文本中包含指定标记时停止生成。  
  说明：生成的文本将在包含指定标记时终止。
- `ignore_eos`: 是否忽略EOS标记并在生成EOS标记后继续生成标记。  
  作用：控制是否在生成EOS标记后停止生成。  
  说明：如果为True，生成文本将忽略EOS标记并继续生成。
- `max_tokens`: 每个输出序列要生成的最大标记数。  
  作用：限制每个生成序列的标记数量。  
  说明：生成的序列将在达到指定的最大标记数后终止。
- `logprobs`: 每个输出标记要返回的对数概率数。请注意，实现遵循OpenAI API：返回结果包括在`logprobs`最有可能的标记上的对数概率，以及选择的标记。API将始终返回所抽样标记的对数概率，因此响应中可能有多达`logprobs+1`个元素。  
  作用：控制返回的对数概率的数量。  
  说明：每个生成的标记将返回指定数量的对数概率。
- `prompt_logprobs`: 每个提示标记要返回的对数概率数。  
  作用：控制每个提示标记返回的对数概率的数量。  
  说明：每个给定的提示标记将返回指定数量的对数概率。
- `skip_special_tokens`: 是否跳过输出中的特殊标记。  
  作用：控制生成文本时是否包含特殊标记。  
  说明：如果为True，生成的文本将不包含特殊标记。
- `spaces_between_special_tokens`: 是否在输出中的特殊标记之间添加空格。默认为True。  
  作用：控制是否在特殊标记之间添加空格。  
  说明：如果为True，生成的文本将在特殊标记之间添加空格。
- `logits_processors`: 根据先前生成的标记修改logits的函数的列表。  
  作用：应用于先前生成的标记的logits的处理函数列表。  
  说明：可以通过指定处理函数列表对生成的文本进行额外的后处理，修改先前生成的标记的logits。

```bash
>>> llm = LLM(model="/mnt/data/LLM/THUDM/chatglm2-6b-32k/", trust_remote_code=True)

INFO 11-24 19:40:35 llm_engine.py:72] Initializing an LLM engine with config: model='/mnt/data/LLM/THUDM/chatglm2-6b-32k', tokenizer='/mnt/data/LLM/THUDM/chatglm2-6b-32k', tokenizer_mode=auto, revision=None, tokenizer_revision=None, trust_remote_code=True, dtype=torch.float16, max_seq_len=32768, download_dir=None, load_format=auto, tensor_parallel_size=1, quantization=None, seed=0)
WARNING 11-24 19:40:35 tokenizer.py:66] Using a slow tokenizer. This might cause a significant slowdown. Consider using a fast tokenizer instead.
INFO 11-24 19:41:00 llm_engine.py:207] # GPU blocks: 132349, # CPU blocks: 9362




1. `Initializing an LLM engine with config:`：初始化 LLM 引擎，并列出了一些配置参数。
2. `model='/mnt/data/LLM/THUDM/chatglm2-6b-32k/'`：指定了模型的路径。
3. `tokenizer='/mnt/data/LLM/THUDM/chatglm2-6b-32k/'`：指定了分词器的路径。
4. `tokenizer_mode=auto`：自动选择分词器模式。
5. `trust_remote_code=True`：信任远程代码，可能是指在模型或分词器加载时信任从远程源加载的代码。
6. `dtype=torch.float16`：指定了张量的数据类型为 float16。
7. `max_seq_len=32768`：设置了最大序列长度。
8. `download_dir=None`：未指定下载目录。
9. `load_format=auto`：自动选择加载格式。
10. `tensor_parallel_size=1`：张量并行大小为 1。
11. `quantization=None`：未启用量化。
12. `seed=0`：随机数生成器的种子值

# GPU blocks 是 132349，CPU blocks 是 9362。这可能是指在模型的计算中，有 132349 个 GPU 计算块和 9362 个 CPU 计算块。
13. `GPU blocks`: 132349 GPU 和 CPU 上的计算块（blocks）数量。
14. `CPU blocks`: 9362：CPU 上的计算块（blocks）数量。

```

后续使用
----

```python
# 编写提示模板
prompts = [
    "你在做什么？",
    "请用中文，为我讲一个关于医生的笑话",
]

# 让模型思考并反馈(推理生成)
outputs = llm.generate(prompts, sampling_params)

# 打印模型的反馈
for output in outputs:
    prompt = output.prompt
    generated_text = output.outputs[0].text
    print(f"Prompt: {prompt!r}, Generated text: {generated_text!r}")


```