---
title: 'WebGL学习 &#8211;> 旋转渐变色线条'
date: '2017-11-16T15:11:10+00:00'
status: publish
permalink: /2017/11/16/webgl%e5%ad%a6%e4%b9%a0-%e6%97%8b%e8%bd%ac%e6%b8%90%e5%8f%98%e8%89%b2%e7%ba%bf%e6%9d%a1
author: 毛巳煜
excerpt: ''
type: post
id: 465
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
        camera.position.z = 350;
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
     * &#21021;&#22987;&#21270; &#32447;&#26465;
     */
    let cube;
    const initCube = function () {

        let geometry = new THREE.Geometry();
        let material = new THREE.LineBasicMaterial({vertexColors: true});

        let start = new THREE.Vector3(0, 0, 100); // &#21019;&#24314;&#36215;&#28857; (x, y, z) &#20301;&#32622;
        geometry.vertices.push(start); // &#23558;&#36215;&#28857;&#25918;&#21040;&#20960;&#20309;&#20307;&#20013;
        let end = new THREE.Vector3(300, 0, -100); // &#21019;&#24314;&#32456;&#28857; (x, y, z) &#20301;&#32622;
        geometry.vertices.push(end); // &#23558;&#32456;&#28857;&#25918;&#21040;&#20960;&#20309;&#20307;&#20013;

        // &#37197;&#32622;&#20960;&#20309;&#20307;&#30340;&#39068;&#33394;
        let color1 = new THREE.Color(0x444444);
        let color2 = new THREE.Color(0xFF0000);
        geometry.colors.push(color1, color2);

        // &#20351;&#29992;&#19978;&#38754;&#30340;&#37197;&#32622; &#30011;&#32447;&#26465;
        let line = new THREE.Line(geometry, material, THREE.LinePieces);
        // &#23558;&#32447;&#26465;&#28155;&#21152;&#21040;&#22330;&#26223;&#20013;
        scene.add(line);
    }

    /**
     * &#28210;&#26579;
     */
    const render = function () {
        requestAnimationFrame(render);
        // &#30456;&#26426;.&#26059;&#36716;&#35282;&#24230;.z &#24490;&#29615;&#25913;&#21464;&#30456;&#26426;&#30340;&#26059;&#36716;&#35282;&#24230;
        camera.rotation.z += 0.01;
        // &#28210;&#26579;
        renderer.render(scene, camera);
    }

    /**
     * &#21021;&#22987;&#21270;
     */
    const init = function () {
        initRenderer();
        initCamera();
        initScene();
        initLight();
        initCube();

        render();
    }

    // &#25191;&#34892;
    init();


</script>



```
```