---
title: "Java 单元测试"
date: "2019-04-23"
categories: 
  - "java"
---

#### java 单元测试

##### maven 依赖

```markup
<!--Test-->
<dependency>
    <groupId>junit</groupId>
    <artifactId>junit</artifactId>
    <scope>test</scope>
</dependency>
<dependency>
    <groupId>org.jmockit</groupId>
    <artifactId>jmockit</artifactId>
    <version>1.45</version>
    <scope>test</scope>
</dependency>
<dependency>
    <groupId>org.assertj</groupId>
    <artifactId>assertj-core</artifactId>
    <scope>test</scope>
</dependency>
```

1. 编写回放代码 (要测试的类中的正常逻辑代码)
2. 编写Mock (当测试的方法中包含 当前类的其它方法时，需要使用 Mock功能 进行模拟)
3. 编写录制代码 (当测试的方法中包含 其它类的引用方法时，需要使用 录制功能 进行模拟)
4. 最后验证代码 （只验证这个方法中最关键的点，比如：方法的返回值，如果没有返回值，这个方法最终执行完，期待的结果是什么等等）

###### 注：写单元测试时，只验证当前方法，不验证引用的方法与无返回值的方法，方法中存在引用`当前类`的方法或`无返回值`的方法使用**Mock**, 引用外部类`有返回值`的方法使用**录制**。

###### 录制与Mock的区别

- 录制：范围更精确
- Mock: 范围更广
- 这两个功能都是进行模拟，但我们使用时，一定是尽量使用更精确的，模拟的影响范围更小的

##### 模型

```java
import org.junit.Test;

import mockit.Expectations;
import mockit.Injectable;
import mockit.Mock;
import mockit.MockUp;
import mockit.Tested;
import mockit.Verifications;

import static org.assertj.core.api.Assertions.*;
/**
 * Service 测试类
 *
 * @author Eric.mao
 */
public class XXXMockit {

    private Service service;

    /**
     * 新增封存数据
     *
     * @author Eric.mao
     */
    @Test
    public void xxxTest() {

        // Service类中 XXX对象 中的 xxx方法
        new MockUp<Service>() {
            @Mock
            public void xxxMethod() {
            }
        };

        // 录制阶段 (将外部类的方法中需要获取数据的部分，创建出来)
        new Expectations() {
            {
                // 代码中需要获取数据的地方，用这个块来造假数据
            }
        };

        // 回放阶段 (真正的去执行 Service类 中真正的方法)

        // 验证阶段 (回放执行结束以后，对回放阶段的执行过程进行验证)
        new Verifications() {
            {
                // 想要验证什么在这里面写
            }
        };
    }
}
```

##### 业务类

##### OrganizationVersionSealedService.java

```java
/**
 * 机构 映射关系待办 Service
 *
 * @author Eric.mao
 */
@Service
public class OrganMappingTodoService {

    /**
     * 手动Mapping
     *
     * @author Eric.mao
     */
    public void doMapping(List<DcOrganMappingTodo> beanList) {
        // 保存到 待办表
        this.saveTodoTable(beanList);

        AppContextHelper.switchOnDynamicDs();
        List<DcOrganMapping> mappingList = organTodoToMapping(beanList);
        AppContextHelper.switchOffDynamicDs();

        // 保存到 Mapping 关系表
        mappingService.saveOrganMapping(mappingList);

        // 同步到 ES
        updateEs(mappingList);
    }
}
```

##### 编写测试类

##### OrganMappingTodoServiceTest.java

```java
import org.junit.Test;

import mockit.Expectations;
import mockit.Injectable;
import mockit.Mock;
import mockit.MockUp;
import mockit.Tested;
import mockit.Verifications;

import static org.assertj.core.api.Assertions.*;

/**
 * 机构 映射关系待办 Service 测试
 *
 * @author Eric.mao
 */
public class OrganMappingTodoServiceTest {

    /**
     * 要测试的类
     */
    @Tested
    private OrganMappingTodoService organMappingTodoService;

    /**
     * 要模拟的对象
     */
    @Injectable
    private DcOrganMappingTodoManager mappingTodoManager;

        /**
     * 手动Mapping
     *
     * @author Eric.mao
     */
    @Test
    public void doMappingTest() {

        new MockUp<OrganMappingTodoService>() {
            @Mock
            public void saveTodoTable(List<DcOrganMappingTodo> mappingTodos) {
            }

            @Mock
            protected void updateEs(List<DcOrganMapping> mappingList) {
            }

            @Mock
            protected List<DcOrganMapping> organTodoToMapping(List<DcOrganMappingTodo> beanList) {
                List<DcOrganMapping> mappingList = new ArrayList<>();

                DcOrganMapping organMapping = new DcOrganMapping();
                organMapping.setDealerCode("D0000001");
                organMapping.setDealerName("测试数据");
                organMapping.setSourceOrganName("终端410");
                mappingList.add(organMapping);

                organMapping = new DcOrganMapping();
                organMapping.setDealerCode("D0000001");
                organMapping.setDealerName("测试数据");
                organMapping.setSourceOrganName("终端809");
                mappingList.add(organMapping);

                organMapping = new DcOrganMapping();
                organMapping.setDealerCode("D0000001");
                organMapping.setDealerName("测试数据");
                organMapping.setSourceOrganName("终端537");
                mappingList.add(organMapping);
                return mappingList;
            }
        };

        new MockUp<OrganMappingService>() {
            @Mock
            public void saveOrganMapping(DcOrganMapping dcOrganMapping) {
            }
        };

        new MockUp<AppContextHelper>() {
            @Mock
            public void switchOnDynamicDs() {
            }

            @Mock
            public void switchOffDynamicDs() {
            }
        };

        // 录制阶段 (将方法中需要获取数据的部分，创建出来)
        new Expectations() {
            {
                // 机构待办数据 转为 机构Mapping
            }
        };

        // 回放阶段
        organMappingTodoService.doMapping(new ArrayList<>());

        // 验证阶段 (回放执行结束以后，对回放阶段的执行过程进行验证)
        new Verifications() {
            {

                List<DcOrganMapping> list;
                mappingService.saveOrganMapping(list = withCapture());

                // 验证这个被引用的方法被执行的次数（注：只能验证引用的方法，类内部方法不能计数）
                times = 1;

                // 验证参数是否正确
                assertThat(list)
                .hasSize(3)
                // 验证当前对象中的 如下字段
                .extracting("dealerCode", "dealerName", "status", "sourceOrganName")
                // 对象集合中 是否完全包含如下内容
                .contains(
                    tuple("D0000001", "测试数据", null, "终端537"),
                    tuple("D0000001", "测试数据", null, "终端410"),
                    tuple("D0000001", "测试数据", null, "终端809")
                );
            }
        };
    }
}
```

[JMockit](http://jmockit.cn/index.htm "JMockit") [AssertJ](http://joel-costigliola.github.io/assertj/ "AssertJ")
