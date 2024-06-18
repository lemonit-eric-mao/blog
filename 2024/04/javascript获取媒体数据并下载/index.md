---
title: "JavaScript获取媒体数据并下载"
date: "2024-04-12"
categories: 
  - "javascript"
---

```javascript
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

        /* 列表样式 */
        #recordingsList {
            list-style-type: none;
            padding: 0;
        }

        .recording-item {
            margin-bottom: 10px;
        }

        .recording-item button {
            margin-left: 10px;
        }
    </style>
</head>
<body>
<!-- 会议名称输入框 -->
<div>
    <label for="meetingName">会议内容名称：</label>
    <input type="text" id="meetingName">
</div>

<!-- 控制按钮区域 -->
<div id="controls">
    <!-- 开始按钮 -->
    <button id="startId" class="button-like-link">开始</button>
    <!-- 停止按钮 -->
    <button id="stopId" class="button-like-link">停止</button>
</div>

<!-- 录音列表 -->
<ul id="recordingsList"></ul>

</body>

<script>
    let startButton = document.getElementById('startId');
    let stopButton = document.getElementById('stopId');
    let recordingsList = document.getElementById('recordingsList');
    let meetingNameInput = document.getElementById('meetingName');

    // 声明一个全局变量以便在不同的函数中访问媒体流对象
    let mediaStream;
    // 捕获媒体流
    let mediaRecorder;

    /**
     * 指定要获取的媒体流对象与相关的授权
     */
    const openMediaStream = async () => {
        let chunks = []; // 存储录音数据块
        try {
            // 获取音频流
            mediaStream = await navigator.mediaDevices.getUserMedia({audio: true, video: true});
            // 创建媒体录制器
            mediaRecorder = new MediaRecorder(mediaStream);

            // 当有数据可用时触发
            mediaRecorder.ondataavailable = (event) => {
                if (event.data && event.data.size > 0) {
                    chunks.push(event.data);
                }
            };

            // 当录制停止时触发
            mediaRecorder.onstop = async () => {

                let blob = new Blob(chunks, {type: "video/mp4"});
                let url = URL.createObjectURL(blob);
                // 创建列表项
                let listItem = document.createElement('li');
                // 获取会议名称输入框的值
                let meetingName = meetingNameInput.value || '未命名会议';
                // 构建列表名称
                let now = new Date();
                let formattedDate = `${now.getFullYear()}_${now.getMonth() + 1}_${now.getDate()}_${now.getHours()}_${now.getMinutes()}_${now.getSeconds()}`;
                let listName = `${meetingName}_${formattedDate}.mp4`;

                // 创建下载链接
                let downloadLink = document.createElement('a');
                downloadLink.href = url;
                downloadLink.download = listName;
                downloadLink.textContent = listName;
                // 创建删除按钮
                let deleteButton = document.createElement('button');
                deleteButton.textContent = '删除';
                deleteButton.onclick = () => {
                    listItem.remove();
                    URL.revokeObjectURL(downloadLink.href);
                };
                // 添加到列表项中
                listItem.appendChild(downloadLink);
                listItem.appendChild(deleteButton);
                // 添加到列表中
                recordingsList.appendChild(listItem);
            };
        } catch (error) {
            console.error('Error accessing media devices:', error);
        }
    };

    /**
     * 点击开始按钮时，先打开视频设备，然后获取视频设备的媒体流数据，然后收集媒体流数据
     * @returns {Promise<void>}
     */
    startButton.onclick = async () => {
        await openMediaStream();
        mediaRecorder.start();
        startButton.style.background = "red";
        startButton.style.color = "black";
    };


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
            startButton.style.background = "";
            startButton.style.color = "";
        }
    };
</script>

</html>

```
