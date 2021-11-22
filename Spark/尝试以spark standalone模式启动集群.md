# 尝试以spark standalone模式启动集群

1. **启动master：** 根据官方文档，运行master server `./sbin/start-master.sh`，可以打开浏览器输入url <http://localhost:8080/>获得spark web界面，需要记录一下spark界面的URL值
2. **启动worker**：运行`./sbin/start-worker.sh spark://iscas-Precision-3551:7077`把`<master-spark-URL>`换成步骤1中的URL值，web界面如下

注：关闭master和worker的命令分别为`sbin/stop-master.sh`与`sbin/stop-worker.sh`

![image-20211101174630634](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211101174630634.png)

- 使用jdk16测试

​        测试主要是运行基于Spark的蒙特卡罗求PI的程序，进入$SPARK_HOME/bin目录下，执行命令`./spark-submit --master spark://iscas-Precision-3551:7077 --class org.apache.spark.examples.SparkPi ../examples/target/scala-2.12/jars/spark-examples_2.12-3.2.0.jar 100`

（补充：运行命令./spark-submit --conf "spark.driver.extraJavaOptions=--illegal-access=permit"  --conf "spark.executor.extraJavaOptions=--illegal-access=permit" --class org.apache.spark.examples.SparkPi --master local ../examples/target/scala-2.12/jars/spark-examples_2.12-3.2.0.jar 100

解释：

--class org.apache.spark.examples.SparkPi表示此次执行的Main class

--master local表示spark程序local执行

../examples/target/scala-2.12/jars/spark-examples_2.12-3.2.0.jar为spark程序的示例包

100表示迭代100次），执行命令后，成功后预期显示`Pi is roughly 3.1411003141100315`，但我这里报错了，错误和运行spark-shell的时候错误一样

![image-20211101175249353](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211101175249353.png)

- 尝试jdk15测试

​       使用jdk15的时候前面没有啥问题，只是运行程序的时候轮流出现以下问题

![image-20211101185134621](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211101185134621.png)

从这里来看，貌似是每次executor分配的空间都是不够的，然后就停止了

打开id为67的executor的stderr文件，发现竟然也出现了和jdk16一样的错误

![image-20211101185741767](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211101185741767.png)

在conf文件夹下复制spark-env.sh.template为spark-env.sh并修改内容

![image-20211104181141382](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211104181141382.png)

再运行就没有问题了

![image-20211104181238800](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211104181238800.png)

---

**尝试解决JDK16中的`java.lang.IllegalAccessError: class org.apache.spark.storage.StorageUtils$ (in unnamed module @0x4097a8c6) cannot access class sun.nio.ch.DirectBuffer (in module java.base) because module java.base does not export sun.nio.ch to unnamed module @0x4097a8c6`问题**

* 失败：修改spark-defaults.conf.template文件，将最后一行修改为`spark.executor.extraJavaOptions  -XX:+PrintGCDetails -Dkey=value -Dnumbers="one two three" --illegal-access=permit`并去除#

![image-20211101193153970](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211101193153970.png)

修改过后并没有生效

* 失败：看到spark-defaults.conf

  ![image-20211104110551741](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211104110551741.png)

  以为与我的spark/conf下的spark-defaults.conf.template不一样，复制一份spark-defaults.conf.template文件并重命名为spark-defaults.conf，最终还是失败


* 失败：spark-env.sh.template里面加入相关jvm配置

  ![image-20211104124818702](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211104124818702.png)

  不生效

  重新复制一份新命名为spark-env.sh再次尝试，发现依然不生效

* 失败：spark-default.conf文件全部修改加上--illegal-access=permit

  ![image-20211104101509729](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211104101509729.png)

  ![image-20211104101428437](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211104101428437.png)

* 失败：修改spark-env.sh中的Java_OPTS为![image-20211104173136989](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211104173136989.png)

  仍未能解决

* 失败：尝试使用官方编译好的jdk16编译spark源码

  报的一样的错

* 失败：尝试使用官方编译好的spark和官方编译好的jdk16并修改conf文件夹下的spark-env.sh文件，发现仍为一样的错。使用官方编译好的spark和官方编译好的jdk15并修改conf文件夹下的spark-env.sh文件，发现正常运行测试用例。

* 尝试在spark-env.sh里加上`SPARK_LAUNCHER_OPTS="--illegal-access=permit --add-exports=java.base/sun.nio.ch=ALL-UNNAMED"`

  ![image-20211108184046506](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211108184046506.png)
  
  启动master和worker，然后运行测试程序，相较于以前加上了`--conf "spark.driver.extraJavaOptions=--illegal-access=permit"  --conf "spark.executor.extraJavaOptions=--illegal-access=permit"`参数，在bin目录下，命令为
  
  `./spark-submit --master spark://iscas-Precision-3551:7077 --conf "spark.driver.extraJavaOptions=--illegal-access=permit"  --conf "spark.executor.extraJavaOptions=--illegal-access=permit" --class org.apache.spark.examples.SparkPi ../examples/target/scala-2.12/jars/spark-examples_2.12-3.2.0.jar 100`
  
  终于成功
  
  ![image-20211108185410271](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211108185410271.png)
  
  
  
  同理使用该方法spark-shell也能运行，在bin目录下，运行`./spark-shell --conf "spark.driver.extraJavaOptions=--illegal-access=permit"  --conf "spark.executor.extraJavaOptions=--illegal-access=permit"`
  
  成功
  
  ![image-20211108190521239](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211108190521239.png)
  
  