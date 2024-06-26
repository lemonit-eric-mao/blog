---
title: "WebGL学习 --> 在场景中初始化对象"
date: "2017-11-16"
categories: 
  - "webgl"
---

### **1\. 创建立体几何 (我喜欢管它叫做 建模)**

```javascript
const cube = new THREE.CubeGeometry(200, 100, 50, 4, 4);
```

### **2\. 设置模型的材质**

```javascript
// THREE.MeshLambertMaterial() 兰伯特材质，材质中的一种
const yellowMaterial = new THREE.MeshLambertMaterial({color: THREE.ColorKeywords.yellow});
```

### **配置立方体**

```javascript
// 配置立方体
const mesh = new THREE.Mesh(cube1, yellowMaterial);
// 设置立方体所以场景中的位置
mesh.position.set(0, 0, 0);
// 将立方体添加到场景当中
scene.add(mesh);
```

### **实际案例**

```javascript
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

            // 配置网格模型的立方体
            const mesh = new THREE.Mesh(cube1, yellowMaterial);
            // 设置立方体所以场景中的位置
            mesh.position.set(0, 0, 0);
            // 将立方体添加到场景当中
            scene.add(mesh);

            const mesh2 = new THREE.Mesh(cube2, purpleMaterial);
            mesh2.position.set(-300, 0, 0);
            scene.add(mesh2);

            const mesh3 = new THREE.Mesh(cube3, greenyellowMaterial);
            mesh3.position.set(0, -150, 0);
            scene.add(mesh3);

            const mesh4 = new THREE.Mesh(cube3, greenyellowMaterial);
            mesh4.position.set(0, 150, 0);
            scene.add(mesh4);

            const mesh5 = new THREE.Mesh(cube4, bluevioletMaterial);
            mesh5.position.set(300, 0, 0);
            scene.add(mesh5);

            const mesh6 = new THREE.Mesh(cube4, bluevioletMaterial);
            mesh6.position.set(0, 0, -100);
            scene.add(mesh6);
        }
```
