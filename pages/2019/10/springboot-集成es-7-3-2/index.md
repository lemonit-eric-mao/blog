---
title: "SpringBoot 集成ES 7.3.2"
date: "2019-10-28"
categories: 
  - "spring-boot"
---

[ES官方 JavaAPI](https://www.elastic.co/guide/en/elasticsearch/client/java-rest/7.3/java-rest-high-document-index.html "ES 官方 JavaAPI")

##### pom.xml

```markup
......
<dependencies>
    <!-- elasticsearch-->
    <dependency>
        <groupId>org.elasticsearch.client</groupId>
        <artifactId>elasticsearch-rest-high-level-client</artifactId>
        <version>7.3.2</version>
    </dependency>
    <!-- elasticsearch-->
    <dependency>
        <groupId>org.elasticsearch</groupId>
        <artifactId>elasticsearch</artifactId>
        <version>7.3.2</version>
    </dependency>
    <!-- elasticsearch-->
    <dependency>
        <groupId>org.elasticsearch.client</groupId>
        <artifactId>elasticsearch-rest-client</artifactId>
        <version>7.3.2</version>
    </dependency>

    <!-- Gson -->
    <dependency>
        <groupId>com.google.code.gson</groupId>
        <artifactId>gson</artifactId>
        <version>2.8.6</version>
    </dependency>

    <!-- lang3 -->
    <dependency>
        <groupId>org.apache.commons</groupId>
        <artifactId>commons-lang3</artifactId>
        <version>3.9</version>
    </dependency>
</dependencies>
......
```

* * *

##### application.yml

```yml
server:
  port: 8080
  servlet:
    context-path: /testes

elasticSearch:
  host: 172.160.180.46
  port: 9200
  client:
    connectNum: 100
    connectPerRoute: 500
```

##### ESClientSpringFactory 引入ES必备配置

```java
package com.my.springboot.common.sinoelasticsearch.config;

import org.apache.http.HttpHost;
import org.elasticsearch.client.RestClient;
import org.elasticsearch.client.RestClientBuilder;
import org.elasticsearch.client.RestHighLevelClient;

import java.io.IOException;

public class ESClientSpringFactory {

    public static int CONNECT_TIMEOUT_MILLIS = 10000;
    public static int SOCKET_TIMEOUT_MILLIS = 300000;
    public static int CONNECTION_REQUEST_TIMEOUT_MILLIS = 5000;
    public static int MAX_CONN_PER_ROUTE = 100;
    public static int MAX_CONN_TOTAL = 300;

    private static HttpHost HTTP_HOST;
    private RestClientBuilder builder;
    private RestClient restClient;
    private RestHighLevelClient restHighLevelClient;

    private static ESClientSpringFactory esClientSpringFactory = new ESClientSpringFactory();

    private ESClientSpringFactory() {
    }

    public static ESClientSpringFactory build(HttpHost httpHost, Integer maxConnectNum, Integer maxConnectPerRoute) {
        HTTP_HOST = httpHost;
        MAX_CONN_TOTAL = maxConnectNum;
        MAX_CONN_PER_ROUTE = maxConnectPerRoute;
        return esClientSpringFactory;
    }

    public static ESClientSpringFactory build(HttpHost httpHost, Integer connectTimeOut, Integer socketTimeOut, Integer connectionRequestTime, Integer maxConnectNum, Integer maxConnectPerRoute) {
        HTTP_HOST = httpHost;
        CONNECT_TIMEOUT_MILLIS = connectTimeOut;
        SOCKET_TIMEOUT_MILLIS = socketTimeOut;
        CONNECTION_REQUEST_TIMEOUT_MILLIS = connectionRequestTime;
        MAX_CONN_TOTAL = maxConnectNum;
        MAX_CONN_PER_ROUTE = maxConnectPerRoute;
        return esClientSpringFactory;
    }


    public void init() {
        builder = RestClient.builder(HTTP_HOST);
        setConnectTimeOutConfig();
        setMutiConnectConfig();
        restClient = builder.build();
        restHighLevelClient = new RestHighLevelClient(builder);
        System.out.println("init factory");
    }

    // 配置连接时间延时
    public void setConnectTimeOutConfig() {
        builder.setRequestConfigCallback(requestConfigBuilder -> {
            requestConfigBuilder.setConnectTimeout(CONNECT_TIMEOUT_MILLIS);
            requestConfigBuilder.setSocketTimeout(SOCKET_TIMEOUT_MILLIS);
            requestConfigBuilder.setConnectionRequestTimeout(CONNECTION_REQUEST_TIMEOUT_MILLIS);
            return requestConfigBuilder;
        });
    }

    // 使用异步httpclient时设置并发连接数
    public void setMutiConnectConfig() {
        builder.setHttpClientConfigCallback(httpClientBuilder -> {
            httpClientBuilder.setMaxConnTotal(MAX_CONN_TOTAL);
            httpClientBuilder.setMaxConnPerRoute(MAX_CONN_PER_ROUTE);
            return httpClientBuilder;
        });
    }

    public RestClient getClient() {
        return restClient;
    }

    public RestHighLevelClient getRhlClient() {
        return restHighLevelClient;
    }

    public void close() {
        if (restClient != null) {
            try {
                restClient.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        System.out.println("close client");
    }
}

```

##### ESConfig 引入ES必备配置

```java
package com.my.springboot.common.sinoelasticsearch.config;

import org.apache.http.HttpHost;
import org.elasticsearch.client.RestClient;
import org.elasticsearch.client.RestHighLevelClient;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Scope;

@Configuration
@ComponentScan(basePackageClasses = ESClientSpringFactory.class)
public class ESConfig {
    @Value("${elasticSearch.host}")
    private String host;

    @Value("${elasticSearch.port}")
    private int port;

    @Value("${elasticSearch.client.connectNum}")
    private Integer connectNum;

    @Value("${elasticSearch.client.connectPerRoute}")
    private Integer connectPerRoute;

    @Bean
    public HttpHost httpHost() {
        return new HttpHost(host, port, "http");
    }

    @Bean(initMethod = "init", destroyMethod = "close")
    public ESClientSpringFactory getFactory() {
        return ESClientSpringFactory. build(httpHost(), connectNum, connectPerRoute);
    }

    @Bean
    @Scope("singleton")
    public RestClient getRestClient() {
        return getFactory().getClient();
    }

    @Bean
    @Scope("singleton")
    public RestHighLevelClient getRHLClient() {
        return getFactory().getRhlClient();
    }

}
```

##### ESAttribute 自定义注解

```java
package com.my.springboot.common.sinoelasticsearch.annotation;

import java.lang.annotation.*;

/**
 * 为动态生成 索引做准备
 */
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.FIELD)
@Documented
public @interface ESAttribute {

    /**
     * 列名 (必须)
     *
     * @return
     */
    String column();

    /**
     * 列类型
     *
     * @return
     */
    String type() default "keyword";

    /**
     * 指定分词器
     *
     * @return
     */
    String analyzer() default "";

}
```

* * *

* * *

##### TestEntity 测试实体类

```java
package com.my.springboot.common.sinoelasticsearch;

import com.my.springboot.common.sinoelasticsearch.annotation.ESAttribute;

/**
 * 测试用实体类
 */
public class TestEntity {

    @ESAttribute(column = "title")
    private String title;

    @ESAttribute(column = "years")
    private String years;

    private String author;

    @ESAttribute(column = "content", type = "text", analyzer = "hanlp")
    private String content;

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getYears() {
        return years;
    }

    public void setYears(String years) {
        this.years = years;
    }

    public String getAuthor() {
        return author;
    }

    public void setAuthor(String author) {
        this.author = author;
    }

    public String getContent() {
        return content;
    }

    public void setContent(String content) {
        this.content = content;
    }
}

```

* * *

* * *

##### 封装工具类 1 ESCreateIndexMappingFactory

```java
package com.my.springboot.common.sinoelasticsearch.tools;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.my.springboot.common.sinoelasticsearch.TestEntity;
import com.my.springboot.common.sinoelasticsearch.annotation.ESAttribute;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/**
 * 创建索引与映射
 */

public class ESCreateIndexMappingFactory {

    private static Gson gson = new GsonBuilder().create();

    public static <T> String createIndexJson(T t) {

        Map<String, Object> mapping = new HashMap<>();
        Map<String, Object> properties = new HashMap<>();
        // 将 properties 加入到 mapping 中
        mapping.put("properties", properties);

        /***********以上是创建索引的默认json格式的配置***********/

        // 使用反射获取类中带有ESAttribute注解的属性
        Arrays.stream(t.getClass().getDeclaredFields()).forEach((field) -> {

            Map<String, Object> attribute = new HashMap<>();

            if (field.isAnnotationPresent(ESAttribute.class)) {
                // 获取注解
                ESAttribute annotation = field.getAnnotation(ESAttribute.class);
                // 获取注解中配置的类型
                attribute.put("type", annotation.type());
                // 获取注解中配置的分词器
                if (!"".equals(annotation.analyzer())) {
                    attribute.put("analyzer", annotation.analyzer());
                }
                // 将类属性加入到 properties 中
                properties.put(annotation.column(), attribute);

            } else {
                // 实体对象默认属性 用ES默认的配置
                attribute.put("type", "keyword");
                properties.put(field.getName(), attribute);
            }

        });

        // 将 map 将为 json
        return gson.toJson(mapping);
    }

    /**
     * 用来测试脚本
     *
     * @param args
     */
    public static void main(String[] args) {

        String indexJson = ESCreateIndexMappingFactory.createIndexJson(new TestEntity());
        System.out.println(indexJson);
    }

}

```

##### 封装工具类 2 ESCreateIndex

```java
package com.my.springboot.common.sinoelasticsearch.tools;

import org.elasticsearch.action.admin.indices.alias.Alias;
import org.elasticsearch.client.RequestOptions;
import org.elasticsearch.client.RestHighLevelClient;
import org.elasticsearch.client.indices.CreateIndexRequest;
import org.elasticsearch.client.indices.CreateIndexResponse;
import org.elasticsearch.client.indices.GetIndexRequest;
import org.elasticsearch.common.settings.Settings;
import org.elasticsearch.common.xcontent.XContentType;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Component;

import java.io.IOException;
import java.util.List;

/**
 * 创建索引与映射
 */
@Component
public class ESCreateIndex {


    @Qualifier("getRHLClient")
    @Autowired
    public RestHighLevelClient client;

    /**
     * 创建索引
     *
     * @return
     * @throws IOException
     */
    public <T> void createIndex(T t, String indexName) throws IOException {

        CreateIndexRequest request = new CreateIndexRequest(indexName);
        request.mapping(ESCreateIndexMappingFactory.createIndexJson(t), XContentType.JSON);

        request.settings(Settings.builder()
                .put("index.number_of_shards", 3)
                .put("index.number_of_replicas", 2)
        );

        getResponse(request, indexName);
    }

    /**
     * 创建带单个别名的索引
     *
     * @return
     * @throws IOException
     */
    public <T> void createIndex(T t, String indexName, Alias alias) throws IOException {

        CreateIndexRequest request = new CreateIndexRequest(indexName);
        request.mapping(ESCreateIndexMappingFactory.createIndexJson(t), XContentType.JSON);

        request.settings(Settings.builder()
                .put("index.number_of_shards", 3)
                .put("index.number_of_replicas", 2)
        );

        // 创建单个别名
        request.alias(alias);

        getResponse(request, indexName);
    }

    /**
     * 创建带多个别名的索引
     *
     * @return
     * @throws IOException
     */
    public <T> void createIndex(T t, String indexName, List<Alias> aliasList) throws IOException {

        CreateIndexRequest request = new CreateIndexRequest(indexName);
        request.mapping(ESCreateIndexMappingFactory.createIndexJson(t), XContentType.JSON);

        request.settings(Settings.builder()
                .put("index.number_of_shards", 3)
                .put("index.number_of_replicas", 2)
        );

        // 创建多个别名
        request.aliases(aliasList);

        getResponse(request, indexName);
    }

    /**
     * 发起请求
     *
     * @param request
     * @param indexName
     * @throws IOException
     */
    private CreateIndexResponse getResponse(CreateIndexRequest request, String indexName) throws IOException {

        boolean exists = indexIsExists(indexName);
        if (exists) return null;

        // 发起请求，并获取响应体
        CreateIndexResponse response = client.indices().create(request, RequestOptions.DEFAULT);
        return response;
    }

    /**
     * 索引存在
     *
     * @param indexName
     * @return
     * @throws IOException
     */
    private boolean indexIsExists(String indexName) throws IOException {

        GetIndexRequest getIndexRequest = new GetIndexRequest(indexName);
        getIndexRequest.local(false);
        getIndexRequest.humanReadable(true);
        getIndexRequest.includeDefaults(false);
        return client.indices().exists(getIndexRequest, RequestOptions.DEFAULT);
    }


}

```

##### 封装工具类 3 ESInsert

```java
package com.my.springboot.common.sinoelasticsearch.tools;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import org.elasticsearch.action.index.IndexRequest;
import org.elasticsearch.action.index.IndexResponse;
import org.elasticsearch.client.RequestOptions;
import org.elasticsearch.client.RestHighLevelClient;
import org.elasticsearch.common.xcontent.XContentType;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Component;

import java.io.IOException;

/**
 * 创建索引与映射
 */
@Component
public class ESInsert {


    @Qualifier("getRHLClient")
    @Autowired
    public RestHighLevelClient client;

    private Gson gson = new GsonBuilder().create();

    public <T> String insert(T t, String indexName) throws IOException {

        IndexRequest request = new IndexRequest(indexName);
        request.source(gson.toJson(t), XContentType.JSON);

        IndexResponse indexResponse = client.index(request, RequestOptions.DEFAULT);

        return indexResponse.status().toString();
    }

    public <T> String insert(T t, String indexName, String id) throws IOException {

        IndexRequest request = new IndexRequest(indexName);
        request.id(id);
        request.source(gson.toJson(t), XContentType.JSON);

        IndexResponse indexResponse = client.index(request, RequestOptions.DEFAULT);

        return indexResponse.status().toString();
    }

}

```

* * *

* * *

##### DemoApplication 程序入口

```java
package com.my.springboot.demo;

import com.my.springboot.common.sinoelasticsearch.TestEntity;
import com.my.springboot.common.sinoelasticsearch.tools.ESCreateIndex;
import com.my.springboot.common.sinoelasticsearch.tools.ESInsert;
import org.elasticsearch.action.admin.indices.alias.Alias;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.io.IOException;

@RestController
@SpringBootApplication
@ComponentScan("com.my.springboot")
public class DemoApplication {

    public static void main(String[] args) {
        SpringApplication.run(DemoApplication.class, args);
        System.out.println("插入测试数据web访问：http://localhost:8080/testes/init");
    }


    /**
     * ==================================以下是 Controller==========================================
     */

    @Autowired
    private ESCreateIndex esCreateIndex;

    @Autowired
    private ESInsert esInsert;

    @GetMapping(value = "init")
    public String init() throws IOException {

        String indexName = "eric_test_schema";

        // 创建索引
        esCreateIndex.createIndex(new TestEntity(), indexName, new Alias("eric_test_schema_alias"));

        // 插入数据
        TestEntity entity = new TestEntity();
        entity.setTitle("秋雨叹");
        entity.setYears("唐代");
        entity.setAuthor("杜甫");
        entity.setContent("雨中百草秋烂死，阶下决明颜色鲜。著叶满枝翠羽盖，开花无数黄金钱。凉风萧萧吹汝急，恐汝后时难独立。堂上书生空白头，临风三嗅馨香泣。");
        esInsert.insert(entity, indexName);

        return "SUCCESS";
    }


}

```

* * *

* * *

###### [下载项目](https://share.weiyun.com/5Op9bKc "下载项目")
