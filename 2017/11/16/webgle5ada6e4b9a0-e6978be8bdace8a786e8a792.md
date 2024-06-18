---
title: 'WebGL学习 &#8211;>  旋转视角'
date: '2017-11-16T15:12:40+00:00'
status: publish
permalink: /2017/11/16/webgl%e5%ad%a6%e4%b9%a0-%e6%97%8b%e8%bd%ac%e8%a7%86%e8%a7%92
author: 毛巳煜
excerpt: ''
type: post
id: 471
category:
    - WebGL
tag: []
post_format: []
hestia_layout_select:
    - default
---
**轨道控制器**
---------

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

**应用示例**
--------

```
<pre data-language="HTML">```markup



    <meta charset="UTF-8"></meta>
    <title>画3D坐标系</title>
    <script src="../js/three.js"></script>
    <script src="../js/OrbitControls.js"></script>
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
        // &#22330;&#26223;&#30340;&#32972;&#26223;&#33394;
        renderer.setClearColor('#FFF');
        // &#23558;&#22330;&#26223;&#25918;&#21040; body&#20013;&#26174;&#31034;
        document.body.appendChild(renderer.domElement);
    }

    /**
     * &#21021;&#22987;&#21270; &#30456;&#26426;
     */
    let camera;
    const initCamera = function () {
        // &#21019;&#24314;&#19968;&#20010;&#36879;&#35270;&#30456;&#26426;
        camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 1, 1000);
        // &#22240;&#20026; three.js &#26159;&#21491;&#25163;&#22352;&#26631;&#31995;, &#25152;&#20197; z&#22352;&#26631;&#25351;&#21521;&#30340;&#26159;&#33258;&#24049;; z=5 &#34920;&#31034;&#30456;&#26426;&#21040;&#29289;&#20307;&#20043;&#38388;&#30340;&#36317;&#31163;
        camera.position.z = 10;
    }

    /**
     * &#21021;&#22987;&#21270; &#22330;&#26223;
     */
    let scene;
    const initScene = function () {
        scene = new THREE.Scene();
    }

    /**
     * &#21021;&#22987;&#21270; &#28783;&#20809;
     */
    const initLight = function () {

    }

    /**
     * &#21021;&#22987;&#21270; &#32593;&#26684;
     */
    let grid;
    const initGrid = function () {
        // &#32593;&#26684;&#30340;&#36793;&#38271;&#26159;10&#65292;&#27599;&#20010;&#23567;&#32593;&#26684;&#30340;&#36793;&#38271;&#26159;20, &#20013;&#24515;&#32447;&#39068;&#33394;0x0000ff, &#32593;&#32476;&#39068;&#33394;0x808080
        grid = new THREE.GridHelper(10, 20, 0x0000ff, 0x808080);
        scene.add(grid);
    }

    /**
     * &#21021;&#22987;&#21270; &#31435;&#26041;&#20307;
     */
    let mesh;
    const initCube = function () {
    }

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
    }

    /**
     * &#21021;&#22987;&#21270;
     */
    let controls;
    const init = function () {
        initScene();
        initCamera();
        initRenderer();
        initLight();
        initGrid();
        initCube();

        // &#21021;&#22987;&#21270; &#36712;&#36947;&#25511;&#21046;&#22120;
        controls = ThreeOrbitCtrl.init(camera);
        // &#21021;&#22987;&#21270; 3D&#22352;&#26631;&#31995;
        ThreeArrowHelper.init(scene);

        render();
    }

    // &#25191;&#34892;
    init();


</script>



```
```