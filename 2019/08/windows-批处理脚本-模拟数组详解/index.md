---
title: "windows 批处理脚本 模拟数组详解"
date: "2019-08-30"
categories: 
  - "非技术文档"
---

##### 模拟数组

```batch
@ECHO off
:: developer author Eric.mao

::设置本地为延迟环境变量扩展
SETLOCAL EnableDelayedExpansion

SET Data[0].Name=Data1
SET Data[0].Value=Value1

SET Data[1].Name=Data2
SET Data[1].Value=Value2


:: 创建默认索引
SET index=0
:: 创建接收结果属性
SET result.Name=0
SET result.Value=0

:: `usebackq 把单引号字符串作为命令`
:: `delims 告诉for每一行应该拿什么作为分隔符，默认的分隔符是空格和tab键; 这里是以点和等号做分割 .=`
:: `tokens 作用就是当你通过delims将每一行分为更小的元素时，由tokens来控制要取哪一个或哪几个。`
:: `       以点和等号做分割, 从结果中获取第一列至第三列，tokens=1-3，全部显示则使用通配符tokens=*。`
:: `       怎么多出一个 %%J %%K ？`
:: `       这是因为你的tokens后面要取每一行的第一列至第三列，用%%I表示第一列，用%%J表示第二列，用%%K表示第二列。`
:: `       并且必须是按照英文字母顺序排列的，%%J不能换成%%K，因为I后面是J。`
FOR /F "usebackq delims=.= tokens=1-3" %%I IN (`SET Data[%index%]`) DO (
  :: 动态替换属性值
  SET result.%%J=%%K
)

ECHO %result.Name%
ECHO %result.Value%

PAUSE
```

* * *

* * *

* * *

##### 复用菜单

```batch
@ECHO off
:: developer author Eric.mao

::设置本地为延迟环境变量扩展
SETLOCAL EnableDelayedExpansion

SET Data[0].Name=Data_0
SET Data[0].Value=Value_0
SET Data[1].Name=Data_1
SET Data[1].Value=Value_1

COLOR 2

:init
    :: `CALL :函数名`
    CALL :menu
    :: 创建接收结果属性
    SET result.Name=0
    SET result.Value=0
        :: `usebackq 把单引号字符串作为命令`
        :: `delims 告诉for每一行应该拿什么作为分隔符，默认的分隔符是空格和tab键; 这里是以点和等号做分割 .=`
        :: `tokens 作用就是当你通过delims将每一行分为更小的元素时，由tokens来控制要取哪一个或哪几个。`
        :: `       以点和等号做分割, 从结果中获取第一列至第三列，tokens=1-3，全部显示则使用通配符tokens=*。`
        :: `       怎么多出一个 %%J %%K ？`
        :: `       这是因为你的tokens后面要取每一行的第一列至第三列，用%%I表示第一列，用%%J表示第二列，用%%K表示第二列。`
        :: `       并且必须是按照英文字母顺序排列的，%%J不能换成%%K，因为I后面是J。`
        FOR /F "usebackq delims=.= tokens=1-3" %%I IN (`SET Data[%index%]`) DO (
          SET result.%%J=%%K
        )

        ECHO %result.Name%
        ECHO %result.Value%
        :: `跳转到:init标签`
        GOTO init

:menu
    ECHO.
    ECHO ***************复用菜单***************
    SET /p param=请输入0或1:
        :: 接收索引
        SET index=%param%
        :: `GOTO :EOF 在批处理作用主要有二：`
        :: `1、在无call的情况下，会直接退出批处理，此时等同于exit`
        :: `2、在有call的情况下，会中止call，继续执行其他命令`
        GOTO :EOF

PAUSE
```
