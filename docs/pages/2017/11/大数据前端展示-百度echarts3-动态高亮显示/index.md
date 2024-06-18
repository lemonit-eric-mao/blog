---
title: "大数据前端展示 --> Apache ECharts3 动态高亮显示"
date: "2017-11-16"
categories: 
  - "大数据"
---

## [Apache ECharts3 官方API 文本](https://echarts.apache.org/zh/index.html)

```javascript
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
