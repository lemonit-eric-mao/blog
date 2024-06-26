---
title: "JavaFX 实现WebView截图"
date: "2018-01-29"
categories: 
  - "java"
---

### JavaFX 实现截图

##### 项目目录

```tree
.
├── pom.xml
└── src
    └── main
        ├── java
        │   └── cn
        │       └── lemonit
        │           └── robot
        │               └── runner
        │                   └── plugin
        │                       └── automatic
        │                           └── browser
        │                               ├── controller
        │                               │   └── LemonRobotBrowserController.java
        │                               └── Main.java
        └── resources
            └── layout
                └── lemon-robot-browser.fxml

13 directories, 4 files
```

#### 入口类 Main.java

```java
package cn.lemonit.robot.runner.plugin.automatic.browser;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.stage.Stage;

import java.io.File;

public class Main extends Application {

    @Override
    public void start(Stage primaryStage) throws Exception {
        Parent root = FXMLLoader.load(Main.class.getClassLoader().getResource("layout" + File.separator + "lemon-robot-browser.fxml"));
        primaryStage.setTitle("柠檬机器人-图像处理");
        primaryStage.setScene(new Scene(root, 1024, 768));
        primaryStage.show();
    }

    public static void main(String[] args) {
        launch(args);
    }

}
```

#### 图像处理功能界面fxml lemon-robot-browser.fxml

```markup
<?xml version="1.0" encoding="UTF-8"?>

<?import javafx.scene.control.Button?>
<?import javafx.scene.control.Label?>
<?import javafx.scene.control.TextField?>
<?import javafx.scene.layout.Pane?>
<?import javafx.scene.web.WebView?>

<Pane maxHeight="-Infinity" maxWidth="-Infinity" minHeight="-Infinity" minWidth="-Infinity" prefHeight="930.0" prefWidth="1140.0" xmlns="http://javafx.com/javafx/9" xmlns:fx="http://javafx.com/fxml/1" fx:controller="cn.lemonit.robot.runner.plugin.automatic.browser.controller.LemonRobotBrowserController">
   <children>
      <TextField fx:id="mUrl" layoutX="128.0" layoutY="19.0" prefHeight="26.0" prefWidth="316.0" />
      <Button layoutX="472.0" layoutY="19.0" mnemonicParsing="false" onAction="#openView" text="打开" />
      <Button layoutX="541.0" layoutY="18.0" mnemonicParsing="false" onAction="#scrollView" text="滚动" />
      <Label layoutX="52.0" layoutY="24.0" text="请输入URL: " />
      <WebView fx:id="mBrowser" layoutX="52.0" layoutY="56.0" prefHeight="0" prefWidth="0" />
      <Button layoutX="616.0" layoutY="18.0" mnemonicParsing="false" onAction="#onScreenshot" text="截图" />
   </children>
</Pane>
```

#### 图像处理功能界面fxml 对应的Controller LemonRobotBrowserController.java

```java
package cn.lemonit.robot.runner.plugin.automatic.browser.controller;

import javafx.embed.swing.SwingFXUtils;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.geometry.Rectangle2D;
import javafx.scene.control.TextField;
import javafx.scene.image.Image;
import javafx.scene.image.WritableImage;
import javafx.scene.web.WebEngine;
import javafx.scene.web.WebView;
import javafx.stage.Screen;
import netscape.javascript.JSObject;

import javax.imageio.ImageIO;
import java.io.File;
import java.io.IOException;
import java.net.URL;
import java.util.ResourceBundle;

/**
 * WebView 截图
 *
 * @author mao-siyu
 */
public class LemonRobotBrowserController implements Initializable {

    /**
     * 页面输入url地址
     */
    @FXML
    private TextField mUrl;

    /**
     * webview浏览器
     */
    @FXML
    private WebView mBrowser;

    /**
     * JavaScript 引擎
     */
    private WebEngine webEngine;

    /**
     * 屏幕宽
     */
    private double screenWidth;

    /**
     * 屏幕高
     */
    private double screenHeight;

    /**
     * 窗体加载完成后渲染
     *
     * @param location
     * @param resources
     */
    @Override
    public void initialize(URL location, ResourceBundle resources) {

        // 获取当前屏幕的宽高
        Rectangle2D rectangle2D = Screen.getPrimary().getVisualBounds();
        screenWidth = 930;
        screenHeight = rectangle2D.getHeight();

        // 设置webview的宽高
        mBrowser.setPrefWidth(screenWidth);
        mBrowser.setPrefHeight(screenHeight);

        webEngine = mBrowser.getEngine();
        webEngine.setJavaScriptEnabled(true);
    }

    /**
     * 使用webview打开浏览器
     */
    @FXML
    public void openView() {
        webEngine.load(mUrl.getText());
        // 初始化 JavaScript 回调内部类对象
        JSObject window = (JSObject) webEngine.executeScript("window");
        window.setMember("app", javaApplication);
    }

    /**
     * 浏览器滚动脚本
     */
    @FXML
    public void scrollView() {
        // js 操作webview滚动页面
        String script = "" +
                "var intervalId = setInterval(function() {\n" +
                "    var scrollTop = document.documentElement.scrollTop += 1000;\n" +
                "    var scrollHeight = document.documentElement.scrollHeight;\n" +
                "\n" +
                "    if((scrollTop + 1000) >= scrollHeight) {\n" +
                "        window.clearInterval(intervalId);\n" +
                "        document.documentElement.scrollTop = 0;\n" +
                "        app.scrollEndCallback(scrollHeight);\n" +
                "    }\n" +
                "}, 600);";
        webEngine.executeScript(script);
    }

    /**
     * WebView 控制截图
     *
     * @throws IOException
     */
    @FXML
    public void onScreenshot() throws IOException {

        // 生成图片的宽度与高度
        WritableImage image = new WritableImage((int) screenWidth, (int) screenHeight);
        // 开始截图!
        Image outputImage = mBrowser.snapshot(null, image);
        // 生成文件的全路径
        File fileFullPath = new File("." + File.separator + System.currentTimeMillis() + ".png");
        // 生成文件
        ImageIO.write(SwingFXUtils.fromFXImage(outputImage, null), "png", fileFullPath);
    }


    /**
     * JavaScript 回调内部类
     *
     * @author mao-siyu
     */
    public class JavaApplication {

        /**
         * 滚动事件结束回调
         *
         * @param clientHeight
         */
        public void scrollEndCallback(String clientHeight) {
            screenHeight = Double.valueOf(clientHeight);
            mBrowser.setPrefHeight(screenHeight);
            System.out.println(clientHeight + "=================");
        }
    }

    /**
     * 实例化 JavaScript回调内部类
     */
    private JavaApplication javaApplication = new JavaApplication();
}
```
