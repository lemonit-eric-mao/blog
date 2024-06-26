---
title: "WebGL学习 --> 画3D坐标系"
date: "2017-11-16"
categories: 
  - "webgl"
---

### **关键代码**

```javascript
/**
 * 添加 3D 辅助箭头
 * Created by mao_siyu on 2017/11/2.
 */
let ThreeArrowHelper = {
    /**
     * 初始化
     * @param scene 场景 (必填)
     */
    init(scene) {
        if (!scene) throw '未设置场景！'
        // 创建 X 箭头
        scene.add(this.createArrow({x: 90}, 'red'));
        // 创建 Y 箭头
        scene.add(this.createArrow({}, 'green'));
        // 创建 Z 箭头
        scene.add(this.createArrow({z: 90}, 'blue'));
    },
    /**
     * 创建 三维坐标系的箭头
     * @param position 设置箭头的方向
     * @param color 箭头颜色
     * @param length 箭头长度
     */
    createArrow(position, color, length) {
        position = Object.assign({x: 0, y: 0, z: 0}, position);
        color = color || Math.random() * 0xffffff;
        length = length || 6;

        let dir = new THREE.Vector3(position.x, position.y, position.z);
        dir.normalize();
        let origin = new THREE.Vector3(0, 0, 0);
        let arrowHelper = new THREE.ArrowHelper(dir, origin, length, color);
        return arrowHelper;
    }
}
```

### **应用案例**

```markup
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>画3D坐标系</title>
    <script src="../js/three.js"></script>
    <script src="../js/ThreeArrowHelper.js"></script>
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
    let mThreeArrowHelper;
    const initScene = function () {
        scene = new THREE.Scene();
        // 初始化 3D坐标系
        ThreeArrowHelper.init(scene);
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
        var axesHelper = new THREE.AxesHelper(5);
        scene.add(axesHelper);

        render();
    }

    // 执行
    init();

</script>
</body>
</html>
```
