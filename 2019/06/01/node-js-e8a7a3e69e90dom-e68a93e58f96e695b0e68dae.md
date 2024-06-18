---
title: 'Node.js 解析DOM 抓取数据'
date: '2019-06-01T06:13:25+00:00'
status: publish
permalink: /2019/06/01/node-js-%e8%a7%a3%e6%9e%90dom-%e6%8a%93%e5%8f%96%e6%95%b0%e6%8d%ae
author: 毛巳煜
excerpt: ''
type: post
id: 4719
category:
    - node.js
tag: []
post_format: []
---
##### 使用 插件 cheerio 进行解析

```javascript
const <span class="katex math inline">cheerio = require('cheerio')
const</span>axios = require('axios')

class Domain {

    /**
     * 查询域名
     */
    async queryDomain(params) {

        let result = {}
        let html = await <span class="katex math inline">axios.get(`https://www.whois.com/whois/</span>{params.domain}`);
        const <span class="katex math inline">=</span>cheerio.load(html.data);
        let row = <span class="katex math inline">('#page-wrapper > div > div.whois_main_column > div.df-block > div.df-row');
        row.map((i, row) => {
            // 在获取到的内容中 br元素后面追加 分隔符</span>('br', row).append(' | ');
            let text = $(row).text().split(':');
            result[text[0]] = text[1];
        });

        return result;
    };
}

module.exports = Domain;

```