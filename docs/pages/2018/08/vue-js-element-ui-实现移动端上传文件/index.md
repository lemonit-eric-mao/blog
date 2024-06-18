---
title: "Vue.js + element-ui 实现移动端上传文件"
date: "2018-08-26"
categories: 
  - "移动端"
---

#### element-ui 上传按钮

```markup
<template>
    <section>
        <div class="ident-info">
            <el-upload ref="upload" action="string" :http-request="uploadFile">
                <el-button class="file" size="small" type="primary">点击上传</el-button>
            </el-upload>
        </div>
    </section>
</template>
```

#### 关键方法

```javascript
    uploadFile(param) {
        // 获取文件
        let file = param.file;
        // 获取文件后 清除历史文件
        this.$refs.upload.clearFiles();
        //
        let fileReader = new FileReader();
        // 文件读取
        fileReader.readAsDataURL(file);
        // 读取完成
        fileReader.onload = async (result) => {

            this.$message.info(`正在上传中... ${(file.size / 1024 / 1024).toFixed(2)} MB`);

            try {
                // 上传到 Face++ 做图像识别
                let infoJson = await axios({
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded'
                    },
                    url: 'https://api-cn.faceplusplus.com/cardpp/v1/ocridcard',
                    method: 'post',
                    data: {
                        api_key: 'tUNYFPGEFbbCPikpKh-51mxBOmzj5jBY',
                        api_secret: 'DfUqQMivquOa_gEl-mCF4HDBdoPKpQIF',
                        image_base64: result.srcElement.result
                    },
                    transformRequest: [(data) => {
                        // 做任何你想改变的数据
                        let ret = '';
                        for (let it in data) {
                            ret += `${encodeURIComponent(it)}=${encodeURIComponent(data[it])}&`
                        }
                        return ret;
                    }]
                });

                this.identInfo = infoJson.data.cards[0];
                this.$message.success('证件上传成功!');

            } catch (e) {
                this.$message.error('证件上传失败!');
            }
        }
    }
```

* * *

## 以下是借助第三方插件, 做图片压缩后上传.

`三方插件:` `npm i -S lrz` `import lrz from 'lrz';` [lrz](https://github.com/think2011/localResizeIMG "lrz")

#### 关键方法

```javascript
async uploadFile(param) {

    try {

        // 获取文件
        let file = param.file;
        // 获取文件后 清除历史文件
        this.$refs.upload.clearFiles();

        /**
         * 压缩图片
         * Face++
         * 图片要求 ：
         * 图片格式：JPG(JPEG)，PNG
         * 图片像素尺寸：最小48*48像素，最大4096*4096像素
         * 图片文件大小：2MB === 2097152 byte
         */
        let result = await lrz(file);

        this.$message.info(`正在上传中... ${(result.base64Len / 1024 / 1024).toFixed(2)} MB`);

        let infoJson = await axios({
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            url: 'https://api-cn.faceplusplus.com/cardpp/v1/ocridcard',
            method: 'post',
            data: {
                api_key: 'tUNYFPGEFbbCPikpKh-51mxBOmzj5jBY',
                api_secret: 'DfUqQMivquOa_gEl-mCF4HDBdoPKpQIF',
                image_base64: result.base64
            },
            transformRequest: [(data) => {
                // 做任何你想改变的数据
                let ret = '';
                for (let it in data) {
                    ret += `${encodeURIComponent(it)}=${encodeURIComponent(data[it])}&`
                }
                return ret;
            }]
        });

        this.identInfo = infoJson.data.cards[0];
        this.$message.success('证件上传成功!');

    } catch (e) {
        this.$message.error(`证件上传失败, 请重新调整拍摄位置!`);
    }
}
```
