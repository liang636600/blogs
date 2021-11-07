# 运行spark-shell出错：java.lang.IllegalAccessError

我是使用jdk16编译spark源码，编译完成后，当时是build success的，但当我运行`./bin/spark-shell`的时候，出现了如下错误

![image-20211101111810677](https://raw.githubusercontent.com/liang636600/cloudImg/master/img/image-20211101111810677.png)

`java.lang.IllegalAccessError: class org.apache.spark.storage.StorageUtils$ (in unnamed module @0x4097a8c6) cannot access class sun.nio.ch.DirectBuffer (in module java.base) because module java.base does not export sun.nio.ch to unnamed module @0x4097a8c6
  at org.apache.spark.storage.StorageUtils$.<init>(StorageUtils.scala:213)
  at org.apache.spark.storage.StorageUtils$.<clinit>(StorageUtils.scala)
  at org.apache.spark.storage.BlockManagerMasterEndpoint.<init>(BlockManagerMasterEndpoint.scala:110)
  at org.apache.spark.SparkEnv$.$anonfun$create$9(SparkEnv.scala:348)
  at org.apache.spark.SparkEnv$.registerOrLookupEndpoint$1(SparkEnv.scala:287)
  at org.apache.spark.SparkEnv$.create(SparkEnv.scala:336)
  at org.apache.spark.SparkEnv$.createDriverEnv(SparkEnv.scala:191)
  at org.apache.spark.SparkContext.createSparkEnv(SparkContext.scala:277)
  at org.apache.spark.SparkContext.<init>(SparkContext.scala:460)
  at org.apache.spark.SparkContext$.getOrCreate(SparkContext.scala:2690)
  at org.apache.spark.sql.SparkSession$Builder.$anonfun$getOrCreate$2(SparkSession.scala:949)
  at scala.Option.getOrElse(Option.scala:189)
  at org.apache.spark.sql.SparkSession$Builder.getOrCreate(SparkSession.scala:943)
  at org.apache.spark.repl.Main$.createSparkSession(Main.scala:112)
  ... 55 elided
<console>:14: error: not found: value spark
       import spark.implicits._
              ^
<console>:14: error: not found: value spark
       import spark.sql
              ^`

最终在（https://stackoverflow.com/questions/69710694/spark-unable-to-load-native-hadoop-library-for-platform）上面找到了和我一样的错

![image-20211101112116436](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/cfad6899912738a7470bf3c25c2bab01.png)

他这里使用的是jdk17编译spark源码出错，在后面的解决方案中提到

> Java 17 isn't supported - Spark runs on Java 8/11 (source: https://spark.apache.org/docs/latest/).
>
> So install Java 11 and point Spark to that.

目前来看，原因可能暂时spark还不支持jdk16和jdk17，当我使用jdk15的时候没有出现问题。
