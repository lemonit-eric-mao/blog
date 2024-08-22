---
title: "AI 工具调用 Function Call 工作原理"
date: "2024-04-01"
categories: 
  - "人工智能"
---

# AI 工具调用

## 工作原理

> 1. 大语言模型必须具备`"Function Call"`功能。
> 2. 你可以随意编写一个方法，但关键在于让大型模型了解哪些方法是可以做为工具使用的。
> 3. 要让模型知道有哪些方法可以做为工具使用，需要按照模型熟悉的数据格式来提供信息，具体如下：
>     - `system_info = {"role": "system", "content": "尽可能回答以下问题。你可以利用以下工具：", "tools": tools}`
> 4. 结合用户提问的提示词，由大型模型来判断并决定使用哪个方法以及为哪些参数进行赋值。
> 5. 模型会指导你使用哪些工具方法来获取所需数据。
> 6. 利用Python的动态执行函数功能，执行指定的工具方法。
> 7. 将工具方法返回的信息追加到历史记录中，并返回给模型，以供后续推理任务使用。

## 必要条件

> 大语言模型本身必须要支持这样的能力

## 适用场景

> 让大语言模型通过`模型自身对提示`的理解，自主选择调用合理的函数来满足`提问需求`

## 应用开发

> ```python
> # pip install psutil
> import psutil
> 
> 
> def bytes_to_human_readable(bytes_value):
>     """
>     将字节数转换为可读的字符串，带有相应的大小参数（GB、MB等）
> 
>     Args:
>         bytes_value (int): 字节值
> 
>     Returns:
>         str: 可读的字符串
>     """
>     for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
>         if bytes_value < 1024:
>             return f"{round(bytes_value)} {unit}"
>         bytes_value /= 1024
> 
> 
> def get_cpu_usage():
>     """
>     获取CPU使用率
> 
>     Returns:
>         dict: 包含CPU使用率的字典，键为'CPU使用率'，值为当前CPU使用率（百分比）
>     """
>     return {"CPU使用率": psutil.cpu_percent(interval=1)}
> 
> 
> def get_memory_usage():
>     """
>     获取内存使用情况
> 
>     Returns:
>         dict: 包含内存使用情况的字典，包括总内存、可用内存、已使用内存、空闲内存和内存使用率
>     """
>     mem = psutil.virtual_memory()
>     return {
>         "总内存": bytes_to_human_readable(mem.total),
>         "可用内存": bytes_to_human_readable(mem.available),
>         "已使用内存": bytes_to_human_readable(mem.used),
>         "空闲内存": bytes_to_human_readable(mem.free),
>         "内存使用率": mem.percent
>     }
> 
> 
> def get_disk_usage():
>     """
>     获取磁盘使用情况
> 
>     Returns:
>         dict: 包含磁盘使用情况的字典，键为磁盘设备名，值为包括总磁盘空间、已使用磁盘空间、剩余磁盘空间和磁盘使用率的子字典
>     """
>     partitions = psutil.disk_partitions()
>     disk_usage = {}
>     for partition in partitions:
>         usage = psutil.disk_usage(partition.mountpoint)
>         disk_usage[partition.device] = {
>             "总磁盘空间": bytes_to_human_readable(usage.total),
>             "已使用磁盘空间": bytes_to_human_readable(usage.used),
>             "剩余磁盘空间": bytes_to_human_readable(usage.free),
>             "磁盘使用率": usage.percent
>         }
>     return disk_usage
> 
> 
> # pip install lunardate
> from lunardate import LunarDate
> 
> 
> def get_lunar_date(year, month, day):
>     """
>     获取指定年份、月份和日期的农历日期
> 
>     Args:
>         year (int): 年份
>         month (int): 月份
>         day (int): 日
> 
>     Returns:
>         dict: 农历日期
>     """
>     lunar_date = LunarDate.fromSolarDate(year, month, day)
>     return {
>         "year": lunar_date.year,
>         "month": lunar_date.month,
>         "day": lunar_date.day
>     }
> 
> 
> from zhipuai import ZhipuAI
> 
> client = ZhipuAI(
>     api_key="你的 API Key"
> )
> 
> 
> def exec_tools(messages):
>     """
>     与智能助理交互，执行工具。
> 
>     1: 准备工具列表，包括可用的函数及其参数描述。
>     2: 准备用户的问题。
>     3: 通知模型可用的工具和用户问题。
>     4: 模型选择是否调用用户提供的工具，并提供参数信息。
>     5: 解析返回的工具信息。
>     6: 根据返回的工具信息，动态执行工具并获取执行结果。
>         6.1: 获取方法所有信息
>         6.2: 提取方法名
>         6.3: 提取方法参数，将字符串形式的参数转换成字典
>         6.4: 获取对应的函数对象
>         6.5: 动态执行函数
> 
>     Raises:
>         Exception: 如果未找到函数。
> 
>     Returns:
>         None
>     """
>     import json
> 
>     # Step 1: 准备，用户有哪些工具可以使用
>     """
>     {
>         "type": "function", // 工具的类型是函数
>         "function": {
>             "name": "函数的名称",
>             "description": "函数的描述",
>             "parameters": { // 函数的参数列表
>                 "type": "object", // 参数的类型是一个对象
>                 "properties": { // 对象的属性
>                     "year": {// 第一个属性是 year
>                         "type": "int", // 参数的类型
>                         "description": "year (int): 年份", // 对参数的描述
>                     },
>                     "unit": { // 第二个属性是unit
>                         "type": "string", // unit的类型是字符串
>                         "enum": ["celsius", "fahrenheit"] // unit的可选值是摄氏度或华氏度
>                     }
>                 },
>                 "required": ["year"] // 指定必填参数，必填的参数是year
>             }
>         }
>     }
>     """
>     tools = [
>         {
>             "type": "function",
>             "function": {
>                 "name": "get_cpu_usage",
>                 "description": "获取CPU使用情况",
>                 "parameters": {"type": "object", "properties": {}, }
>             },
>         },
>         {
>             "type": "function",
>             "function": {
>                 "name": "get_memory_usage",
>                 "description": "获取内存使用情况",
>                 "parameters": {"type": "object", "properties": {}, }
>             },
>         },
>         {
>             "type": "function",
>             "function": {
>                 "name": "get_disk_usage",
>                 "description": "获取磁盘使用情况",
>                 "parameters": {"type": "object", "properties": {}, }
>             },
>         },
>         {
>             "type": "function",
>             "function": {
>                 "name": "get_lunar_date",
>                 "description": "获取指定年份、月份和日期的农历日期",
>                 "parameters": {
>                     "type": "object",
>                     "properties": {
>                         "year": {"type": "int", "description": "year (int): 年份", },
>                         "month": {"type": "int", "description": "month (int): 月份", },
>                         "day": {"type": "int", "description": "day (int): 日", },
>                     },
>                     "required": ["year", "month", "day"],
>                 },
>             },
>         },
>     ]
> 
>     # Step 2: 准备，用户的问题
>     system_info = {"role": "system", "content": "尽可能回答以下问题。您可以访问以下工具："}
>     history = [system_info, messages]
> 
>     # Step 3: 告诉模型用户有哪些工具可以使用，用户的问题又是什么
>     response = client.chat.completions.create(
>         model="glm-3-turbo",
>         tools=tools,
>         messages=history,
>         stream=False,
>     )
>     # print(f"choices: {response.choices}")
> 
>     # Step 4: 模型根据你的提问自己区别是否要调用用户的工具，并根据问题来分析出工具的参数应该如何填写，最后返回要调用的工具的信息。
>     assistant_content = response.choices[0].message
>     # print(f"assistant_content: {assistant_content}")
> 
>     # Step 5: 获取工具信息
>     tool_calls = assistant_content.tool_calls
>     # print(f"tool_calls: {tool_calls}")
> 
>     # Step 6: 根据返回的工具信息，动态执行工具并获取执行结果; 如果 tool_calls 为空就不执行
>     for tool_call in tool_calls or []:
>         # print(f"tool_call: {tool_call}")
> 
>         # Step 6.1: 获取方法所有信息
>         function = tool_call.function
>         # print(f"function: {function}")
> 
>         # Step 6.2: 提取方法名
>         function_name = function.name
>         # print(f"function_name: {function_name}")
> 
>         # Step 6.3: 提取方法参数，将字符串形式的参数转换成字典
>         arguments = json.loads(function.arguments)
>         # print(f"arguments: {arguments}")
> 
>         # Step 6.4: 获取对应的函数对象
>         function = globals().get(function_name)
> 
>         # Step 6.5: 动态执行函数
>         if function:
>             # 动态执行函数并获取结果
>             result = function(**arguments)
>             # 将用户提问与工具返回的信息进行拼接
>             # TODO 注意：工具返回的结果最好是【字符串字典】格式，例如：{'role': 'tool', 'tool_call_id': 'call_8530406551538221399', 'content': "{'year': 2099, 'month': 1, 'day': 16}"}}
>             # TODO 只有这样，模型才能更好地理解。已经尝试过仅返回字符串给模型，但效果非常不佳。
>             history.append({"role": "tool", "tool_call_id": tool_call.id, "content": str(result)})
>             # print(f"执行方法 {function_name}\n    结果为：{result}")
>         else:
>             print(f"找不到方法 {function_name}")
> 
>     return history
> 
> 
> if __name__ == "__main__":
>     # 2099年2月5日的农历时间是多少？
>     # 获取CPU使用情况。
>     # 获取内存使用情况。
>     # 获取磁盘使用情况。
>     messages = {"role": "user", "content": "2099年2月5日的农历时间是多少？"}
> 
>     new_messages = exec_tools(messages)
>     print(new_messages)
> 
>     second_response = client.chat.completions.create(
>         model="glm-3-turbo",
>         messages=new_messages,
>         stream=False,
>         temperature=0.1,
>     )
>     print(second_response.choices[0].message.content)
> ```

* * *

# 使用离线方式加载模型

```python
import datetime
import os

import psutil  # pip install psutil
from lunardate import LunarDate  # pip install lunardate
from transformers import AutoTokenizer, AutoModel


def bytes_to_human_readable(bytes_value):
    """
    将字节数转换为可读的字符串，带有相应的大小参数（GB、MB等）

    Args:
        bytes_value (int): 字节值

    Returns:
        str: 可读的字符串
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024:
            return f"{round(bytes_value)} {unit}"
        bytes_value /= 1024


def get_cpu_usage():
    """
    获取CPU使用率

    Returns:
        dict: 包含CPU使用率的字典，键为'CPU使用率'，值为当前CPU使用率（百分比）
    """
    return {"CPU使用率": psutil.cpu_percent(interval=1)}


def get_memory_usage():
    """
    获取内存使用情况

    Returns:
        dict: 包含内存使用情况的字典，包括总内存、可用内存、已使用内存、空闲内存和内存使用率
    """
    mem = psutil.virtual_memory()
    return {
        "总内存": bytes_to_human_readable(mem.total),
        "可用内存": bytes_to_human_readable(mem.available),
        "已使用内存": bytes_to_human_readable(mem.used),
        "空闲内存": bytes_to_human_readable(mem.free),
        "内存使用率": mem.percent
    }


def get_disk_usage():
    """
    获取磁盘使用情况

    Returns:
        dict: 包含磁盘使用情况的字典，键为磁盘设备名，值为包括总磁盘空间、已使用磁盘空间、剩余磁盘空间和磁盘使用率的子字典
    """
    partitions = psutil.disk_partitions()
    disk_usage = {}
    for partition in partitions:
        usage = psutil.disk_usage(partition.mountpoint)
        disk_usage[partition.device] = {
            "总磁盘空间": bytes_to_human_readable(usage.total),
            "已使用磁盘空间": bytes_to_human_readable(usage.used),
            "剩余磁盘空间": bytes_to_human_readable(usage.free),
            "磁盘使用率": usage.percent
        }
    return disk_usage


def get_lunar_date(year, month, day):
    """
    获取指定年份、月份和日期的农历日期

    Args:
        year (int): 年份
        month (int): 月份
        day (int): 日

    Returns:
        dict: 农历日期
    """
    lunar_date = LunarDate.fromSolarDate(year, month, day)
    return {
        "year": lunar_date.year,
        "month": lunar_date.month,
        "day": lunar_date.day
    }


def get_current_time():
    """
    获取当前时间

    Returns:
        dict: 返回包含当前的字典
    """
    current_time = datetime.datetime.now()
    return {"当前时间": current_time}


# -----------------------------------------------------------------------------------

MODEL_PATH = os.environ.get('MODEL_PATH', '/data/LLM/THUDM/chatglm3-6b')
TOKENIZER_PATH = os.environ.get("TOKENIZER_PATH", MODEL_PATH)

tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_PATH, trust_remote_code=True)
client = AutoModel.from_pretrained(MODEL_PATH, trust_remote_code=True).cuda().eval()


def exec_tools(message):
    # Step 1: 准备，用户有哪些工具可以使用
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_cpu_usage",
                "description": "获取CPU使用情况",
                "parameters": {"type": "object", "properties": {}, }
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_memory_usage",
                "description": "获取内存使用情况",
                "parameters": {"type": "object", "properties": {}, }
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_disk_usage",
                "description": "获取磁盘使用情况",
                "parameters": {"type": "object", "properties": {}, }
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_lunar_date",
                "description": "获取指定年份、月份和日期的农历日期",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "year": {"type": "int", "description": "year (int): 年份", },
                        "month": {"type": "int", "description": "month (int): 月份", },
                        "day": {"type": "int", "description": "day (int): 日", },
                    },
                    "required": ["year", "month", "day"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_current_time",
                "description": "获取当前时间",
                "parameters": {"type": "object", "properties": {}, }
            },
        },
    ]

    # Step 2: 准备，用户的问题
    system_info = {"role": "system", "content": "尽可能回答以下问题。您可以访问以下工具：", "tools": tools}
    history = [system_info]
    # print(f"history: {history}")

    # Step 3: 告诉模型用户有哪些工具可以使用，用户的问题又是什么
    response, _ = client.chat(tokenizer, message, history=history, role="user")
    print(f"response: {response}")

    if isinstance(response, dict) and "name" in response:
        # Step 4: 提取方法名
        function_name = response["name"]
        # print(f"function_name: {function_name}")

        # Step5: 提取方法参数，将字符串形式的参数转换成字典
        arguments = response["parameters"]
        # print(f"arguments: {arguments}")

        # Step 6: 获取对应的函数对象
        function = globals().get(function_name)

        # Step 7: 动态执行函数
        if function:
            # 动态执行函数并获取结果
            result = function(**arguments)
            # 将用户提问与工具返回的信息进行拼接
            # role in ["system", "user", "assistant", "observation"]
            history.append({"role": "observation", "content": str(result)})
            # print(f"执行方法 {function_name}\n    结果为：{result}")
            return None, history
        else:
            print(f"找不到方法 {function_name}")

    return response, None


if __name__ == "__main__":
    # 2099年2月5日的农历时间是多少？
    # 获取CPU使用情况。
    # 获取内存使用情况。
    # 获取磁盘使用情况。
    # 现在几点了？

    print("欢迎使用 ChatGLM3-6B模型 工具调用功能，输入内容即可进行对话，exit 终止程序")
    while True:
        query = input("\n用户：")

        if query.strip() == "exit":
            break
        print("\nChatGLM：", end="")

        # 执行工具
        new_response, new_history = exec_tools(query)
        print("------------------------------------------------")
        print(new_response)
        print("------------------------------------------------")
        if new_history:
            # 概述工具查询的结果
            response, _ = client.chat(tokenizer, "根据'监控工具'返回的信息，回答'用户'的提问。", history=new_history, role="user")
            print(response, end="\n", flush=True)
        elif new_response:
            print(new_response, end="\n", flush=True)

```

---

---

---

# 封装成适用于在项目中使用的工具类
``` python
import inspect
import json
from types import GenericAlias
from typing import get_origin, Annotated


class FunctionCall:
    def __init__(self):
        # 获取调用 FunctionCall 的模块信息并赋值给 METHOD_PATH
        self.METHOD_PATH = inspect.getmodule(inspect.stack()[1][0])
        self._TOOL_DESCRIPTIONS = {}

    # 定义一个装饰器函数，用于注册工具函数
    def register_tool(self, func: callable):
        # 获取工具函数的名称
        tool_name = func.__name__
        # 获取工具函数的文档字符串并去除首尾空白字符
        tool_description = inspect.getdoc(func).strip()
        # 获取工具函数的参数信息
        python_params = inspect.signature(func).parameters
        # 用于存储工具函数的参数信息的列表
        tool_params = []
        # 遍历工具函数的参数
        for name, param in python_params.items():
            # 跳过函数的关键字参数 'self' 和 'cls'
            if name in ('self', 'cls'):
                continue
            # 获取参数的注释类型
            annotation = param.annotation
            # 检查参数的注释类型是否为空
            if annotation is inspect.Parameter.empty:
                # 如果为空，抛出类型错误，指示参数缺少类型注释
                raise TypeError(f"参数 `{name}` 缺少类型注释")
            # 检查参数的注释类型是否为 Annotated
            if get_origin(annotation) != Annotated:
                # 如果不是，抛出类型错误，指示参数的注释类型必须为 typing.Annotated
                raise TypeError(f"`{name}` 的注释类型必须为 typing.Annotated")

            # 获取参数的实际类型和元数据
            typ, (description, required) = annotation.__origin__, annotation.__metadata__
            # 将参数的实际类型转换为字符串，如果是泛型则使用GenericAlias生成别名
            typ: str = str(typ) if isinstance(typ, GenericAlias) else typ.__name__
            # 检查参数的描述是否为字符串
            if not isinstance(description, str):
                # 如果不是，抛出类型错误，指示参数的描述必须为字符串
                raise TypeError(f"`{name}` 的描述必须为字符串")
            # 检查参数的必需性是否为布尔值
            if not isinstance(required, bool):
                # 如果不是，抛出类型错误，指示参数的必需性必须为布尔值
                raise TypeError(f"`{name}` 的必需性必须为布尔值")

            # 将参数的信息添加到工具参数列表中
            tool_params.append({
                "name": name,
                "description": description,
                "type": typ,
                "required": required
            })
        # 构建工具描述信息的字典
        tool_def = {
            "name": tool_name,
            "description": tool_description,
            "params": tool_params
        }
        # 将工具描述信息存储在全局字典中，以工具名称为键
        self._TOOL_DESCRIPTIONS[tool_name] = tool_def

        # 返回原始的工具函数
        return func

    # 获取工具方法列表
    def get_tools(self) -> list:
        tools_list = []
        for tool_name, tool_info in self._TOOL_DESCRIPTIONS.items():
            parameters = []
            for param_info in tool_info["params"]:
                parameters.append({
                    "name": param_info["name"],
                    "type": param_info["type"],
                    "description": param_info["description"],
                    "required": param_info["required"],  # 添加此行以包含参数的必需性信息
                })

            tool_data = {
                "type": "function",
                "function": {
                    "name": tool_name,
                    "description": tool_info["description"],
                    "parameters": {
                        "type": "object",
                        "properties": {param["name"]: {"type": param["type"], "description": param["description"]} for param in parameters},
                        "required": [param["name"] for param in parameters if param["required"]]
                    }
                }
            }
            tools_list.append(tool_data)
        return tools_list

    # 执行模型返回的工具方法
    def exec_tools(self, tool_calls, history, clazz=None):
        """
        执行模型返回的工具方法。

        Args:
            tool_calls (list): 模型返回的工具方法列表。
            history (list): 对话历史列表。
            clazz (object): 类对象，如果注释的方法属于类内方法，就需要传入类对象。

        Returns:
            list: 更新后的对话历史列表。
        """
        # 根据返回的工具信息，动态执行工具并获取执行结果; 如果 tool_calls 为空就不执行
        for tool_call in tool_calls or []:
            function = tool_call.function

            function_name = function.name
            arguments = json.loads(function.arguments)

            # 使用getattr动态获取函数
            if clazz:
                # 以类对象的方式执行
                function = getattr(clazz, function_name, None)
            else:
                # 以独立函数的方式执行
                function = getattr(self.METHOD_PATH, function_name, None)

            # 动态执行函数
            if function:
                result = function(**arguments)
                history.append({"role": "tool", "tool_call_id": tool_call.id, "content": str(result)})
            else:
                print(f"找不到方法 {self.METHOD_PATH}/{function_name}")

        return history

# @register_tool
# def get_cpu_usage():
#     """
#     获取CPU使用情况。
#
#     Returns: 包含CPU使用率的字典。
#     """
#     import psutil
#     return {"CPU使用率": psutil.cpu_percent(interval=1)}
#
#
# @register_tool
# def get_lunar_date(year: Annotated[int, "农历年份", True], month: Annotated[int, "农历月份", True], day: Annotated[int, "农历日", False]):
#     """
#     获取指定年份、月份和日期的农历日期
#
#     Args:
#         year (int): 年份
#         month (int): 月份
#         day (int): 日
#
#     Returns:
#         dict: 农历日期
#     """
#     from lunardate import LunarDate
#     lunar_date = LunarDate.fromSolarDate(year, month, day)
#     return {
#         "year": lunar_date.year,
#         "month": lunar_date.month,
#         "day": lunar_date.day
#     }


# if __name__ == '__main__':
#     from zhipuai import ZhipuAI
#
#     client = ZhipuAI(
#         api_key="your_api_key"
#     )
#
#     # Step 1: 准备，用户的问题
#     system_info = {"role": "system", "content": "尽可能回答以下问题。您可以访问以下工具："}
#     messages = {"role": "user", "content": "获取CPU使用情况"}
#     history = [system_info, messages]
#
#     # Step 2: 告诉模型用户有哪些工具可以使用，用户的问题又是什么
#     response = client.chat.completions.create(
#         model="glm-3-turbo",
#         components=get_tools(),
#         messages=history,
#         stream=False,
#     )
#
#     # Step 3: 解析模型返回的JSON字符串
#     assistant_content = response.choices[0].message
#
#     # Step 4: 获取工具方法列表
#     tool_calls = assistant_content.tool_calls
#
#     # Step 5: 执行模型返回的工具方法
#     new_messages = exec_tools(tool_calls, history)
#
#     # Step 6: 再次调用模型，将新的对话历史传递给模型
#     second_response = client.chat.completions.create(
#         model="glm-3-turbo",
#         messages=new_messages,
#         stream=False,
#         temperature=0.1,
#     )
#     print(second_response.choices[0].message.content)

```
