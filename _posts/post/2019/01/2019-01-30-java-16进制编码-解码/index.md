---
title: "Java 16进制编码 解码"
date: "2019-01-30"
categories: 
  - "java"
---

```java
public class Example {

    public static void main(String[] args) {

        String str = "毛巳煜";
        String s = Example.charToHexString(str.getBytes(), str.getBytes().length);
        System.out.println(s);
        String s1 = bytes2HexStr(str.getBytes());
        System.out.println(s1);

        byte[] b = hexStr2Bytes(s);
        System.out.println(new String(b));

    }


    /**
     * byte转为hex串 (指纹厂商提供的转换方法)
     *
     * @param val    字节
     * @param valLen 字节的长度
     * @return
     */
    private static String charToHexString(byte[] val, int valLen) {
        String temp = "";
        for (int i = 0; i < valLen; i++) {
            String hex = Integer.toHexString(0xff & val[i]);
            if (hex.length() == 1) {
                hex = '0' + hex;
            }
            temp += hex.toUpperCase();
        }
        return temp;
    }

    /**
     * byte转为hex串
     *
     * @param byteArr
     * @return
     */
    static String bytes2HexStr(byte[] byteArr) {
        if (null == byteArr || byteArr.length < 1) return "";
        StringBuilder sBuilder = new StringBuilder();
        for (byte t : byteArr) {
            if ((t & 0xF0) == 0) sBuilder.append("0");
            // t & 0xFF 操作是为去除Integer高位多余的符号位（java数据是用补码表示）
            sBuilder.append(Integer.toHexString(t & 0xFF));
        }
        return sBuilder.toString();
    }

    /**
     * hex串转为byte
     *
     * @param hexStr
     * @return
     */
    static byte[] hexStr2Bytes(String hexStr) {

        if (null == hexStr || hexStr.length() < 1) {
            return null;
        }

        int byteLen = hexStr.length() / 2;
        byte[] result = new byte[byteLen];
        char[] hexChar = hexStr.toCharArray();
        for (int i = 0; i < byteLen; i++) {
            result[i] = (byte) (Character.digit(hexChar[i * 2], 16) << 4 | Character.digit(hexChar[i * 2 + 1], 16));
        }

        return result;
    }

}
```
