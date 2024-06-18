---
title: 'JavaScript 自定义下拉列表'
date: '2024-04-16T01:17:46+00:00'
status: private
permalink: /2024/04/16/javascript-%e8%87%aa%e5%ae%9a%e4%b9%89%e4%b8%8b%e6%8b%89%e5%88%97%e8%a1%a8
author: 毛巳煜
excerpt: ''
type: post
id: 10811
category:
    - JavaScript
tag: []
post_format: []
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
hestia_layout_select:
    - sidebar-right
---
```javascript



    <meta charset="UTF-8"></meta>
    <meta content="width=device-width, initial-scale=1.0" name="viewport"></meta>
    <title>下拉列表</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css" rel="stylesheet"></link>
    <style>
        /* &#19979;&#25289;&#21015;&#34920;-&#26679;&#24335; */
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
            top: calc(100% + 0px); /* &#35774;&#32622;&#19979;&#25289;&#26694;&#36317;&#31163;&#25353;&#38062;&#24213;&#37096;&#30340;&#36317;&#31163;&#65292;&#21487;&#26681;&#25454;&#23454;&#38469;&#24773;&#20917;&#35843;&#25972; */
            left: 0;
            width: calc(100% + 0px);
            box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.2);
            padding: 8px 0;
            z-index: 1;
            border-radius: 4px;
            display: none;
            max-height: 160px; /* &#26368;&#22823;&#39640;&#24230;&#20026; 160px */
            overflow-y: auto; /* &#24403;&#20869;&#23481;&#39640;&#24230;&#36229;&#36807; 160px &#26102;&#26174;&#31034;&#22402;&#30452;&#28378;&#21160;&#26465; */
            overflow-x: hidden;
        }

        /* &#33258;&#23450;&#20041;&#28378;&#21160;&#26465;&#26679;&#24335; */
        .dropdown-content::-webkit-scrollbar {
            width: 4px; /* &#35774;&#32622;&#28378;&#21160;&#26465;&#23485;&#24230;&#20026; 2px */
        }

        /* &#28378;&#21160;&#26465;&#36712;&#36947; */
        .dropdown-content::-webkit-scrollbar-track {
            background-color: #f9f9f9; /* &#28378;&#21160;&#26465;&#36712;&#36947;&#32972;&#26223;&#33394; */
        }

        /* &#28378;&#21160;&#26465;&#28369;&#22359; */
        .dropdown-content::-webkit-scrollbar-thumb {
            background-color: #ccc; /* &#28378;&#21160;&#26465;&#28369;&#22359;&#39068;&#33394; */
            border-radius: 1px; /* &#28378;&#21160;&#26465;&#28369;&#22359;&#22278;&#35282; */
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

        /* &#40664;&#35748;&#31661;&#22836;&#21521;&#21491;&#65292;&#28857;&#20987;&#21518;&#21521;&#24038; */
        .arrow-down {
            width: 0;
            height: 0;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 5px solid white;
            transition: transform 0.3s ease-in-out; /* &#28155;&#21152;&#36807;&#28193;&#25928;&#26524; */
            transform: rotate(180deg); /* &#40664;&#35748;&#26041;&#21521; */
        }

        .dropdown.active .arrow-down {
            transform: rotate(0deg); /* &#28857;&#20987;&#21518;&#31661;&#22836;&#26041;&#21521; */
        }
    </style>



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
        dropdown.classList.toggle('active'); // &#20999;&#25442; active &#31867;
    }

    window.onclick = function (event) {
        if (!event.target.closest('.dropdown')) {
            dropdownContent.style.display = "none";
            dropdown.classList.remove('active'); // &#31227;&#38500; active &#31867;
        }
    }
</script>





```