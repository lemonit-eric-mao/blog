---
title: "WebGL学习 -->  旋转视角"
date: "2017-11-16"
categories: 
  - "webgl"
---

## **轨道控制器**

```javascript
/**
 * 轨道控制器
 * Created by mao-siyu on 17-11-3.
 */
let ThreeOrbitCtrl = {
    // 初始化 轨道控制器
    init(camera) {
        // 轨道控制允许摄像机在目标周围绕行
        return new THREE.OrbitControls(camera);
    }
}
```

## **应用示例**

```markup
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>画3D坐标系</title>
    <script src="../js/three.js"></script>
    <script src="../js/OrbitControls.js"></script>
    <script src="../js/plugins/ThreeOrbitCtrl.js"></script>
    <script src="../js/plugins/ThreeArrowHelper.js"></script>
</head>
<body>

<script>
    /**
     * 初始化 渲染器
     */
    let renderer;
    const initRenderer = function () {
        renderer = new THREE.WebGLRenderer({
            antialias: true // 抗锯齿
        });
        // 渲染的场景大小
        renderer.setSize(window.innerWidth, window.innerHeight);
        // 场景的背景色
        renderer.setClearColor('#FFF');
        // 将场景放到 body中显示
        document.body.appendChild(renderer.domElement);
    }

    /**
     * 初始化 相机
     */
    let camera;
    const initCamera = function () {
        // 创建一个透视相机
        camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 1, 1000);
        // 因为 three.js 是右手坐标系, 所以 z坐标指向的是自己; z=5 表示相机到物体之间的距离
        camera.position.z = 10;
    }

    /**
     * 初始化 场景
     */
    let scene;
    const initScene = function () {
        scene = new THREE.Scene();
    }

    /**
     * 初始化 灯光
     */
    const initLight = function () {

    }

    /**
     * 初始化 网格
     */
    let grid;
    const initGrid = function () {
        // 网格的边长是10，每个小网格的边长是20, 中心线颜色0x0000ff, 网络颜色0x808080
        grid = new THREE.GridHelper(10, 20, 0x0000ff, 0x808080);
        scene.add(grid);
    }

    /**
     * 初始化 立方体
     */
    let mesh;
    const initCube = function () {
    }

    /**
     * 渲染
     */
    const render = function () {
        // 轨道控制器 需要requestAnimationFrame
        requestAnimationFrame(render);
        // 渲染
        renderer.render(scene, camera);
        // 轨道控制器
        controls.update();
    }

    /**
     * 初始化
     */
    let controls;
    const init = function () {
        initScene();
        initCamera();
        initRenderer();
        initLight();
        initGrid();
        initCube();

        // 初始化 轨道控制器
        controls = ThreeOrbitCtrl.init(camera);
        // 初始化 3D坐标系
        ThreeArrowHelper.init(scene);

        render();
    }

    // 执行
    init();


</script>
</body>
</html>
```
