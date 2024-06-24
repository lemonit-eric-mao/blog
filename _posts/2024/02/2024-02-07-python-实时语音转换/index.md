---
title: "Python 实时语音转换"
date: "2024-02-07"
categories: 
  - "python"
  - "人工智能"
---

# 实时语音转换

```python
import queue  # 导入队列模块，用于在多线程中安全地传递数据
import sys
import time  # 导入Time库，用于添加延迟
import wave

import keyboard  # 导入Keyboard库，用于监听键盘事件
import numpy as np  # 导入NumPy库，用于处理音频数据
import sounddevice as sd  # 导入SoundDevice库，用于录音和播放音频


class AudioRecorder:
    def __init__(self, sample_rate=44100, channels=1):
        """
        初始化录音器对象

        参数:
        sample_rate (int): 音频采样率，默认为16000Hz
        """
        self.sample_rate = sample_rate  # 设置音频采样率
        self.channels = channels  # 设置音频通道数
        self.q = queue.Queue()  # 创建队列，用于存储音频数据
        self.frames = []  # 初始化音频数据帧列表

    def callback(self, indata, frames, time, status):
        """
        回调函数，用于获取音频数据并放入队列中

        参数:
        indata: 输入音频数据
        frames: 帧数
        time: 时间
        status: 状态
        """
        if status:
            print(status, file=sys.stderr)  # 打印状态信息（如果有）
        self.q.put(indata.copy())  # 将音频数据放入队列中，保证数据的线程安全

    def open_audio_stream(self):
        """
        打开音频流

        返回:
        sd.InputStream: 返回打开的音频流对象
        """
        return sd.InputStream(callback=self.callback, channels=self.channels, samplerate=self.sample_rate)  # 打开音频流，设置回调函数以获取音频数据

    def record_audio(self):
        """
        录制音频

        录制持续到空格键释放，并实时处理音频数据
        """
        recording = True  # 设置录音状态标志为True
        self.frames = []  # 清空音频数据帧列表
        with self.open_audio_stream():  # 打开音频流
            while recording:  # 在录音状态下
                time.sleep(0.01)  # 添加短暂延迟，减少CPU占用

                # 开始录音
                audio_chunk = self.q.get()  # 获取音频数据块
                audio_numpy = np.concatenate([audio_chunk])  # 将音频数据块连接成NumPy数组
                audio_numpy = audio_numpy.flatten()  # 将多维数组扁平化
                self.frames.append(audio_numpy)  # 将音频数据帧添加到音频数据帧列表中

                # 实时处理音频数据
                self.process_audio(audio_numpy)  # 调用处理音频数据的方法

                # 结束录音
                if not keyboard.is_pressed('space'):  # 如果空格键未被按下
                    recording = False  # 设置录音状态标志为False，结束录音
                    self.save_local()  # 保存为音频文件到本地

    def process_audio(self, audio_numpy):
        """
        处理音频数据

        在这里添加对音频数据的处理逻辑，比如传递给模型进行实时解析

        参数:
        audio_numpy (ndarray): 包含音频数据的NumPy数组
        """
        print(audio_numpy.tolist())
        pass

    def save_local(self, filename='recording.wav'):
        # 将所有帧数据连接成一个数组
        audio_data = np.concatenate(self.frames)

        # 浮点数范围归一化到int16的范围，并转换类型
        audio_data = (audio_data * 32767).astype(np.int16)

        # 使用wave模块保存WAV文件
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(2)  # 设置样本宽度为2，一般表示16位PCM
            wf.setframerate(self.sample_rate)
            wf.writeframes(audio_data.tobytes())

    def run(self):
        """
        运行录音器

        在同时按住空格键和Ctrl键时开始录音，并持续录音直到释放这两个键
        """
        print("按住空格键和Ctrl键开始录音，放开这两个键结束录音。")  # 打印提示信息
        while True:  # 无限循环
            if keyboard.is_pressed('space') and keyboard.is_pressed('ctrl'):  # 如果同时按下空格键和Ctrl键
                print("开始录音...")  # 打印开始录音提示
                self.record_audio()  # 开始录音
                print("录音结束")  # 打印录音结束提示
                print("按住空格键和Ctrl键开始下一次录音。")  # 提示用户可以开始下一次录音
            time.sleep(0.1)  # 添加延迟，减少CPU占用


# 创建录音器对象并执行程序
recorder = AudioRecorder()  # 创建录音器对象
recorder.run()  # 执行录音器对象的run()方法，开始录音

```
