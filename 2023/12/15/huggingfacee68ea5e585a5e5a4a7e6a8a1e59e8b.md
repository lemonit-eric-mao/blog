---
title: HuggingFace接入大模型
date: '2023-12-15T02:32:23+00:00'
status: private
permalink: /2023/12/15/huggingface%e6%8e%a5%e5%85%a5%e5%a4%a7%e6%a8%a1%e5%9e%8b
author: 毛巳煜
excerpt: ''
type: post
id: 10621
category:
    - 人工智能
tag: []
post_format: []
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
hestia_layout_select:
    - sidebar-right
---
HF(HuggingFace)接入大模型【[代码调用](https://huggingface.co/THUDM/chatglm3-6b-32k#%E4%BB%A3%E7%A0%81%E8%B0%83%E7%94%A8-code-usage)】
==========================================================================================================================

### 准备测试

```python
(vllm-0.2.2) [cloud@New-test1 (19:16:08) /mnt/data/siyu.mao/vllm-0.2.2]
└─$ python
Python 3.10.12 (main, Jul  5 2023, 18:54:27) [GCC 11.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>


```

1. ```python
  # 导入所需的库
  from transformers import AutoTokenizer, AutoModel
  
  ```
2. ```python
  # 从预训练模型路径加载分词器（tokenizer）和模型（model）这个过程会稍微慢一点
  tokenizer = AutoTokenizer.from_pretrained("/mnt/data/NewLLM/THUDM/chatglm3-6b-32k", trust_remote_code=True)
  model = AutoModel.from_pretrained("/mnt/data/NewLLM/THUDM/chatglm3-6b-32k", trust_remote_code=True).half().cuda()
  
  ```
3. ```python
  # 设置模型为评估模式
  model = model.eval()
  
  ```
4. ```python
  # 进行对话交互
  # 第一轮对话
  response, history = model.chat(tokenizer, "你好", history=[])
  print(response)
  # 输出
  你好👋！我是 ChatGLM3-6B，很高兴见到你，欢迎问我任何问题。
  
  ```
5. ```python
  # 第二轮对话，使用上一轮的历史对话
  response, history = model.chat(tokenizer, "晚上睡不着应该怎么办", history=history)
  print(response)
  # 输出
  晚上睡不着可能会让人感到焦虑和沮丧，但以下方法可能会帮助你改善睡眠：
  
  1. 建立规律的睡眠时间表：每天尽量在相同的时间上床和起床，包括周末。
  2. 创建舒适的睡眠环境：确保你的睡眠环境安静、黑暗、凉爽且舒适，床垫和枕头也应该舒适。
  3. 避免刺激性物质：避免在睡前饮用咖啡、茶或其他含咖啡因的饮料，以及避免食用过多的糖分和脂肪。
  4. 放松技巧：尝试使用一些放松技巧，如深呼吸、冥想、渐进性肌肉松弛或瑜伽，这些方法可以帮助你放松身心并入睡。
  5. 避免在床上看电视或使用电脑：在床上看电视或使用电脑可能会影响睡眠质量，因此最好在床上看书或听一些柔和的音乐。
  
  如果以上方法都无法帮助你改善睡眠，建议你咨询医生或专业心理医生的意见。
  
  ```

- - - - - -

- - - - - -

- - - - - -

模型返回的数据格式
=========

未转码
---

```bash
{"text": "", "error_code": 0, "usage": {"prompt_tokens": 10, "completion_tokens": 1, "total_tokens": 11}, "finish_reason": null}
{"text": "", "error_code": 0, "usage": {"prompt_tokens": 10, "completion_tokens": 2, "total_tokens": 12}, "finish_reason": null}
{"text": "", "error_code": 0, "usage": {"prompt_tokens": 10, "completion_tokens": 3, "total_tokens": 13}, "finish_reason": null}
{"text": "\u6211\u662f", "error_code": 0, "usage": {"prompt_tokens": 10, "completion_tokens": 4, "total_tokens": 14}, "finish_reason": null}
{"text": "\u6211\u662f Chat", "error_code": 0, "usage": {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15}, "finish_reason": null}
{"text": "\u6211\u662f ChatGL", "error_code": 0, "usage": {"prompt_tokens": 10, "completion_tokens": 6, "total_tokens": 16}, "finish_reason": null}
{"text": "\u6211\u662f ChatGLM", "error_code": 0, "usage": {"prompt_tokens": 10, "completion_tokens": 7, "total_tokens": 17}, "finish_reason": null}
{"text": "\u6211\u662f ChatGLM3", "error_code": 0, "usage": {"prompt_tokens": 10, "completion_tokens": 8, "total_tokens": 18}, "finish_reason": null}
{"text": "\u6211\u662f ChatGLM3-", "error_code": 0, "usage": {"prompt_tokens": 10, "completion_tokens": 9, "total_tokens": 19}, "finish_reason": null}
{"text": "\u6211\u662f ChatGLM3-6", "error_code": 0, "usage": {"prompt_tokens": 10, "completion_tokens": 10, "total_tokens": 20}, "finish_reason": null}
{"text": "\u6211\u662f ChatGLM3-6B", "error_code": 0, "usage": {"prompt_tokens": 10, "completion_tokens": 11, "total_tokens": 21}, "finish_reason": null}
{"text": "\u6211\u662f ChatGLM3-6B\uff0c", "error_code": 0, "usage": {"prompt_tokens": 10, "completion_tokens": 12, "total_tokens": 22}, "finish_reason": null}
{"text": "\u6211\u662f ChatGLM3-6B\uff0c\u662f", "error_code": 0, "usage": {"prompt_tokens": 10, "completion_tokens": 13, "total_tokens": 23}, "finish_reason": null}
{"text": "\u6211\u662f ChatGLM3-6B\uff0c\u662f\u6e05\u534e\u5927\u5b66", "error_code": 0, "usage": {"prompt_tokens": 10, "completion_tokens": 14, "total_tokens": 24}, "finish_reason": null}
{"text": "\u6211\u662f ChatGLM3-6B\uff0c\u662f\u6e05\u534e\u5927\u5b66KE", "error_code": 0, "usage": {"prompt_tokens": 10, "completion_tokens": 15, "total_tokens": 25}, "finish_reason": null}
{"text": "\u6211\u662f ChatGLM3-6B\uff0c\u662f\u6e05\u534e\u5927\u5b66KEG", "error_code": 0, "usage": {"prompt_tokens": 10, "completion_tokens": 16, "total_tokens": 26}, "finish_reason": null}
{"text": "\u6211\u662f ChatGLM3-6B\uff0c\u662f\u6e05\u534e\u5927\u5b66KEG\u5b9e\u9a8c\u5ba4", "error_code": 0, "usage": {"prompt_tokens": 10, "completion_tokens": 17, "total_tokens": 27}, "finish_reason": "stop"}

```

**需要做处理才能被用户使用**  
**FastChat调用模型的源代码**

```python
    total_len = 0
    for total_ids in model.stream_generate(**inputs, **gen_kwargs):
        total_ids = total_ids.tolist()[0]
        total_len = len(total_ids)
        if echo:
            output_ids = total_ids
        else:
            output_ids = total_ids[input_echo_len:]
        response = tokenizer.decode(output_ids)
        response = process_response(response)

        yield {
            "text": response,
            "usage": {
                "prompt_tokens": input_echo_len,
                "completion_tokens": total_len - input_echo_len,
                "total_tokens": total_len,
            },
            "finish_reason": None,
        }

```

**业务封装，调用FastChat Model Worker的代码**

```python
    # 请求 FastChat Worker 并进行流式返回
    def generate_completion_stream(self, params):
        Logger.debug("请求 FastChat Worker 并进行流式返回")
        # 获取工作地址
        worker_addr = self.controller.get_worker_address(self.model_name)
        # 发送POST请求到工作地址上的worker_generate_stream端点，传入参数params，设置流式传输
        response = requests.post(
            worker_addr + "/worker_generate_stream",  # 构造完整的工作地址
            json=params,  # 将参数params转换为JSON格式并发送
            stream=True,  # 设置为流式传输，以便逐行接收响应
        )

        prev = 0  # 初始化前一次输出的长度
        # 遍历响应的数据流，以'\0'作为分隔符逐行处理
        for chunk in response.iter_lines(delimiter=b"\0"):
            if chunk:  # 如果数据块非空
                data = json.loads(chunk)  # 解析JSON数据块
                output = data["text"].strip()  # 获取文本输出并去除首尾空白
                Logger.debug(output[prev:])  # 输出当前文本片段（避免重复输出已经输出过的部分）
                yield output[prev:]  # 使用yield返回当前文本片段（避免重复输出已经输出过的部分）
                prev = len(output)  # 更新前一次输出的长度，以便下一次输出时截取正确的部分


```