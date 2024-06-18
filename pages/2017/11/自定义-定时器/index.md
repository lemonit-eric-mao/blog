---
title: "自定义-定时器"
date: "2017-11-16"
categories: 
  - "node-js"
---

```javascript
/**
 * 定时器
 * 可迭代的、可自动扩充容量
 * Created by mao_siyu on 2017/1/14.
 */

// 定时器
var intervalId;
// 开关
var status;

var LK_timer = function () {
}

// 参数配置
LK_timer.options = {
    activeVolume: 0, // 可用容量
    extensionNumber: 10, // 每次扩充的数
    usedCapacityIndex: 0, // 已用容量位置
    time: 1000, // 间隔时间 默认1秒
    extensionFun: function () { // 扩充回调
        // 每次扩充一数量
        LK_timer.options.activeVolume += LK_timer.options.extensionNumber;
        LK_timer.startInterval();
    },
    callback: function (index) { // 程序执行时回调
        console.info(index);
    }
}

/**
 * 核心逻辑
 * @param options
 */
LK_timer.iteration = function (options) {
    // 使用容量百分比
    var percent = options.usedCapacityIndex / options.activeVolume * 100;
    // 如果资源将要耗尽时（90%）需要关闭定时器 || 因为首次除0时会报错NaN, 所以能过NaN判断是否是首次
    if (percent >= 90 || isNaN(percent)) {
        // 停止
        LK_timer.killInterval();
        // 扩充 （扩充后会继续执行）
        LK_timer.extension(options);

        // 只有在资源充足时才可执行程序
    } else if (options.activeVolume > 0) {
        options.usedCapacityIndex++;
        options.callback(options.usedCapacityIndex);
    }
}

/**
 * 扩充容量
 * @constructor
 */
LK_timer.extension = function (options) {
    console.info('程序正在扩充容量，请等待！');
    var timeoutId = setTimeout(function () {
        LK_timer.options.extensionFun();
    }, 3000);
}

/**
 * 启动定时器
 */
LK_timer.startInterval = function () {
    if (!status) {
        intervalId = setInterval(function () {
            status = true;
            LK_timer.iteration(LK_timer.options);
        }, LK_timer.options.time);
    }
}

/**
 * 结束定时器
 */
LK_timer.killInterval = function () {
    status = false;
    clearInterval(intervalId);
}

// 测试执行
LK_timer.startInterval();

module.exports = LK_timer;
```
