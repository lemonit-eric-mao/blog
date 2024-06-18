---
title: "JavaScript 自定义下拉列表"
date: "2024-04-16"
categories: 
  - "javascript"
---

```javascript
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>下拉列表</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
    <style>
        /* 下拉列表-样式 */
        .dropdown {
            display: flex;
            flex-direction: column;
            position: relative;
            width: 100px;
        }

        .dropbtn {
            background-color: #4CAF50;
            color: white;
            padding: 10px;
            font-size: 16px;
            border: none;
            cursor: pointer;
            border-radius: 4px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .dropdown-content {
            background-color: #f9f9f9;
            position: absolute;
            top: calc(100% + 0px); /* 设置下拉框距离按钮底部的距离，可根据实际情况调整 */
            left: 0;
            width: calc(100% + 0px);
            box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.2);
            padding: 8px 0;
            z-index: 1;
            border-radius: 4px;
            display: none;
            max-height: 160px; /* 最大高度为 160px */
            overflow-y: auto; /* 当内容高度超过 160px 时显示垂直滚动条 */
            overflow-x: hidden;
        }

        /* 自定义滚动条样式 */
        .dropdown-content::-webkit-scrollbar {
            width: 4px; /* 设置滚动条宽度为 2px */
        }

        /* 滚动条轨道 */
        .dropdown-content::-webkit-scrollbar-track {
            background-color: #f9f9f9; /* 滚动条轨道背景色 */
        }

        /* 滚动条滑块 */
        .dropdown-content::-webkit-scrollbar-thumb {
            background-color: #ccc; /* 滚动条滑块颜色 */
            border-radius: 1px; /* 滚动条滑块圆角 */
        }

        .dropdown-content li {
            list-style: none;
            padding: 8px 16px;
            cursor: pointer;
            display: flex;
            justify-content: center;
            align-items: center;
            width: auto;
        }

        .dropdown-content li:hover {
            background-color: #ddd;
        }

        /* 默认箭头向右，点击后向左 */
        .arrow-down {
            width: 0;
            height: 0;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 5px solid white;
            transition: transform 0.3s ease-in-out; /* 添加过渡效果 */
            transform: rotate(180deg); /* 默认方向 */
        }

        .dropdown.active .arrow-down {
            transform: rotate(0deg); /* 点击后箭头方向 */
        }
    </style>
</head>
<body>

<div class="dropdown" onclick="toggleDropdown()">
    <div class="dropbtn"><span>下拉列表</span><i class="arrow-down"></i></div>
    <ul class="dropdown-content" id="dropdownContent" style="display: none;">
        <li>选项1</li>
        <li>选项2</li>
        <li>选项3</li>
        <li>选项4</li>
        <li>选项5</li>
        <li>选项6</li>
        <li>选项7</li>
        <li>选项8</li>
        <li>选项9</li>
        <li>选项10</li>
    </ul>
</div>


<script>
    const dropdownContent = document.getElementById("dropdownContent");
    const dropdown = document.querySelector('.dropdown');

    function toggleDropdown() {
        dropdownContent.style.display = dropdownContent.style.display === "none" ? "block" : "none";
        dropdown.classList.toggle('active'); // 切换 active 类
    }

    window.onclick = function (event) {
        if (!event.target.closest('.dropdown')) {
            dropdownContent.style.display = "none";
            dropdown.classList.remove('active'); // 移除 active 类
        }
    }
</script>

</body>
</html>

```
