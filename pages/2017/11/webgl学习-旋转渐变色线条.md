---
title: "WebGL学习 --> 旋转渐变色线条"
date: "2017-11-16"
categories: 
  - "webgl"
---

```markup
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <script src="../js/three.js"></script>
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
        camera.position.z = 350;
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
     * 初始化 线条
     */
    let cube;
    const initCube = function () {

        let geometry = new THREE.Geometry();
        let material = new THREE.LineBasicMaterial({vertexColors: true});

        let start = new THREE.Vector3(0, 0, 100); // 创建起点 (x, y, z) 位置
        geometry.vertices.push(start); // 将起点放到几何体中
        let end = new THREE.Vector3(300, 0, -100); // 创建终点 (x, y, z) 位置
        geometry.vertices.push(end); // 将终点放到几何体中

        // 配置几何体的颜色
        let color1 = new THREE.Color(0x444444);
        let color2 = new THREE.Color(0xFF0000);
        geometry.colors.push(color1, color2);

        // 使用上面的配置 画线条
        let line = new THREE.Line(geometry, material, THREE.LinePieces);
        // 将线条添加到场景中
        scene.add(line);
    }

    /**
     * 渲染
     */
    const render = function () {
        requestAnimationFrame(render);
        // 相机.旋转角度.z 循环改变相机的旋转角度
        camera.rotation.z += 0.01;
        // 渲染
        renderer.render(scene, camera);
    }

    /**
     * 初始化
     */
    const init = function () {
        initRenderer();
        initCamera();
        initScene();
        initLight();
        initCube();

        render();
    }

    // 执行
    init();


</script>
</body>
</html>
```
