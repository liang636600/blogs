# 运行`GroupByRDD-sample.sh`

## 解析`GroupByRDD-sample.sh`

![image-20211127101248921](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211127101248921.png)

```
#table_hdfs_file=/usr/lijie/data/sql/Rankings-1GB-UserVisits-2GB/uservisits/UserVisits.dat0
table_hdfs_file=/home/iscas/Desktop/SparkGC/sampledata/sql/Rankings-UserVisits/UserVisits.txt
#output_hdfs_dir=/usr/lijie/output/sql/RDDGroupByTest
output_hdfs_dir=/home/iscas/Desktop/RDDGroupByTest

#$HADOOP_HOME/bin/hdfs dfs -rm -r $output_hdfs_dir
logFile=/home/iscas/Desktop/sample.log
/home/iscas/Downloads/sparkJDK16Bin/bin/spark-submit --name "RDDGroupBy-test-1-7G" \
                                             --class applications.sql.rdd.RDDGroupByTest \
                                             --master local\
                                               --total-executor-cores 10 \
                                              --executor-cores 1 \
                                              --executor-memory 3G \
                                              --conf spark.default.parallelism=10 \
                                             --conf "spark.driver.extraJavaOptions=--illegal-access=permit -XX:+UseZGC  -verbose:gc -Xlog:gc:/home/iscas/Desktop/drivergc.log -Xlog:gc* -Xlog:::time,level,tags -Xlog:safepoint"  --conf spark.executor.extraJavaOptions="--illegal-access=permit -XX:+UseZGC  -verbose:gc -Xlog:gc:/home/iscas/Desktop/executorgc.log -Xlog:gc* -Xlog:::time,level,tags -Xlog:safepoint"  \
                                             /home/iscas/Desktop/SparkGC/target/scala-2.12/sparkgc_2.12-1.0.jar \
$table_hdfs_file $output_hdfs_dir 2>&1 | tee $logFile
```

### 1 输入

`UserVisits.txt`文件作为输入，该文件内容为

![image-20211127101654884](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211127101654884.png)

其中一行的数据为

`169.124.27.16|2jmsklgffzpkfsvjfgreppkhwwlsfxwygjrrvxxbwmlcfgmlmdqctakpwvictfazpsrkqp.html|1983-11-23|484.530311958|Mozilla/2.0 compatible; Check&Get 1.1x|GMB|GMB-FS|processing|2`总共有9列，共1000条数据

一行数据解释是`sourceIP destURL visitDate adRevenue userAgent countryCode languageCode searchWord duration`

### 2 输出

输入在一个文件夹下

![image-20211127102310015](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211127102310015.png)

这里共有10个part（编号0~9），应该意味着10个partition，每个partition对应一个part

打开一个part文件

![image-20211127102509668](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211127102509668.png)

其中文件的一行数据为

```
(165.113,CompactBuffer([165.113.15.40,4tyljkwmommzklsnboqjpzoic.html,1994-7-27,325.16875438,ozelot/2.7.3,PER,PER-XH,black,7], [165.113.25.28,5ecaznwfftso.html,1979-7-13,363.249884691,ZipppBot/0.xx,ARM,ARM-AQ,UV,5]))
```

结合该函数应该是GroupBy，所以该脚本的功能是将IP前两位作为key，groupby

### 3 logFile

程序运行期间的log放在logFile中

### 4 运行的Scala文件

运行的是`applications.sql.rdd.RDDGroupByTest`这个文件

在这个文件中加上注释理解

```scala
package applications.sql.rdd

import org.apache.spark.sql.{Row, SparkSession}
import org.apache.spark.sql.types.{StringType, StructField, StructType}

/**
  * Created by xulijie on 17-6-21.
  *
  * SELECT * FROM UserVisits GROUP BY SUBSTR(sourceIP, 1, 7);
  */
object RDDGroupByTest {
  def main(args: Array[String]): Unit = {

    if (args.length < 2) {
      System.err.println("Usage: RDDGroupByTest <table_hdfs_file> <output_file>")
      System.exit(1)
    }

    // $example on:init_session$
    val spark = SparkSession
      .builder()
      .getOrCreate()


    // $example off:init_session$
    // $example on:programmatic_schema$
    // Create an RDD
	// args(0)对应的输入文件路径
    val uservisits = spark.sparkContext.textFile(args(0))


    // The schema is encoded in a string
    val uservisitsSchemaString = "sourceIP destURL visitDate adRevenue userAgent countryCode languageCode searchWord duration"

    // Generate the schema based on the string of schema
    // StructField(String name, DataType dataType, boolean nullable)
    val uservisitsFields = uservisitsSchemaString.split(" ")
      .map(fieldName => StructField(fieldName, StringType, nullable = true))
    val uservisitsSchema = StructType(uservisitsFields)

    // Convert records of the RDD (people) to Rows
    val uservisitsRDD = uservisits
      .map(_.split("\\|"))
      .map(attributes => (attributes(0).substring(0, 7), Row(attributes(0), attributes(1), attributes(2), attributes(3), attributes(4), attributes(5),
        attributes(6), attributes(7), attributes(8))))

    // Apply the schema to the RDD
    // val uservisitsDF = spark.createDataFrame(uservisitsRDD, uservisitsSchema)

    // Creates a temporary view using the DataFrame
    // uservisitsDF.createOrReplaceTempView("uservisits")

    // SQL can be run over a temporary view created using DataFrames
    // val results = spark.sql("SELECT name FROM people")

    val result = uservisitsRDD.groupByKey()
	// args(1)表示输出路径，最后为一个textFile
    result.saveAsTextFile(args(1))
  }

}
```

# 运行`RDDJoinTest-sample.sh`

```
table1_hdfs_file=/home/iscas/Desktop/SparkGC/sampledata/sql/Rankings-UserVisits/Rankings.txt
table2_hdfs_file=/home/iscas/Desktop/SparkGC/sampledata/sql/Rankings-UserVisits/UserVisits.txt
output_hdfs_dir=/home/iscas/Desktop/output/RDDJoinTest


#$HADOOP_HOME/bin/hdfs dfs -rm -r $output_hdfs_dir
logFile=/home/iscas/Desktop/sample.log

#/root/spark/spark-2.1.4.19-bin-2.7.1/sbin/start-slaves.sh
#sleep 5
/home/iscas/Downloads/sparkJDK16Bin/bin/spark-submit --name "RDDJoin-test-1-7G" \
                                             --class applications.sql.rdd.RDDJoinTest \
                                             --master local\
                                               --total-executor-cores 10 \
                                              --executor-cores 1 \
                                              --executor-memory 3G \
                                              --conf spark.default.parallelism=10 \
                                             --conf "spark.driver.extraJavaOptions=--illegal-access=permit -XX:+UseZGC  -verbose:gc -Xlog:gc:/home/iscas/Desktop/drivergc.log -Xlog:gc* -Xlog:::time,level,tags -Xlog:safepoint"  --conf spark.executor.extraJavaOptions="--illegal-access=permit -XX:+UseZGC  -verbose:gc -Xlog:gc:/home/iscas/Desktop/executorgc.log -Xlog:gc* -Xlog:::time,level,tags -Xlog:safepoint"  \
                                             /home/iscas/Desktop/SparkGC/target/scala-2.12/sparkgc_2.12-1.0.jar \
$table1_hdfs_file $table2_hdfs_file $output_hdfs_dir 2>&1 | tee $logFile
```


```scala
package applications.sql.rdd

import org.apache.spark.sql.types.{StringType, StructField, StructType}
import org.apache.spark.sql.{Row, SparkSession}

/**
  * Created by xulijie on 17-6-20.
  *
  * SELECT URL, adRevenue, pageRank FROM Rankings As R, UserVisits As UV WHERE R.URL = UR.URL
  */
object RDDJoinTest {
  def main(args: Array[String]): Unit = {

    if (args.length < 3) {
      System.err.println("Usage: RDDJoinTest <table1_hdfs_file> <table2_hdfs_file> <output_file>")
      System.exit(1)
    }

    // $example on:init_session$
    val spark = SparkSession
      .builder()
      .getOrCreate()

    // $example off:init_session$
    // $example on:programmatic_schema$
    // Create an RDD
    val uservisits = spark.sparkContext.textFile(args(1))
    val rankings = spark.sparkContext.textFile(args(0))

    // The schema is encoded in a string
    val uservisitsSchemaString = "sourceIP destURL d1 d2 visitDate adRevenue userAgent countryCode languageCode searchWord duration"

    // Convert records of the RDD (people) to Rows
    val uservisitsRDD = uservisits
      .map(_.split("\\||\\t"))
      .map(attributes => (attributes(2), attributes(6)))

    // The schema is encoded in a string
    val rankingsSchemaString = "pageURL pageRank avgDuration"


    // Convert records of the RDD (people) to Rows
    val rankingsRDD = rankings
      .map(_.split("\\||\\t"))
      .map(attributes => (attributes(1), attributes(2)))


    val result = uservisitsRDD.join(rankingsRDD)

    result.saveAsTextFile(args(2))

  }
}
```

运行时报错`java.lang.ArrayIndexOutOfBoundsException: Index 6 out of bounds for length 3`

* 失败：尝试将上面的`.map(_.split("\\||\\t"))`修改为`.map(_.split("\\|"))`，再重新sbt编译一下

* 发现shell脚本输入参数顺序与Scala程序接受参数顺序反了，修改为

  ```
  val uservisits = spark.sparkContext.textFile(args(1))
  val rankings = spark.sparkContext.textFile(args(0))
  ```

---

join推断是根据html来，继续修改

```
val uservisitsRDD = uservisits
      .map(_.split("\\||\\t"))
      .map(attributes => (attributes(2), attributes(6)))
```

为

```
val uservisitsRDD = uservisits
      .map(_.split("\\||\\t"))
      .map(attributes => (attributes(1), attributes(0)))
```

表示根据html值相同的join，重新编译运行后看到有join完成

![image-20211128174543617](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211128174543617.png)

最终版本的Scala程序为

```scala
package applications.sql.rdd

import org.apache.spark.sql.types.{StringType, StructField, StructType}
import org.apache.spark.sql.{Row, SparkSession}

/**
  * Created by xulijie on 17-6-20.
  *
  * SELECT URL, adRevenue, pageRank FROM Rankings As R, UserVisits As UV WHERE R.URL = UR.URL
  */
object RDDJoinTest {
  def main(args: Array[String]): Unit = {

    if (args.length < 3) {
      System.err.println("Usage: RDDJoinTest <table1_hdfs_file> <table2_hdfs_file> <output_file>")
      System.exit(1)
    }

    // $example on:init_session$
    val spark = SparkSession
      .builder()
      .getOrCreate()

    // $example off:init_session$
    // $example on:programmatic_schema$
    // Create an RDD
    val uservisits = spark.sparkContext.textFile(args(1))
    val rankings = spark.sparkContext.textFile(args(0))

    // The schema is encoded in a string
    val uservisitsSchemaString = "sourceIP destURL d1 d2 visitDate adRevenue userAgent countryCode languageCode searchWord duration"

    // Convert records of the RDD (people) to Rows
    val uservisitsRDD = uservisits
      .map(_.split("\\|"))
      .map(attributes => (attributes(1), attributes(0)))

    // The schema is encoded in a string
    val rankingsSchemaString = "pageURL pageRank avgDuration"


    // Convert records of the RDD (people) to Rows
    val rankingsRDD = rankings
      .map(_.split("\\|"))
      .map(attributes => (attributes(1), attributes(2)))


    val result = uservisitsRDD.join(rankingsRDD)

    result.saveAsTextFile(args(2))

  }
}
```

# 运行`SVM-sample.sh`

```
input_file=/home/iscas/Desktop/SparkGC/sampledata/mllib/kdd12-sample.txt

logFile=/home/iscas/Desktop/sample.log

iter=10
#dimension=27343226
dimension=54686452
/home/iscas/Downloads/sparkJDK16Bin/bin/spark-submit --name "SVM-test-1-7G" \
                                             --class applications.ml.SVMWithSGDExample \
                                             --master local\
                                             --driver-memory 10G\
                                               --total-executor-cores 10 \
                                              --executor-cores 1 \
                                              --executor-memory 3G \
                                              --conf spark.default.parallelism=10 \
                                             --conf "spark.driver.extraJavaOptions=--illegal-access=permit -XX:+UseZGC  -verbose:gc -Xlog:gc:/home/iscas/Desktop/drivergc.log "  --conf spark.executor.extraJavaOptions="--illegal-access=permit -XX:+UseZGC  -verbose:gc -Xlog:gc:/home/iscas/Desktop/executorgc.log -Xlog:gc* -Xlog:::time,level,tags -Xlog:safepoint"  \
                                             /home/iscas/Desktop/SparkGC/target/scala-2.12/sparkgc_2.12-1.0.jar \
$input_file $iter $dimension 2>&1 | tee $logFile
```

这里要给driver分配足够的内存，不然会出现OOM错误

# 运行PageRank

在sampledata中没有发现Twitter相关数据
