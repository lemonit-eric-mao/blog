---
title: "Rerank 重新排序"
date: "2024-04-02"
categories: 
  - "人工智能"
---

# Rerank 重新排序

## 参考资料

**[中文介绍](https://github.com/FlagOpen/FlagEmbedding/blob/master/README_zh.md "中文介绍")** **[模型下载](https://huggingface.co/BAAI/bge-reranker-large "模型下载")** **[加载模型](https://github.com/FlagOpen/FlagEmbedding/tree/master/examples/reranker#using-flagembedding "加载模型")**

## 应用开发

```python
from FlagEmbedding import FlagReranker

reranker = FlagReranker('/data/LLM/BAAI/bge-reranker-large', use_fp16=True)

# 句子对
sentence_pairs = [
    ["杏仁核的作用有哪些？", "杏仁核参与情绪的处理和识别，尤其是对威胁性和愉悦性刺激的反应。"],
    ["杏仁核的作用有哪些？", "杏仁核是恐惧条件反射的重要组成部分，与恐惧相关的情景和刺激引发的生理反应。"],
    ["杏仁核的作用有哪些？", "杏仁核通过影响自主神经系统的活动来调节生理反应，如心率和呼吸。"],
    ["杏仁核的作用有哪些？", "杏仁核参与社交行为，包括识别面部表情和理解他人的情感。"],
    ["杏仁核的作用有哪些？", "杏仁核参与压力的感知和应对，调节应激反应和应激激素的释放。"],
    ["杏仁核的作用有哪些？", "杏仁核参与决策制定，特别是在情绪驱动的决策中起到重要作用。"],
    ["杏仁核的作用有哪些？", "杏仁核有助于处理社会信号，如面部表情和身体语言。"],
    ["杏仁核的作用有哪些？", "杏仁核参与调节注意力，特别是在面对情绪性刺激时引导注意力的方向。"],
    ["杏仁核的作用有哪些？", "杏仁核有助于情绪记忆的形成和存储，特别是与情绪相关的记忆。"],
    ["杏仁核的作用有哪些？", "杏仁核通过与其他大脑区域的连接，参与调节情绪和情绪反应的生成。"]
]

score_list = reranker.compute_score(sentence_pairs=sentence_pairs)
# print(score_list)

# 使用enumerate函数获取元素和它们的索引位置，构成元组
index_list = list(enumerate(score_list))

# 对index_list进行排序，按照元组的第二个元素（即列表中的数字）排序，降序排列
sort_index_list = sorted(index_list, key=lambda x: x[1], reverse=True)
# print(sort_index_list)

top = 3  # 指定你想获取的前 x 个句子对数量
top_k = min(top, len(sentence_pairs))

# 获取评分最好的[x个]句子对
for i in range(top_k):
    # 获取排序后的列表中的[原始索引]和[评分]
    original_index, score = sort_index_list[i]
    # 根据[原始索引]获取对应的[句子对]
    pair = sentence_pairs[original_index]

    print(f"Rank {i + 1}:")
    print("Original index:", original_index)
    print("Score:", score)
    print("Sentence pair:", pair)
    print()

# 清除 sentence_pairs 列表释放空间
del sentence_pairs

```
