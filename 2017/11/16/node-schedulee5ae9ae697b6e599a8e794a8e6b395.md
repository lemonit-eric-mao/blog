---
title: node-schedule定时器用法
date: '2017-11-16T11:02:02+00:00'
status: publish
permalink: /2017/11/16/node-schedule%e5%ae%9a%e6%97%b6%e5%99%a8%e7%94%a8%e6%b3%95
author: 毛巳煜
excerpt: ''
type: post
id: 109
category:
    - node.js
tag: []
post_format: []
hestia_layout_select:
    - default
---
```javascript
===========================================================================
============================= Cron风格定时器 ================================
===========================================================================


var schedule = require('node-schedule');

schedule.scheduleJob('30 * * * * *', function () {
    console.log('每分钟的第30秒触发一次:' + new Date());
});


// 参数位置图解

*  *  *  *  *  *
┬  ┬  ┬  ┬  ┬  ┬
│  │  │  │  │  │
│  │  │  │  │  └────────── day of week (0 - 7) (0 or 7 is Sun) 周几
│  │  │  │  └───────────── month (1 - 12)                      月
│  │  │  └──────────────── day of month (1 - 31)               日
│  │  └─────────────────── hour (0 - 23)                       时
│  └────────────────────── minute (0 - 59)                     分
└───────────────────────── second (0 - 59, OPTIONAL)           秒



// 参数详解

6个占位符从左到右分别代表：秒、分、时、日、月、周几
'*'表示通配符，匹配任意，当秒是'*'时，表示任意秒数都触发，其它类推
下面可以看看以下传入参数分别代表的意思


每分钟的第30秒触发： '30 * * * * *'

每小时的1分30秒触发 ：'30 1 * * * *'

每天的凌晨1点1分30秒触发 ：'30 1 1 * * *'

每月的1日1点1分30秒触发 ：'30 1 1 1 * *'

2016年的1月1日1点1分30秒触发 ：'30 1 1 1 2016 *'

每周1的1点1分30秒触发 ：'30 1 1 * * 1'


===========================================================================
=========================== 对象文本语法定时器 =============================
===========================================================================


var schedule = require('node-schedule');

var rule = new schedule.RecurrenceRule();
rule.dayOfWeek = 2;   // 周几 (0 - 7) (0 or 7 is Sun)
rule.month = 3;       // 月   (1 - 12)
rule.dayOfMonth = 1;  // 日   (1 - 31)
rule.hour = 1;        // 时   (0 - 23)
rule.minute = 42;     // 分   (0 - 59)
rule.second = 0;      // 秒   (0 - 59, OPTIONAL)

schedule.scheduleJob(rule, function () {
    console.log('scheduleRecurrenceRule:' + new Date());
});

```