---
title: "windows 批处理脚本"
date: "2019-04-11"
categories: 
  - "非技术文档"
---

##### 使用batch 脚本批量控制 gitlab版本

```batch
@ECHO off
:: developer author Eric.mao

::设置本地为延迟环境变量扩展
SETLOCAL EnableDelayedExpansion

ECHO 注: 请将此脚本置于Git项目同级目录中执行:

SET Data[0]=paas_management paas-rpc-outer-interface paas-rpc-inner-interface paas-po paas-parent paas-common-test paas-common-resource paas-common-logtrigger paas-common-jms paas-common-imports paas-common-dict  

SET Data[1]=003-paas-static 004-paas-login 005-paas-system 006-paas-importcheck 007-paas-filesystem 008-paas-platform 009-paas-metadata 012-paas-gensdk 013-paas-comet 014-paas-bloom 015-paas-logs 018-paas-share 017-paas-schedule 020-paas-position 021-paas-sftp 022-paas-msgimpexp 023-paas-workflow   024-paas-dcupload 025-paas-dcmapping 026-paas-dcqualitytesting 027-paas-dcdeliver 028-paas-commonqt 029-paas-workday

SET Data[2]=101-innovent-innoventweb 102-innovent-innoventreports 120-innovent-innoventpos innovent-parent

SET Data[3]=201-hrbm-hrbmweb 220-hrbm-hrbmpos hrbm-parent

SET Data[4]=sino-app-starter-rabbitmq sino-app-starter-elasticsearch sino-app-starter-hessian

SET Data[5]=401-pfizer-login 402-pfizer-workflow 403-pfizer-pos 404-pfizer-edi 405-pfizer-workplan 406-pfizer-collect 407-pfizer-portal 408-pfizer-dealfile 409-pfizer-mdm 410-pfizer-fetcher 411-pfizer-downloader 412-pfizer-ftpbackup

SET Data[6]=501-kl-web 502-kl-kelunpos 503-kl-kelunworkflow

SET Data[a]=%Data[0]% %Data[1]% %Data[2]% %Data[3]% %Data[4]%

:init
    ECHO.
    COLOR 2
    ECHO ***********菜单***********
    ECHO [0] 克隆项目
    ECHO [1] 拉取远程分支到本地
    ECHO [2] 切换本地分支
    ECHO [3] pull项目
    ECHO [99] 退出
    ECHO **************************

    SET /p param=请选择:
        IF /I %param%==0 GOTO clone
        IF /I %param%==1 GOTO branch
        IF /I %param%==2 GOTO local
        IF /I %param%==3 GOTO pull
        IF /I %param%==99 EXIT

:: 创建函数 通用菜单
:menu
    ECHO.
    :: `1% 表示接收传入的第一个参数`
    ECHO ********** %1 **********
    ECHO [0] paas共用组件项目
    ECHO [1] paas平台项目
    ECHO [2] 信达项目
    ECHO [3] 华润北贸
    ECHO [4] 数据处理
    ECHO [5] 辉瑞
    ECHO [6] 科轮
    ECHO [a] 所有
    ECHO [9] 上一页
    ECHO ******************************

    SET /p param=请选择:
        IF /I %param%==9 GOTO init
        FOR /F "usebackq delims== tokens=2" %%I IN (`SET Data[%param%]`) DO (
          SET result=%%I
        )
        GOTO :EOF

:: 克隆模块
:clone
    CALL :menu 克隆项目
    FOR %%I IN (%result%) DO (
        git clone git@git.paas.dev:root/%%I.git && ECHO ======    %%I      ====== && git --git-dir=%%I/.git branch -a
    )
    :: 执行完后返回到clone位置
    GOTO clone

:: 拉分支模块
:branch
    CALL :menu 拉取远程分支到本地
    SET /p branch=请输入分支名:
        FOR %%I IN (%result%) DO (
            git --git-dir=%%I/.git --work-tree=%%I checkout -b !branch! origin/!branch! && ECHO ======    %%I      ====== && git --git-dir=%%I/.git branch -a
        )
        :: 执行完后返回到branch位置
        GOTO branch

:: 切分支模块
:local
    CALL :menu 切换本地分支
    SET /p branch=请输入分支名:
        FOR %%I IN (%result%) DO (
            ECHO ======    %%I      ====== && git --git-dir=%%I/.git --work-tree=%%I checkout !branch! && git --git-dir=%%I/.git branch -a
        )
        :: 执行完后返回到local位置
        GOTO local

:: 拉取项目
:pull
    CALL :menu pull项目
    FOR %%I IN (%result%) DO (
        ECHO ======    %%I      ====== && git --git-dir=%%I/.git --work-tree=%%I pull
    )
    :: 执行完后返回到pull位置
    GOTO pull
```
