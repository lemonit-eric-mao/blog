---
title: "Node.js 上传处理 Excel 为 Json"
date: "2018-09-04"
categories: 
  - "vue"
---

```markup
<template>
    <section>
        <el-upload ref="upload" accept=".xls, .xlsx" :limit="1" :on-exceed="onExceed" :multiple="false" action="" :auto-upload="false" :on-change="onChange">
            <el-button slot="trigger" class="el-icon-upload" size="small" type="primary"> 点击上传</el-button>
            <el-button style="margin-left: 10px;" size="small" type="success" @click="submitUpload">上传到服务器</el-button>
        </el-upload>
    </section>
</template>
```

* * *

```javascript
<script>

    import XLSX from 'xlsx';

    /**
     * 上传附件
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
                // 文件列表
                fileList: [],
            }
        },
        methods: {

            /**
             * 将列表中文件上传到服务器
             */
            submitUpload() {
                // 获取 File对象
                let file = this.fileList[0].raw;
                // 读取 Excel
                this.readExcel(file, async (sheetArray) => {
                    console.log(JSON.stringify(sheetArray[0], null, 4));
                    let params = {
                        data: sheetArray[0]
                    };
                    await this.$axios.post('/data/bqroot/upload', params);
                    // 上传成功提示
                    this.$message.success('文件上传成功!');
                });
            },

            /**
             * 文件超出个数限制时
             */
            onExceed() {
                this.$message.error('只允许单文件上传!');
            },

            /**
             * 文件状态改变时
             */
            onChange(file, fileList) {
                this.fileList = fileList;
            },

            /**
             * 读取 解析 excel文件
             * @param file 对象
             */
            readExcel(file, callback) {

                let fileReader = new FileReader();
                fileReader.readAsBinaryString(file);
                // 等待文件读取结束
                fileReader.onload = (ev) => {

                    let data = ev.target.result;
                    // 解析 excel
                    let workbook = XLSX.read(data, {
                        type: 'binary'
                    });
                    // 进一步解析 sheet
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

* * *

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
