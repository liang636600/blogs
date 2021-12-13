# 监控GC相关参数

jvm options在jdk11后出现了改动，以下的jvm参数改动

```
-XX:+PrintGCTimeStamps    
-XX:+PrintGCDateStamps    ==>  decoration options
                               -Xlog:::time,level,tags
-XX:+PrintGCDetails       ==>  -Xlog:gc*
-XX:+PrintGCApplicationStoppedTime ==> -Xlog:safepoint
```

因此修改`GroupByRDD-sample.sh`里的内容

![image-20211212163635213](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211212163635213.png)

```
--conf "spark.driver.extraJavaOptions=--illegal-access=permit -XX:+UseZGC  -verbose:gc -Xlog:gc:/tmp/Drivergc.log -Xlog:gc* -Xlog:::time,level,tags -Xlog:safepoint"  --conf spark.executor.extraJavaOptions="--illegal-access=permit -XX:+UseZGC  -verbose:gc -Xlog:gc:/tmp/executorgc.log -Xlog:gc* -Xlog:::time,level,tags -Xlog:safepoint" 
```

发现在日志中确实是使用的ZGC，并且打印了GC日志

![image-20211127130529781](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211127130529781.png)

在conf参数中加上

```
-Xlog:gc:/home/iscas/Desktop/Drivergc.log
```

gc:后面是log的路径

![image-20211127183751619](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211127183751619.png)

## 1 Web UI相关

每一个SparkContext都会有一个Web UI，默认在4040端口(http://<driver-node>:4040)

想通过WebUI控制台页面来查看具体的job运行细节，正在运行时的任务可以通过访问 **http:ip/4040** (一旦任务结束，该端口将会自动关闭)，有时需要查看历史的job，这时需要用到 **spark-history-server.sh** 服务，操作如下：

具体参考<https://blog.csdn.net/saranjiao/article/details/106239872>中的Web-UI

可以启动history-server来记录log，`./sbin/start-history-server.sh`，默认运行在http://<server-url>:18080，通过spark-history-server可以查看一些统计信息，目前的话只能查看到GC time和duration

![image-20211127175329904](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211127175329904.png)

## 2 GC参数监测

在<https://github.com/JerryLead/SparkProfiler>中，作者设置了三种profiler可以统计运行时间

* The execution time profiler measures the execution time of each application and each map/reduce task
* The dataflow profiler collects the number and size of the records in each data processing phase. We extend the Spark log system to record the spilled data size and spill time
* The resource profiler collects the CPU, memory usage, and GC metrics of each task

