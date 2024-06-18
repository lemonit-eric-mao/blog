---
title: 'WebGL学习 &#8211;> 画3D坐标系'
date: '2017-11-16T15:12:10+00:00'
status: publish
permalink: /2017/11/16/webgl%e5%ad%a6%e4%b9%a0-%e7%94%bb3d%e5%9d%90%e6%a0%87%e7%b3%bb
author: 毛巳煜
excerpt: ''
type: post
id: 469
category:
    - WebGL
tag: []
post_format: []
hestia_layout_select:
    - default
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

```
<pre data-language="HTML">```markup



    <meta charset="UTF-8"></meta>
    <title>画3D坐标系</title>
    <script src="../js/three.js"></script>
    <script src="../js/ThreeArrowHelper.js"></script>



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
    let mThreeArrowHelper;
    const initScene = function () {
        scene = new THREE.Scene();
        // &#21021;&#22987;&#21270; 3D&#22352;&#26631;&#31995;
        ThreeArrowHelper.init(scene);
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
        // &#32593;&#32476;&#26059;&#36716;&#35282;&#24230;
        grid.rotation.x = 0.3;
        grid.rotation.y = -0.4;
        // &#28210;&#26579;
        renderer.render(scene, camera);
    }

    /**
     * &#21021;&#22987;&#21270;
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

    // &#25191;&#34892;
    init();

</script>



```
```