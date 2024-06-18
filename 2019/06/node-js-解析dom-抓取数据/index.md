---
title: "Node.js 解析DOM 抓取数据"
date: "2019-06-01"
categories: 
  - "node-js"
---

##### 使用 插件 cheerio 进行解析

```javascript
const $cheerio = require('cheerio')
const $axios = require('axios')

class Domain {

    /**
     * 查询域名
     */
    async queryDomain(params) {

        let result = {}
        let html = await $axios.get(`https://www.whois.com/whois/${params.domain}`);
        const $ = $cheerio.load(html.data);
        let row = $('#page-wrapper > div > div.whois_main_column > div.df-block > div.df-row');
        row.map((i, row) => {
            // 在获取到的内容中 br元素后面追加 分隔符
            $('br', row).append(' | ');
            let text = $(row).text().split(':');
            result[text[0]] = text[1];
        });

        return result;
    };
}

module.exports = Domain;
```
