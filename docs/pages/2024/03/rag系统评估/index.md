---
title: "RAG系统评估"
date: "2024-03-23"
categories: 
  - "python"
  - "人工智能"
---

# RAG 系统评估

## 环境准备

```bash
conda create -n ragas python==3.10.12 -c http://172.16.21.146:8081/repository/anaconda-proxy/main --override-channels

pip install -i http://172.16.21.146:8081/repository/pypi/simple  --trusted-host 172.16.21.146 --timeout 0 -r ./requirements.txt
```

## 实现流程

> 收集RAG系统中的数据 --> 制作测试数据集 --> 使用RAGAS项目针对数据集进行评估 --> 使用umap进行指标可视化
> 
> 1. 既然是创造数据集，就要先知道数据集的格式是什么？
> 2. 确定的数据集的格式，才能正确的填充数据内容。

## 先学会造数据

> 数据从你的RAG系统中产出，你要自己创建问题，自己给出正确的答案，然后从RAG系统中收集产生的数据，最后将数据制作成数据集备用。

## 使用RAGAS工具，基于数据集评估你的RAG系统

### 线上版`start_evaluate.py`

```python
"""
使用说明:
告诉 Hugging Face Datasets 库在离线模式下工作。
当设置 HF_DATASETS_OFFLINE=1 后，该库将不会尝试在线下载数据集，而是会尝试在本地找到数据集的缓存版本。
export HF_DATASETS_OFFLINE=1
python start_evaluation.py
"""

print("----------------------------------------------创建数据集--------------------------------------------------")

from datasets import Dataset

"""
假设你已经成功构建了一个RAG 系统，并且现在想要评估它的性能。为了这个目的，你需要一个评估数据集，该数据集包含以下列：

- question:        list[str]       （问题）：想要评估的RAG的问题
- ground_truths:   list[str]       （真实答案）：问题的真实答案
- answer:          list[str]       （答案）：RAG 预测的答案
- contexts:        list[list[str]] （上下文）：RAG 用于生成答案的相关信息列表
"""
# 将您的数据加载到字典中
data = {
    "question": ["法国的首都是什么？", "《哈利波特》的作者是谁？", "水的沸点是多少？"],
    "ground_truths": ["巴黎", "J.K.罗琳", "100度摄氏度"],
    "answer": ["巴黎", "J.K.罗琳", "100度摄氏度"],
    "contexts": [
        ["巴黎是法国的首都。"],
        ["J.K.罗琳写了《哈利波特》。"],
        ["水在海平面下沸腾的温度是100摄氏度。"]
    ]
}

# 使用字典创建 Dataset 对象
dataset = Dataset.from_dict(data)

print("----------------------------------------------加载数据集--------------------------------------------------")

# 修改数据集中的列名
dataset_dict = dataset.rename_columns({"ground_truths": "ground_truth"})
print(f"修改数据集中的列名\n{dataset_dict}")

# 划分数据集
dataset_dict = dataset_dict.train_test_split(test_size=0.2)  # 80% 训练集，20% 验证集
print(f"划分数据集\n{dataset_dict}")

print("-----------------------------------------------加载模型---------------------------------------------------")

from langchain_openai import ChatOpenAI, OpenAIEmbeddings

BASE_URL = "http://172.16.176.59:7002"

# 加载大语言模型
llm = ChatOpenAI(base_url=BASE_URL, api_key="Empty", model="Baichuan2-13B-Chat")
print("加载大语言模型完成")

# 加载 embedding 模型
# 注意：使用`OpenAIEmbeddings客户端`时它需要一个`tokenizer模型`来计算token数量，
#      这一功能在离线场景是无法下载`tokenizer模型`的所以会产生异常，所以需要手动下载`tokenizer模型`并做离线配置影响的参数如下：
#      , tiktoken_enabled=False, tiktoken_model_name="/data/tokenizer/tiktoken_cl100k_base"
#      模型是从 git clone https://huggingface.co/DWDMaiMai/tiktoken_cl100k_base 地址下载，并保存到/data/tokenizer路径下
embedding_model = OpenAIEmbeddings(base_url=BASE_URL, api_key="Empty", model="bge-large-zh-v1.5", tiktoken_enabled=False, tiktoken_model_name="/data/tokenizer/tiktoken_cl100k_base")
print("加载 embedding 模型完成")

print("----------------------------------------------评估数据集--------------------------------------------------")

from ragas import evaluate
from ragas.metrics import (
    answer_relevancy,
    answer_similarity,
    context_entity_recall,
    context_precision,
    faithfulness,
)

# 使用ragas库的evaluate函数评估模型
result = evaluate(
    dataset=dataset_dict["train"],  # 传入训练集
    llm=llm,
    raise_exceptions=False,
    embeddings=embedding_model,  # 传入 embedding
    metrics=[
        answer_relevancy,
        answer_similarity,
        context_precision,
        context_entity_recall,
        faithfulness,
    ],
)
print(f"""
评估结果 / Evaluation Results:\n
回答相关性：     {result["answer_relevancy"]}
回答相似度：     {result["answer_similarity"]}
上下文精确度：   {result["context_precision"]}
上下文实体召回率：{result["context_entity_recall"]}
忠实度：        {result["faithfulness"]}
""")

"""
### 所有指标

1. **answer_relevancy**（回答相关性评分）
   根据给定的问题评估回答的相关性。
2. **answer_similarity**（回答相似度评分）
   评估生成的回答与实际回答之间的语义相似度。
3. **answer_correctness**（回答正确性评分）
   根据事实性和语义相似度综合评估回答的正确性。
4. **context_precision**（上下文精确度）
   平均精确度指标，评估模型选择的所有相关项是否排名更高。
5. **context_recall**（上下文召回率）
   通过使用注释的回答和检索到的上下文估计TP和FN来估计上下文召回率。
6. **context_entity_recall**（上下文实体召回率）
   根据实际情况和上下文中存在的实体计算召回率。
7. **AnswerCorrectness**（答案正确性）
   根据事实性和语义相似度的组合比较回答的正确性。
8. **AnswerRelevancy**（回答相关性）
   根据给定问题评估回答的相关性。
9. **AnswerSimilarity**（回答相似度）
   评估生成的回答与实际回答之间的语义相似度。
10. **AspectCritique**（观点评论）
    根据指标定义的标准对提交进行二进制结果评估。
11. **ContextEntityRecall**（上下文实体召回率）
    根据实际情况和上下文中存在的实体计算召回率。
12. **ContextPrecision**（上下文精确度）
    平均精确度指标，评估模型选择的所有相关项是否排名更高。
13. **ContextRecall**（上下文召回率）
    通过使用注释的回答和检索到的上下文估计TP和FN来估计上下文召回率。
14. **ContextRelevancy**（上下文相关性）
    从上下文中提取与问题相关的句子，并进行自一致性检查。
15. **ContextUtilization**（上下文利用率）
16. **Faithfulness**（忠实度）
"""

print("----------------------------------------------展示报表--------------------------------------------------")

# renumics-spotlight==1.6.8
from renumics import spotlight

data_frame = result.to_pandas()
spotlight.show(dataset=data_frame, host="127.0.0.1", port=6100, dtype={"image_url": spotlight.Image})

```

**输出结果**

```bash
----------------------------------------------创建数据集--------------------------------------------------
----------------------------------------------加载数据集--------------------------------------------------
修改数据集中的列名
Dataset({
    features: ['question', 'ground_truth', 'answer', 'contexts'],
    num_rows: 3
})
划分数据集
DatasetDict({
    train: Dataset({
        features: ['question', 'ground_truth', 'answer', 'contexts'],
        num_rows: 2
    })
    test: Dataset({
        features: ['question', 'ground_truth', 'answer', 'contexts'],
        num_rows: 1
    })
})
-----------------------------------------------加载模型---------------------------------------------------
加载大语言模型完成
加载 embedding 模型完成
----------------------------------------------评估数据集--------------------------------------------------
Evaluating: 100%|██████████| 10/10 [00:29<00:00,  2.92s/it]

评估结果 / Evaluation Results:

回答相关性：     0.5080443833601872
回答相似度：     0.9999999999999999
上下文精确度：   0.9999999999
上下文实体召回率：0.9999999900000002
忠实度：        1.0

----------------------------------------------展示报表--------------------------------------------------
Flattening the indices: 100%|██████████| 2/2 [00:00<00:00, 333.07 examples/s]
Flattening the indices: 100%|██████████| 2/2 [00:00<00:00, 501.83 examples/s]
Spotlight running on http://127.0.0.1:6100/
```

* * *

### 离线版

> 离线版: 目前RAGAS系统无法实现，原因是RAGAS系统`调用模型的方式`只支持`两种自定义的类型`，如下：
> 
> ```python
> ~\miniconda3\envs\ragas\Lib\site-packages\ragas\evaluation.py
> def evaluate(
>    #......
>    llm: t.Optional[BaseRagasLLM | LangchainLLM] = None,
>    embeddings: t.Optional[BaseRagasEmbeddings | LangchainEmbeddings] = None,
>    #......
> ) -> Result:
> ```
> 
> 所以因加载模型的方式受限，无法使用`Hugging Face`等其它不支持的方式进行加载。

```python
"""
使用说明:
告诉 Hugging Face Datasets 库在离线模式下工作。
当设置 HF_DATASETS_OFFLINE=1 后，该库将不会尝试在线下载数据集，而是会尝试在本地找到数据集的缓存版本。
export HF_DATASETS_OFFLINE=1
python start_evaluation.py
"""
from datasets import Dataset

print("----------------------------------------------创建数据集--------------------------------------------------")

"""
假设你已经成功构建了一个RAG 系统，并且现在想要评估它的性能。为了这个目的，你需要一个评估数据集，该数据集包含以下列：

- question:        list[str]       （问题）：想要评估的RAG的问题
- ground_truths:   list[str]       （真实答案）：问题的真实答案
- answer:          list[str]       （答案）：RAG 预测的答案
- contexts:        list[list[str]] （上下文）：RAG 用于生成答案的相关信息列表
"""
# 将您的数据加载到字典中
data = {
    "question": ["法国的首都是什么？", "《哈利波特》的作者是谁？", "水的沸点是多少？"],
    "ground_truths": ["巴黎", "J.K.罗琳", "100度摄氏度"],
    "answer": ["巴黎", "J.K.罗琳", "100度摄氏度"],
    "contexts": [
        ["巴黎是法国的首都。"],
        ["J.K.罗琳写了《哈利波特》。"],
        ["水在海平面下沸腾的温度是100摄氏度。"]
    ]
}

# 使用字典创建 Dataset 对象
dataset = Dataset.from_dict(data)

# 保存数据集
dataset.save_to_disk("./Datasets/test_data")

print("----------------------------------------------加载数据集--------------------------------------------------")

# 加载数据集
from datasets import load_from_disk

# 加载数据集
dataset_dict = load_from_disk("./Datasets/test_data")
print(f"加载数据集\n{dataset_dict}")

# 修改数据集中的列名
dataset_dict = dataset_dict.rename_columns({"ground_truths": "ground_truth"})
print(f"修改数据集中的列名\n{dataset_dict}")

# 划分数据集
dataset_dict = dataset_dict.train_test_split(test_size=0.2)  # 80% 训练集，20% 验证集
print(f"划分数据集\n{dataset_dict}")

print("----------------------------------------------评估数据集--------------------------------------------------")

from ragas import evaluate
from ragas.metrics import (
    answer_relevancy,
    faithfulness,
    context_recall,
    context_utilization,
)
from transformers import AutoModelForSeq2SeqLM, AutoModel

# 加载本地大语言模型
model_path = "/data/LLM/THUDM/chatglm3-6b"  # 替换为您的大语言模型的路径
#llm = AutoModelForSeq2SeqLM.from_pretrained(model_path, trust_remote_code=True) # 使用CPU
llm = AutoModelForSeq2SeqLM.from_pretrained(model_path, trust_remote_code=True).cuda().eval() # 使用GPU
print("加载本地大语言模型完成")

# 加载本地 embedding 模型
embedding_model_path = "/data/LLM/BAAI/bge-large-zh-v1.5"  # 替换为您的 embedding 模型的路径
#embedding_model = AutoModel.from_pretrained(embedding_model_path, trust_remote_code=True) # 使用CPU
embedding_model = AutoModel.from_pretrained(embedding_model_path, trust_remote_code=True).cuda().eval() # 使用GPU
print("加载本地 embedding 模型完成")

# 使用ragas库的evaluate函数评估模型
result = evaluate(
    dataset=dataset_dict["train"],  # 传入训练集
    llm=llm,
    embeddings=embedding_model,  # 传入 embedding
    metrics=[  # 指定需要评估的指标
        context_utilization,  # 上下文精确度
        faithfulness,  # 忠实度
        answer_relevancy,  # 回答相关性
        context_recall,  # 上下文召回率
    ],
)
print("使用ragas库的evaluate函数评估模型完成")

print(f"评估结果：\n{result}")

```

* * *

### 依赖包 requirements.txt

```txt
aiohttp==3.9.3
aiosignal==1.3.1
annotated-types==0.6.0
anyio==4.3.0
appdirs==1.4.4
async-timeout==4.0.3
attrs==23.2.0
certifi==2024.2.2
charset-normalizer==3.3.2
dataclasses-json==0.6.4
datasets==2.18.0
dill==0.3.8
distro==1.9.0
exceptiongroup==1.2.0
filelock==3.13.1
frozenlist==1.4.1
fsspec==2024.2.0
greenlet==3.0.3
h11==0.14.0
httpcore==1.0.4
httpx==0.27.0
huggingface-hub==0.21.4
idna==3.6
Jinja2==3.1.3
jsonpatch==1.33
jsonpointer==2.4
langchain==0.1.13
langchain-community==0.0.29
langchain-core==0.1.33
langchain-openai==0.1.0
langchain-text-splitters==0.0.1
langsmith==0.1.31
MarkupSafe==2.1.5
marshmallow==3.21.1
mpmath==1.3.0
multidict==6.0.5
multiprocess==0.70.16
mypy-extensions==1.0.0
nest-asyncio==1.6.0
networkx==3.2.1
numpy==1.26.4
nvidia-cublas-cu12==12.1.3.1
nvidia-cuda-cupti-cu12==12.1.105
nvidia-cuda-nvrtc-cu12==12.1.105
nvidia-cuda-runtime-cu12==12.1.105
nvidia-cudnn-cu12==8.9.2.26
nvidia-cufft-cu12==11.0.2.54
nvidia-curand-cu12==10.3.2.106
nvidia-cusolver-cu12==11.4.5.107
nvidia-cusparse-cu12==12.1.0.106
nvidia-nccl-cu12==2.19.3
nvidia-nvjitlink-cu12==12.4.99
nvidia-nvtx-cu12==12.1.105
openai==1.14.2
orjson==3.9.15
packaging==23.2
pandas==2.2.1
pyarrow==15.0.2
pyarrow-hotfix==0.6
pydantic==2.6.4
pydantic_core==2.16.3
pysbd==0.3.4
python-dateutil==2.9.0.post0
pytz==2024.1
PyYAML==6.0.1
ragas==0.1.5
regex==2023.12.25
requests==2.31.0
safetensors==0.4.2
six==1.16.0
sniffio==1.3.1
SQLAlchemy==2.0.28
sympy==1.12
tenacity==8.2.3
tiktoken==0.6.0
tokenizers==0.15.2
torch==2.2.1
tqdm==4.66.2
transformers==4.39.0
triton==2.2.0
typing-inspect==0.9.0
typing_extensions==4.10.0
tzdata==2024.1
urllib3==2.2.1
xxhash==3.4.1
yarl==1.9.4
```
