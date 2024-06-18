---
title: '大数据前端展示 &#8211;> Apache ECharts3 动态高亮显示'
date: '2017-11-16T16:13:24+00:00'
status: publish
permalink: /2017/11/16/%e5%a4%a7%e6%95%b0%e6%8d%ae%e5%89%8d%e7%ab%af%e5%b1%95%e7%a4%ba-%e7%99%be%e5%ba%a6echarts3-%e5%8a%a8%e6%80%81%e9%ab%98%e4%ba%ae%e6%98%be%e7%a4%ba
author: 毛巳煜
excerpt: ''
type: post
id: 526
category:
    - 大数据
tag: []
post_format: []
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
hestia_layout_select:
    - sidebar-right
---
[Apache ECharts3 官方API 文本](https://echarts.apache.org/zh/index.html)
--------------------------------------------------------------------

```
<pre class="line-numbers prism-highlight" data-start="1">```javascript
  /**
   * 高亮动画
   * @param myChart  你的chart
   * @param option  你的 option
   */
  const highlightAnimation = (myChart, option) => {

    let app = {};
    app.currentIndex = -1;

    setInterval(() => {

      let dataLen = option.series[0].data.length;
      // 取消之前高亮的图形
      myChart.dispatchAction({
        type: 'downplay',
        seriesIndex: 0,
        dataIndex: app.currentIndex
      });
      app.currentIndex = (app.currentIndex + 1) % dataLen;

      // 高亮当前图形
      myChart.dispatchAction({
        type: 'highlight',
        seriesIndex: 0,
        dataIndex: app.currentIndex
      });

      // 显示 tooltip
      myChart.dispatchAction({
        type: 'showTip',
        seriesIndex: 0,
        dataIndex: app.currentIndex
      });

    }, 1000);
  }

```
```