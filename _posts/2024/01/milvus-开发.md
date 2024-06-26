---
title: "Milvus 开发"
date: "2024-01-17"
categories: 
  - "milvus"
---

```python
from typing import List

from pymilvus import Collection, connections, db, FieldSchema, DataType, CollectionSchema, utility
from tabulate import tabulate

from models.embedding import LoadEmbeddingModel

# 加载 Embedding 模型
model = LoadEmbeddingModel()
model.load()


# 创建向量数据库Collection
# text_data 业务数据
def create_milvus(text_data: str):
    # 连接到 Milvus 服务器
    connections.connect(host="172.16.176.66", port=19530)
    # 使用数据库
    db.using_database("default")

    # ============================================================

    # 创建主键
    pk_id = FieldSchema(
        name="pk_id",
        dtype=DataType.INT64,
        is_primary=True,
    )
    # 创建标量，用来记录视频时间
    video_time = FieldSchema(
        name="video_time",
        dtype=DataType.VARCHAR,
        max_length=200,
        default_value="Unknown"
    )
    # 创建向量，用来记录视频中的旁白文字
    video_context = FieldSchema(
        name="video_context",
        dtype=DataType.VARCHAR,
        max_length=500,
        default_value="Unknown"
    )
    # 创建向量，用来记录视频中的旁白文字向量化
    video_context_vector = FieldSchema(
        name="video_context_vector",
        dtype=DataType.FLOAT_VECTOR,
        dim=1024
    )
    # 将列名放入CollectionSchema对象中，为创建Collection做准备
    schema = CollectionSchema(
        fields=[pk_id, video_time, video_context, video_context_vector],
        description="根据旁白文字查询视频时间",
        enable_dynamic_field=True
    )
    # Collection名
    collection_name = "video"

    # 在default数据库中创建Collection
    collection = Collection(
        name=collection_name,
        schema=schema,
        using='default'
    )

    # ============================================================

    # 创建向量索引
    index_params = {
        "metric_type": "L2",
        "index_type": "HNSW",
        "params": {
            "M": 8,
            "efConstruction": 64
        }
    }

    # 为Collection中的向量列名video_context_vector添加向量索引
    collection.create_index(
        field_name="video_context_vector",
        index_params=index_params
    )
    utility.index_building_progress("video")

    # ============================================================

    # 插入业务数据
    data = []

    # 将文本数据分割成每个时间段的旁白文字
    segments = [segment.strip() for segment in text_data.split("\n\n")]
    # 遍历每个时间段的旁白文字
    for idx, segment in enumerate(segments):
        # ['时间范围', '旁白文字']
        temp = segment.split("\n")
        print(temp)
        # 获取时间范围
        time_range = temp[0]
        # 获取旁白文字
        text = temp[1]
        # 使用嵌入模型获取旁白文字的向量
        embedding_vector = model.encode(text)
        # 创建数据点字典
        data_point = {
            "pk_id": idx + 1,  # 主键
            "video_time": f"{time_range}s",  # 视频时间
            "video_context": text,  # 旁白文字
            "video_context_vector": embedding_vector.tolist()  # 旁白文字向量
        }
        # 添加到数据列表
        data.append(data_point)

    # 插入数据到Milvus
    collection.insert(data)
    # 加载Collection
    collection.load()


# 查询向量数据库
# query_vector 查询条件向量
def search_milvus(query_vector: List):
    # 连接到 Milvus 服务器
    conn = connections.connect(host="172.16.176.66", port=19530)
    # 使用数据库
    db.using_database("default")

    # 获取现有的集合
    collection = Collection("video")
    # 加载集合到内存
    collection.load()

    # 准备搜索参数
    search_params = {
        "metric_type": "L2",
        "offset": 0,
        "ignore_growing": False,
        "params": {"ef": 250}
    }

    # 进行搜索操作
    results = collection.search(
        data=[query_vector],  # 待搜索的数据，这里使用二维数组表示
        anns_field="video_context_vector",  # 指定进行向量搜索的列名
        # `param` 中 `offset` 和 `limit` 的总和应小于 16384
        param=search_params,  # 搜索参数，包括偏移和限制等
        limit=1,  # 搜索结果返回的数量限制
        expr=None,  # 表达式，用于进一步筛选结果，这里设置为 None
        # 指定要从搜索结果中检索的列名(非内置列名都要写)
        output_fields=['pk_id', 'video_time', 'video_context'],
        consistency_level="Strong"  # 一致性级别，这里设置为“Strong”
    )

    # 输出结果格式化成横向表格
    # 定义列头
    headers = ["pk_id", "score", "video_time", "video_context"]
    data = []
    for i, hit in enumerate(results[0]):
        data.append([hit.pk_id, hit.score, hit.video_time, hit.video_context])

    # 打印表格
    print(tabulate(data, headers=headers))

    # 释放加载的集合，减少内存消耗
    # conn.release()

    # 断开与 Milvus 服务器的连接
    # conn.disconnect()

    return results[0]
```
