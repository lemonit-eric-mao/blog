---
title: 'WebGL学习 &#8211;> 旋转立方体'
date: '2017-11-16T15:10:42+00:00'
status: publish
permalink: /2017/11/16/webgl%e5%ad%a6%e4%b9%a0-%e6%97%8b%e8%bd%ac%e7%ab%8b%e6%96%b9%e4%bd%93
author: 毛巳煜
excerpt: ''
type: post
id: 463
category:
    - WebGL
tag: []
post_format: []
hestia_layout_select:
    - default
---
```
<pre data-language="HTML">```markup



    <meta charset="UTF-8"></meta>
    <title>Title</title>
    <script src="../js/three.js"></script>



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
        renderer.setClearColor('#666');
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
        camera.position.z = 5;
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
     * &#21021;&#22987;&#21270; &#31435;&#26041;&#20307;
     */
    let cube;
    const initCube = function () {
        let geometry = new THREE.CubeGeometry(2, 2, 2);
        let material = new THREE.MeshBasicMaterial({color: '#9f9'});
        cube = new THREE.Mesh(geometry, material);
        scene.add(cube);
    }

    /**
     * &#28210;&#26579;
     */
    const render = function () {
        requestAnimationFrame(render);
        // &#31435;&#26041;&#20307;.&#26059;&#36716;&#35282;&#24230;.z &#24490;&#29615;&#25913;&#21464;&#31435;&#26041;&#20307;&#30340;&#26059;&#36716;&#35282;&#24230;
        cube.rotation.x += 0.01;
        cube.rotation.y += 0.01;
        cube.rotation.z += 0.01;
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
        initCube();

        render();
    }

    // &#25191;&#34892;
    init();


</script>



```
```