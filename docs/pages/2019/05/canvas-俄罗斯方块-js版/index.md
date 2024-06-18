---
title: "Canvas 俄罗斯方块 JS版"
date: "2019-05-10"
categories: 
  - "javascript"
---

```markup
<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <style>
    html, body, canvas {
      padding: 0;
      margin: 0;
    }
  </style>
</head>

<body>
<!--游戏机-->
<canvas id="gamesConsole" class="games-console" width="480" height="720" style="background-color: #2b2b2b"></canvas>
```

```javascript
<script>
  /**
   * 初始化 Context
   */
  class GMCanvas {

    constructor(canvas) {

      this.ctx = canvas.getContext('2d');
      this.width = canvas.clientWidth;
      this.height = canvas.clientHeight;
      // 左、右、下 移动的距离
      this.distance = 40;
      // 方块的历史记录
      this.history = [];
      //
      this.temp = [];
    }

    generateGraph() {
      // I 横
      let IH = [{x: 0, y: 0, w: 38, h: 38}, {x: 40, y: 0, w: 38, h: 38}, {x: 80, y: 0, w: 38, h: 38}, {
        x: 120,
        y: 0,
        w: 38,
        h: 38
      }];
      // I 竖
      let IV = [{x: 0, y: 0, w: 38, h: 38}, {x: 0, y: 40, w: 38, h: 38}, {x: 0, y: 80, w: 38, h: 38}, {
        x: 0,
        y: 120,
        w: 38,
        h: 38
      }];
      // L 横
      let LH = [{x: 0, y: 0, w: 38, h: 38}, {x: 40, y: 0, w: 38, h: 38}, {x: 80, y: 0, w: 38, h: 38}, {
        x: 80,
        y: -40,
        w: 38,
        h: 38
      }];
      // L 竖
      let LV = [{x: 0, y: 0, w: 38, h: 38}, {x: 0, y: 40, w: 38, h: 38}, {x: 0, y: 80, w: 38, h: 38}, {
        x: 40,
        y: 80,
        w: 38,
        h: 38
      }];

      let libs = [IH, IH, IH, IH];

      let random = Math.floor(Math.random() * (libs.length - 1));
      this.temp = libs[random];
    }

    /**
     * 1.生成背景网格
     * @param x
     * @param y
     * @param w
     * @param h
     */
    gmFillRectGrid(x, y, w, h) {
      this.ctx.save();
      this.ctx.lineWidth = 0.2;
      this.ctx.strokeStyle = 'hsla(200, 100%, 50%, .9)';
      this.ctx.strokeRect(x, y, w, h);
      this.ctx.restore();
    }

    /**
     * 2.生成方块
     * @param x
     * @param y
     * @param w
     * @param h
     */
    gmFillRect(x, y, w, h) {
      this.ctx.save();
      // 设置画布 坐标系原点位置（注：是画笔相对的位置，即：每次画新的图都会便宜）
      this.ctx.translate(1, 1);
      // 设置方块填充色
      this.ctx.fillStyle = 'hsla(200, 100%, 50%, .5)';
      // 绘制空心方块，默认黑色
      this.ctx.fillRect(x, y, w, h);
      this.ctx.restore();
    }

    /**
     * 3.生成网格 游戏背景
     */
    generateGrid() {
      for (let i = 0; i < 216; i++) {
        this.gmFillRectGrid((i % 12) * 40, Math.floor(i / 12) * 40, 40, 40);
      }
    }

    /**
     * 4.重绘方块
     */
    repaintRect(callback) {
      this.temp.map((rect) => {
        if (callback) {
          callback(rect);
        }
        this.gmFillRect(rect.x, rect.y, rect.w, rect.h);
      });
    }

    /**
     * 5.更新方块
     */
    gmUpdateRect() {
      this.ctx.clearRect(0, 0, this.width, this.height);
      this.generateGrid();
      // 载入历史方块
      this.history.map((arr) => {
        arr.map((rect) => {
          this.gmFillRect(rect.x, rect.y, rect.w, rect.h);
        });
      });
    }

    /**
     * 6.历史记录(记录已经完成的方块)
     *
     * @param arr 数据
     */
    saveHistory(arr) {
      if (Object.prototype.toString.call(arr) === '[object Array]') {
        this.history.push(arr);
      }
    }

    /**
     * 左移
     */
    gmMoveLeft() {
      this.gmUpdateRect();
      // 计算 是否位移
      let result = this.temp.every((rect) => {
        // 如果有一个方块越界，其余的将不在进行计算
        if (rect.x > 0) {
          return true;
        }
        // 越界
        return false;
      });

      // 重绘方块
      this.repaintRect((rect) => {
        if (result) {
          rect.x -= this.distance;
        }
      });
    }

    /**
     * 右移
     */
    gmMoveRight() {
      this.gmUpdateRect();
      // 计算 是否位移
      let result = this.temp.every((rect) => {
        // 如果有一个方块越界，其余的将不在进行计算
        if (rect.x < this.width - this.distance) {
          return true;
        }
        // 越界
        return false;
      });

      // 重绘方块
      this.repaintRect((rect) => {
        if (result) {
          rect.x += this.distance;
        }
      });
    }

    /**
     * 下移
     */
    gmMoveDown() {
      this.gmUpdateRect();
      // 计算 是否位移
      let result = this.temp.every((rect) => {
        // 如果有一个方块越界，其余的将不在进行计算
        if (rect.y >= this.height - this.distance) {
          // 越界
          return false;
        }
        return true;
      });

      // 重绘方块
      this.repaintRect((rect) => {
        if (result) {
          rect.y += this.distance;
        }
      });

      // 如果发生越界表示，就让方块变为历史
      if(!result) {
        // 保存为历史方块
        this.saveHistory(this.temp);
        // 重新随机生成模型
        this.generateGraph();
      }
    }

    gmTimer() {
      // 每秒执行一次
      this.intervalId = setInterval(() => {
        this.gmMoveDown();
      }, 1000);
    }

  }
</script>
<script>

  let canvas = document.getElementById('gamesConsole');
  let gmCanvas = new GMCanvas(canvas);

  function startGame() {
    // 生成网格 游戏背景
    gmCanvas.generateGrid();
    // 生成图形模型
    gmCanvas.generateGraph();
    // 重绘图形
    gmCanvas.repaintRect();
    // 开启定时器
    gmCanvas.gmTimer();
  }

  startGame();
</script>

<script>
  document.onkeydown = function (e) {
    switch (e.key) {
      case 'ArrowUp':
        break;
      case 'ArrowDown':
        gmCanvas.gmMoveDown();
        break;
      case 'ArrowLeft':
        gmCanvas.gmMoveLeft();
        break;
      case 'ArrowRight':
        gmCanvas.gmMoveRight();
        break;
    }
  }
</script>
```

```markup
</body>

</html>
```
