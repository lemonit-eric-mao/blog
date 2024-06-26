---
title: "WebGL学习 --> 光源效果及应用"
date: "2017-11-16"
categories: 
  - "webgl"
---

### **环境光:**

笼罩在整个空间无处不在的光, 环境光可以说是场景的整体基调

```javascript
// THREE.AmbientLight = function ( color, intensity ) {}
// color: 光的颜色值, 十六进制, 默认值为0xffffff
// intensity: 光的强度, 默认是1.0, 就是说灯光的强度是100%,
var light = new THREE.AmbientLight(0xFF00FF, 0.8);
scene.add(light); // 只需要将光源加入场景, 场景就能够通过光源渲染出好的效果来了。
```

### **点光源:**

向四面八方发射的单点光源

```javascript
// THREE.PointLight = function ( color, intensity, distance, decay ) {}
// color: 光的颜色值, 十六进制, 默认值为0xffffff
// intensity: 光的强度, 默认是1.0, 就是说灯光的强度是100%,
// distance: 光的距离, 默认为0, 表示无穷远都能照到.
// decay: 光的衰减, 随着光的距离, 强度衰减的程度, 默认为1, 为模拟真实效果, 建议设置为2
var light = new THREE.PointLight(0x00FFFF, 0.2, 100, 2);
light.position.set(3, 3, 3);
scene.add(light);
```

### **聚光灯:**

发射出锥形状的光, 模拟手电筒, 台灯等光源

```javascript
// THREE.SpotLight = function ( color, intensity, distance, angle, penumbra, decay ) {}
// color: 光的颜色值, 十六进制, 默认值为0xffffff
// intensity: 光的强度, 默认是1.0, 就是说灯光的强度是100%,
// distance: 光的距离, 默认为0, 表示无穷远都能照到.
// angle: 圆椎体的半顶角角度, 最大不超过90度, 默认为最大值,
// penumbra: 光照边缘的模糊化程度，范围0-1，默认为0，不模糊,
// decay: 光的衰减, 随着光的距离, 强度衰减的程度, 默认为1, 为模拟真实效果, 建议设置为2
var light = new THREE.SpotLight(0xFFFF00, 1, 100, 0.06, 0.5, 2);
light.position.set(0, 4, 0);
scene.add(light);
```

### **平行光:**

平行的一束光, 模拟从很远处照射的太阳光

```javascript
// THREE.DirectionalLight = function ( color, intensity ) {}
// color: 光的颜色值, 十六进制, 默认值为0xffffff
// intensity: 光的强度, 默认是1.0, 就是说灯光的强度是100%,
var light = new THREE.DirectionalLight(0xFF00FF, 1);
light.position.set(0, 6, 0);
scene.add(light);
```

### **实际案例**

```javascript
// 初始化 灯光
let light;
const initLight = () => {
    // 环境光: 笼罩在整个空间无处不在的光, 环境光可以说是场景的整体基调
    // THREE.AmbientLight = function ( color, intensity ) {}
    // color: 光的颜色值, 十六进制, 默认值为0xffffff
    // intensity: 光的强度, 默认是1.0, 就是说灯光的强度是100%,
    light = new THREE.AmbientLight(0xFFFF00, 0.4);
    light.position.set(100, 100, 200);
    scene.add(light); // 只需要将光源加入场景, 场景就能够通过光源渲染出好的效果来了。

    // 点光源: 向四面八方发射的单点光源
    // THREE.PointLight = function ( color, intensity, distance, decay ) {}
    // color: 光的颜色值, 十六进制, 默认值为0xffffff
    // intensity: 光的强度, 默认是1.0, 就是说灯光的强度是100%,
    // distance: 光的距离, 默认为0, 表示无穷远都能照到.
    // decay: 光的衰减, 随着光的距离, 强度衰减的程度, 默认为1, 为模拟真实效果, 建议设置为2
    light = new THREE.PointLight(0xFF00FF, 0.9, 0, 2);
    light.position.set(0, 0, 25);
    scene.add(light);

    // 聚光灯: 发射出锥形状的光, 模拟手电筒, 台灯等光源
    // THREE.SpotLight = function ( color, intensity, distance, angle, penumbra, decay ) {}
    // color: 光的颜色值, 十六进制, 默认值为0xffffff
    // intensity: 光的强度, 默认是1.0, 就是说灯光的强度是100%,
    // distance: 光的距离, 默认为0, 表示无穷远都能照到.
    // angle: 圆椎体的半顶角角度, 最大不超过90度, 默认为最大值,
    // penumbra: 光照边缘的模糊化程度，范围0-1，默认为0，不模糊,
    // decay: 光的衰减, 随着光的距离, 强度衰减的程度, 默认为1, 为模拟真实效果, 建议设置为2
    light = new THREE.SpotLight(THREE.ColorKeywords.blue, 1, 0, 0.2, 0.5, 2);
    light.position.set(500, -360, 200);
    scene.add(light);

    // 平行光: 平行的一束光, 模拟从很远处照射的太阳光
    // THREE.DirectionalLight = function ( color, intensity ) {}
    // color: 光的颜色值, 十六进制, 默认值为0xffffff
    // intensity: 光的强度, 默认是1.0, 就是说灯光的强度是100%,
    light = new THREE.DirectionalLight(0x00BB00, 0.6);
    light.position.set(0, 0, 1);
    scene.add(light);
}
```
