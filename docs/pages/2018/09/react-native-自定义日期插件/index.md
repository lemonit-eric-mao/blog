---
title: "React-Native 自定义日期插件"
date: "2018-09-06"
categories: 
  - "移动端"
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
        for (let i = 2009; i <= new Date().getFullYear(); i++) {
            yearSrc.push(i);
        }
        let monthSrc = ['请选择', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12];
        let daySrc = ['请选择', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28];

        this.state = {
            yearSrc: yearSrc,
            monthSrc: monthSrc,
            daySrc: daySrc,
            year: year,
            month: month,
            day: day,
            yearItems: [],
            monthItems: [],
            dayItems: []
        }
    }

    componentWillMount() {
        this.getYear();
        this.getMonth();
        this.getDay();
    }

    getYear() {

        for (let i = 0, len = this.state.yearSrc.length; i < len; i++) {
            this.state.yearItems.push(<Picker.Item label={`${this.state.yearSrc[i]}年`} value={this.state.yearSrc[i]}/>);
        }
    }

    getMonth() {

        for (let i = 0, len = this.state.monthSrc.length; i < len; i++) {
            this.state.monthItems.push(<Picker.Item label={`${this.state.monthSrc[i]}月`} value={this.state.monthSrc[i]}/>);
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
        for (let i = 0, len = temp.length; i < len; i++) {
            dayItems.push(<Picker.Item label={`${temp[i]}日`} value={temp[i]}/>);
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
            <View>
                {/*获取日期*/}
                <Button onPress={() => {
                    alert(`${this.state.year}${this.state.month}${this.state.day}`.replace('请选择', ''));
                }} title="获取日期" color="#841584"/>

                {/*年*/}
                <Picker
                    placeholder={`${this.state.year}年`}
                    // selectedValue 数据回显用
                    selectedValue={this.state.year}
                    onValueChange={async (year) => {
                        await this.setState({year: year});
                        await this.setState({month: '请选择'});
                        await this.setState({day: '请选择'});
                    }}>
                    {this.state.yearItems}
                </Picker>

                {/*月*/}
                <Picker
                    placeholder={`${this.state.month}月`}
                    selectedValue={this.state.month}
                    onValueChange={async (month) => {
                        await this.setState({month: month});
                        this.getDay();
                    }}>
                    {this.state.monthItems}
                </Picker>

                {/*日*/}
                <Picker
                    placeholder={`${this.state.day}日`}
                    selectedValue={this.state.day}
                    onValueChange={async (day) => this.setState({day: day})}>
                    {this.state.dayItems}
                </Picker>

            </View>

        );
    }
}

export default LeaderBoard;
```
