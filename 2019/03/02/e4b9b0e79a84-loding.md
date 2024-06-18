---
title: '买的 Loding'
date: '2019-03-02T07:04:49+00:00'
status: private
permalink: /2019/03/02/%e4%b9%b0%e7%9a%84-loding
author: 毛巳煜
excerpt: ''
type: post
id: 3482
category:
    - 前端开发
tag: []
post_format: []
---
```
<pre data-language="HTML">```markup



    <meta charset="utf-8"></meta>
    <title>css加载动画</title>

    <style>
        /* Demo Styles - It's all in the SVG  */
        html {
            height: 100%;
            min-height: 100%;
            overflow: hidden;
        }

        html body {
            background: #222428;
            background-size: 163px;
            font: 14px/21px Monaco, sans-serif;
            color: #999;
            font-smoothing: antialiased;
            -webkit-text-size-adjust: 100%;
            -moz-text-size-adjust: 100%;
            -ms-text-size-adjust: 100%;
            text-size-adjust: 100%;
            height: 100%;
            min-height: 100%;
        }

        html body a, html body a:visited {
            text-decoration: none;
            color: #FF805F;
        }

        html body h4 {
            margin: 0;
            color: #666;
        }

        .scene {
            width: 100%;
            height: 100%;
            -webkit-perspective: 600;
            perspective: 600;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .scene svg {
            width: 240px;
            height: 240px;
        }

        .dc-logo {
            position: fixed;
            right: 10px;
            bottom: 10px;
        }

        .dc-logo:hover svg {
            -webkit-transform-origin: 50% 50%;
            transform-origin: 50% 50%;
            -webkit-animation: arrow-spin 2.5s 0s cubic-bezier(0.165, 0.84, 0.44, 1) infinite;
            animation: arrow-spin 2.5s 0s cubic-bezier(0.165, 0.84, 0.44, 1) infinite;
        }

        .dc-logo:hover:hover:before {
            content: '\2764';
            padding: 6px;
            font: 10px/1 Monaco, sans-serif;
            font-size: 10px;
            color: #00fffe;
            text-transform: uppercase;
            position: absolute;
            left: -70px;
            top: -30px;
            white-space: nowrap;
            z-index: 20px;
            box-shadow: 0px 0px 4px #222;
            background: rgba(0, 0, 0, 0.4);
        }

        .dc-logo:hover:hover:after {
            content: 'Digital Craft';
            padding: 6px;
            font: 10px/1 Monaco, sans-serif;
            font-size: 10px;
            color: #6E6F71;
            text-transform: uppercase;
            position: absolute;
            right: 0;
            top: -30px;
            white-space: nowrap;
            z-index: 20px;
            box-shadow: 0px 0px 4px #222;
            background: rgba(0, 0, 0, 0.4);
            background-image: none;
        }

        @-webkit-keyframes arrow-spin {
            50% {
                -webkit-transform: rotateY(360deg);
                transform: rotateY(360deg);
            }
        }

        @keyframes arrow-spin {
            50% {
                -webkit-transform: rotateY(360deg);
                transform: rotateY(360deg);
            }
        }
    </style>



<h4>DC SVG Loader v.1</h4>

<div class="scene">
    <svg height:="" id="dc-spinner" preserveaspectratio="xMinYMin meet" version="1.1" viewbox="0 0 38 38" width:="" x="0px" xmlns="http://www.w3.org/2000/svg" y="0px">
    <text fill="grey" font-family="Monaco" font-size="2px" style="letter-spacing:0.6" x="14" y="21">LOADING
        <animate attributename="opacity" dur="1.8s" repeatcount="indefinite" values="0;1;0"></animate>
    </text>
    <path d="M20,35c-8.271,0-15-6.729-15-15S11.729,5,20,5s15,6.729,15,15S28.271,35,20,35z M20,5.203
    C11.841,5.203,5.203,11.841,5.203,20c0,8.159,6.638,14.797,14.797,14.797S34.797,28.159,34.797,20
    C34.797,11.841,28.159,5.203,20,5.203z" fill="#373a42">
    </path>

    <path d="M20,33.125c-7.237,0-13.125-5.888-13.125-13.125S12.763,6.875,20,6.875S33.125,12.763,33.125,20
    S27.237,33.125,20,33.125z M20,7.078C12.875,7.078,7.078,12.875,7.078,20c0,7.125,5.797,12.922,12.922,12.922
    S32.922,27.125,32.922,20C32.922,12.875,27.125,7.078,20,7.078z" fill="#373a42">
    </path>

    <path d="M5.203,20
            c0-8.159,6.638-14.797,14.797-14.797V5C11.729,5,5,11.729,5,20s6.729,15,15,15v-0.203C11.841,34.797,5.203,28.159,5.203,20z" fill="#2AA198" stroke="#2AA198" stroke-miterlimit="10" stroke-width="0.6027">
        <animatetransform attributename="transform" calcmode="spline" dur="2s" from="0 20 20" keysplines="0.4, 0, 0.2, 1" keytimes="0;1" repeatcount="indefinite" to="360 20 20" type="rotate"></animatetransform>
    </path>

    <path d="M7.078,20
  c0-7.125,5.797-12.922,12.922-12.922V6.875C12.763,6.875,6.875,12.763,6.875,20S12.763,33.125,20,33.125v-0.203
  C12.875,32.922,7.078,27.125,7.078,20z" fill="#859900" stroke="#859900" stroke-miterlimit="10" stroke-width="0.2027">
        <animatetransform attributename="transform" dur="1.8s" from="0 20 20" repeatcount="indefinite" to="360 20 20" type="rotate"></animatetransform>
    </path>
    </svg>
</div>




```
```