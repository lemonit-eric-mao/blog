---
title: "ASR媒体流转换文字"
date: "2024-04-08"
categories: 
  - "人工智能"
---

# JavaScript 展示获取视频流

```markup
<!DOCTYPE html>
<html>
<head>
    <!-- 设置文档使用的字符编码 -->
    <meta charset="UTF-8">
    <!-- 设置 viewport 元标签，以确保页面在移动设备上正确显示和缩放 -->
    <meta name="viewport" content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <!-- 启用苹果移动设备的全屏模式 -->
    <meta name="apple-mobile-web-capable" content="yes">
    <!-- 页面标题 -->
    <title>展示获取视频流</title>
    <!-- 页面样式 -->
    <style>
        /* 设置视频元素样式 */
        #videoId {
            width: 512px;
            height: 256px;
        }

        /* 按钮样式 */
        .button-like-link {
            display: inline-block;
            padding: 10px 20px;
            background-color: #f0f0f0;
            border: 1px solid #ddd;
            text-decoration: none;
            color: #333;
            cursor: pointer;
            border-radius: 4px; /* 添加圆角 */
            transition: background-color 0.3s, color 0.3s; /* 添加过渡效果 */
            font-size: 14px;
        }

        /* 鼠标悬停时的样式 */
        .button-like-link:hover {
            background-color: #e7e7e7;
            color: #000;
        }

        /* 禁用状态时的样式 */
        .button-like-link:disabled {
            background-color: #ccc;
            color: #999;
            cursor: not-allowed;
        }

    </style>
</head>
<body>
<!-- 控制按钮区域 -->
<div id="controls">
    <!-- 开始按钮 -->
    <button id="startId" class="button-like-link">开始</button>
    <!-- 停止按钮 -->
    <button id="stopId" class="button-like-link">停止</button>
    <!-- 下载按钮 -->
    <a id="downloadId" class="button-like-link" href="javascript:;">下载</a>
</div>
<!-- 视频播放区域 -->
<video controls autoplay="false" id="videoId"></video>
</body>

<script>
    let startButton = document.getElementById('startId');
    let stopButton = document.getElementById('stopId');
    let downloadButton = document.getElementById('downloadId');
    // 获取视频元素
    let video = document.getElementById('videoId');

    // 声明一个全局变量以便在不同的函数中访问媒体流对象
    let mediaStream;
    // 捕获媒体流
    let mediaRecorder;

    /**
     * 点击开始按钮时，先打开视频设备，然后获取视频设备的媒体流数据，然后收集媒体流数据
     * @returns {Promise<void>}
     */
    startButton.onclick = async () => {
        // 媒体约束对象，指定获取的媒体类型为音频和视频，视频宽高为理想值1280x720，使用用户前置摄像头，帧率为10到15
        let constraints = {
            audio: true,
            video: true
        };

        // 1. 打开视频设备，获取用户媒体设备的流对象
        mediaStream = await navigator.mediaDevices.getUserMedia(constraints);

        // 将获取到的媒体设备的流对象，赋值给视频元素的 srcObject 属性
        video.srcObject = mediaStream;
        // 当媒体元数据已加载时执行的回调函数，开始播放视频
        video.onloadedmetadata = () => {
            video.play();
        };

        startButton.style.background = "red";
        startButton.style.color = "black";

        // 2. 捕获媒体流
        mediaRecorder = new MediaRecorder(mediaStream);
        mediaRecorder.start();
        // console.log(mediaRecorder.state);
        // console.log("recorder started");

        // 3. 收集录制的数据
        let chunks = [];
        // 当关闭mediaRecorder.stop()时会触发这个事件
        mediaRecorder.ondataavailable = (event) => {
            chunks.push(event.data);
            // console.log(event.data)
            // console.log(chunks)

            // 测试，收集到的数据是否可以播放
            //     MP4 = 带有 H.264 视频编码和 AAC 音频编码的 MPEG 4 文件
            //     WebM = 带有 VP8 视频编码和 Vorbis 音频编码的 WebM 文件
            //     Ogg = 带有 Theora 视频编码和 Vorbis 音频编码的 Ogg 文件
            //
            //     格式   MIME-type
            //     MP4  video/mp4
            //     WebM video/webm
            //     Ogg  video/ogg
            let blob = new Blob(chunks, {type: "video/ogg; codecs=opus"});
            let url = URL.createObjectURL(blob);
            video.src = url;
            // 更新下载按钮的 href 属性，以便用户可以下载视频
            downloadButton.href = url;
            downloadButton.download = `${new Date().toLocaleString()}_recorded_video.mp4`;
            downloadButton.disabled = false; // 启用下载按钮
        };
    }


    /**
     * 停止捕获视频流
     */
    stopButton.onclick = () => {
        if (mediaStream) {
            // 停止所有媒体流上的轨道
            mediaStream.getTracks().forEach(track => {
                track.stop();
            });

            // 停止媒体流的捕获
            mediaRecorder.stop();
            // console.log(mediaRecorder.state);

            // 清除视频元素的 srcObject 属性
            video.srcObject = null;

            startButton.style.background = "";
            startButton.style.color = "";
        }
    }
</script>

</html>

```

# 测试验证媒体流传输

### 前端

```markup
<!DOCTYPE html>
<html>
<head>
    <!-- 设置文档使用的字符编码 -->
    <meta charset="UTF-8">
    <!-- 设置 viewport 元标签，以确保页面在移动设备上正确显示和缩放 -->
    <meta name="viewport" content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <!-- 启用苹果移动设备的全屏模式 -->
    <meta name="apple-mobile-web-capable" content="yes">
    <!-- 页面标题 -->
    <title>测试验证媒体流传输</title>
    <!-- 页面样式 -->
    <style>
        /* 设置视频元素样式 */
        #videoId {
            width: 512px;
            height: 256px;
        }
    </style>
</head>
<body>
<!-- 控制按钮区域 -->
<div id="controls">
    <!-- 开始按钮 -->
    <button id="startId">开始</button>
    <!-- 停止按钮 -->
    <button id="stopId">停止</button>
</div>
<!-- 视频播放区域 -->
<video controls autoplay="false" id="videoId"></video>
</body>

<script>
    let startButton = document.getElementById('startId');
    let stopButton = document.getElementById('stopId');
    // 获取视频元素
    let video = document.getElementById('videoId');

    // 声明一个全局变量以便在不同的函数中访问媒体流对象
    let mediaStream;
    // 捕获媒体流
    let mediaRecorder;

    /**
     * 点击开始按钮时，先打开视频设备，然后获取视频设备的媒体流数据，然后收集媒体流数据
     * @returns {Promise<void>}
     */
    startButton.onclick = async () => {
        // 媒体约束对象，指定获取的媒体类型为音频和视频，视频宽高为理想值1280x720，使用用户前置摄像头，帧率为10到15
        let constraints = {
            audio: true,
            video: true
        };

        // 1. 打开视频设备，获取用户媒体设备的流对象
        mediaStream = await navigator.mediaDevices.getUserMedia(constraints);

        // 将获取到的媒体设备的流对象，赋值给视频元素的 srcObject 属性
        video.srcObject = mediaStream;
        // 当媒体元数据已加载时执行的回调函数，开始播放视频
        video.onloadedmetadata = () => {
            video.play();
        };

        startButton.style.background = "red";
        startButton.style.color = "black";

        // 2. 捕获媒体流
        mediaRecorder = new MediaRecorder(mediaStream);
        mediaRecorder.start();

        // 3. 收集录制的数据
        let chunks = [];
        // 当关闭mediaRecorder.stop()时会触发这个事件
        mediaRecorder.ondataavailable = async (event) => {
            chunks.push(event.data);
            // 创建一个新的Blob对象，包含已收集到的视频数据
            let blob = new Blob(chunks, {type: 'video/webm'});

            // 创建一个FormData对象，用于将视频数据发送到FastAPI端点
            let formData = new FormData();
            formData.append('file', blob, 'video.webm');

            // 使用Fetch API将视频数据发送到FastAPI端点
            let response = await fetch('http://172.16.176.59:8000/upload/', {
                method: 'POST',
                body: formData
            });
            // 服务端返回结果
            let data = await response.json();
            console.log(data);
        };
    }


    /**
     * 停止捕获视频流
     */
    stopButton.onclick = () => {
        if (mediaStream) {
            // 停止所有媒体流上的轨道
            mediaStream.getTracks().forEach(track => {
                track.stop();
            });

            // 停止媒体流的捕获
            mediaRecorder.stop();
            // console.log(mediaRecorder.state);

            // 清除视频元素的 srcObject 属性
            video.srcObject = null;

            startButton.style.background = "";
            startButton.style.color = "";
        }
    }
</script>

</html>

```

### 服务端

```python
import io

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 添加跨域资源共享中间件，允许跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,  # 允许凭证
    allow_methods=["*"],  # 允许所有 HTTP 方法
    allow_headers=["*"],  # 允许所有 HTTP 头部
)


# FastAPI端点，用于处理上传的视频流
@app.post("/upload/")
async def upload_video(upload_file: UploadFile = File(...)):
    # 前端传入的媒体流是blob格式，也就是bytes格式，所以这里要做转换才能被模型识别
    audio_bytes = await upload_file.read()
    # 将 bytes 数据转换为 BinaryIO 类型
    audio_bytes_io = io.BytesIO(audio_bytes)

    print(audio_bytes_io)

    # 返回成功消息
    return {"message": "音频数据已接收并处理"}


# 运行FastAPI应用
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

```

# 引入ASR模型

### 修改服务端

```python
import io
from typing import Union, BinaryIO

import numpy as np
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from faster_whisper import WhisperModel  # 导入WhisperModel类

app = FastAPI()

# 添加跨域资源共享中间件，允许跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,  # 允许凭证
    allow_methods=["*"],  # 允许所有 HTTP 方法
    allow_headers=["*"],  # 允许所有 HTTP 头部
)

# 初始化模型
model_path = "/data/LLM/openai/faster-whisper-large-v3"
model = WhisperModel(model_path, device="cuda", compute_type="float16")


def transcribe_audio(audio: Union[str, BinaryIO, np.ndarray]):
    try:
        segments, info = model.transcribe(language="zh", audio=audio, beam_size=5)
        return segments, info
    except Exception as e:
        print("音频转录时出错:", e)


# FastAPI端点，用于处理上传的视频流
@app.post("/upload/")
async def upload_video(upload_file: UploadFile = File(...)):
    # 前端传入的媒体流是blob格式，也就是bytes格式，所以这里要做转换才能被模型识别
    audio_bytes = await upload_file.read()
    # 将 bytes 数据转换为 BinaryIO 类型
    audio_bytes_io = io.BytesIO(audio_bytes)

    segments, info = transcribe_audio(audio_bytes_io)

    print("检测到语言 '%s'，置信度为 %f" % (info.language, info.language_probability))

    texts = []
    for segment in segments:
        print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
        texts.append(segment.text)

    # 返回成功消息
    return {"message": ','.join(texts)}


# 运行FastAPI应用
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

```

# 引入ASR模型-增量翻译

### 修改前端

```markup
<!DOCTYPE html>
<html>
<head>
    <!-- 设置文档使用的字符编码 -->
    <meta charset="UTF-8">
    <!-- 设置 viewport 元标签，以确保页面在移动设备上正确显示和缩放 -->
    <meta name="viewport" content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <!-- 启用苹果移动设备的全屏模式 -->
    <meta name="apple-mobile-web-capable" content="yes">
    <!-- 页面标题 -->
    <title>引入ASR模型-增量翻译</title>
</head>
<body>
<!-- 控制按钮区域 -->
<div id="controls">
    <!-- 开始按钮 -->
    <button id="startId">开始</button>
    <!-- 停止按钮 -->
    <button id="stopId">停止</button>
</div>
<div id="messageId"></div>
</body>

<script>
    let startButton = document.getElementById('startId');
    let stopButton = document.getElementById('stopId');
    let message = document.getElementById('messageId');


    // 用于存储MediaRecorder实例
    let mediaRecorder;
    // 用于存储录制的Blob片段
    let chunks = [];

    // 打开视频设备，获取用户媒体设备的流对象
    navigator.mediaDevices.getUserMedia({audio: true, video: false}).then((mediaStream) => {

        // 初始化MediaRecorder
        mediaRecorder = new MediaRecorder(mediaStream);

        // 当有数据可用时触发
        mediaRecorder.ondataavailable = (event) => {
            if (event.data && event.data.size > 0) {
                chunks.push(event.data);
            }
        };

        // 当录制停止时触发
        mediaRecorder.onstop = async () => {
            // 将所有Blob片段合并为一个Blob
            let blob = new Blob(chunks, {type: 'video/webm'});
            // 创建一个FormData对象，用于将视频数据发送到FastAPI端点
            let formData = new FormData();
            formData.append('file', blob, 'video.webm');

            // 使用Fetch API将视频数据发送到FastAPI端点
            let response = await fetch('http://172.16.176.59:8000/upload/', {
                method: 'POST',
                body: formData
            });
            // 服务端返回结果
            let data = await response.json();
            message.innerText = data.message;
        };

        /**
         * 开始捕获视频流
         */
        startButton.onclick = () => {
            // 开始捕获视频流
            mediaRecorder.start();
            startButton.style.background = "red";
            startButton.style.color = "black";
        }

        /**
         * 停止捕获视频流
         */
        stopButton.onclick = () => {
            // 停止捕获视频流
            mediaRecorder.stop();
            startButton.style.background = "";
            startButton.style.color = "";
        }

    })
</script>

</html>

```

* * *

# 长按录音

### 修改前端

```markup
<!DOCTYPE html>
<html>
<head>
    <!-- 设置文档使用的字符编码 -->
    <meta charset="UTF-8">
    <!-- 设置 viewport 元标签，以确保页面在移动设备上正确显示和缩放 -->
    <meta name="viewport" content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <!-- 启用苹果移动设备的全屏模式 -->
    <meta name="apple-mobile-web-capable" content="yes">
    <!-- 页面标题 -->
    <title>引入ASR模型-增量翻译</title>
</head>
<body>
<!-- 控制按钮区域 -->
<div id="controls">
    <!-- 开始按钮 -->
    <button id="startId">长按录音</button>
</div>
<div id="messageId"></div>
</body>

<script>
    let startButton = document.getElementById('startId'); // 获取长按录音按钮
    let message = document.getElementById('messageId'); // 获取消息显示区域
    let mediaStream; // 媒体流对象
    let mediaRecorder; // 媒体录制器对象

    // 打开音频设备，获取用户媒体设备的流对象
    const openMediaStream = async () => {
        let chunks = []; // 存储录音数据块
        try {
            mediaStream = await navigator.mediaDevices.getUserMedia({audio: true, video: false}); // 获取音频流
            mediaRecorder = new MediaRecorder(mediaStream); // 创建媒体录制器

            // 当有数据可用时触发
            mediaRecorder.ondataavailable = (event) => {
                if (event.data && event.data.size > 0) {
                    chunks.push(event.data);
                }
            };

            // 当录制停止时触发
            mediaRecorder.onstop = async () => {
                // 将所有Blob片段合并为一个Blob
                const blob = new Blob(chunks, {type: 'audio/webm'});
                // 创建一个FormData对象，用于将音频数据发送到FastAPI端点
                const formData = new FormData();
                formData.append('file', blob, 'audio.webm');

                // 使用Fetch API将音频数据发送到FastAPI端点
                const response = await fetch('http://172.16.176.59:8000/upload/', {
                    method: 'POST',
                    body: formData
                });
                // 服务端返回结果
                const data = await response.json();
                message.innerText = data.message;
            };
        } catch (error) {
            console.error('Error accessing media devices:', error);
        }
    };

    /**
     * 长按录音
     * @type {boolean}
     */
    let isRecording = false; // 记录是否正在录音
    let timeout;
    const startRecording = () => {
        isRecording = true;
        startButton.innerText = '录音中...';
        startButton.style.color = "green";
        startButton.style.fontWeight = "600";
        mediaRecorder.start(); // 开始录音
    };
    const stopRecording = () => {
        isRecording = false;
        startButton.innerText = '长按录音';
        startButton.style.color = "#000000";
        startButton.style.fontWeight = "";
        mediaRecorder.stop(); // 停止录音
    };

    /**
     * 监听按钮的鼠标事件(支持PC端事件)
     */
    startButton.addEventListener('mousedown', () => {
        timeout = setTimeout(() => {
            if (!isRecording) {
                openMediaStream().then(startRecording);
            }
        }, 500); // 长按时间，单位：毫秒
    });
    startButton.addEventListener('mouseup', () => {
        clearTimeout(timeout);
        if (isRecording) {
            stopRecording();
        }
    });

    /**
     * 监听按钮的触摸事件(支持移动端事件)
     */
    startButton.addEventListener('touchstart', () => {
        timeout = setTimeout(() => {
            if (!isRecording) {
                openMediaStream().then(startRecording);
            }
        }, 1000); // 长按时间，单位：毫秒
    });
    startButton.addEventListener('touchend', () => {
        clearTimeout(timeout);
        if (isRecording) {
            stopRecording();
        }
    });
</script>

</html>

```

* * *

# 长按录音-基于[模型适配服务端](https://gitee.com/eric-mao/ai-0x04 "模型适配服务端")

```markup
<!DOCTYPE html>
<html>
<head>
    <!-- 设置文档使用的字符编码 -->
    <meta charset="UTF-8">
    <!-- 设置 viewport 元标签，以确保页面在移动设备上正确显示和缩放 -->
    <meta name="viewport" content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <!-- 启用苹果移动设备的全屏模式 -->
    <meta name="apple-mobile-web-capable" content="yes">
    <!-- 页面标题 -->
    <title>引入ASR模型-增量翻译</title>
</head>
<body>
<!-- 控制按钮区域 -->
<div id="controls">
    <!-- 开始按钮 -->
    <button id="startId">长按录音</button>
</div>
<div id="messageId"></div>
</body>

<script>
    let startButton = document.getElementById('startId'); // 获取长按录音按钮
    let message = document.getElementById('messageId'); // 获取消息显示区域
    let mediaStream; // 媒体流对象
    let mediaRecorder; // 媒体录制器对象

    // 打开音频设备，获取用户媒体设备的流对象
    const openMediaStream = async () => {
        let chunks = []; // 存储录音数据块
        try {
            mediaStream = await navigator.mediaDevices.getUserMedia({audio: true, video: false}); // 获取音频流
            mediaRecorder = new MediaRecorder(mediaStream); // 创建媒体录制器

            // 当有数据可用时触发
            mediaRecorder.ondataavailable = (event) => {
                if (event.data && event.data.size > 0) {
                    chunks.push(event.data);
                }
            };

            // 当录制停止时触发
            mediaRecorder.onstop = async () => {
                // 将所有Blob片段合并为一个Blob
                const blob = new Blob(chunks, {type: 'audio/webm'});
                // 创建一个FormData对象，用于将音频数据发送到FastAPI端点
                const formData = new FormData();
                formData.append('file', blob, 'audio.webm');
                formData.append('model', 'faster-whisper-large-v3');
                // formData.append('timestamp_granularities', 'word');
                // formData.append('timestamp_granularities', 'segment');

                // 使用Fetch API将音频数据发送到FastAPI端点
                const response = await fetch('http://172.16.176.59:7001/audio/transcriptions', {
                    method: 'POST',
                    body: formData
                });
                // 服务端返回结果
                const data = await response.json();
                message.innerText = data.text;
            };
        } catch (error) {
            console.error('Error accessing media devices:', error);
        }
    };

    /**
     * 长按录音
     * @type {boolean}
     */
    let isRecording = false; // 记录是否正在录音
    let timeout;
    const startRecording = () => {
        isRecording = true;
        startButton.innerText = '录音中...';
        startButton.style.color = "green";
        startButton.style.fontWeight = "600";
        mediaRecorder.start(); // 开始录音
    };
    const stopRecording = () => {
        isRecording = false;
        startButton.innerText = '长按录音';
        startButton.style.color = "#000000";
        startButton.style.fontWeight = "";
        mediaRecorder.stop(); // 停止录音
    };

    /**
     * 监听按钮的鼠标事件(支持PC端事件)
     */
    startButton.addEventListener('mousedown', () => {
        timeout = setTimeout(() => {
            if (!isRecording) {
                openMediaStream().then(startRecording);
            }
        }, 500); // 长按时间，单位：毫秒
    });
    startButton.addEventListener('mouseup', () => {
        clearTimeout(timeout);
        if (isRecording) {
            stopRecording();
        }
    });

    /**
     * 监听按钮的触摸事件(支持移动端事件)
     */
    startButton.addEventListener('touchstart', () => {
        timeout = setTimeout(() => {
            if (!isRecording) {
                openMediaStream().then(startRecording);
            }
        }, 1000); // 长按时间，单位：毫秒
    });
    startButton.addEventListener('touchend', () => {
        clearTimeout(timeout);
        if (isRecording) {
            stopRecording();
        }
    });
</script>

</html>

```

* * *

> 以上都是前置条件与基础知识的储备，接下来才是真正的基于`Web实时通信`实现的`实时流媒体`传输 `WebRTC`全称是`Web Real-Time Communication`，`网页即时通信`。 WebRTC在2011年6月1日开源，并在Google、Mozilla、Opera等各家巨头公司的支持下被纳入W3C 推荐标准，给浏览器和移动应用提供了即时通信的能力。
> 
> ### 优势
> 
> - 跨平台(Web、Windows、MacOS、Linux、iOS、Android)
> - 实时传输
> - 音视频引擎
> - 免费、免插件、免安装
> - 主流浏览器支持
> 
> ### 应用场景
> 
> - 音视频会议
> - 即时通讯工具 IM
> - 直播
> - 共享远程桌面
> - 等等
> 
> ### RTCPeerConnection
> 
> 使用WebRTC实现实时通信最核心的API就是`RTCPeerConnection`，它代表一个由本地计算机到远端的WebRTC连接，该接口提供了创建、保持、监控及关闭连接的方法的实现，有点类似于`socket`。 相关的API
> 
> - createOffer 创建Offer方法
> - setLocalDescription 设置本地SDP描述信息
> - peer.onicecandidate 设置完本地SDP描述信息后会触发该方法，打开一个连接，开始运转媒体流
> - setRemoteDescription 设置远端的SDP描述信息，由本地发送
> - peer.ontrack 设置完远端SDP描述信息后会触发该方法，接收对方的媒体流
> - createAnswer 远端创建应答Answer方法
> - RTCIceCandidate RTC网络信息，IP、端口等
> - addIceCandidate 连接添加对方的网络信息
