---
title: "WebGL学习 --> 网格+不同颜色的立方体"
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
        let geometry = new THREE.BoxGeometry(2, 2, 2);
        for (let i = 0; i < geometry.faces.length; i += 2) {
            let hex = Math.random() * 0xffffff;
            geometry.faces[i].color.setHex(hex);
            geometry.faces[i + 1].color.setHex(hex);
        }
        let material = new THREE.MeshBasicMaterial({vertexColors: THREE.FaceColors});
        mesh = new THREE.Mesh(geometry, material);
        mesh.position = new THREE.Vector3(0, 0, 0);
        scene.add(mesh);
    }

    /**
     * 渲染
     */
    const render = function () {
        requestAnimationFrame(render);
        // 立方体旋转角度
        mesh.rotation.x = 0.3;
        mesh.rotateY(0.01);
        // 网络旋转角度
        grid.rotation.x = 0.3;
        grid.rotation.y = -0.4;
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
        initGrid();
        initCube();

        render();
    }

    // 执行
    init();


</script>
</body>
</html>
```
