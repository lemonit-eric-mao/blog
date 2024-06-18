---
title: 接入自动语音识别模型
date: '2024-01-17T11:28:46+00:00'
status: private
permalink: /2024/01/17/%e6%8e%a5%e5%85%a5%e8%87%aa%e5%8a%a8%e8%af%ad%e9%9f%b3%e8%af%86%e5%88%ab%e6%a8%a1%e5%9e%8b
author: 毛巳煜
excerpt: ''
type: post
id: 10651
category:
    - 人工智能
tag: []
post_format: []
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
hestia_layout_select:
    - sidebar-right
---
**[OpenAI 开源语音识别 Whisper](https://www.zhihu.com/question/575983499/answer/3075691670 "OpenAI 开源语音识别 Whisper")**

**[Whisper](https://huggingface.co/openai/whisper-large-v3 "Whisper")**

```python
# 导入所需的库
import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline

# 检查是否有可用的CUDA设备，选择合适的设备
device = "cuda:0" if torch.cuda.is_available() else "cpu"
# 根据CUDA是否可用，选择合适的数据类型
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

# 指定本地模型和音频文件的路径
model_path = "/data/LLM/openai/whisper-large-v3"
audio_path = "/data/AI_Assistant.mp3"

# 从预训练模型加载模型，设置相关参数，并将模型移动到指定设备
model = AutoModelForSpeechSeq2Seq.from_pretrained(
    model_path, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
)
model.to(device)

# 从预训练模型加载处理器
processor = AutoProcessor.from_pretrained(model_path)

# 创建自动语音识别的管道
pipe = pipeline(
    task="automatic-speech-recognition",  # 任务类型为自动语音识别
    model=model,  # 指定模型，可以是模型标识符、预训练模型实例（PreTrainedModel）、或TF预训练模型实例（TFPreTrainedModel）
    tokenizer=processor.tokenizer,  # 指定分词器，可以是分词器标识符、预训练分词器实例（PreTrainedTokenizer）、或者PreTrainedTokenizerFast实例
    feature_extractor=processor.feature_extractor,  # 指定特征提取器，可以是特征提取器标识符或者预训练特征提取器实例（PreTrainedFeatureExtractor）
    max_new_tokens=128,  # 最大新令牌数
    chunk_length_s=30,  # 分块长度（秒）
    batch_size=16,  # 批处理大小
    return_timestamps=True,  # 是否返回时间戳
    torch_dtype=torch_dtype,  # 指定PyTorch张量的数据类型
    device=device,  # 指定设备
)

# 使用管道进行语音识别
result = pipe(audio_path, generate_kwargs={"language": "chinese"})
# 打印识别结果中的文本部分
# print(result["text"])

# 逐行打印数据
for entry in result["chunks"]:
    print(f"Timestamp: {entry['timestamp']}, Text: {entry['text']}")


```