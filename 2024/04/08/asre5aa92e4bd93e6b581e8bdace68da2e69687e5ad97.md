---
title: ASR媒体流转换文字
date: '2024-04-08T03:58:28+00:00'
status: publish
permalink: /2024/04/08/asr%e5%aa%92%e4%bd%93%e6%b5%81%e8%bd%ac%e6%8d%a2%e6%96%87%e5%ad%97
author: 毛巳煜
excerpt: ''
type: post
id: 10780
category:
    - 人工智能
tag: []
post_format: []
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
hestia_layout_select:
    - sidebar-right
---
JavaScript 展示获取视频流
==================

```
<pre data-language="HTML">```markup



    
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

    </style>



<div id="controls">
    
    <button class="button-like-link" id="startId">开始</button>
    
    <button class="button-like-link" id="stopId">停止</button>
    
    <a class="button-like-link" href="javascript:;" id="downloadId">下载</a>
</div>

<video autoplay="false" controls="" id="videoId"></video>


<script>
    let startButton = document.getElementById('startId');
    let stopButton = document.getElementById('stopId');
    let downloadButton = document.getElementById('downloadId');
    // &#33719;&#21462;&#35270;&#39057;&#20803;&#32032;
    let video = document.getElementById('videoId');

    // &#22768;&#26126;&#19968;&#20010;&#20840;&#23616;&#21464;&#37327;&#20197;&#20415;&#22312;&#19981;&#21516;&#30340;&#20989;&#25968;&#20013;&#35775;&#38382;&#23186;&#20307;&#27969;&#23545;&#35937;
    let mediaStream;
    // &#25429;&#33719;&#23186;&#20307;&#27969;
    let mediaRecorder;

    /**
     * &#28857;&#20987;&#24320;&#22987;&#25353;&#38062;&#26102;&#65292;&#20808;&#25171;&#24320;&#35270;&#39057;&#35774;&#22791;&#65292;&#28982;&#21518;&#33719;&#21462;&#35270;&#39057;&#35774;&#22791;&#30340;&#23186;&#20307;&#27969;&#25968;&#25454;&#65292;&#28982;&#21518;&#25910;&#38598;&#23186;&#20307;&#27969;&#25968;&#25454;
     * @returns {Promise<void>}
     */
    startButton.onclick = async () => {
        // &#23186;&#20307;&#32422;&#26463;&#23545;&#35937;&#65292;&#25351;&#23450;&#33719;&#21462;&#30340;&#23186;&#20307;&#31867;&#22411;&#20026;&#38899;&#39057;&#21644;&#35270;&#39057;&#65292;&#35270;&#39057;&#23485;&#39640;&#20026;&#29702;&#24819;&#20540;1280x720&#65292;&#20351;&#29992;&#29992;&#25143;&#21069;&#32622;&#25668;&#20687;&#22836;&#65292;&#24103;&#29575;&#20026;10&#21040;15
        let constraints = {
            audio: true,
            video: true
        };

        // 1. &#25171;&#24320;&#35270;&#39057;&#35774;&#22791;&#65292;&#33719;&#21462;&#29992;&#25143;&#23186;&#20307;&#35774;&#22791;&#30340;&#27969;&#23545;&#35937;
        mediaStream = await navigator.mediaDevices.getUserMedia(constraints);

        // &#23558;&#33719;&#21462;&#21040;&#30340;&#23186;&#20307;&#35774;&#22791;&#30340;&#27969;&#23545;&#35937;&#65292;&#36171;&#20540;&#32473;&#35270;&#39057;&#20803;&#32032;&#30340; srcObject &#23646;&#24615;
        video.srcObject = mediaStream;
        // &#24403;&#23186;&#20307;&#20803;&#25968;&#25454;&#24050;&#21152;&#36733;&#26102;&#25191;&#34892;&#30340;&#22238;&#35843;&#20989;&#25968;&#65292;&#24320;&#22987;&#25773;&#25918;&#35270;&#39057;
        video.onloadedmetadata = () => {
            video.play();
        };

        startButton.style.background = "red";
        startButton.style.color = "black";

        // 2. &#25429;&#33719;&#23186;&#20307;&#27969;
        mediaRecorder = new MediaRecorder(mediaStream);
        mediaRecorder.start();
        // console.log(mediaRecorder.state);
        // console.log("recorder started");

        // 3. &#25910;&#38598;&#24405;&#21046;&#30340;&#25968;&#25454;
        let chunks = [];
        // &#24403;&#20851;&#38381;mediaRecorder.stop()&#26102;&#20250;&#35302;&#21457;&#36825;&#20010;&#20107;&#20214;
        mediaRecorder.ondataavailable = (event) => {
            chunks.push(event.data);
            // console.log(event.data)
            // console.log(chunks)

            // &#27979;&#35797;&#65292;&#25910;&#38598;&#21040;&#30340;&#25968;&#25454;&#26159;&#21542;&#21487;&#20197;&#25773;&#25918;
            //     MP4 = &#24102;&#26377; H.264 &#35270;&#39057;&#32534;&#30721;&#21644; AAC &#38899;&#39057;&#32534;&#30721;&#30340; MPEG 4 &#25991;&#20214;
            //     WebM = &#24102;&#26377; VP8 &#35270;&#39057;&#32534;&#30721;&#21644; Vorbis &#38899;&#39057;&#32534;&#30721;&#30340; WebM &#25991;&#20214;
            //     Ogg = &#24102;&#26377; Theora &#35270;&#39057;&#32534;&#30721;&#21644; Vorbis &#38899;&#39057;&#32534;&#30721;&#30340; Ogg &#25991;&#20214;
            //
            //     &#26684;&#24335;   MIME-type
            //     MP4  video/mp4
            //     WebM video/webm
            //     Ogg  video/ogg
            let blob = new Blob(chunks, {type: "video/ogg; codecs=opus"});
            let url = URL.createObjectURL(blob);
            video.src = url;
            // &#26356;&#26032;&#19979;&#36733;&#25353;&#38062;&#30340; href &#23646;&#24615;&#65292;&#20197;&#20415;&#29992;&#25143;&#21487;&#20197;&#19979;&#36733;&#35270;&#39057;
            downloadButton.href = url;
            downloadButton.download = `${new Date().toLocaleString()}_recorded_video.mp4`;
            downloadButton.disabled = false; // &#21551;&#29992;&#19979;&#36733;&#25353;&#38062;
        };
    }


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
            // console.log(mediaRecorder.state);

            // &#28165;&#38500;&#35270;&#39057;&#20803;&#32032;&#30340; srcObject &#23646;&#24615;
            video.srcObject = null;

            startButton.style.background = "";
            startButton.style.color = "";
        }
    }
</script>




```
```

测试验证媒体流传输
=========

### 前端

<div style="overflow:hidden; clear:both; width: 100%; height: 40px; position: relative;">- - - - - -

 <span style="position: absolute;top: 50%;left: 50%; transform: translate(-50%, -50%); background-color: white;">以下为隐藏内容</span> </div> ```
<pre data-language="HTML">```markup



    
    <meta charset="UTF-8"></meta>
    
    <meta content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0" name="viewport"></meta>
    
    <meta content="yes" name="apple-mobile-web-capable"></meta>
    
    <title>测试验证媒体流传输</title>
    
    <style>
        /* &#35774;&#32622;&#35270;&#39057;&#20803;&#32032;&#26679;&#24335; */
        #videoId {
            width: 512px;
            height: 256px;
        }
    </style>



<div id="controls">
    
    <button id="startId">开始</button>
    
    <button id="stopId">停止</button>
</div>

<video autoplay="false" controls="" id="videoId"></video>


<script>
    let startButton = document.getElementById('startId');
    let stopButton = document.getElementById('stopId');
    // &#33719;&#21462;&#35270;&#39057;&#20803;&#32032;
    let video = document.getElementById('videoId');

    // &#22768;&#26126;&#19968;&#20010;&#20840;&#23616;&#21464;&#37327;&#20197;&#20415;&#22312;&#19981;&#21516;&#30340;&#20989;&#25968;&#20013;&#35775;&#38382;&#23186;&#20307;&#27969;&#23545;&#35937;
    let mediaStream;
    // &#25429;&#33719;&#23186;&#20307;&#27969;
    let mediaRecorder;

    /**
     * &#28857;&#20987;&#24320;&#22987;&#25353;&#38062;&#26102;&#65292;&#20808;&#25171;&#24320;&#35270;&#39057;&#35774;&#22791;&#65292;&#28982;&#21518;&#33719;&#21462;&#35270;&#39057;&#35774;&#22791;&#30340;&#23186;&#20307;&#27969;&#25968;&#25454;&#65292;&#28982;&#21518;&#25910;&#38598;&#23186;&#20307;&#27969;&#25968;&#25454;
     * @returns {Promise<void>}
     */
    startButton.onclick = async () => {
        // &#23186;&#20307;&#32422;&#26463;&#23545;&#35937;&#65292;&#25351;&#23450;&#33719;&#21462;&#30340;&#23186;&#20307;&#31867;&#22411;&#20026;&#38899;&#39057;&#21644;&#35270;&#39057;&#65292;&#35270;&#39057;&#23485;&#39640;&#20026;&#29702;&#24819;&#20540;1280x720&#65292;&#20351;&#29992;&#29992;&#25143;&#21069;&#32622;&#25668;&#20687;&#22836;&#65292;&#24103;&#29575;&#20026;10&#21040;15
        let constraints = {
            audio: true,
            video: true
        };

        // 1. &#25171;&#24320;&#35270;&#39057;&#35774;&#22791;&#65292;&#33719;&#21462;&#29992;&#25143;&#23186;&#20307;&#35774;&#22791;&#30340;&#27969;&#23545;&#35937;
        mediaStream = await navigator.mediaDevices.getUserMedia(constraints);

        // &#23558;&#33719;&#21462;&#21040;&#30340;&#23186;&#20307;&#35774;&#22791;&#30340;&#27969;&#23545;&#35937;&#65292;&#36171;&#20540;&#32473;&#35270;&#39057;&#20803;&#32032;&#30340; srcObject &#23646;&#24615;
        video.srcObject = mediaStream;
        // &#24403;&#23186;&#20307;&#20803;&#25968;&#25454;&#24050;&#21152;&#36733;&#26102;&#25191;&#34892;&#30340;&#22238;&#35843;&#20989;&#25968;&#65292;&#24320;&#22987;&#25773;&#25918;&#35270;&#39057;
        video.onloadedmetadata = () => {
            video.play();
        };

        startButton.style.background = "red";
        startButton.style.color = "black";

        // 2. &#25429;&#33719;&#23186;&#20307;&#27969;
        mediaRecorder = new MediaRecorder(mediaStream);
        mediaRecorder.start();

        // 3. &#25910;&#38598;&#24405;&#21046;&#30340;&#25968;&#25454;
        let chunks = [];
        // &#24403;&#20851;&#38381;mediaRecorder.stop()&#26102;&#20250;&#35302;&#21457;&#36825;&#20010;&#20107;&#20214;
        mediaRecorder.ondataavailable = async (event) => {
            chunks.push(event.data);
            // &#21019;&#24314;&#19968;&#20010;&#26032;&#30340;Blob&#23545;&#35937;&#65292;&#21253;&#21547;&#24050;&#25910;&#38598;&#21040;&#30340;&#35270;&#39057;&#25968;&#25454;
            let blob = new Blob(chunks, {type: 'video/webm'});

            // &#21019;&#24314;&#19968;&#20010;FormData&#23545;&#35937;&#65292;&#29992;&#20110;&#23558;&#35270;&#39057;&#25968;&#25454;&#21457;&#36865;&#21040;FastAPI&#31471;&#28857;
            let formData = new FormData();
            formData.append('file', blob, 'video.webm');

            // &#20351;&#29992;Fetch API&#23558;&#35270;&#39057;&#25968;&#25454;&#21457;&#36865;&#21040;FastAPI&#31471;&#28857;
            let response = await fetch('http://172.16.176.59:8000/upload/', {
                method: 'POST',
                body: formData
            });
            // &#26381;&#21153;&#31471;&#36820;&#22238;&#32467;&#26524;
            let data = await response.json();
            console.log(data);
        };
    }


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
            // console.log(mediaRecorder.state);

            // &#28165;&#38500;&#35270;&#39057;&#20803;&#32032;&#30340; srcObject &#23646;&#24615;
            video.srcObject = null;

            startButton.style.background = "";
            startButton.style.color = "";
        }
    }
</script>




```
```

### 服务端

<div style="overflow:hidden; clear:both; width: 100%; height: 40px; position: relative;">- - - - - -

 <span style="position: absolute;top: 50%;left: 50%; transform: translate(-50%, -50%); background-color: white;">以下为隐藏内容</span> </div> ```
<pre data-language="HTML">```markup



    
    <meta charset="UTF-8"></meta>
    
    <meta content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0" name="viewport"></meta>
    
    <meta content="yes" name="apple-mobile-web-capable"></meta>
    
    <title>测试验证媒体流传输</title>
    
    <style>
        /* &#35774;&#32622;&#35270;&#39057;&#20803;&#32032;&#26679;&#24335; */
        #videoId {
            width: 512px;
            height: 256px;
        }
    </style>



<div id="controls">
    
    <button id="startId">开始</button>
    
    <button id="stopId">停止</button>
</div>

<video autoplay="false" controls="" id="videoId"></video>


<script>
    let startButton = document.getElementById('startId');
    let stopButton = document.getElementById('stopId');
    // &#33719;&#21462;&#35270;&#39057;&#20803;&#32032;
    let video = document.getElementById('videoId');

    // &#22768;&#26126;&#19968;&#20010;&#20840;&#23616;&#21464;&#37327;&#20197;&#20415;&#22312;&#19981;&#21516;&#30340;&#20989;&#25968;&#20013;&#35775;&#38382;&#23186;&#20307;&#27969;&#23545;&#35937;
    let mediaStream;
    // &#25429;&#33719;&#23186;&#20307;&#27969;
    let mediaRecorder;

    /**
     * &#28857;&#20987;&#24320;&#22987;&#25353;&#38062;&#26102;&#65292;&#20808;&#25171;&#24320;&#35270;&#39057;&#35774;&#22791;&#65292;&#28982;&#21518;&#33719;&#21462;&#35270;&#39057;&#35774;&#22791;&#30340;&#23186;&#20307;&#27969;&#25968;&#25454;&#65292;&#28982;&#21518;&#25910;&#38598;&#23186;&#20307;&#27969;&#25968;&#25454;
     * @returns {Promise<void>}
     */
    startButton.onclick = async () => {
        // &#23186;&#20307;&#32422;&#26463;&#23545;&#35937;&#65292;&#25351;&#23450;&#33719;&#21462;&#30340;&#23186;&#20307;&#31867;&#22411;&#20026;&#38899;&#39057;&#21644;&#35270;&#39057;&#65292;&#35270;&#39057;&#23485;&#39640;&#20026;&#29702;&#24819;&#20540;1280x720&#65292;&#20351;&#29992;&#29992;&#25143;&#21069;&#32622;&#25668;&#20687;&#22836;&#65292;&#24103;&#29575;&#20026;10&#21040;15
        let constraints = {
            audio: true,
            video: true
        };

        // 1. &#25171;&#24320;&#35270;&#39057;&#35774;&#22791;&#65292;&#33719;&#21462;&#29992;&#25143;&#23186;&#20307;&#35774;&#22791;&#30340;&#27969;&#23545;&#35937;
        mediaStream = await navigator.mediaDevices.getUserMedia(constraints);

        // &#23558;&#33719;&#21462;&#21040;&#30340;&#23186;&#20307;&#35774;&#22791;&#30340;&#27969;&#23545;&#35937;&#65292;&#36171;&#20540;&#32473;&#35270;&#39057;&#20803;&#32032;&#30340; srcObject &#23646;&#24615;
        video.srcObject = mediaStream;
        // &#24403;&#23186;&#20307;&#20803;&#25968;&#25454;&#24050;&#21152;&#36733;&#26102;&#25191;&#34892;&#30340;&#22238;&#35843;&#20989;&#25968;&#65292;&#24320;&#22987;&#25773;&#25918;&#35270;&#39057;
        video.onloadedmetadata = () => {
            video.play();
        };

        startButton.style.background = "red";
        startButton.style.color = "black";

        // 2. &#25429;&#33719;&#23186;&#20307;&#27969;
        mediaRecorder = new MediaRecorder(mediaStream);
        mediaRecorder.start();

        // 3. &#25910;&#38598;&#24405;&#21046;&#30340;&#25968;&#25454;
        let chunks = [];
        // &#24403;&#20851;&#38381;mediaRecorder.stop()&#26102;&#20250;&#35302;&#21457;&#36825;&#20010;&#20107;&#20214;
        mediaRecorder.ondataavailable = async (event) => {
            chunks.push(event.data);
            // &#21019;&#24314;&#19968;&#20010;&#26032;&#30340;Blob&#23545;&#35937;&#65292;&#21253;&#21547;&#24050;&#25910;&#38598;&#21040;&#30340;&#35270;&#39057;&#25968;&#25454;
            let blob = new Blob(chunks, {type: 'video/webm'});

            // &#21019;&#24314;&#19968;&#20010;FormData&#23545;&#35937;&#65292;&#29992;&#20110;&#23558;&#35270;&#39057;&#25968;&#25454;&#21457;&#36865;&#21040;FastAPI&#31471;&#28857;
            let formData = new FormData();
            formData.append('file', blob, 'video.webm');

            // &#20351;&#29992;Fetch API&#23558;&#35270;&#39057;&#25968;&#25454;&#21457;&#36865;&#21040;FastAPI&#31471;&#28857;
            let response = await fetch('http://172.16.176.59:8000/upload/', {
                method: 'POST',
                body: formData
            });
            // &#26381;&#21153;&#31471;&#36820;&#22238;&#32467;&#26524;
            let data = await response.json();
            console.log(data);
        };
    }


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
            // console.log(mediaRecorder.state);

            // &#28165;&#38500;&#35270;&#39057;&#20803;&#32032;&#30340; srcObject &#23646;&#24615;
            video.srcObject = null;

            startButton.style.background = "";
            startButton.style.color = "";
        }
    }
</script>




```
```

引入ASR模型
=======

### 修改服务端

<div style="overflow:hidden; clear:both; width: 100%; height: 40px; position: relative;">- - - - - -

 <span style="position: absolute;top: 50%;left: 50%; transform: translate(-50%, -50%); background-color: white;">以下为隐藏内容</span> </div> ```
<pre data-language="HTML">```markup



    
    <meta charset="UTF-8"></meta>
    
    <meta content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0" name="viewport"></meta>
    
    <meta content="yes" name="apple-mobile-web-capable"></meta>
    
    <title>测试验证媒体流传输</title>
    
    <style>
        /* &#35774;&#32622;&#35270;&#39057;&#20803;&#32032;&#26679;&#24335; */
        #videoId {
            width: 512px;
            height: 256px;
        }
    </style>



<div id="controls">
    
    <button id="startId">开始</button>
    
    <button id="stopId">停止</button>
</div>

<video autoplay="false" controls="" id="videoId"></video>


<script>
    let startButton = document.getElementById('startId');
    let stopButton = document.getElementById('stopId');
    // &#33719;&#21462;&#35270;&#39057;&#20803;&#32032;
    let video = document.getElementById('videoId');

    // &#22768;&#26126;&#19968;&#20010;&#20840;&#23616;&#21464;&#37327;&#20197;&#20415;&#22312;&#19981;&#21516;&#30340;&#20989;&#25968;&#20013;&#35775;&#38382;&#23186;&#20307;&#27969;&#23545;&#35937;
    let mediaStream;
    // &#25429;&#33719;&#23186;&#20307;&#27969;
    let mediaRecorder;

    /**
     * &#28857;&#20987;&#24320;&#22987;&#25353;&#38062;&#26102;&#65292;&#20808;&#25171;&#24320;&#35270;&#39057;&#35774;&#22791;&#65292;&#28982;&#21518;&#33719;&#21462;&#35270;&#39057;&#35774;&#22791;&#30340;&#23186;&#20307;&#27969;&#25968;&#25454;&#65292;&#28982;&#21518;&#25910;&#38598;&#23186;&#20307;&#27969;&#25968;&#25454;
     * @returns {Promise<void>}
     */
    startButton.onclick = async () => {
        // &#23186;&#20307;&#32422;&#26463;&#23545;&#35937;&#65292;&#25351;&#23450;&#33719;&#21462;&#30340;&#23186;&#20307;&#31867;&#22411;&#20026;&#38899;&#39057;&#21644;&#35270;&#39057;&#65292;&#35270;&#39057;&#23485;&#39640;&#20026;&#29702;&#24819;&#20540;1280x720&#65292;&#20351;&#29992;&#29992;&#25143;&#21069;&#32622;&#25668;&#20687;&#22836;&#65292;&#24103;&#29575;&#20026;10&#21040;15
        let constraints = {
            audio: true,
            video: true
        };

        // 1. &#25171;&#24320;&#35270;&#39057;&#35774;&#22791;&#65292;&#33719;&#21462;&#29992;&#25143;&#23186;&#20307;&#35774;&#22791;&#30340;&#27969;&#23545;&#35937;
        mediaStream = await navigator.mediaDevices.getUserMedia(constraints);

        // &#23558;&#33719;&#21462;&#21040;&#30340;&#23186;&#20307;&#35774;&#22791;&#30340;&#27969;&#23545;&#35937;&#65292;&#36171;&#20540;&#32473;&#35270;&#39057;&#20803;&#32032;&#30340; srcObject &#23646;&#24615;
        video.srcObject = mediaStream;
        // &#24403;&#23186;&#20307;&#20803;&#25968;&#25454;&#24050;&#21152;&#36733;&#26102;&#25191;&#34892;&#30340;&#22238;&#35843;&#20989;&#25968;&#65292;&#24320;&#22987;&#25773;&#25918;&#35270;&#39057;
        video.onloadedmetadata = () => {
            video.play();
        };

        startButton.style.background = "red";
        startButton.style.color = "black";

        // 2. &#25429;&#33719;&#23186;&#20307;&#27969;
        mediaRecorder = new MediaRecorder(mediaStream);
        mediaRecorder.start();

        // 3. &#25910;&#38598;&#24405;&#21046;&#30340;&#25968;&#25454;
        let chunks = [];
        // &#24403;&#20851;&#38381;mediaRecorder.stop()&#26102;&#20250;&#35302;&#21457;&#36825;&#20010;&#20107;&#20214;
        mediaRecorder.ondataavailable = async (event) => {
            chunks.push(event.data);
            // &#21019;&#24314;&#19968;&#20010;&#26032;&#30340;Blob&#23545;&#35937;&#65292;&#21253;&#21547;&#24050;&#25910;&#38598;&#21040;&#30340;&#35270;&#39057;&#25968;&#25454;
            let blob = new Blob(chunks, {type: 'video/webm'});

            // &#21019;&#24314;&#19968;&#20010;FormData&#23545;&#35937;&#65292;&#29992;&#20110;&#23558;&#35270;&#39057;&#25968;&#25454;&#21457;&#36865;&#21040;FastAPI&#31471;&#28857;
            let formData = new FormData();
            formData.append('file', blob, 'video.webm');

            // &#20351;&#29992;Fetch API&#23558;&#35270;&#39057;&#25968;&#25454;&#21457;&#36865;&#21040;FastAPI&#31471;&#28857;
            let response = await fetch('http://172.16.176.59:8000/upload/', {
                method: 'POST',
                body: formData
            });
            // &#26381;&#21153;&#31471;&#36820;&#22238;&#32467;&#26524;
            let data = await response.json();
            console.log(data);
        };
    }


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
            // console.log(mediaRecorder.state);

            // &#28165;&#38500;&#35270;&#39057;&#20803;&#32032;&#30340; srcObject &#23646;&#24615;
            video.srcObject = null;

            startButton.style.background = "";
            startButton.style.color = "";
        }
    }
</script>




```
```

引入ASR模型-增量翻译
============

### 修改前端

<div style="overflow:hidden; clear:both; width: 100%; height: 40px; position: relative;">- - - - - -

 <span style="position: absolute;top: 50%;left: 50%; transform: translate(-50%, -50%); background-color: white;">以下为隐藏内容</span> </div> ```
<pre data-language="HTML">```markup



    
    <meta charset="UTF-8"></meta>
    
    <meta content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0" name="viewport"></meta>
    
    <meta content="yes" name="apple-mobile-web-capable"></meta>
    
    <title>测试验证媒体流传输</title>
    
    <style>
        /* &#35774;&#32622;&#35270;&#39057;&#20803;&#32032;&#26679;&#24335; */
        #videoId {
            width: 512px;
            height: 256px;
        }
    </style>



<div id="controls">
    
    <button id="startId">开始</button>
    
    <button id="stopId">停止</button>
</div>

<video autoplay="false" controls="" id="videoId"></video>


<script>
    let startButton = document.getElementById('startId');
    let stopButton = document.getElementById('stopId');
    // &#33719;&#21462;&#35270;&#39057;&#20803;&#32032;
    let video = document.getElementById('videoId');

    // &#22768;&#26126;&#19968;&#20010;&#20840;&#23616;&#21464;&#37327;&#20197;&#20415;&#22312;&#19981;&#21516;&#30340;&#20989;&#25968;&#20013;&#35775;&#38382;&#23186;&#20307;&#27969;&#23545;&#35937;
    let mediaStream;
    // &#25429;&#33719;&#23186;&#20307;&#27969;
    let mediaRecorder;

    /**
     * &#28857;&#20987;&#24320;&#22987;&#25353;&#38062;&#26102;&#65292;&#20808;&#25171;&#24320;&#35270;&#39057;&#35774;&#22791;&#65292;&#28982;&#21518;&#33719;&#21462;&#35270;&#39057;&#35774;&#22791;&#30340;&#23186;&#20307;&#27969;&#25968;&#25454;&#65292;&#28982;&#21518;&#25910;&#38598;&#23186;&#20307;&#27969;&#25968;&#25454;
     * @returns {Promise<void>}
     */
    startButton.onclick = async () => {
        // &#23186;&#20307;&#32422;&#26463;&#23545;&#35937;&#65292;&#25351;&#23450;&#33719;&#21462;&#30340;&#23186;&#20307;&#31867;&#22411;&#20026;&#38899;&#39057;&#21644;&#35270;&#39057;&#65292;&#35270;&#39057;&#23485;&#39640;&#20026;&#29702;&#24819;&#20540;1280x720&#65292;&#20351;&#29992;&#29992;&#25143;&#21069;&#32622;&#25668;&#20687;&#22836;&#65292;&#24103;&#29575;&#20026;10&#21040;15
        let constraints = {
            audio: true,
            video: true
        };

        // 1. &#25171;&#24320;&#35270;&#39057;&#35774;&#22791;&#65292;&#33719;&#21462;&#29992;&#25143;&#23186;&#20307;&#35774;&#22791;&#30340;&#27969;&#23545;&#35937;
        mediaStream = await navigator.mediaDevices.getUserMedia(constraints);

        // &#23558;&#33719;&#21462;&#21040;&#30340;&#23186;&#20307;&#35774;&#22791;&#30340;&#27969;&#23545;&#35937;&#65292;&#36171;&#20540;&#32473;&#35270;&#39057;&#20803;&#32032;&#30340; srcObject &#23646;&#24615;
        video.srcObject = mediaStream;
        // &#24403;&#23186;&#20307;&#20803;&#25968;&#25454;&#24050;&#21152;&#36733;&#26102;&#25191;&#34892;&#30340;&#22238;&#35843;&#20989;&#25968;&#65292;&#24320;&#22987;&#25773;&#25918;&#35270;&#39057;
        video.onloadedmetadata = () => {
            video.play();
        };

        startButton.style.background = "red";
        startButton.style.color = "black";

        // 2. &#25429;&#33719;&#23186;&#20307;&#27969;
        mediaRecorder = new MediaRecorder(mediaStream);
        mediaRecorder.start();

        // 3. &#25910;&#38598;&#24405;&#21046;&#30340;&#25968;&#25454;
        let chunks = [];
        // &#24403;&#20851;&#38381;mediaRecorder.stop()&#26102;&#20250;&#35302;&#21457;&#36825;&#20010;&#20107;&#20214;
        mediaRecorder.ondataavailable = async (event) => {
            chunks.push(event.data);
            // &#21019;&#24314;&#19968;&#20010;&#26032;&#30340;Blob&#23545;&#35937;&#65292;&#21253;&#21547;&#24050;&#25910;&#38598;&#21040;&#30340;&#35270;&#39057;&#25968;&#25454;
            let blob = new Blob(chunks, {type: 'video/webm'});

            // &#21019;&#24314;&#19968;&#20010;FormData&#23545;&#35937;&#65292;&#29992;&#20110;&#23558;&#35270;&#39057;&#25968;&#25454;&#21457;&#36865;&#21040;FastAPI&#31471;&#28857;
            let formData = new FormData();
            formData.append('file', blob, 'video.webm');

            // &#20351;&#29992;Fetch API&#23558;&#35270;&#39057;&#25968;&#25454;&#21457;&#36865;&#21040;FastAPI&#31471;&#28857;
            let response = await fetch('http://172.16.176.59:8000/upload/', {
                method: 'POST',
                body: formData
            });
            // &#26381;&#21153;&#31471;&#36820;&#22238;&#32467;&#26524;
            let data = await response.json();
            console.log(data);
        };
    }


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
            // console.log(mediaRecorder.state);

            // &#28165;&#38500;&#35270;&#39057;&#20803;&#32032;&#30340; srcObject &#23646;&#24615;
            video.srcObject = null;

            startButton.style.background = "";
            startButton.style.color = "";
        }
    }
</script>




```
```

- - - - - -

长按录音
====

<div style="overflow:hidden; clear:both; width: 100%; height: 40px; position: relative;">- - - - - -

 <span style="position: absolute;top: 50%;left: 50%; transform: translate(-50%, -50%); background-color: white;">以下为隐藏内容</span> </div> ```
<pre data-language="HTML">```markup



    
    <meta charset="UTF-8"></meta>
    
    <meta content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0" name="viewport"></meta>
    
    <meta content="yes" name="apple-mobile-web-capable"></meta>
    
    <title>测试验证媒体流传输</title>
    
    <style>
        /* &#35774;&#32622;&#35270;&#39057;&#20803;&#32032;&#26679;&#24335; */
        #videoId {
            width: 512px;
            height: 256px;
        }
    </style>



<div id="controls">
    
    <button id="startId">开始</button>
    
    <button id="stopId">停止</button>
</div>

<video autoplay="false" controls="" id="videoId"></video>


<script>
    let startButton = document.getElementById('startId');
    let stopButton = document.getElementById('stopId');
    // &#33719;&#21462;&#35270;&#39057;&#20803;&#32032;
    let video = document.getElementById('videoId');

    // &#22768;&#26126;&#19968;&#20010;&#20840;&#23616;&#21464;&#37327;&#20197;&#20415;&#22312;&#19981;&#21516;&#30340;&#20989;&#25968;&#20013;&#35775;&#38382;&#23186;&#20307;&#27969;&#23545;&#35937;
    let mediaStream;
    // &#25429;&#33719;&#23186;&#20307;&#27969;
    let mediaRecorder;

    /**
     * &#28857;&#20987;&#24320;&#22987;&#25353;&#38062;&#26102;&#65292;&#20808;&#25171;&#24320;&#35270;&#39057;&#35774;&#22791;&#65292;&#28982;&#21518;&#33719;&#21462;&#35270;&#39057;&#35774;&#22791;&#30340;&#23186;&#20307;&#27969;&#25968;&#25454;&#65292;&#28982;&#21518;&#25910;&#38598;&#23186;&#20307;&#27969;&#25968;&#25454;
     * @returns {Promise<void>}
     */
    startButton.onclick = async () => {
        // &#23186;&#20307;&#32422;&#26463;&#23545;&#35937;&#65292;&#25351;&#23450;&#33719;&#21462;&#30340;&#23186;&#20307;&#31867;&#22411;&#20026;&#38899;&#39057;&#21644;&#35270;&#39057;&#65292;&#35270;&#39057;&#23485;&#39640;&#20026;&#29702;&#24819;&#20540;1280x720&#65292;&#20351;&#29992;&#29992;&#25143;&#21069;&#32622;&#25668;&#20687;&#22836;&#65292;&#24103;&#29575;&#20026;10&#21040;15
        let constraints = {
            audio: true,
            video: true
        };

        // 1. &#25171;&#24320;&#35270;&#39057;&#35774;&#22791;&#65292;&#33719;&#21462;&#29992;&#25143;&#23186;&#20307;&#35774;&#22791;&#30340;&#27969;&#23545;&#35937;
        mediaStream = await navigator.mediaDevices.getUserMedia(constraints);

        // &#23558;&#33719;&#21462;&#21040;&#30340;&#23186;&#20307;&#35774;&#22791;&#30340;&#27969;&#23545;&#35937;&#65292;&#36171;&#20540;&#32473;&#35270;&#39057;&#20803;&#32032;&#30340; srcObject &#23646;&#24615;
        video.srcObject = mediaStream;
        // &#24403;&#23186;&#20307;&#20803;&#25968;&#25454;&#24050;&#21152;&#36733;&#26102;&#25191;&#34892;&#30340;&#22238;&#35843;&#20989;&#25968;&#65292;&#24320;&#22987;&#25773;&#25918;&#35270;&#39057;
        video.onloadedmetadata = () => {
            video.play();
        };

        startButton.style.background = "red";
        startButton.style.color = "black";

        // 2. &#25429;&#33719;&#23186;&#20307;&#27969;
        mediaRecorder = new MediaRecorder(mediaStream);
        mediaRecorder.start();

        // 3. &#25910;&#38598;&#24405;&#21046;&#30340;&#25968;&#25454;
        let chunks = [];
        // &#24403;&#20851;&#38381;mediaRecorder.stop()&#26102;&#20250;&#35302;&#21457;&#36825;&#20010;&#20107;&#20214;
        mediaRecorder.ondataavailable = async (event) => {
            chunks.push(event.data);
            // &#21019;&#24314;&#19968;&#20010;&#26032;&#30340;Blob&#23545;&#35937;&#65292;&#21253;&#21547;&#24050;&#25910;&#38598;&#21040;&#30340;&#35270;&#39057;&#25968;&#25454;
            let blob = new Blob(chunks, {type: 'video/webm'});

            // &#21019;&#24314;&#19968;&#20010;FormData&#23545;&#35937;&#65292;&#29992;&#20110;&#23558;&#35270;&#39057;&#25968;&#25454;&#21457;&#36865;&#21040;FastAPI&#31471;&#28857;
            let formData = new FormData();
            formData.append('file', blob, 'video.webm');

            // &#20351;&#29992;Fetch API&#23558;&#35270;&#39057;&#25968;&#25454;&#21457;&#36865;&#21040;FastAPI&#31471;&#28857;
            let response = await fetch('http://172.16.176.59:8000/upload/', {
                method: 'POST',
                body: formData
            });
            // &#26381;&#21153;&#31471;&#36820;&#22238;&#32467;&#26524;
            let data = await response.json();
            console.log(data);
        };
    }


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
            // console.log(mediaRecorder.state);

            // &#28165;&#38500;&#35270;&#39057;&#20803;&#32032;&#30340; srcObject &#23646;&#24615;
            video.srcObject = null;

            startButton.style.background = "";
            startButton.style.color = "";
        }
    }
</script>




```
```

- - - - - -

长按录音-基于[模型适配服务端](https://gitee.com/eric-mao/ai-0x04 "模型适配服务端")
==============================================================

<div style="overflow:hidden; clear:both; width: 100%; height: 40px; position: relative;">- - - - - -

 <span style="position: absolute;top: 50%;left: 50%; transform: translate(-50%, -50%); background-color: white;">以下为隐藏内容</span> </div> ```
<pre data-language="HTML">```markup



    
    <meta charset="UTF-8"></meta>
    
    <meta content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0" name="viewport"></meta>
    
    <meta content="yes" name="apple-mobile-web-capable"></meta>
    
    <title>测试验证媒体流传输</title>
    
    <style>
        /* &#35774;&#32622;&#35270;&#39057;&#20803;&#32032;&#26679;&#24335; */
        #videoId {
            width: 512px;
            height: 256px;
        }
    </style>



<div id="controls">
    
    <button id="startId">开始</button>
    
    <button id="stopId">停止</button>
</div>

<video autoplay="false" controls="" id="videoId"></video>


<script>
    let startButton = document.getElementById('startId');
    let stopButton = document.getElementById('stopId');
    // &#33719;&#21462;&#35270;&#39057;&#20803;&#32032;
    let video = document.getElementById('videoId');

    // &#22768;&#26126;&#19968;&#20010;&#20840;&#23616;&#21464;&#37327;&#20197;&#20415;&#22312;&#19981;&#21516;&#30340;&#20989;&#25968;&#20013;&#35775;&#38382;&#23186;&#20307;&#27969;&#23545;&#35937;
    let mediaStream;
    // &#25429;&#33719;&#23186;&#20307;&#27969;
    let mediaRecorder;

    /**
     * &#28857;&#20987;&#24320;&#22987;&#25353;&#38062;&#26102;&#65292;&#20808;&#25171;&#24320;&#35270;&#39057;&#35774;&#22791;&#65292;&#28982;&#21518;&#33719;&#21462;&#35270;&#39057;&#35774;&#22791;&#30340;&#23186;&#20307;&#27969;&#25968;&#25454;&#65292;&#28982;&#21518;&#25910;&#38598;&#23186;&#20307;&#27969;&#25968;&#25454;
     * @returns {Promise<void>}
     */
    startButton.onclick = async () => {
        // &#23186;&#20307;&#32422;&#26463;&#23545;&#35937;&#65292;&#25351;&#23450;&#33719;&#21462;&#30340;&#23186;&#20307;&#31867;&#22411;&#20026;&#38899;&#39057;&#21644;&#35270;&#39057;&#65292;&#35270;&#39057;&#23485;&#39640;&#20026;&#29702;&#24819;&#20540;1280x720&#65292;&#20351;&#29992;&#29992;&#25143;&#21069;&#32622;&#25668;&#20687;&#22836;&#65292;&#24103;&#29575;&#20026;10&#21040;15
        let constraints = {
            audio: true,
            video: true
        };

        // 1. &#25171;&#24320;&#35270;&#39057;&#35774;&#22791;&#65292;&#33719;&#21462;&#29992;&#25143;&#23186;&#20307;&#35774;&#22791;&#30340;&#27969;&#23545;&#35937;
        mediaStream = await navigator.mediaDevices.getUserMedia(constraints);

        // &#23558;&#33719;&#21462;&#21040;&#30340;&#23186;&#20307;&#35774;&#22791;&#30340;&#27969;&#23545;&#35937;&#65292;&#36171;&#20540;&#32473;&#35270;&#39057;&#20803;&#32032;&#30340; srcObject &#23646;&#24615;
        video.srcObject = mediaStream;
        // &#24403;&#23186;&#20307;&#20803;&#25968;&#25454;&#24050;&#21152;&#36733;&#26102;&#25191;&#34892;&#30340;&#22238;&#35843;&#20989;&#25968;&#65292;&#24320;&#22987;&#25773;&#25918;&#35270;&#39057;
        video.onloadedmetadata = () => {
            video.play();
        };

        startButton.style.background = "red";
        startButton.style.color = "black";

        // 2. &#25429;&#33719;&#23186;&#20307;&#27969;
        mediaRecorder = new MediaRecorder(mediaStream);
        mediaRecorder.start();

        // 3. &#25910;&#38598;&#24405;&#21046;&#30340;&#25968;&#25454;
        let chunks = [];
        // &#24403;&#20851;&#38381;mediaRecorder.stop()&#26102;&#20250;&#35302;&#21457;&#36825;&#20010;&#20107;&#20214;
        mediaRecorder.ondataavailable = async (event) => {
            chunks.push(event.data);
            // &#21019;&#24314;&#19968;&#20010;&#26032;&#30340;Blob&#23545;&#35937;&#65292;&#21253;&#21547;&#24050;&#25910;&#38598;&#21040;&#30340;&#35270;&#39057;&#25968;&#25454;
            let blob = new Blob(chunks, {type: 'video/webm'});

            // &#21019;&#24314;&#19968;&#20010;FormData&#23545;&#35937;&#65292;&#29992;&#20110;&#23558;&#35270;&#39057;&#25968;&#25454;&#21457;&#36865;&#21040;FastAPI&#31471;&#28857;
            let formData = new FormData();
            formData.append('file', blob, 'video.webm');

            // &#20351;&#29992;Fetch API&#23558;&#35270;&#39057;&#25968;&#25454;&#21457;&#36865;&#21040;FastAPI&#31471;&#28857;
            let response = await fetch('http://172.16.176.59:8000/upload/', {
                method: 'POST',
                body: formData
            });
            // &#26381;&#21153;&#31471;&#36820;&#22238;&#32467;&#26524;
            let data = await response.json();
            console.log(data);
        };
    }


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
            // console.log(mediaRecorder.state);

            // &#28165;&#38500;&#35270;&#39057;&#20803;&#32032;&#30340; srcObject &#23646;&#24615;
            video.srcObject = null;

            startButton.style.background = "";
            startButton.style.color = "";
        }
    }
</script>




```
```

- - - - - -

> 以上都是前置条件与基础知识的储备，接下来才是真正的基于`Web实时通信`实现的`实时流媒体`传输
> 
>  `WebRTC`全称是`Web Real-Time Communication`，`网页即时通信`。
> 
>  WebRTC在2011年6月1日开源，并在Google、Mozilla、Opera等各家巨头公司的支持下被纳入W3C 推荐标准，给浏览器和移动应用提供了即时通信的能力。
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
>  使用WebRTC实现实时通信最核心的API就是`RTCPeerConnection`，它代表一个由本地计算机到远端的WebRTC连接，该接口提供了创建、保持、监控及关闭连接的方法的实现，有点类似于`socket`。
> 
>  相关的API
> 
> - createOffer 创建Offer方法
> - setLocalDescription 设置本地SDP描述信息
> - peer.onicecandidate 设置完本地SDP描述信息后会触发该方法，打开一个连接，开始运转媒体流
> - setRemoteDescription 设置远端的SDP描述信息，由本地发送
> - peer.ontrack 设置完远端SDP描述信息后会触发该方法，接收对方的媒体流
> - createAnswer 远端创建应答Answer方法
> - RTCIceCandidate RTC网络信息，IP、端口等
> - addIceCandidate 连接添加对方的网络信息