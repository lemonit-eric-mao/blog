---
title: "Java 多线程，数据分组入库"
date: "2020-02-21"
categories: 
  - "java"
---

###### 分组入库

```java
    /**
     * dataList 中包含 27130条数据，要用50个并发，每个并发中有40条数，插入到数据库中
     */
    public void pushHisDataToEmpiPatientByList(List<PatientStageModel> dataList) {

        // 上限 50 并发
        ExecutorService fixedThreadPool = Executors.newFixedThreadPool(50);

        // 集合长度
        int listSize = dataList.size();

        // 先将集合的下标进行分组存放
        List<List<Integer>> indexList = new ArrayList<>();
        List<Integer> list = new ArrayList<>();
        for (int i = 0; i < listSize; i++) {
            list.add(i);
            // 计算结果要包含余数
            if (i % 40 == 0 || i == listSize - 1) {
                indexList.add(list);
                list = new ArrayList<>();
            }
        }

        // 迭代集合中计算好的下标，通过下标来分段获取集合中的数据
        // 这里是获取每一组的下标，并放到子线程中处理
        for (List<Integer> ls : indexList) {
            fixedThreadPool.execute(() -> {
                List<PatientStageModel> datas = new ArrayList<>();
                // 迭代下标，通过下标获取集合中的数据
                for (Integer l : ls) {
                    datas.add(dataList.get(l));
                }
                // 将数据库保存到数据库
                patientStageMapper.insertBatch(datas);
                patientStageTempMapper.insertBatch(datas);
            });
        }

        fixedThreadPool.shutdown();
        Instant start = Instant.now();
        while (true) {
            if (fixedThreadPool.isTerminated()) {
                DateUtil.timeConsum(start, "HIS 数据入库");
                break;
            }
        }

    }

```

* * *

* * *

* * *

###### 多线程的正确用法

`上面的多线程用法是有问题的`

```java
import java.time.Duration;
import java.time.Instant;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import java.util.concurrent.*;

public class BatchProcessor {

    private static final int CORE_THREAD_NUM = 10;
    private static final Random RDM = new Random();
    private static final List<String> DATA = new ArrayList<>(1000);
    private static final CyclicBarrier BARRIER = new CyclicBarrier(CORE_THREAD_NUM + 1);
    private static ThreadPoolExecutor EXECUTOR;

    static {
        EXECUTOR = new ThreadPoolExecutor(
                CORE_THREAD_NUM, CORE_THREAD_NUM, 1000, TimeUnit.MILLISECONDS,
                new LinkedBlockingQueue<>(1000)

        );
    }

    /**
     * 计算程序耗时
     */
    public static void timeConsum(Instant start, String message) {

        Duration timeElapsed = Duration.between(start, Instant.now());
        // 获取毫秒
        long ms = timeElapsed.toMillis();
        // 毫秒转为 时-分-秒-毫秒
        // 时
        long hour = ms / 1000 / 60 / 60;
        // 分
        long min = ms / 1000 / 60 % 60;
        // 秒
        long sec = ms / 1000 % 60;
        // 毫秒
        long mi = ms % 1000;

        System.out.printf("%s耗时: \n ---< %d小时 %d分 %d秒 %d毫秒 >---\n", message, hour, min, sec, mi);
    }

    public static void main(String[] args) throws BrokenBarrierException, InterruptedException {

        while (true) {
            DATA.clear();
            Instant start = Instant.now();
            for (int i = 0; i < 10; i++) {
                EXECUTOR.submit(() -> {
//                    long tid = Thread.currentThread().getId();
                    int time = RDM.nextInt(1000) + 2000;
                    DATA.add(new StringBuilder().append(time).toString());
                    Thread.sleep(time);
                    BARRIER.await();
                    return null;
                });
            }

            BARRIER.await();
            System.out.printf("所有子线程完成，准备批处理:%s", DATA);
            timeConsum(start, "");
            System.out.println();
        }
    }

}
```
