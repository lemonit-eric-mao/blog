---
title: 'Java 定时执行 Linux shell 命令'
date: '2018-08-13T11:23:45+00:00'
status: publish
permalink: /2018/08/13/java-%e5%ae%9a%e6%97%b6%e6%89%a7%e8%a1%8c-linux-shell-%e5%91%bd%e4%bb%a4
author: 毛巳煜
excerpt: ''
type: post
id: 2268
category:
    - Java
tag: []
post_format: []
hestia_layout_select:
    - default
---
```java
package com.bqhx.officeautomation.user.center;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.ScheduledThreadPoolExecutor;
import java.util.concurrent.TimeUnit;

/**
 * 测试 java 原生 定时器
 *
 * @author: mao-siyu
 * @date: 18-8-13 10:13
 * @description:
 */
public class TestTimer {

    public static void main(String[] args) {
        int corePoolSize = 1000;
        // 创建时间线程池
        ScheduledExecutorService executorService = new ScheduledThreadPoolExecutor(corePoolSize);
        // 每隔1秒触发一次
        executorService.scheduleAtFixedRate(() -> {
            try {
                String[] command = {"/bin/sh", "-c", "ifconfig | grep inet"};
                String result = execShell(command);
                System.out.println(result);
            } catch (IOException e) {
                e.printStackTrace();
            }
        }, 0, 100, TimeUnit.SECONDS);
    }

    /**
     * 执行 shell 字符串为参数
     *
     * @param command
     * @return
     * @throws IOException
     */
    private static String execShell(String command) throws IOException {

        Process process = Runtime.getRuntime().exec(command);
        return execCommand(process);
    }

    /**
     * 执行 shell 重载数组为参数
     *
     * @param command
     * @return
     * @throws IOException
     */
    private static String execShell(String[] command) throws IOException {

        Process process = Runtime.getRuntime().exec(command);
        return execCommand(process);
    }

    /**
     * 执行
     *
     * @param process
     * @return
     * @throws IOException
     */
    private static String execCommand(Process process) throws IOException {

        BufferedReader input = new BufferedReader(new InputStreamReader(process.getInputStream()));

        StringBuffer stringBuffer = new StringBuffer();
        String line;

        while ((line = input.readLine()) != null) {
            stringBuffer.append(line).append("\n");
        }

        input.close();

        return stringBuffer.toString();
    }
}

```