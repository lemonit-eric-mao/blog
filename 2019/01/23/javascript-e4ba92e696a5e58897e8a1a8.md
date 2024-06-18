---
title: 'JavaScript 互斥列表'
date: '2019-01-23T13:15:40+00:00'
status: publish
permalink: /2019/01/23/javascript-%e4%ba%92%e6%96%a5%e5%88%97%e8%a1%a8
author: 毛巳煜
excerpt: ''
type: post
id: 3416
category:
    - JavaScript
tag: []
post_format: []
---
```
<pre data-language="HTML">```markup



    <meta charset="UTF-8"></meta>
    <span>span</span>
    
    <style type="text/css">
        table, tr, th, td {
            padding: 0px;
            margin: 0px;
        }

        table.gridtable {
            width: 1500px;
            font-family: verdana, arial, sans-serif;
            font-size: 11px;
            color: #333333;
            border-width: 1px;
            border-color: #666666;
            border-collapse: collapse;
        }

        table.gridtable th {
            border-width: 1px;
            padding: 8px;
            border-style: solid;
            border-color: #666666;
            background-color: #dedede;
        }

        table.gridtable td {
            border-width: 1px;
            padding: 8px;
            border-style: solid;
            border-color: #666666;
            background-color: #ffffff;
        }

        table.gridtable td > label {
            display: block;
            width: 100%;
            height: 100%;
            line-height: 100%;
            background: aqua;
        }
    </style>






<table class="gridtable">

    <thead>
    <tr>
        <th>属性</th>
        <th>记录1</th>
        <th>记录2</th>
        <th>记录3</th>
        <th>预览</th>
    </tr>
    <tr>
        <th>主记录</th>
        <th><input checked="checked" name="th-radio-name" onclick="thRadioOnClick('0')" type="radio"></input></th>
        <th><input name="th-radio-name" onclick="thRadioOnClick('1')" type="radio"></input></th>
        <th><input name="th-radio-name" onclick="thRadioOnClick('2')" type="radio"></input></th>
        <th>------</th>
    </tr>
    </thead>

    <tbody id="tbodyId">
    <tr>
        <td>机构类型名称</td>
        <td>
            <label>
                <input checked="checked" id="radio-id-0-0" name="radio-0" onclick="tdRadioOnClick('span-id-0-0', 'td-id-0')" type="radio"></input>
                <span id="span-id-0-0">医院0</span>
            </label>
        </td>
        <td>
            <label>
                <input id="radio-id-0-1" name="radio-0" onclick="tdRadioOnClick('span-id-0-1', 'td-id-0')" type="radio"></input>
                <span id="span-id-0-1">地区0</span>
            </label>
        </td>
        <td>
            <label>
                <input id="radio-id-0-2" name="radio-0" onclick="tdRadioOnClick('span-id-0-2', 'td-id-0')" type="radio"></input>
                <span id="span-id-0-2">姓名0</span>
            </label>
        </td>
        <td id="td-id-0"></td>
    </tr>
    <tr>
        <td>客户分类名称</td>
        <td>
            <label>
                <input checked="checked" id="radio-id-1-0" name="radio-1" onclick="tdRadioOnClick('span-id-1-0', 'td-id-1')" type="radio"></input>
                <span id="span-id-1-0">医院1</span>
            </label>
        </td>
        <td>
            <label>
                <input id="radio-id-1-1" name="radio-1" onclick="tdRadioOnClick('span-id-1-1', 'td-id-1')" type="radio"></input>
                <span id="span-id-1-1">地区1</span>
            </label>
        </td>
        <td>
            <label>
                <input id="radio-id-1-2" name="radio-1" onclick="tdRadioOnClick('span-id-1-2', 'td-id-1')" type="radio"></input>
                <span id="span-id-1-2">姓名1</span>
            </label>
        </td>
        <td id="td-id-1"></td>
    </tr>
    <tr>
        <td>机构名称</td>
        <td><label><input checked="checked" id="radio-id-2-0" name="radio-2" onclick="tdRadioOnClick('span-id-2-0', 'td-id-2')" type="radio"></input><span id="span-id-2-0">医院2</span></label>
        </td>
        <td><label><input id="radio-id-2-1" name="radio-2" onclick="tdRadioOnClick('span-id-2-1', 'td-id-2')" type="radio"></input><span id="span-id-2-1">地区2</span></label>
        </td>
        <td><label><input id="radio-id-2-2" name="radio-2" onclick="tdRadioOnClick('span-id-2-2', 'td-id-2')" type="radio"></input><span id="span-id-2-2">姓名2</span></label>
        </td>
        <td id="td-id-2"></td>
    </tr>
    <tr>
        <td>机构级别</td>
        <td><label><input checked="checked" id="radio-id-3-0" name="radio-3" onclick="tdRadioOnClick('span-id-3-0', 'td-id-3')" type="radio"></input><span id="span-id-3-0">医院3</span></label>
        </td>
        <td><label><input id="radio-id-3-1" name="radio-3" onclick="tdRadioOnClick('span-id-3-1', 'td-id-3')" type="radio"></input><span id="span-id-3-1">地区3</span></label>
        </td>
        <td><label><input id="radio-id-3-2" name="radio-3" onclick="tdRadioOnClick('span-id-3-2', 'td-id-3')" type="radio"></input><span id="span-id-3-2">姓名3</span></label>
        </td>
        <td id="td-id-3"></td>
    </tr>
    <tr>
        <td>业务系统编码</td>
        <td><label><input checked="checked" id="radio-id-4-0" name="radio-4" onclick="tdRadioOnClick('span-id-4-0', 'td-id-4')" type="radio"></input><span id="span-id-4-0">医院4</span></label>
        </td>
        <td><label><input id="radio-id-4-1" name="radio-4" onclick="tdRadioOnClick('span-id-4-1', 'td-id-4')" type="radio"></input><span id="span-id-4-1">地区4</span></label>
        </td>
        <td><label><input id="radio-id-4-2" name="radio-4" onclick="tdRadioOnClick('span-id-4-2', 'td-id-4')" type="radio"></input><span id="span-id-4-2">姓名4</span></label>
        </td>
        <td id="td-id-4"></td>
    </tr>
    </tbody>

</table>
<script>
    /**
     * th&#20013;&#30340; radio &#28857;&#20987;&#20107;&#20214;
     * @param spanId
     * @param tdId
     */
    function thRadioOnClick(colId) {
        resetRadio();
        let tbody = document.getElementById('tbodyId');
        for (let i = 0; i < tbody.childElementCount; i++) {
            document.getElementById(`radio-id-${i}-${colId}`).checked = true;
            let spanText = document.getElementById(`span-id-${i}-${colId}`).innerText;
            document.getElementById(`td-id-${i}`).innerText = spanText;
        }
    }

    /**
     * td&#20013;&#30340; radio &#28857;&#20987;&#20107;&#20214;
     * @param spanId
     * @param tdId
     */
    function tdRadioOnClick(spanId, tdId) {
        let spanText = document.getElementById(spanId).innerText;
        document.getElementById(tdId).innerText = spanText;
    }

    /**
     * &#37325;&#32622;&#25152;&#26377;radio&#36873;&#20013;&#29366;&#24577;
     */
    function resetRadio() {
        let radios = document.querySelectorAll('#tbodyId > tr > td > label > input[type="radio"]');
        for (let i = 0; i < radios.length; i++) {
            radios[i].removeAttribute('checked');
        }
    }
</script>



```
```