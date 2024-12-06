# Embedding模型 基于词表微调的核心思想



> 场景：
>
> 
>
> 
>
> 需求是构建一个**同义词扩展词典**，其中包含了类似`“普拉多”`和`“霸道SUV”`这样的`同义词`或`近义词`对，并希望利用这些信息来增强词嵌入模型的能力。

### 如何利用这个同义词扩展词典提升模型能力

#### 1. **创建同义词对的映射表**

首先，确保同义词扩展词典格式清晰，并且可以有效地映射每对同义词。例如，以下数据格式：

| 标准词     | 近似词   |
| ---------- | -------- |
| 普拉多     | 霸道SUV  |
| 苹果       | 苹果手机 |
| 蝴蝶结     | 领结     |
| 越野车     | SUV      |
| 丰田       | 丰田汽车 |
| 陆地巡洋舰 | 普拉多   |
| 跑车       | 敞篷车   |

每行表示一对同义词或近义词，可以将这些同义词对作为模型学习的额外信息来增强模型的语义理解。

##### 2. **通过词嵌入调整进行后处理**

如果已经有了预训练的词嵌入模型，并且想通过现有的同义词扩展词典来增强模型，可以使用**`后处理`**的方法，调整同义词对在嵌入空间中的位置。

- **在向量空间中调整位置：**
  使用现有的同义词对，通过调整向量，使同义词对在嵌入空间中的向量尽可能靠近。例如，如果`"普拉多"`和`"霸道SUV"`在当前嵌入空间中距离较远，可以通过优化算法（如梯度下降）来调整它们之间的向量差异，使它们的向量更加接近。

- ``` python
  from sklearn.metrics.pairwise import cosine_similarity
  import numpy as np
  
  # 同义词扩展词典
  synonym_pairs = [
      ("普拉多", "霸道SUV"),
      ("苹果", "苹果手机"),
      ("蝴蝶结", "领结"),
      ("越野车", "SUV"),
      ("丰田", "丰田汽车"),
      ("陆地巡洋舰", "普拉多"),
      ("跑车", "敞篷车")
  ]
  
  # 模拟一个预训练的词向量字典
  word_vectors = {
      "普拉多": np.random.rand(300),
      "霸道SUV": np.random.rand(300),
      "苹果": np.random.rand(300),
      "苹果手机": np.random.rand(300),
      "蝴蝶结": np.random.rand(300),
      "领结": np.random.rand(300),
      "越野车": np.random.rand(300),
      "SUV": np.random.rand(300),
      "丰田": np.random.rand(300),
      "丰田汽车": np.random.rand(300),
      "陆地巡洋舰": np.random.rand(300),
      "跑车": np.random.rand(300),
      "敞篷车": np.random.rand(300)
  }
  
  # 调整同义词对词向量，使它们更加接近
  def adjust_synonym_vectors(word_vectors, synonym_pairs, adjustment_factor=0.01, iterations=5):
      """
      调整同义词对向量，使它们更加接近。
      :param word_vectors: 词向量字典
      :param synonym_pairs: 同义词对的列表
      :param adjustment_factor: 向量调整的因子
      :param iterations: 调整的轮数
      """
      for iteration in range(1, iterations + 1):
          for word1, word2 in synonym_pairs:
              """
              具体操作：
                - 对于每一对同义词（比如“普拉多”和“霸道SUV”），我们首先计算这两个词向量之间的差异
                  diff = vec1 - vec2）。
                - 然后，我们使用一个调整因子（adjustment_factor）来缩小这个差距。
                  - 对于第一个词向量（vec1），我们减少它与第二个词向量（vec2）之间的差距，即：
                    word_vectors[word1] = vec1 - adjustment_factor * diff。
                  - 对于第二个词向量（vec2），我们增加它与第一个词向量（vec1）之间的差距，即：
                    word_vectors[word2] = vec2 + adjustment_factor * diff。
  
              这样做的结果是：
                - 每个词向量会在与另一个词向量的方向上做出调整，逐渐逼近对方的方向。
                - 这是一种"双向"的调整，旨在使得这两个词的词向量更接近，而不仅仅是让其中一个词的词向量向另一个词的词向量靠近。
              """
              # 获取标准词和近似词的词向量
              vec1 = word_vectors[word1]
              vec2 = word_vectors[word2]
              
              # 计算标准词与近似词的向量差距
              diff = vec1 - vec2
              
              # 使用调整因子来缩小差距
              word_vectors[word1] = vec1 - adjustment_factor * diff
              word_vectors[word2] = vec2 + adjustment_factor * diff
  
  # 评估调整后的词向量相似度
  def evaluate_similarity(word_vectors, synonym_pairs):
      """
      评估调整后的同义词对词向量的相似度。
      :param word_vectors: 词向量字典
      :param synonym_pairs: 同义词对的列表
      """
      for word1, word2 in synonym_pairs:
          vec1 = word_vectors[word1]
          vec2 = word_vectors[word2]
          similarity = cosine_similarity([vec1], [vec2])[0][0]
          print(f"{word1} 和 {word2} 的余弦相似度: {similarity}")
  
  # 1. 调整前评估相似度
  print("1. 调整前评估相似度")
  evaluate_similarity(word_vectors, synonym_pairs)
  
  # 2. 进行调整
  print("\n2. 进行调整")
  adjust_synonym_vectors(word_vectors, synonym_pairs)
  
  # 3. 调整后评估相似度
  print("\n3. 调整后评估相似度")
  evaluate_similarity(word_vectors, synonym_pairs)
  
  # 查看最终调整后的词向量（只显示前5个元素）
  print("\n4. --- Final word vectors ---")
  for word, vec in word_vectors.items():
      print(f"{word}: {vec[:5]}")  # 只显示前5个元素
  
  
  # ----------------------------------------------------------------
  
  
  # 计算任意两个词的相似度
  def calculate_input_similarity(word_vectors):
      """
      从控制台获取两个词，并计算它们的相似度。
      :param word_vectors: 词向量字典
      """
      # 获取用户输入的两个词
      word1 = input("请输入第一个词: ").strip()
      word2 = input("请输入第二个词: ").strip()
  
      # 检查这两个词是否在词向量字典中
      if word1 not in word_vectors or word2 not in word_vectors:
          print("输入的词不在词向量字典中，请检查输入。")
          return
      
      # 计算余弦相似度
      vec1 = word_vectors[word1]
      vec2 = word_vectors[word2]
      similarity = cosine_similarity([vec1], [vec2])[0][0]
      
      print(f"词 '{word1}' 和 '{word2}' 的余弦相似度为: {similarity}")
  
  # 5. 控制台测试：输入两个词并计算相似度
  print("\n5. 控制台测试：输入两个词计算相似度")
  calculate_input_similarity(word_vectors)
  ```

  效果

  ``` bash
  1. 调整前评估相似度
  普拉多 和 霸道SUV 的余弦相似度: 0.742629214876434
  苹果 和 苹果手机 的余弦相似度: 0.7638639611826197
  蝴蝶结 和 领结 的余弦相似度: 0.7460335567029709
  越野车 和 SUV 的余弦相似度: 0.7290492563173148
  丰田 和 丰田汽车 的余弦相似度: 0.7688060029822296
  陆地巡洋舰 和 普拉多 的余弦相似度: 0.7506011161437118
  跑车 和 敞篷车 的余弦相似度: 0.7609496292159811
  
  2. 进行调整
  
  3. 调整后评估相似度
  普拉多 和 霸道SUV 的余弦相似度: 0.967426663403759
  苹果 和 苹果手机 的余弦相似度: 0.971694788901358
  蝴蝶结 和 领结 的余弦相似度: 0.9692520535689286
  越野车 和 SUV 的余弦相似度: 0.9670045120851791
  丰田 和 丰田汽车 的余弦相似度: 0.9723331833598198
  陆地巡洋舰 和 普拉多 的余弦相似度: 0.9716861328574308
  跑车 和 敞篷车 的余弦相似度: 0.9712669686786736
  
  4. --- Final word vectors ---
  普拉多: [0.6324979  0.4713945  0.43293642 0.53168258 0.75938752]
  霸道SUV: [0.75885907 0.5571144  0.49006485 0.42369174 0.74600453]
  苹果: [0.58183056 0.31572518 0.47956451 0.43314278 0.36544717]
  苹果手机: [0.66857146 0.48492703 0.67100155 0.28065662 0.22752654]
  蝴蝶结: [0.70687526 0.70662601 0.13206105 0.56150919 0.27360911]
  领结: [0.65034919 0.47172245 0.10095241 0.50083673 0.24705496]
  越野车: [0.25993406 0.11914242 0.33463368 0.73583161 0.51909042]
  SUV: [0.4284568  0.09804652 0.56214652 0.52657592 0.50134129]
  丰田: [0.81539151 0.68755596 0.39266791 0.14003417 0.60694795]
  丰田汽车: [0.8569033  0.72750144 0.57187559 0.09830481 0.46454153]
  陆地巡洋舰: [0.74610979 0.45050235 0.56794315 0.53009251 0.79011364]
  跑车: [0.89119297 0.31242878 0.58536545 0.47197788 0.29908133]
  敞篷车: [0.85548147 0.42719145 0.31124076 0.2856858  0.33303822]
  
  ```





---



## 快问快答



### 问题

> 使用嵌入模型进行检索是否等同于“对称语义检索”，而使用 Rerank 模型进行优化排序是否就是“非对称语义检索”？这两者的关系是否准确？

### 回答

>你的理解是有一定道理的，但可以进一步澄清这两个概念的细微差别。
>
>### 1. **嵌入模型与对称语义检索**
>
>使用嵌入模型（如 BERT、GPT 等）进行检索，通常指的是将查询和文档都转换为向量，然后通过计算它们之间的相似度来进行检索。在这个过程中，查询和文档的向量表示是对称的，即查询和文档在同一个向量空间中进行比较。这种方法常常被称为 **对称语义检索**，因为它没有区别对待查询和文档，二者是对等的，只是通过相似度评分来匹配。
>
>### 2. **Rerank 模型与非对称语义检索**
>
>Rerank 模型通常是在初步检索的基础上，对候选文档进行二次排序优化。初步检索可能依赖于较为简单的检索方法（如基于关键词的检索），而 Rerank 模型会使用更为复杂的语义模型来优化排序，通常是一个 **非对称** 的过程，因为在这一步，查询和文档的处理方式可能会有所不同。查询的向量和文档的向量可能会在不同的上下文中进行解码，从而产生非对称的语义匹配。例如，查询向量可能会带有额外的上下文信息，而文档向量则侧重于理解与查询匹配的内容。
>
>### 3. **对比**
>
>- **对称语义检索**：查询和文档在相同的向量空间中进行相似度计算，无论是查询还是文档，都通过相同的嵌入模型进行编码。
>- **非对称语义检索**：通过 Rerank 模型优化排序时，查询和文档的语义模型可能有所不同。Rerank 阶段往往更侧重于对文档排序，而查询向量的处理可能更加关注查询本身的理解。
>
>### 总结
>
>虽然使用嵌入模型进行检索和使用 Rerank 模型进行优化排序的过程有一定的联系，但它们并不完全等价于“对称语义检索”和“非对称语义检索”。“对称”与“非对称”的核心差别在于查询和文档的处理方式是否相同。对于嵌入模型和 Rerank 模型的应用，这两个步骤的作用和目标是不同的，但它们的结合能实现更高效、更准确的检索效果。





---



# 微调BAAI/bge-m3模型



> pip install sentence-transformers torch datasets



#### train_bge_m3_model.py

``` python
# 安装必要的依赖
!pip install sentence-transformers torch datasets

# 导入相关库
from sentence_transformers import SentenceTransformer, util
from datasets import Dataset
import torch
from torch.utils.data import DataLoader
from sentence_transformers import losses
from sentence_transformers import SentencesDataset
from torch.optim import AdamW

# 加载BGE-M3或其他预训练模型
model_name = "your-bge-m3-model-path"  # 替换为你使用的模型路径
model = SentenceTransformer(model_name)  # 加载预训练模型

# 准备训练数据
# 数据格式：{'text1': 句子1, 'text2': 句子2, 'label': 标签（0或1）}
train_data = [
    {"text1": "普拉多对比车型使用手册", "text2": "霸道SUV对比车型使用手册", "label": 1},  # 相似
    {"text1": "普拉多对比车型使用手册", "text2": "凯迪拉克SUV对比手册", "label": 0},  # 不相似
    {"text1": "宝马X5对比车型手册", "text2": "奔驰GLS对比车型手册", "label": 1},  # 相似
    # 更多数据...
]

# 将数据转化为 Dataset 格式
train_dataset = Dataset.from_dict(train_data)

# 计算句子嵌入并预测相似度
def compute_embeddings(batch):
    """
    计算句子对的嵌入向量，并计算两段文本之间的余弦相似度
    """
    embeddings1 = model.encode(batch['text1'], convert_to_tensor=True, show_progress_bar=True)  # 编码第一个句子
    embeddings2 = model.encode(batch['text2'], convert_to_tensor=True, show_progress_bar=True)  # 编码第二个句子
    
    # 计算两段文本之间的余弦相似度
    similarities = util.pytorch_cos_sim(embeddings1, embeddings2)
    
    # 根据相似度阈值判断相似性（例如：相似度大于0.5认为是相似，反之为不相似）
    predictions = [1 if sim > 0.5 else 0 for sim in similarities.diagonal().tolist()]
    batch['predictions'] = predictions  # 保存预测结果
    return batch

# 将相似度计算函数应用到训练数据集
train_dataset = train_dataset.map(compute_embeddings, batched=True)

# 转换数据为 SentenceDataset 格式
train_sentences = [(item['text1'], item['text2'], item['label']) for item in train_dataset]

# 创建SentenceDataset，训练模型需要这个格式
train_data = SentencesDataset(train_sentences, model)
train_dataloader = DataLoader(train_data, shuffle=True, batch_size=16)  # 设置批次大小

# 定义优化器和损失函数
optimizer = AdamW(model.parameters(), lr=2e-5)  # 设置学习率

# 定义训练损失函数，这里我们使用CosineSimilarityLoss
loss_function = losses.CosineSimilarityLoss(model)

# 训练模型
def train(model, train_dataloader, optimizer, loss_function, epochs=3):
    """
    训练模型，微调模型以提高相似度计算精度
    """
    model.train()  # 将模型设置为训练模式
    for epoch in range(epochs):
        total_loss = 0
        for batch in train_dataloader:
            optimizer.zero_grad()  # 清空梯度
            sentence1, sentence2, labels = batch  # 提取句子对和标签
            labels = torch.tensor(labels).to(torch.float32)  # 将标签转为浮点数类型

            # 计算模型输出并获取损失
            loss = loss_function(sentence1, sentence2, labels)
            total_loss += loss.item()  # 累计损失

            # 反向传播并更新参数
            loss.backward()
            optimizer.step()

        print(f"Epoch {epoch + 1}, Loss: {total_loss / len(train_dataloader)}")  # 打印每轮的平均损失

# 训练模型
train(model, train_dataloader, optimizer, loss_function)

# 保存微调后的模型
model_save_path = "fine_tuned_bge_m3_model"  # 保存的路径
model.save(model_save_path)
print(f"模型已保存到: {model_save_path}")

```



#### evaluate_bge_m3_model.py

``` python
# 安装必要的依赖（如果还没有安装）
!pip install sentence-transformers torch datasets

# 导入相关库
from sentence_transformers import SentenceTransformer, util
from datasets import Dataset
import torch
from sklearn.metrics import accuracy_score, classification_report

# 加载训练好的BGE-M3或其他预训练模型
model_name = "your-bge-m3-model-path"  # 你的训练好的模型路径
model = SentenceTransformer(model_name)  # 加载模型

# 准备评估数据（评估数据与训练数据不同）
# 假设测试数据是以下格式
# 格式：{'text1': 句子1, 'text2': 句子2, 'label': 标签（0或1）}
eval_data = [
    {"text1": "普拉多对比车型使用手册", "text2": "霸道SUV对比车型使用手册", "label": 1},  # 相似
    {"text1": "普拉多对比车型使用手册", "text2": "凯迪拉克SUV对比手册", "label": 0},  # 不相似
    {"text1": "宝马X5对比车型手册", "text2": "奔驰GLS对比车型手册", "label": 1},  # 相似
    # 更多数据...
]

# 将数据转化为 Dataset 格式
eval_dataset = Dataset.from_dict(eval_data)

# 计算句子嵌入并预测相似度
def compute_predictions(batch):
    """
    计算句子对的嵌入并预测相似度
    """
    # 编码句子对
    embeddings1 = model.encode(batch['text1'], convert_to_tensor=True, show_progress_bar=True)
    embeddings2 = model.encode(batch['text2'], convert_to_tensor=True, show_progress_bar=True)
    
    # 计算余弦相似度
    similarities = util.pytorch_cos_sim(embeddings1, embeddings2)
    
    # 根据相似度阈值判断相似性（例如：相似度大于0.5认为是相似，反之为不相似）
    predictions = [1 if sim > 0.5 else 0 for sim in similarities.diagonal().tolist()]
    batch['predictions'] = predictions  # 保存预测结果
    return batch

# 计算预测结果
eval_dataset = eval_dataset.map(compute_predictions, batched=True)

# 获取真实标签和预测结果
y_true = eval_dataset['label']
y_pred = eval_dataset['predictions']

# 计算准确率和分类报告
accuracy = accuracy_score(y_true, y_pred)
report = classification_report(y_true, y_pred, target_names=["不相似", "相似"])

# 输出评估结果
print(f"准确率: {accuracy}")
print("分类报告:")
print(report)

```

