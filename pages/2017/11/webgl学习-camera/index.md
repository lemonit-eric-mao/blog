---
title: "WebGL学习 --> Camera"
date: "2017-11-16"
categories: 
  - "webgl"
---

节选自 WebGL中文网

在Threejs中相机的表示是THREE.Camera，它是相机的抽象基类，其子类有两种相机 分别是: 正投影相机 **THREE.OrthographicCamera** 透视投影相机 **THREE.PerspectiveCamera**

## **正投影相机**

成像效果: 远近高低比例都相同

**参数: left** 左平面距离相机中心点的垂直距离。

**参数: right** 右平面距离相机中心点的垂直距离

**参数: top** 顶平面距离相机中心点的垂直距离。

**参数: bottom** 底平面距离相机中心点的垂直距离。

**参数: near** 近平面距离相机中心点的垂直距离。

**参数: far** 远平面距离相机中心点的垂直距离。

```javascript
let camera = new THREE.OrthographicCamera(left, right, top, bottom, near, far);
```

## **透视投影相机**

成像效果: 近大远小

**视角fov** 可以理解为眼睛睁开的角度，即视角的大小 如果设置为0，相当你闭上眼睛了，所以什么也看不到 如果为180，那么可以认为你的视界很广阔 但是在180度的时候，往往物体很小，因为他在你的整个可视区域中的比例变小了。

**纵横比aspect** 实际窗口的纵横比，即宽度除以高度。 如果这个值越大，说明你宽度越大，那么你可能看的是宽银幕电影了。 如果这个值小于1，那么可能你只能看到的是宽银幕电影的一部分了。

**近平面near** 表示你近处的裁面的距离。补充一下，也可以认为是眼睛距离近处的距离， 假设为10米远，请不要设置为负值，Three.js就傻了，不知道怎么算了。

**远平面far** 表示你远处的裁面。

```javascript
let camera = new THREE.PerspectiveCamera(fov, aspect, near, far);
```

### **实际案例**

```javascript
// 初始化 透视相机
let camera;
const initCamera = () => {
    // THREE.PerspectiveCamera = function( fov, aspect, near, far ) {}
    camera = new THREE.PerspectiveCamera(45, width / height, 1, 10000);
    // 相机位置设定
    camera.position.x = 600;
    camera.position.y = 0;
    camera.position.z = 600;
    // 如果把相机比做是人的头, up 就是头顶
    camera.up.x = 0;
    camera.up.y = 1; // y = 1 表示y轴向上.
    camera.up.z = 0;
    // 如果把相机比做是人的头, lookAt 就是眼睛
    camera.lookAt({
        x: 0,
        y: 0,
        z: 0
    });

    // 注: up 和lookat这两个方向必须垂直, 无论怎么设置, 他们必须互相垂直。不然相机看到的结果无法预知。
}
```
