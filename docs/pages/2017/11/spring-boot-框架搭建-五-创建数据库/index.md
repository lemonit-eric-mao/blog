---
title: "spring-boot 框架搭建 五 (创建数据库)"
date: "2017-11-16"
categories: 
  - "spring-boot"
---

数据库地址: 10.32.156.52 数据库端口: 3306 数据库用户名: dlfc 数据库密码: dlfc#123

### 创建主数据库 masterTest

### 创建主数据库表 users

```sql
/*
Navicat MySQL Data Transfer

Source Server         : 10.32.156.52
Source Server Version : 50712
Source Host           : 10.32.156.52:3306
Source Database       : masterTest

Target Server Type    : MYSQL
Target Server Version : 50712
File Encoding         : 65001

Date: 2017-08-18 17:39:35
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `u_id` varchar(255) DEFAULT NULL,
  `u_name` varchar(255) DEFAULT NULL COMMENT '姓名',
  `u_age` varchar(255) DEFAULT NULL COMMENT '年龄',
  `u_sex` varchar(255) DEFAULT NULL COMMENT '性别'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES ('111', '毛巳煜', '30', '男');
SET FOREIGN_KEY_CHECKS=1;
```

### 创建从数据库 slave1Test

### 创建从数据库表 users

```sql
/*
Navicat MySQL Data Transfer

Source Server         : 10.32.156.52
Source Server Version : 50712
Source Host           : 10.32.156.52:3306
Source Database       : slave1Test

Target Server Type    : MYSQL
Target Server Version : 50712
File Encoding         : 65001

Date: 2017-08-18 17:38:45
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `u_id` varchar(255) DEFAULT NULL,
  `u_name` varchar(255) DEFAULT NULL COMMENT '姓名',
  `u_age` varchar(255) DEFAULT NULL COMMENT '年龄',
  `u_sex` varchar(255) DEFAULT NULL COMMENT '性别'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES ('222', '燕大神', '666', '泰国人');
SET FOREIGN_KEY_CHECKS=1;
```
