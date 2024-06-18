---
title: 'AI 工具调用 Function Call 工作原理'
date: '2024-04-01T08:19:37+00:00'
status: publish
permalink: /2024/04/01/ai-%e5%b7%a5%e5%85%b7%e8%b0%83%e7%94%a8-function-call-%e5%b7%a5%e4%bd%9c%e5%8e%9f%e7%90%86
author: 毛巳煜
excerpt: ''
type: post
id: 10761
category:
    - 人工智能
tag: []
post_format: []
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
hestia_layout_select:
    - sidebar-right
---
AI 工具调用
=======

工作原理
----

> 1. 大语言模型必须具备`"Function Call"`功能。
> 2. 你可以随意编写一个方法，但关键在于让大型模型了解哪些方法是可以做为工具使用的。
> 3. 要让模型知道有哪些方法可以做为工具使用，需要按照模型熟悉的数据格式来提供信息，具体如下： 
>   - `system_info = {"role": "system", "content": "尽可能回答以下问题。你可以利用以下工具：", "tools": tools}`
> 4. 结合用户提问的提示词，由大型模型来判断并决定使用哪个方法以及为哪些参数进行赋值。
> 5. 模型会指导你使用哪些工具方法来获取所需数据。
> 6. 利用Python的动态执行函数功能，执行指定的工具方法。
> 7. 将工具方法返回的信息追加到历史记录中，并返回给模型，以供后续推理任务使用。

必要条件
----

> 大语言模型本身必须要支持这样的能力

适用场景
----

> 让大语言模型通过`模型自身对提示`的理解，自主选择调用合理的函数来满足`提问需求`

应用开发
----

<div style="overflow:hidden; clear:both; width: 100%; height: 40px; position: relative;">- - - - - -

 <span style="position: absolute;top: 50%;left: 50%; transform: translate(-50%, -50%); background-color: white;">以下为隐藏内容</span> </div> > ```python
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
>         if bytes_value 
> ```

- - - - - -

使用离线方式加载模型
==========

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
        if bytes_value 
```