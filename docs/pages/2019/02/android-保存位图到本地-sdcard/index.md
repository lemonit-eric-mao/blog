---
title: "Android 从网络获取图片，保存位图到本地 SDcard"
date: "2019-02-16"
categories: 
  - "移动端"
---

##### 要求Android版本为 >= 23, 低于23版本会无法获取SDcard读写权限

```java
package com.baidu.idl.sample.utils;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.Environment;
import android.util.Log;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;

/**
 * 远程获取图片
 *
 * @author mao_siyu
 */
public class RemoteGetImageUtils {

    private static final String TAG = "RemoteGetImageUtils";
    private static final int NO_1024 = 1024;
    private static final int NO_100 = 100;

    /**
     * 获取网络图片
     *
     * @param imageUrl 图片网络地址
     * @return Bitmap 返回位图
     */
    public static Bitmap getRemoteImage(String imageUrl) throws IOException {
        URL url = new URL(imageUrl);
        HttpURLConnection connection = (HttpURLConnection) url.openConnection();
        // 超时设置
        connection.setConnectTimeout(3000);
        connection.setDoInput(true);
        // 设置不使用缓存
        connection.setUseCaches(false);
        InputStream inputStream = connection.getInputStream();
        Bitmap bitmap = BitmapFactory.decodeStream(inputStream);
        inputStream.close();
        // 尺寸压缩
        return compressSize(bitmap);
    }

    /**
     * 保存位图到本地
     *
     * @param bitmap
     * @param path       保存到本地文件路径
     * @param fileName   文件名称
     * @param suffixName 文件后缀
     */
    public static void savaImage(Bitmap bitmap, String path, String fileName, String suffixName) {
        File file = new File(Environment.getExternalStorageDirectory().getPath(), path);
        // 文件夹不存在，则创建它
        if (!file.exists()) {
            file.mkdirs();
        }
        String name = file.getPath() + File.separator + fileName + suffixName;
        try (FileOutputStream fileOutputStream = new FileOutputStream(name)) {
            bitmap.compress(Bitmap.CompressFormat.JPEG, NO_100, fileOutputStream);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    /**
     * 保存文件
     *
     * @param fileFullPath
     * @param content
     */
    public static void saveTxt(String fileFullPath, String content) throws IOException {
        File file = new File(Environment.getExternalStorageDirectory().getPath(), fileFullPath);
        writeTxtToFile(file.getPath(), content);
    }

    /**
     * 图片按尺寸压缩
     *
     * @param image （根据Bitmap图片压缩）
     * @return
     */
    private static Bitmap compressSize(Bitmap image) {
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        image.compress(Bitmap.CompressFormat.JPEG, NO_100, baos);
        // 判断如果图片大于1M, 进行压缩避免在生成图片（BitmapFactory.decodeStream）时溢出
        if (baos.toByteArray().length / NO_1024 > NO_1024) {
            // 重置baos即清空baos
            baos.reset();
            // 这里压缩80%，把压缩后的数据存放到baos中
            image.compress(Bitmap.CompressFormat.JPEG, 80, baos);
        }

        ByteArrayInputStream isBm = new ByteArrayInputStream(baos.toByteArray());
        BitmapFactory.Options newOpts = new BitmapFactory.Options();
        // 开始读入图片，此时把options.inJustDecodeBounds 设回true了
        newOpts.inJustDecodeBounds = true;
        Bitmap bitmap = BitmapFactory.decodeStream(isBm, null, newOpts);
        newOpts.inJustDecodeBounds = false;

        int w = newOpts.outWidth;
        int h = newOpts.outHeight;

        // 项目要求是900*900分辨率，所以高和宽我们设置为
        float hh = 900f;
        float ww = 900f;
        // 缩放比。由于是固定比例缩放，只用高或者宽其中一个数据进行计算即可
        // be=1表示不缩放
        int be = 1;
        // 如果宽度大的话根据宽度固定大小缩放
        if (w > h && w > ww) {
            be = (int) (newOpts.outWidth / ww);

            // 如果高度高的话根据高度固定大小缩放
        } else if (w < h && h > hh) {
            be = (int) (newOpts.outHeight / hh);
        }
        if (be <= 0) {
            be = 1;
        }
        // 设置缩放比例
        newOpts.inSampleSize = be;
        // newOpts.inPreferredConfig = Config.RGB_565;//降低图片从ARGB888到RGB565
        // 重新读入图片，注意此时已经把options.inJustDecodeBounds 设回false了
        isBm = new ByteArrayInputStream(baos.toByteArray());
        bitmap = BitmapFactory.decodeStream(isBm, null, newOpts);
        // 压缩好比例大小后再进行质量压缩
        return compressQuality(bitmap);
    }

    /**
     * 图片按质量压缩
     *
     * @param image
     * @return
     */
    private static Bitmap compressQuality(Bitmap image) {

        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        // 质量压缩方法，这里100表示不压缩，把压缩后的数据存放到baos中
        image.compress(Bitmap.CompressFormat.JPEG, NO_100, baos);
        int options = NO_100;
        // 循环判断如果压缩后图片是否大于100kb,大于继续压缩
        while (baos.toByteArray().length / NO_1024 > NO_100) {
            // 重置baos即清空baos
            baos.reset();
            // 第一个参数 ：图片格式 ，第二个参数： 图片质量，100为最高，0为最差  ，第三个参数：保存压缩后的数据的流
            // 这里压缩options%，把压缩后的数据存放到baos中
            image.compress(Bitmap.CompressFormat.JPEG, options, baos);
            // 每次都减少10
            options -= 10;
        }
        // 把压缩后的数据baos存放到ByteArrayInputStream中
        ByteArrayInputStream isBm = new ByteArrayInputStream(baos.toByteArray());
        // 把ByteArrayInputStream数据生成图片
        Bitmap bitmap = BitmapFactory.decodeStream(isBm, null, null);
        return bitmap;
    }

    /**
     * 向文件追加内容
     *
     * @param content
     */
    private static void writeTxtToFile(String fileFullPath, String content) throws IOException {
        File file = getFaceTxtDirectory(fileFullPath);
        try (FileOutputStream fos = new FileOutputStream(file.getAbsolutePath(), true)) {
            fos.write(content.getBytes());
            fos.flush();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    /**
     * 获取txt文件目录 并创建文件 到本地SDCard
     *
     * @param fileFullPath 文件全路径
     * @return
     */
    private static File getFaceTxtDirectory(String fileFullPath) throws IOException {
        File file = new File(fileFullPath);
        if (!file.exists()) {
            file.createNewFile();
        }
        return file;
    }
}
```
