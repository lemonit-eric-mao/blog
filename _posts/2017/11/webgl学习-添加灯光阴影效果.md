---
title: "WebGL学习 --> 添加灯光阴影效果"
date: "2017-11-16"
categories: 
  - "webgl"
---

## **关键代码**

```javascript
/**
 * 添加阴影材质
 * Created by mao_siyu on 2017/11/4.
 */
let ThreeShadow = {
    /**
     * 初始化
     * @param scene 场景 (必填)
     */
    init(scene){
        // 阴影材质
        let geometry = new THREE.BoxGeometry(999, 0.1, 999);
        let material = new THREE.ShadowMaterial({color: 0x000000});
        material.opacity = 0.5;
        let groundMesh = new THREE.Mesh(geometry, material);
        groundMesh.receiveShadow = true; // 接受阴影效果
        scene.add(groundMesh);
    }
}
```

## **应用案例**

```markup
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>画3D坐标系</title>
    <style>
        body {
            margin: 0;
            overflow: hidden;
        }

        canvas {
            width: 100%;
            height: 100%
        }
    </style>
    <script src="../js/three.min.js"></script>
    <script src="../js/OrbitControls.js"></script>
    <script src="../js/plugins/ThreeShadow.js"></script>
    <script src="../js/plugins/ThreeOrbitCtrl.js"></script>
    <script src="../js/plugins/ThreeArrowHelper.js"></script>

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
            // 启用阴影映射
            renderer.shadowMap.enabled = true;
            // 将场景放到 body中显示
            document.body.appendChild(renderer.domElement);
        }

        /**
         * 初始化 相机
         */
        let camera;
        const initCamera = function () {
            // 创建一个透视相机
            camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
            // 设置相机初始的 x, y, z
            camera.position.set(16, 15, 20);
        }

        /**
         * 初始化 场景
         */
        let scene;
        const initScene = function () {
            scene = new THREE.Scene();
        }

        /**
         * 初始化 网格
         */
        let grid;
        const initGrid = function () {
            // 网格的边长是10，每个小网格的边长是20, 中心线颜色0xf7ff00, 网络颜色0x808080
            grid = new THREE.GridHelper(40, 40, 0xf7ff00, 0xFFF);
            scene.add(grid);

            // 网格下的底版
            let geometry = new THREE.PlaneGeometry(40, 40, 1, 1);
            let material = new THREE.MeshBasicMaterial({color: 0x9669FE});
            let cube = new THREE.Mesh(geometry, material);
            cube.rotation.x = -Math.PI / 2;
            scene.add(cube);
        }

        /**
         * 初始化 灯光
         */
        let light;
        let dlightHelper;
        const initLight = function () {
            // 环境光 (屋内灯泡)
            light = new THREE.AmbientLight(0xFFFFFF, 0.2);
            scene.add(light);
            // 平行光 (太阳)
            light = new THREE.DirectionalLight(0xFFFFFF, 0.8);
            light.position.set(0, 4, 0);
            light.castShadow = true; // 让灯光支持阴影效果
            scene.add(light);
            // 平行光助手
            dlightHelper = new THREE.DirectionalLightHelper(light, 3);
            scene.add(dlightHelper);
        }

        /**
         * 初始化 立方体
         * 注意：立方体的材质选择，不是所有的材质都受灯光影响
         */
        let mesh;
        const initCube = function () {
            // 创建多个立方体
            for (let i = 0, len = 10; i < len; i += 2) {
                let geometry = new THREE.CubeGeometry(0.5, 3, 0.5);
                // 随机色 Math.random() * 0xfff
                let material = new THREE.MeshStandardMaterial({color: Math.random() * 166 * 0xfff});
                mesh = new THREE.Mesh(geometry, material);
                mesh.castShadow = true; // 让立方体支持阴影效果
                mesh.position.x += i * 2;
                mesh.position.y += 1.5;
                scene.add(mesh);
            }
        }

        // 将立方体添加到场景当中
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
            // 灯光助手
            dlightHelper.update();
            //
            let timer = Date.now() * 0.000025;
            light.position.x = Math.sin(timer * 5) * 10;
            light.position.z = Math.cos(timer * 5) * 10;
        }

        /**
         * 初始化
         */
        let controls;
        const init = function () {
            initRenderer();
            initCamera();
            initScene();
            initLight();
            initGrid();
            initCube();

            // 初始化 轨道控制器
            controls = ThreeOrbitCtrl.init(camera);
            // 初始化 3D坐标系
            ThreeArrowHelper.init(scene);
            // 初始化 阴影效果
            ThreeShadow.init(scene);
            render();
        }
    </script>
</head>
<body onload="init()">
</body>
</html>
```
