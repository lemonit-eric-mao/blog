---
title: "Python 计算两个日期间的工作日，去除周末节假日"
date: "2020-12-27"
categories: 
  - "python"
---

```python
#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time          : 2020/12/27 19:41
# @Author        : Eric.Mao
# @FileName      : main.py
# @Software      : PyCharm
# @Blog          : http://www.dev-share.top/
# @Dependence    : pip3 install chinesecalendar

"""
is_workday： 判断是否为工作日，返回布尔值
is_holiday： 判断是否为节假日，返回布尔值
"""
from chinese_calendar import is_workday, is_holiday
from datetime import datetime, timedelta


# 字符串格式或日期串格式的处理
def day_format(start_date, end_date):
    # 字符串格式日期的处理
    if type(start_date) == str:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    if type(end_date) == str:
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    # 开始日期大，颠倒开始日期和结束日期
    if start_date > end_date:
        start_date, end_date = end_date, start_date

    return start_date, end_date


# 计算两个日期间的工作日天数
# start_date: 开始时间
# end_date: 结束时间
def work_days(start_date, end_date):
    start_date, end_date = day_format(start_date, end_date)

    counts = 0
    while True:
        if start_date > end_date:
            break
        if is_workday(start_date):
            counts += 1
        start_date += timedelta(days=1)
    return counts


# 计算两个日期间的交易日天数
# start_date: 开始时间
# end_date: 结束时间
def trade_days(start_date, end_date):
    start_date, end_date = day_format(start_date, end_date)

    counts = 0
    while True:
        if start_date > end_date:
            break
        if is_holiday(start_date) or start_date.weekday() == 5 or start_date.weekday() == 6:
            start_date += timedelta(days=1)
            continue
        counts += 1
        start_date += timedelta(days=1)
    return counts


if __name__ == '__main__':
    start = '2021-01-01'
    end = '2021-02-10'
    print(f"{start} ~ {end} 间的工作日： {work_days(start, end)}天")
    print(f"{start} ~ {end} 间的交易日： {trade_days(start, end)}天")

```
