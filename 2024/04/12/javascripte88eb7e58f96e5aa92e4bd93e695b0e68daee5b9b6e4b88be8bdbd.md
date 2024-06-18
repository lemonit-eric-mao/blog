---
title: JavaScript获取媒体数据并下载
date: '2024-04-12T03:32:08+00:00'
status: publish
permalink: /2024/04/12/javascript%e8%8e%b7%e5%8f%96%e5%aa%92%e4%bd%93%e6%95%b0%e6%8d%ae%e5%b9%b6%e4%b8%8b%e8%bd%bd
author: 毛巳煜
excerpt: ''
type: post
id: 10808
category:
    - JavaScript
tag: []
post_format: []
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
---
```javascript



    
    <meta charset="UTF-8"></meta>
    
    <meta content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0" name="viewport"></meta>
    
    <meta content="yes" name="apple-mobile-web-capable"></meta>
    
    <title>展示获取视频流</title>
    
    <style>
        /* &#35774;&#32622;&#35270;&#39057;&#20803;&#32032;&#26679;&#24335; */
        #videoId {
            width: 512px;
            height: 256px;
        }

        /* &#25353;&#38062;&#26679;&#24335; */
        .button-like-link {
            display: inline-block;
            padding: 10px 20px;
            background-color: #f0f0f0;
            border: 1px solid #ddd;
            text-decoration: none;
            color: #333;
            cursor: pointer;
            border-radius: 4px; /* &#28155;&#21152;&#22278;&#35282; */
            transition: background-color 0.3s, color 0.3s; /* &#28155;&#21152;&#36807;&#28193;&#25928;&#26524; */
            font-size: 14px;
        }

        /* &#40736;&#26631;&#24748;&#20572;&#26102;&#30340;&#26679;&#24335; */
        .button-like-link:hover {
            background-color: #e7e7e7;
            color: #000;
        }

        /* &#31105;&#29992;&#29366;&#24577;&#26102;&#30340;&#26679;&#24335; */
        .button-like-link:disabled {
            background-color: #ccc;
            color: #999;
            cursor: not-allowed;
        }

        /* &#21015;&#34920;&#26679;&#24335; */
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



<div>
    <label for="meetingName">会议内容名称：</label>
    <input id="meetingName" type="text"></input>
</div>


<div id="controls">
    
    <button class="button-like-link" id="startId">开始</button>
    
    <button class="button-like-link" id="stopId">停止</button>
</div>


<ul id="recordingsList"></ul>



<script>
    let startButton = document.getElementById('startId');
    let stopButton = document.getElementById('stopId');
    let recordingsList = document.getElementById('recordingsList');
    let meetingNameInput = document.getElementById('meetingName');

    // &#22768;&#26126;&#19968;&#20010;&#20840;&#23616;&#21464;&#37327;&#20197;&#20415;&#22312;&#19981;&#21516;&#30340;&#20989;&#25968;&#20013;&#35775;&#38382;&#23186;&#20307;&#27969;&#23545;&#35937;
    let mediaStream;
    // &#25429;&#33719;&#23186;&#20307;&#27969;
    let mediaRecorder;

    /**
     * &#25351;&#23450;&#35201;&#33719;&#21462;&#30340;&#23186;&#20307;&#27969;&#23545;&#35937;&#19982;&#30456;&#20851;&#30340;&#25480;&#26435;
     */
    const openMediaStream = async () => {
        let chunks = []; // &#23384;&#20648;&#24405;&#38899;&#25968;&#25454;&#22359;
        try {
            // &#33719;&#21462;&#38899;&#39057;&#27969;
            mediaStream = await navigator.mediaDevices.getUserMedia({audio: true, video: true});
            // &#21019;&#24314;&#23186;&#20307;&#24405;&#21046;&#22120;
            mediaRecorder = new MediaRecorder(mediaStream);

            // &#24403;&#26377;&#25968;&#25454;&#21487;&#29992;&#26102;&#35302;&#21457;
            mediaRecorder.ondataavailable = (event) => {
                if (event.data && event.data.size > 0) {
                    chunks.push(event.data);
                }
            };

            // &#24403;&#24405;&#21046;&#20572;&#27490;&#26102;&#35302;&#21457;
            mediaRecorder.onstop = async () => {

                let blob = new Blob(chunks, {type: "video/mp4"});
                let url = URL.createObjectURL(blob);
                // &#21019;&#24314;&#21015;&#34920;&#39033;
                let listItem = document.createElement('li');
                // &#33719;&#21462;&#20250;&#35758;&#21517;&#31216;&#36755;&#20837;&#26694;&#30340;&#20540;
                let meetingName = meetingNameInput.value || '&#26410;&#21629;&#21517;&#20250;&#35758;';
                // &#26500;&#24314;&#21015;&#34920;&#21517;&#31216;
                let now = new Date();
                let formattedDate = `<span class="katex math inline">{now.getFullYear()}_{now.getMonth() + 1}_<span class="katex math inline">{now.getDate()}_{now.getHours()}_<span class="katex math inline">{now.getMinutes()}_{now.getSeconds()}`;
                let listName = `<span class="katex math inline">{meetingName}_{formattedDate}.mp4`;

                // &#21019;&#24314;&#19979;&#36733;&#38142;&#25509;
                let downloadLink = document.createElement('a');
                downloadLink.href = url;
                downloadLink.download = listName;
                downloadLink.textContent = listName;
                // &#21019;&#24314;&#21024;&#38500;&#25353;&#38062;
                let deleteButton = document.createElement('button');
                deleteButton.textContent = '&#21024;&#38500;';
                deleteButton.onclick = () => {
                    listItem.remove();
                    URL.revokeObjectURL(downloadLink.href);
                };
                // &#28155;&#21152;&#21040;&#21015;&#34920;&#39033;&#20013;
                listItem.appendChild(downloadLink);
                listItem.appendChild(deleteButton);
                // &#28155;&#21152;&#21040;&#21015;&#34920;&#20013;
                recordingsList.appendChild(listItem);
            };
        } catch (error) {
            console.error('Error accessing media devices:', error);
        }
    };

    /**
     * &#28857;&#20987;&#24320;&#22987;&#25353;&#38062;&#26102;&#65292;&#20808;&#25171;&#24320;&#35270;&#39057;&#35774;&#22791;&#65292;&#28982;&#21518;&#33719;&#21462;&#35270;&#39057;&#35774;&#22791;&#30340;&#23186;&#20307;&#27969;&#25968;&#25454;&#65292;&#28982;&#21518;&#25910;&#38598;&#23186;&#20307;&#27969;&#25968;&#25454;
     * @returns {Promise<void>}
     */
    startButton.onclick = async () => {
        await openMediaStream();
        mediaRecorder.start();
        startButton.style.background = "red";
        startButton.style.color = "black";
    };


    /**
     * &#20572;&#27490;&#25429;&#33719;&#35270;&#39057;&#27969;
     */
    stopButton.onclick = () => {
        if (mediaStream) {
            // &#20572;&#27490;&#25152;&#26377;&#23186;&#20307;&#27969;&#19978;&#30340;&#36712;&#36947;
            mediaStream.getTracks().forEach(track => {
                track.stop();
            });
            // &#20572;&#27490;&#23186;&#20307;&#27969;&#30340;&#25429;&#33719;
            mediaRecorder.stop();
            startButton.style.background = "";
            startButton.style.color = "";
        }
    };
</script>




```