---
title: "接入Embedding模型"
date: "2024-01-17"
categories: 
  - "人工智能"
---

```python
import os

# 从 sentence_transformers 库中导入 SentenceTransformer 类
from typing import List, Union
from torch import Tensor
from numpy import ndarray

from sentence_transformers import SentenceTransformer


class LoadEmbeddingModel(object):

    def __init__(self):
        self.model = None

    def load(self):
        # 获取 EMBEDDING 模型路径，如果未设置则使用默认路径 'BAAI/bge-large-zh-v1.5'
        embedding_model_path = os.environ.get('EMBEDDING_MODEL_PATH', 'BAAI/bge-large-zh-v1.5')
        # 使用 SentenceTransformer 加载预训练的嵌入模型
        self.model = SentenceTransformer(embedding_model_path)

    # 对样例数据列表进行嵌入向量编码，同时进行标准化
    def encode(self, sentences: Union[str, List[str]],
               batch_size: int = 32,
               show_progress_bar: bool = True,
               output_value: str = 'sentence_embedding',
               convert_to_numpy: bool = True,
               convert_to_tensor: bool = False,
               device: str = None,
               normalize_embeddings: bool = True) -> Union[List[Tensor], ndarray, Tensor]:
        # 对样例数据列表进行嵌入向量编码，同时进行标准化
        return self.model.encode(sentences, batch_size, show_progress_bar, output_value, convert_to_numpy, convert_to_tensor, device, normalize_embeddings)


if __name__ == "__main__":
    model = LoadEmbeddingModel()
    model.load()
    # 定义两个样例数据列表
    sentences_1 = "样例数据-1, 样例数据-2"
    sentences_2 = ["样例数据-3", "样例数据-4"]
    embeddings_1 = model.encode(sentences_1)
    embeddings_2 = model.encode(sentences_2)
    print(embeddings_1)
    print(embeddings_2)

```

* * *

# 使用Langchain接入Embedding模型

```python
from langchain_community.embeddings import HuggingFaceBgeEmbeddings

model_name = "/data/LLM/BAAI/bge-large-zh-v1.5"
model_kwargs = {'device': 'cuda'}
encode_kwargs = {'normalize_embeddings': True}  # set True to compute cosine similarity
model = HuggingFaceBgeEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs,
    query_instruction="为这个句子生成表示以用于检索相关文章："
)

print(model.embed_documents("你好"))

```
