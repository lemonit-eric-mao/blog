---
title: "LangChain 调用大模型服务"
date: "2023-10-23"
categories: 
  - "人工智能"
---

## 前置条件

**[准备Chatglm2-6b](chatglm2-6b%e8%b0%83%e7%a0%94%e6%96%87%e6%a1%a3 "准备Chatglm2-6b")**

# 安装LangChain

```bash
(test) [cloud@gpuServer1 (15:17:54) ~]
└─# pip install langchain
```

### LangChain 调用大模型 test\_chat.py

```python
# 导入所需模块和类
import os

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# 设置 OpenAI API 的基础 URL 和 API 密钥
# 如果是私有部署，只需要填写`模型服务端的URL`地址，不需要输出`API KEY`
os.environ["OPENAI_API_BASE"] = "http://172.16.176.59:8100/v1"
os.environ["OPENAI_API_KEY"] = "EMPTY"

# 创建 ChatOpenAI 对象，用于与 OpenAI 的聊天模型进行交互
llm = ChatOpenAI(
    model="chatglm3-6b",
    temperature=0.7,
    model_kwargs={
        "seed": 42
    },
)

# 创建一个包含系统消息和用户输入的聊天模板
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个智能助手,你的名字叫丹妮."),
    ("user", "{input}")
])

# 通过聊天链连接系统消息、用户输入和 OpenAI 聊天模型
chain = prompt | llm

# 输出初始欢迎消息
print("🤖：你好，我是一个智能助手。输入 'exit' 以结束对话。")

# 进入循环，不断接收用户输入，并生成回复
while True:
    # 接收用户输入
    user_input = input("👨：")

    # 如果用户输入为 'exit'，则结束对话
    if user_input.strip().lower() == 'exit':
        print("🤖: Thank you for using. Goodbye!")
        break

    # 通过聊天链生成回复
    result = chain.invoke({"input": user_input})

    # 获取并打印生成的回复
    print(f"🤖：{result.content}")

```

### 测试

```python
python test_chat.py

🤖：你好，我是一个智能助手。输入 'exit' 以结束对话。
👨：你好,请问你都能做什么?
🤖：你好!作为一个智能助手,我可以做很多事情。我可以回答你的问题、提供建议、帮助你完成任务、甚至可以进行聊天。只要是你需要的帮助,我都会尽力去回答或提供支持。
👨：你叫什么名字?
🤖：我的名字是丹妮,是一个人工智能助手。
👨：exit
🤖: Thank you for using. Goodbye!

```
