---
title: 'React-Native 自定义日期插件'
date: '2018-09-06T17:36:59+00:00'
status: publish
permalink: /2018/09/06/react-native-%e8%87%aa%e5%ae%9a%e4%b9%89%e6%97%a5%e6%9c%9f%e6%8f%92%e4%bb%b6
author: 毛巳煜
excerpt: ''
type: post
id: 2341
category:
    - 移动端
tag: []
post_format: []
hestia_layout_select:
    - default
---
```javascript
/**
 * 日期控件
 *
 * @date 2018-09-06
 * @author mao_siyu
 */
import React, {Component} from 'react';
import {
    View,
    Picker,
    Button,
} from 'react-native';


class LeaderBoard extends Component {

    constructor(props) {
        super(props);

        let date = new Date();
        let year = date.getFullYear();
        let month = date.getMonth() + 1;
        let day = date.getDate();

        let yearSrc = [];
        for (let i = 2009; i );
        }
    }

    getMonth() {

        for (let i = 0, len = this.state.monthSrc.length; i );
        }
    }

    getDay() {

        let temp = this.state.daySrc;

        // 生成年
        // 生成月
        // 根据月生成天
        if ([1, 3, 5, 7, 8, 12].includes(this.state.month)) {
            temp = temp.concat(...[29, 30, 31]);
        } else if ([4, 6, 9, 11].includes(this.state.month)) {
            temp = temp.concat(...[29, 30]);
        } else {
            temp = (this.isLeapYear(this.state.year)) ? temp.concat(29) : temp;
        }

        let dayItems = [];
        for (let i = 0, len = temp.length; i );
        }

        this.setState({dayItems: dayItems});
    }

    /**
     * 判断是否是闰年
     * @param year
     * @returns {boolean}
     */
    isLeapYear(year) {
        return (year % 400 == 0) || (year % 4 == 0 && year % 100 != 0);
    }

    render() {

        return (
            <view>
                {/*获取日期*/}
                <button onpress="{()"> {
                    alert(`<span class="katex math inline">{this.state.year}</span>{this.state.month}${this.state.day}`.replace('请选择', ''));
                }} title="获取日期" color="#841584"/>

                {/*年*/}
                <picker onvaluechange="{async" placeholder="{`${this.state.year}年`}" selectedvalue=""> {
                        await this.setState({year: year});
                        await this.setState({month: '请选择'});
                        await this.setState({day: '请选择'});
                    }}>
                    {this.state.yearItems}
                </picker>

                {/*月*/}
                <picker onvaluechange="{async" placeholder="{`${this.state.month}月`}" selectedvalue="{this.state.month}"> {
                        await this.setState({month: month});
                        this.getDay();
                    }}>
                    {this.state.monthItems}
                </picker>

                {/*日*/}
                <picker onvaluechange="{async" placeholder="{`${this.state.day}日`}" selectedvalue="{this.state.day}"> this.setState({day: day})}>
                    {this.state.dayItems}
                </picker>

            </button></view>

        );
    }
}

export default LeaderBoard;

```