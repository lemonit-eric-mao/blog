---
title: 'Go中使用 SQLite 数据库'
date: '2023-08-04T06:47:48+00:00'
status: private
permalink: /2023/08/04/go%e4%b8%ad%e4%bd%bf%e7%94%a8-sqlite-%e6%95%b0%e6%8d%ae%e5%ba%93
author: 毛巳煜
excerpt: ''
type: post
id: 10194
category:
    - Go
    - SQLite
tag: []
post_format: []
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
hestia_layout_select:
    - sidebar-right
---
### sqlite.go 简单封装

```go
package db

import (
    "database/sql"
    "github.com/lemonit-eric-mao/commons/logger"
    "log"

    _ "github.com/mattn/go-sqlite3"
)

var database *sql.DB

func init() {
    var err error
    database, err = sql.Open("sqlite3", "mini_task_program.db")
    if err != nil {
        log.Fatal(err)
    }
}

func Close() error {
    return database.Close()
}

func Exec(query string, args ...any) (sql.Result, error) {

    logger.Debug(len(args))
    // 语句无参数时，直接执行
    if len(args) == 0 {
        return database.Exec(query)
    }

    // 语句有参数时，执行
    // 准备语句的过程包括语法分析、编译以及优化
    stmt, err := database.Prepare(query)
    if err != nil {
        logger.Error(err)
    }
    // 这里要注意，传参时要使用解构语法 args...
    return stmt.Exec(args...)
}

func Query(query string, args ...any) (*sql.Rows, error) {

    // 准备语句的过程包括语法分析、编译以及优化
    stmt, err := database.Prepare(query)
    if err != nil {
        logger.Error(err)
    }
    // 这里要注意，传参时要使用解构语法 args...
    return stmt.Query(args...)
}


```

### 使用方法

```go
package dao

import (
    "fmt"
    "github.com/lemonit-eric-mao/commons/logger"
    "log"
    "mini_task_program/src/commons/db"
)

type ParentTask struct {
}

func NewParentTask() *ParentTask {
    return &ParentTask{}
}

func (p *ParentTask) CreateTable() {
    sql := `
       CREATE TABLE IF NOT EXISTS parent_task (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           name TEXT,
           age INTEGER
       );
    `
    _, err := db.Exec(sql)
    if err != nil {
        logger.Error(err)
    }
}

func (p *ParentTask) InsertData() {
    sql := `
        INSERT INTO parent_task (name, age) VALUES (?, ?)
    `

    result, err := db.Exec(sql, "John Doe", 30)
    if err != nil {
        logger.Error(err)
    }
    fmt.Println(result)
}

func (p *ParentTask) UpdateData() {
    updateDataSQL := `
        UPDATE parent_task SET age = ? WHERE name = ?
    `
    _, err := db.Exec(updateDataSQL, 35, "John Doe")
    if err != nil {
        logger.Error(err)
    }
}

func (p *ParentTask) DeleteData() {
    deleteDataSQL := `
        DELETE FROM parent_task WHERE name = ?
    `
    _, err := db.Exec(deleteDataSQL, "John Doe")
    if err != nil {
        logger.Error(err)
    }
}

func (p *ParentTask) QueryData() {
    queryDataSQL := `
        SELECT id, name, age FROM parent_task WHERE age > ?
    `
    rows, err := db.Query(queryDataSQL, 25)
    if err != nil {
        logger.Error(err)
    }
    defer rows.Close()

    for rows.Next() {
        var id, age int
        var name string
        err = rows.Scan(&id, &name, &age)
        if err != nil {
            logger.Error(err)
        }
        log.Printf("ID: %d, Name: %s, Age: %d", id, name, age)
    }
}


```