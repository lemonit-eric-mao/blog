---
title: "JavaScript 行列转换思路"
date: "2019-01-24"
categories: 
  - "javascript"
---

```markup
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="./jquery-3.3.1.min.js">
    <!-- CSS goes in the document HEAD or added to your external stylesheet -->
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
    <script src="jquery-3.3.1.min.js"></script>
</head>
<body>
<input id="getDataId" type="button" value="获取结果！"/>

<!--创建模型-->
<script>
    // 创建 table
    // 创建 thead
    // 创建 tr
    // 创建 th
    // 创建 tbody
    // 创建 tr
    // 创建 td

    var createTable = function () {
        return $('<table class="gridtable"></table>');
    }

    var createThead = function () {
        var thead = $('<thead></thead>');
        return thead;
    }

    var createTbody = function () {
        return $('<tbody id="tbodyId"></tbody>')
    }

    var createTr = function () {
        return $('<tr></tr>')
    }

    var createTh = function () {
        return $('<th></th>');
    }

    var createTd = function (id) {
        var td = (!id) ? $('<td></td>') : $('<td class="result-data" id="' + id + '" data=""></td>');
        return td;
    }

    var createThRadio = function (index) {
        var radio = $('<input type="radio" name="th-radio-name" onclick="thRadioOnClick(' + index + ')" />');
        radio.prop('checked', index == 0);
        return radio;
    }

    var createTdRadio = function (i, j, spanText) {
        var label = $('<label></label>');
        var span = $('<span id="span-id-' + i + '-' + j + '"></span>');
        span.text(spanText);
        var radio = $('<input type="radio" id="radio-id-' + i + '-' + j + '" name="radio-' + i + '" onclick="tdRadioOnClick(\'span-id-' + i + '-' + j + '\', \'td-id-' + i + '\')"/>');
        radio.prop('checked', j == 0);
        radio.appendTo(label);
        span.appendTo(label);
        return label;
    }

</script>

<!--转换数据-->
<script>
    function dataConvert(json) {
        // 创建数据源
        // json = json || [{
        //     id: 10,
        //     name1: '医院0',
        //     name2: '卫生院0',
        //     name3: '建水李浩寨小旷野村卫生所0',
        //     name4: '',
        //     name5: '1097593'
        // }, {
        //     id: 1,
        //     name1: '医院1',
        //     name2: '卫生院1',
        //     name3: '建水李浩寨小旷野村卫生所1',
        //     name4: '',
        //     name5: '1097593'
        // }, {
        //     id: 2,
        //     name1: '医院2',
        //     name2: '卫生院2',
        //     name3: '建水李浩寨小旷野村卫生所2',
        //     name4: '辽宁省',
        //     name5: '1097593'
        // }];

        // 转成如下数据格式
        // var convertJson = [
        //     [{id: 0}, {id: 1}, {id: 2}],
        //     [{name1: '医院0'}, {name1: '医院1'}, {name1: '医院2'}],
        //     [{name2: '卫生院0'}, {name1: '卫生院1'}, {name2: '卫生院2'}],
        //     [{name3: '建水李浩寨小旷野村卫生所0'}, {name3: '建水李浩寨小旷野村卫生所1'}, {name3: '建水李浩寨小旷野村卫生所2'}],
        //     [{name4: '辽宁省0'}, {name4: '辽宁省1'}, {name4: '辽宁省2'}],
        //     [{name5: '10975930'}, {name5: '10975931'}, {name5: '10975932'}],
        // ];

        var data = {};
        for (var i = 0; i < json.length; i++) {
            var item = json[i];
            for (k in item) {
                // 动态生成一个对象
                var obj = {};
                obj[k] = item[k];
                // 创建 存放同一个key的数组
                var row = data[k] || [];
                row.push(obj);
                data[k] = row;
            }
        }
        // console.log(data);
        // 只取所有属性即可
        var result = Object.values(data);
        $.fn.convertJson = result;
        // result.unshift(['标题一', '标题二', '标题三', '标题四', '标题五', '标题六']);
        // Object.assign(data, Object.values(data));
        return result;
    }
</script>

<!--创建表格-->
<script>
    var table = createTable();
    var thead = createThead();
    var tbody = createTbody();
    thead.appendTo(table);
    tbody.appendTo(table);
    $('body').append(table);

    var createHead = function (convertJson) {
        var convertJson = $.fn.convertJson;
        // 第一层表头
        var tr = createTr();
        tr.appendTo(thead);

        var th = createTh('');
        th.appendTo(tr);
        th.text('属性');
        // 中间列
        for (var i = 0; i < convertJson[0].length; i++) {
            var th = createTh('');
            th.appendTo(tr);
            th.text('记录' + i);
        }
        // 预览列
        var th = createTh('');
        th.appendTo(tr);
        th.text('预览');

        // 第二层表头
        var tr = createTr();
        tr.appendTo(thead);
        var th = createTh('');
        th.appendTo(tr);
        th.text('主记录');
        // 中间列
        for (var i = 0; i < convertJson[0].length; i++) {
            var th = createTh('');
            th.appendTo(tr);
            createThRadio(i).appendTo(th);
        }
        // 预览列
        var th = createTh('');
        th.appendTo(tr);
        th.text('-----');

    }
    var createBody = function (titles) {
        var convertJson = $.fn.convertJson;
        for (var i = 0; i < convertJson.length; i++) {
            var tr = createTr();
            tr.appendTo(tbody);
            // 主属性 主记录列
            var td = createTd();
            td.appendTo(tr);
            td.text(titles[i]);
            // 数据列
            var child = convertJson[i];
            for (var j = 0; j < child.length; j++) {
                for (var key in child[j]) {
                    var td = createTd();
                    td.appendTo(tr);
                    if (child[j][key]) {
                        createTdRadio(i, j, child[j][key]).appendTo(td);
                    }
                }
            }
            // 预览 列
            var td = createTd('td-id-' + i);
            td.appendTo(tr);
        }
    }

    /**
     * th中的 radio 点击事件
     * @param spanId
     * @param tdId
     */
    function thRadioOnClick(colId) {
        resetRadio();
        $('#tbodyId > tr').each(function (index, tr) {
            // 当前列所有选项为选中状态
            $('#radio-id-' + index + '-' + colId).prop('checked', true);
            var span = $('#span-id-' + index + '-' + colId);
            var spanText = span.text();

            // 将选中的值 赋给 预览列
            var td = $('#td-id-' + index);
            td.text(spanText);
            // 记录当前选中的 行列位置
            var arr = [index, colId];
            td.attr("data", arr);
        });
    }

    /**
     * td中的 radio 点击事件
     * @param spanId
     * @param tdId
     */
    function tdRadioOnClick(spanId, tdId) {
        var arr = spanId.replace('span-id-', '').split('-');
        $('#' + tdId).attr("data", arr);
        var spanText = $('#' + spanId).text();
        $('#' + tdId).text(spanText);
    }

    /**
     * 重置所有radio选中状态
     */
    function resetRadio() {
        $('tbody input[type="radio"]').each(function (index, radio) {
            $(radio).prop('checked', false);
        });
    }

    /**
     * 获取预览列记录的所有选中的 行列位置
     */
    $.fn.getResult = function () {
        var temp = [];
        $('.result-data').each(function (i, td) {
            var result = $(td).attr('data');
            if (result) {
                temp.push(result);
            }
        });

        // 根据行列位置， 从二维数据串获取对应的 对象数据
        var result = {};
        for (var i = 0; i < temp.length; i++) {
            var arr = temp[i].split(',');
            Object.assign(result, $.fn.convertJson[arr[0]][arr[1]]);
        }
        return result;
    }
</script>

<!--初始化-->
<script>
    $.fn.merge = function (title, json) {
        dataConvert(json);
        createHead();
        createBody(title);
    }
    var title = ['标题一', '标题二', '标题三', '标题四', '标题五', '标题六'];
    var json = [{
        id: 10,
        name1: '医院0',
        name2: '卫生院0',
        name3: '建水李浩寨小旷野村卫生所0',
        name4: '',
        name5: '1097593'
    }, {
        id: 1,
        name1: '医院1',
        name2: '卫生院1',
        name3: '建水李浩寨小旷野村卫生所1',
        name4: '',
        name5: '1097593'
    }, {
        id: 2,
        name1: '医院2',
        name2: '卫生院2',
        name3: '建水李浩寨小旷野村卫生所2',
        name4: '辽宁省2',
        name5: '1097593'
    }];

    $.fn.merge(title, json);
    $('#getDataId').click(function () {
        console.log($.fn.getResult())
    });
</script>
</body>
</html>
```
