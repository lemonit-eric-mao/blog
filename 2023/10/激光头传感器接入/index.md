---
title: "激光头传感器接入"
date: "2023-10-29"
categories: 
  - "树莓派"
---

## 环境准备

> 基于已有的环境，克隆一个新环境，用测试部署倾斜传感器

```bash
## 现有环境
[siyu.mao@raspberrypi (11:30:21) ~]
└─$ conda env list
# conda environments:
#
base                  *  /home/siyu.mao/miniconda3


## 克隆环境
[siyu.mao@raspberrypi (11:29:33) ~]
└─$ conda create -n laser --clone base


## 激活环境
[siyu.mao@raspberrypi (12:51:27) ~]
└─$ conda activate laser
(laser) [siyu.mao@raspberrypi (12:51:35) ~]
└─$


## 确认pip是否可用
(laser) [siyu.mao@raspberrypi (14:55:08) ~]
└─$ which pip
/home/siyu.mao/miniconda3/envs/laser/bin/pip


```

* * *

# 接入`KY008激光头`传感器

## 安装工具依赖包

```bash
(laser) [siyu.mao@raspberrypi (14:56:40) ~]
└─$ pip install RPI.GPIO

```

### 编写python测试代码`laser.py`

> 示例代码，假设您将传感器的信号引脚连接到树莓派的`GPIO 18`引脚 这段代码会控制传感器状态

```python
# 导入RPi.GPIO库，用于树莓派的GPIO控制
import RPi.GPIO as GPIO
import time

if __name__ == "__main__":
    pin_sig = 12  # 使用板子编号12的引脚，该引脚将控制激光头的开关

    # 设置GPIO模式为BOARD模式，按照物理引脚编号
    GPIO.setmode(GPIO.BOARD)

    # 配置指定引脚为输出模式，以便控制激光头
    GPIO.setup(pin_sig, GPIO.OUT)

    # 初始状态设置为高电平，打开激光头
    GPIO.output(pin_sig, GPIO.HIGH)

    try:
        while True:
            print('亮3秒')
            GPIO.output(pin_sig, GPIO.HIGH)  # 将引脚电平设置为高，打开激光头
            time.sleep(3)  # 程序暂停3秒

            print('灭3秒')
            GPIO.output(pin_sig, GPIO.LOW)  # 将引脚电平设置为低，关闭激光头
            time.sleep(3)  # 程序暂停3秒

    except KeyboardInterrupt:
        print('\n Ctrl + C QUIT')

    finally:
        # 清理GPIO资源，将引脚恢复初始状态，以免影响下次使用
        GPIO.cleanup()

```

**测试**

```bash
(laser) [siyu.mao@raspberrypi (15:07:19) /data/laser]
└─$ python laser.py

亮3秒
灭3秒
亮3秒
灭3秒
亮3秒
灭3秒
亮3秒
灭3秒

```
