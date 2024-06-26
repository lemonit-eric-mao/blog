---
title: "WebGL学习 --> 整合 渲染器, 摄像机, 场景, 灯光, 模型"
date: "2017-11-16"
categories: 
  - "webgl"
---

```markup
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>整合</title>
    <style type="text/css">
        html, body {
            padding: 0px;
            margin: 0px;
        }

        .canvas-frame {
            border: none;
            cursor: pointer;
            width: 100%;
            height: 600px;
            background-color: #EEEEEE;
        }

    </style>

    <script src="../common/js/Stats.js"></script>
    <script>
        // 性能监视器Stats
        let stats;
        const initStats = () => {
            stats = new Stats();
            stats.setMode(0); // 默认显示风格 0: FPS, 1: MS, 2: MB
            // 将stats的界面对应左上角
            stats.domElement.style.position = 'absolute';
            stats.domElement.style.left = '50%';
            stats.domElement.style.top = '0px';
            document.body.appendChild(stats.domElement);
        }
    </script>

    <script src="../common/js/three.js"></script>
    <script>

        // 初始化 WebGL渲染器
        let renderer;
        const initThree = () => {
            width = document.getElementById('canvas-frame').clientWidth;
            height = document.getElementById('canvas-frame').clientHeight;
            renderer = new THREE.WebGLRenderer({
                antialias: true // 抗锯齿
            });
            // 设置渲染区域的宽高
            renderer.setSize(width, height);
            // 指定渲染区域的背景色
            renderer.setClearColor(0xFFFFFF, 1.0);
            // 指定将渲染的结果放到哪个容器当中
            document.getElementById('canvas-frame').appendChild(renderer.domElement);
        }

        // 初始化一个透视相机
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
            // 注: up 和lookat这两个方向必须垂直，无论怎么设置，他们必须互相垂直。不然相机看到的结果无法预知。
        }

        // 初始化 场景
        let scene;
        const initScene = () => {
            scene = new THREE.Scene();
        }

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

        // 初始化 立方体
        let cube;
        const initObject = () => {

            // 创建立方体
            // 第一种 立方体
            const cube1 = new THREE.CubeGeometry(200, 100, 50, 4, 4);
            // 第二种 立方体
            const cube2 = new THREE.CubeGeometry(200, 100, 50, 4, 4);
            // 第三种 立方体
            const cube3 = new THREE.CubeGeometry(200, 100, 50, 4, 4);
            // 第四种 立方体
            const cube4 = new THREE.CubeGeometry(200, 100, 50, 4, 4);

            // 设置立方体的材质
            // THREE.MeshLambertMaterial() 兰伯特材质，材质中的一种
            // 黄色
            const yellowMaterial = new THREE.MeshLambertMaterial({color: THREE.ColorKeywords.yellow});
            // 紫红色
            const purpleMaterial = new THREE.MeshLambertMaterial({color: THREE.ColorKeywords.purple});
            // 黄绿色
            const greenyellowMaterial = new THREE.MeshLambertMaterial({color: THREE.ColorKeywords.greenyellow});
            // 蓝色
            const bluevioletMaterial = new THREE.MeshLambertMaterial({color: THREE.ColorKeywords.blueviolet});
            // 白色
            const whiteMaterial = new THREE.MeshLambertMaterial({color: THREE.ColorKeywords.white});

            // 配置立方体
            const mesh = new THREE.Mesh(cube1, whiteMaterial);
            // 设置立方体所以场景中的位置
            mesh.position.set(0, 0, 0);
            // 将立方体添加到场景当中
            scene.add(mesh);

            const mesh2 = new THREE.Mesh(cube2, whiteMaterial);
            mesh2.position.set(-300, 0, 0);
            scene.add(mesh2);

            const mesh3 = new THREE.Mesh(cube3, whiteMaterial);
            mesh3.position.set(0, -150, 0);
            scene.add(mesh3);

            const mesh4 = new THREE.Mesh(cube3, whiteMaterial);
            mesh4.position.set(0, 150, 0);
            scene.add(mesh4);

            const mesh5 = new THREE.Mesh(cube4, whiteMaterial);
            mesh5.position.set(300, 0, 0);
            scene.add(mesh5);

            const mesh6 = new THREE.Mesh(cube4, whiteMaterial);
            mesh6.position.set(0, 0, -100);
            scene.add(mesh6);
        }

        // 启动
        const threeStart = () => {
            initStats();
            initThree();
            initCamera();
            initScene();
            initLight();
            initObject();
            render();
        }

        // 渲染
        const render = () => {
            renderer.clear();
            renderer.render(scene, camera);
            stats.update();
        }

    </script>
</head>
<body onload="threeStart()">
<div class="canvas-frame" id="canvas-frame"></div>
</body>
</html>
```
