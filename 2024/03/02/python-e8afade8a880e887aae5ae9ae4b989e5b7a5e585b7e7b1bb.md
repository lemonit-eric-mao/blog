---
title: 'Python 语言自定义工具类'
date: '2024-03-02T02:07:47+00:00'
status: private
permalink: /2024/03/02/python-%e8%af%ad%e8%a8%80%e8%87%aa%e5%ae%9a%e4%b9%89%e5%b7%a5%e5%85%b7%e7%b1%bb
author: 毛巳煜
excerpt: ''
type: post
id: 10692
category:
    - Python
tag: []
post_format: []
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
hestia_layout_select:
    - sidebar-right
---
自定义logger
---------

```python
from datetime import datetime

class Logger:
    # ANSI转义码颜色常量
    # 定义了一些 ANSI 转义码，用于控制终端输出的颜色
    RESET = '\033[0m'  # 重置所有属性
    BOLD = '\033[1m'  # 粗体
    UNDERLINE = '\033[4m'  # 下划线
    BLACK = '\033[30m'  # 黑色
    RED = '\033[31m'  # 红色
    GREEN = '\033[32m'  # 绿色
    DEEP_GREEN = '\033[38;2;0;128;0m'  # 深绿色
    YELLOW = '\033[33m'  # 黄色
    BLUE = '\033[34m'  # 蓝色
    MAGENTA = '\033[35m'  # 紫红色
    CYAN = '\033[36m'  # 青蓝色
    WHITE = '\033[37m'  # 白色

    # 日志级别与颜色映射字典
    # 定义了日志级别与输出颜色的映射关系
    COLORS = {
        'DEBUG': CYAN,
        'INFO': DEEP_GREEN,
        'WARNING': YELLOW,
        'ERROR': RED,
        'CRITICAL': MAGENTA,
    }

    @staticmethod
    def log(level, message):
        # 获取当前时间，并格式化成字符串
        timestamp = datetime.now().strftime(f"{Logger.GREEN}%Y-%m-%d %H:%M:%S{Logger.RESET}")
        # 检查日志级别是否在映射字典中
        if level.upper() in Logger.COLORS:
            color = Logger.COLORS[level.upper()]
            # 输出带有时间戳和颜色的日志
            print(f"{timestamp} | {color}{level.upper()}: {message}{Logger.RESET}")
        else:
            # 如果级别不在字典中，则按照默认方式输出日志
            print(f"{timestamp} | {level.upper()}: {message}")

    @staticmethod
    def debug(msg):
        # 调用 log 方法记录调试信息
        Logger.log("DEBUG", msg)

    @staticmethod
    def info(msg):
        # 调用 log 方法记录信息
        Logger.log("INFO", msg)

    @staticmethod
    def warning(msg):
        # 调用 log 方法记录警告信息
        Logger.log("WARNING", msg)

    @staticmethod
    def error(msg):
        # 调用 log 方法记录错误信息
        Logger.log("ERROR", msg)

    @staticmethod
    def critical(msg):
        # 调用 log 方法记录严重错误信息
        Logger.log("CRITICAL", msg)


if __name__ == "__main__":
    # 测试日志记录器
    Logger.debug("这是一个调试信息")
    Logger.info("这是一个信息")
    Logger.warning("这是一个警告")
    Logger.error("这是一个错误")
    Logger.critical("这是一个严重错误")


```

- - - - - -

- - - - - -

- - - - - -

流式输出代码（此代码不能执行，只描述思路）
---------------------

```python
import json
import requests
from sse_starlette import EventSourceResponse

from utils.logger import Logger  # 导入日志记录工具


def generate_completion_stream(params):
    # 获取FastChat Worker地址
    worker_address = "http://your_fastchat_worker_address"  # 替换为实际的FastChat Worker地址
    Logger.debug(f"发起请求并进行流式返回: {worker_address}")

    # 发送POST请求到FastChat Worker
    response = requests.post(
        worker_address,
        json=params,
        stream=True,  # 设置为流式传输
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


def exec_test():
    result = generate_completion_stream({})
    for r in result:
        Logger.info(r)  # 记录文本输出
    # 返回 EventSourceResponse 对象，具体如何处理取决于你的应用程序
    return EventSourceResponse(result)


if __name__ == '__main__':
    exec_test()


```