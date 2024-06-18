---
title: "WebGL学习 --> 旋转立方体"
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
        renderer.setClearColor('#666');
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
        camera.position.z = 5;
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
     * 初始化 立方体
     */
    let cube;
    const initCube = function () {
        let geometry = new THREE.CubeGeometry(2, 2, 2);
        let material = new THREE.MeshBasicMaterial({color: '#9f9'});
        cube = new THREE.Mesh(geometry, material);
        scene.add(cube);
    }

    /**
     * 渲染
     */
    const render = function () {
        requestAnimationFrame(render);
        // 立方体.旋转角度.z 循环改变立方体的旋转角度
        cube.rotation.x += 0.01;
        cube.rotation.y += 0.01;
        cube.rotation.z += 0.01;
        // 渲染
        renderer.render(scene, camera);
    }

    /**
     * 初始化
     */
    const init = function () {
        initScene();
        initCamera();
        initRenderer();
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
