---
title: "H5 调用手机摄像头;  上传 图片, 音频, 视频"
date: "2018-08-23"
categories: 
  - "移动端"
---

```markup
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1,maximum-scale=1,user-scalable=no">
    <title>H5调用手机摄像头</title>
</head>

<body>

<div>
    <h3>image 图片</h3>
    <input id="imageId" type="file" accept="image/*" onchange="imageChange(this)" capture="camera"/>
    <script>
        function imageChange(self) {
            // 获取文件流
            let file = self.files[0];
            // 获取文件名
            console.log(file.name);
            console.log(file.size);

            // Base64
            let fileReader = new FileReader();
            fileReader.readAsDataURL(file);
            fileReader.onload = function () {
                let img = document.createElement(`img`);
                img.src = fileReader.result;
                self.parentElement.appendChild(img);
            };
        }
    </script>
</div>

<hr/>

<div>
    <h3>image 图片 – 多选</h3>
    <input id="imagesId" type="file" accept="image/*" multiple/>
</div>

<hr/>

<div>
    <h3>image图片 - 前置摄像头调用</h3>
    <p>重点来了，iOS 10.3以后可以通过给 input[type='file'] 的标签里指定 capture="user" 来调用手机前置摄像头了。</p>
    <p><b>注意：</b>如果手机不支持这个特性还是使用的是后置摄像头。</p>
    <input id="userId" type="file" accept="image/*" capture="user"/>
    <p>经过实际测试，Android和IOS两种系统的手机调用的还是后置摄像头！！</p>
</div>

<hr/>

<div>
    <h3>video 视频</h3>
    <input type="file" accept="video/*" capture="camcorder" onchange="videoChange(this)"/>
    <video id="videoId" autoplay="" class="video-js jd-video" x5-video-player-type="h5" webkit-playsinline="" playsinline="" controls=""></video>
    <script>
        function videoChange(self) {
            // 获取文件流
            let file = self.files[0];
            // 获取文件名
            console.log(file.name);
            console.log(file.size);

            // Base64
            let fileReader = new FileReader();
            fileReader.readAsDataURL(file);
            fileReader.onload = function () {
                let source = document.createElement(`source`);
                source.type = 'video/mp4';
                source.src = fileReader.result;
                document.getElementById('videoId').appendChild(source);
            };
        }
    </script>
</div>

<hr/>

<div>
    <h3>audio 音频</h3>
    <input type="file" accept="audio/*" capture="microphone" onchange="audioChange(this)"/>
    <audio id="audioId" controls=""></audio>
    <script>
        function audioChange(self) {
            // 获取文件流
            let file = self.files[0];
            // 获取文件名
            console.log(file.name);
            console.log(file.size);

            // Base64
            let fileReader = new FileReader();
            fileReader.readAsDataURL(file);
            fileReader.onload = function () {
                let source = document.createElement(`source`);
                source.type = 'audio/mpeg';
                source.src = fileReader.result;
                document.getElementById('audioId').appendChild(source);
            };
        }
    </script>
</div>

</body>
</html>
```

#### 附加 使用axios 将图片发送给 Face++ 进行解析

```javascript
<script>
    axios({
        url: 'https://api-cn.faceplusplus.com/cardpp/v1/ocridcard',
        method: 'post',
        data: {
            api_key: 'tUNYFPGEFbbCPikpKh-51mxBOmzj5jBY',
            api_secret: 'DfUqQMivquOa_gEl-mCF4HDBdoPKpQIF',
            image_base64: 'data:image/jpeg;.........'
        },
        transformRequest: [function (data) {
            // 做任何你想改变的数据
            let ret = ''
            for (let it in data) {
                ret += `${encodeURIComponent(it)}=${encodeURIComponent(data[it])}&`
            }
            return ret;
        }],
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    });
</script>
```
