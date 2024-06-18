---
title: "Java 反射与泛型使用 练习"
date: "2017-11-16"
categories: 
  - "java"
---

```java
/**
 * 最终共通工具类.
 *
 * @author 毛 巳煜
 * @version 1.0
 * @since 2014/08/20
 */
public final class Util extends StringUtils {

    /**
     * 私有构造 提供单例模式.
     */
    private Util() {}

    /**
     * 单例 静态方法.
     * @return Util
     */
    public static final Util getUtil() {
        return new Util();
    }

    /**
     * 使用 java 的反射机制 将 map 转换成 entity实体类
     *
     * 说明 <T>： 这个T的意思 是给这个方法中其它的T 做一个声明 如果删掉就会报错。
     *
     * @param map 原数据
     * @param clazz 新数据
     * @return
     */
    @SuppressWarnings("unchecked")
    public static final <T> T mapConvertEntity(Map map, Class<T> entityClass) throws Exception {

        if (null == map || null == entityClass) {
            throw new Exception("mapConvertEntity(map=" + map + ", entityClass=" + entityClass+")");
        }

        // 初始化 entity
        Object object = entityClass.newInstance();
        // 获得对象的所有属性
        Field[] fields = entityClass.getDeclaredFields();
        // 存放 key
        String mapKey;
        // 存放 set 方法名
        String methodName;
        // 动态接收 方法
        Method method;

        // 迭代所有的属性并取得所有属性的set方法
        for(Field key : fields) {
            // 取得属性名
            mapKey = key.getName();
            // 拼接 entity 属性的 set 方法名
            methodName = "set" + mapKey.substring(0, 1).toUpperCase() + mapKey.substring(1);

            if (map.containsKey(mapKey)) {
                // 取得属性的 set 方法
                // 说明 （
                //    第一个参数是方法名 ：methodName
                //    第二个参数是该方法的参数类型 ： key.getType()是取得该属性的类型）
                method = entityClass.getDeclaredMethod(methodName, key.getType());
                // 动态执行调用这个方法 并进行传参
                // 说明 （
                //    第一个参数是具体调用该方法的对象
                //    第二个参数是执行该方法的具体参数）
                method.invoke(object, map.get(mapKey));
            }
        }

        return (T) object;
    }


    /**
     * 使用相对路径 动态读取文件
     *
     * @param sqlFileName 文件夹 + 文件名.后缀名
     * @throws IOException
     * @throws NotFoundException
     */
    public final String getFile(String sqlFileName) throws IOException, Exception {

        // 指定 文件夹 + 文件名.后缀名
        String tomcatPath = "org/com/cn/sqlcontext/" + sqlFileName;
        // 获取当前类的类加载器
        ClassLoader classLoader = this.getClass().getClassLoader();
        // 在指定的文件夹下 取得指定的文件的URL路径。
        URL urlPath = classLoader.getResource(tomcatPath);
        // 如果文件不存在 异常抛出
        if (null == urlPath) {
            throw new Exception("找不到指定的文件！");
        }
        // 取得绝对路径
        String path = urlPath.getPath();
        // 转码 （去空格）
        path = URLDecoder.decode(path, "UTF-8");
        // 读取文件
        BufferedReader stream = new BufferedReader(new InputStreamReader(new FileInputStream(path)));
        // 读取一行
        String lineText;
        // 存放读取后的全部内容
        StringBuffer bufferContent = new StringBuffer();
        // 逐行读取
        while ((lineText = stream.readLine()) != null) {
            // 追加到 buffer 中
            bufferContent.append(lineText);
            // 多追加一个空格 防止sql语句粘连
            bufferContent.append(" ");
        }
        return bufferContent.toString();
    }

}
```
