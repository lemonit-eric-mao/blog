---
title: 'Node.js 上传处理 Excel 为 Json'
date: '2018-09-04T19:38:26+00:00'
status: publish
permalink: /2018/09/04/node-js-%e4%b8%8a%e4%bc%a0%e5%a4%84%e7%90%86-excel-%e4%b8%ba-json
author: 毛巳煜
excerpt: ''
type: post
id: 2302
category:
    - vue
tag: []
post_format: []
---
```
<pre data-language="HTML">```markup
<template>
    <section>
        <el-upload :auto-upload="false" :limit="1" :multiple="false" :on-change="onChange" :on-exceed="onExceed" accept=".xls, .xlsx" action="" ref="upload">
            <el-button class="el-icon-upload" size="small" slot="trigger" type="primary"> 点击上传</el-button>
            <el-button size="small" style="margin-left: 10px;" type="success">上传到服务器</el-button>
        </el-upload>
    </section>
</template>

```
```

- - - - - -

```javascript
<script>

    import XLSX from 'xlsx';

    /**
     * &#19978;&#20256;&#38468;&#20214;
     *
     * @date 2018-08-31
     * @author mao_siyu
     */
    export default {
        name: 'upload',
        props: {
            parentsUpload: {
                childUploadMethod(params) {
                }
            }
        },
        data() {
            return {
                // &#25991;&#20214;&#21015;&#34920;
                fileList: [],
            }
        },
        methods: {

            /**
             * &#23558;&#21015;&#34920;&#20013;&#25991;&#20214;&#19978;&#20256;&#21040;&#26381;&#21153;&#22120;
             */
            submitUpload() {
                // &#33719;&#21462; File&#23545;&#35937;
                let file = this.fileList[0].raw;
                // &#35835;&#21462; Excel
                this.readExcel(file, async (sheetArray) => {
                    console.log(JSON.stringify(sheetArray[0], null, 4));
                    let params = {
                        data: sheetArray[0]
                    };
                    await this.<span class="katex math inline">axios.post('/data/bqroot/upload', params);
                    // &#19978;&#20256;&#25104;&#21151;&#25552;&#31034;
                    this.message.success('&#25991;&#20214;&#19978;&#20256;&#25104;&#21151;!');
                });
            },

            /**
             * &#25991;&#20214;&#36229;&#20986;&#20010;&#25968;&#38480;&#21046;&#26102;
             */
            onExceed() {
                this.$message.error('&#21482;&#20801;&#35768;&#21333;&#25991;&#20214;&#19978;&#20256;!');
            },

            /**
             * &#25991;&#20214;&#29366;&#24577;&#25913;&#21464;&#26102;
             */
            onChange(file, fileList) {
                this.fileList = fileList;
            },

            /**
             * &#35835;&#21462; &#35299;&#26512; excel&#25991;&#20214;
             * @param file &#23545;&#35937;
             */
            readExcel(file, callback) {

                let fileReader = new FileReader();
                fileReader.readAsBinaryString(file);
                // &#31561;&#24453;&#25991;&#20214;&#35835;&#21462;&#32467;&#26463;
                fileReader.onload = (ev) => {

                    let data = ev.target.result;
                    // &#35299;&#26512; excel
                    let workbook = XLSX.read(data, {
                        type: 'binary'
                    });
                    // &#36827;&#19968;&#27493;&#35299;&#26512; sheet
                    let sheetArray = [];
                    for (let sheet in workbook.Sheets) {
                        sheetArray.push(XLSX.utils.sheet_to_json(workbook.Sheets[sheet]));
                    }

                    callback(sheetArray);
                }
            }
        }

    }
</script>

```

- - - - - -

```css
<style lang="scss">
    .upload-demo {
        margin: 10px auto;
        .el-upload--text {
            width: auto !important;
            height: auto !important;
            vertical-align: middle;
            border: none;
        }
        .el-upload-dragger {
            width: auto !important;
            height: auto !important;
        }
    }
</style>

```