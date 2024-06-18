---
title: 'WebGL学习 &#8211;> 添加灯光阴影效果'
date: '2017-11-16T15:14:06+00:00'
status: publish
permalink: /2017/11/16/webgl%e5%ad%a6%e4%b9%a0-%e6%b7%bb%e5%8a%a0%e7%81%af%e5%85%89%e9%98%b4%e5%bd%b1%e6%95%88%e6%9e%9c
author: 毛巳煜
excerpt: ''
type: post
id: 476
category:
    - WebGL
tag: []
post_format: []
hestia_layout_select:
    - default
---
**关键代码**
--------

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

**应用案例**
--------

```
<pre data-language="HTML">```markup



    <meta charset="UTF-8"></meta>
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
         * &#21021;&#22987;&#21270; &#28210;&#26579;&#22120;
         */
        let renderer;
        const initRenderer = function () {
            renderer = new THREE.WebGLRenderer({
                antialias: true // &#25239;&#38191;&#40831;
            });
            // &#28210;&#26579;&#30340;&#22330;&#26223;&#22823;&#23567;
            renderer.setSize(window.innerWidth, window.innerHeight);
            // &#21551;&#29992;&#38452;&#24433;&#26144;&#23556;
            renderer.shadowMap.enabled = true;
            // &#23558;&#22330;&#26223;&#25918;&#21040; body&#20013;&#26174;&#31034;
            document.body.appendChild(renderer.domElement);
        }

        /**
         * &#21021;&#22987;&#21270; &#30456;&#26426;
         */
        let camera;
        const initCamera = function () {
            // &#21019;&#24314;&#19968;&#20010;&#36879;&#35270;&#30456;&#26426;
            camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
            // &#35774;&#32622;&#30456;&#26426;&#21021;&#22987;&#30340; x, y, z
            camera.position.set(16, 15, 20);
        }

        /**
         * &#21021;&#22987;&#21270; &#22330;&#26223;
         */
        let scene;
        const initScene = function () {
            scene = new THREE.Scene();
        }

        /**
         * &#21021;&#22987;&#21270; &#32593;&#26684;
         */
        let grid;
        const initGrid = function () {
            // &#32593;&#26684;&#30340;&#36793;&#38271;&#26159;10&#65292;&#27599;&#20010;&#23567;&#32593;&#26684;&#30340;&#36793;&#38271;&#26159;20, &#20013;&#24515;&#32447;&#39068;&#33394;0xf7ff00, &#32593;&#32476;&#39068;&#33394;0x808080
            grid = new THREE.GridHelper(40, 40, 0xf7ff00, 0xFFF);
            scene.add(grid);

            // &#32593;&#26684;&#19979;&#30340;&#24213;&#29256;
            let geometry = new THREE.PlaneGeometry(40, 40, 1, 1);
            let material = new THREE.MeshBasicMaterial({color: 0x9669FE});
            let cube = new THREE.Mesh(geometry, material);
            cube.rotation.x = -Math.PI / 2;
            scene.add(cube);
        }

        /**
         * &#21021;&#22987;&#21270; &#28783;&#20809;
         */
        let light;
        let dlightHelper;
        const initLight = function () {
            // &#29615;&#22659;&#20809; (&#23627;&#20869;&#28783;&#27873;)
            light = new THREE.AmbientLight(0xFFFFFF, 0.2);
            scene.add(light);
            // &#24179;&#34892;&#20809; (&#22826;&#38451;)
            light = new THREE.DirectionalLight(0xFFFFFF, 0.8);
            light.position.set(0, 4, 0);
            light.castShadow = true; // &#35753;&#28783;&#20809;&#25903;&#25345;&#38452;&#24433;&#25928;&#26524;
            scene.add(light);
            // &#24179;&#34892;&#20809;&#21161;&#25163;
            dlightHelper = new THREE.DirectionalLightHelper(light, 3);
            scene.add(dlightHelper);
        }

        /**
         * &#21021;&#22987;&#21270; &#31435;&#26041;&#20307;
         * &#27880;&#24847;&#65306;&#31435;&#26041;&#20307;&#30340;&#26448;&#36136;&#36873;&#25321;&#65292;&#19981;&#26159;&#25152;&#26377;&#30340;&#26448;&#36136;&#37117;&#21463;&#28783;&#20809;&#24433;&#21709;
         */
        let mesh;
        const initCube = function () {
            // &#21019;&#24314;&#22810;&#20010;&#31435;&#26041;&#20307;
            for (let i = 0, len = 10; i < len; i += 2) {
                let geometry = new THREE.CubeGeometry(0.5, 3, 0.5);
                // &#38543;&#26426;&#33394; Math.random() * 0xfff
                let material = new THREE.MeshStandardMaterial({color: Math.random() * 166 * 0xfff});
                mesh = new THREE.Mesh(geometry, material);
                mesh.castShadow = true; // &#35753;&#31435;&#26041;&#20307;&#25903;&#25345;&#38452;&#24433;&#25928;&#26524;
                mesh.position.x += i * 2;
                mesh.position.y += 1.5;
                scene.add(mesh);
            }
        }

        // &#23558;&#31435;&#26041;&#20307;&#28155;&#21152;&#21040;&#22330;&#26223;&#24403;&#20013;
        /**
         * &#28210;&#26579;
         */
        const render = function () {
            // &#36712;&#36947;&#25511;&#21046;&#22120; &#38656;&#35201;requestAnimationFrame
            requestAnimationFrame(render);
            // &#28210;&#26579;
            renderer.render(scene, camera);
            // &#36712;&#36947;&#25511;&#21046;&#22120;
            controls.update();
            // &#28783;&#20809;&#21161;&#25163;
            dlightHelper.update();
            //
            let timer = Date.now() * 0.000025;
            light.position.x = Math.sin(timer * 5) * 10;
            light.position.z = Math.cos(timer * 5) * 10;
        }

        /**
         * &#21021;&#22987;&#21270;
         */
        let controls;
        const init = function () {
            initRenderer();
            initCamera();
            initScene();
            initLight();
            initGrid();
            initCube();

            // &#21021;&#22987;&#21270; &#36712;&#36947;&#25511;&#21046;&#22120;
            controls = ThreeOrbitCtrl.init(camera);
            // &#21021;&#22987;&#21270; 3D&#22352;&#26631;&#31995;
            ThreeArrowHelper.init(scene);
            // &#21021;&#22987;&#21270; &#38452;&#24433;&#25928;&#26524;
            ThreeShadow.init(scene);
            render();
        }
    </script>





```
```