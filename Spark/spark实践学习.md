# **启动spark：**

在bin目录下，运行

```
./spark-shell --conf "spark.driver.extraJavaOptions=--illegal-access=permit"  --conf "spark.executor.extraJavaOptions=--illegal-access=permit"
```

# 用sbt编译打包Scala程序

1. 官网下载<https://www.scala-sbt.org/download.html>

2. 在解压后的主目录下新建一个shell脚本名字sbt

   ```
   SBT_OPTS="-Xms512M -Xmx1536M -Xss1M -XX:+CMSClassUnloadingEnabled -XX:MaxPermSize=256M"
   
   java $SBT_OPTS -jar `dirname $0`/sbt-launch.jar "$@" 
   ```

   增加可执行权限`chmod u+x sbt `

   配置环境变量在path中加上bin路径

   测试是否成功`sbt sbtVersion`

   ![image-20211116231841299](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211116231841299.png)

   

3. 创建项目结构，主项目sparkapp

   `mkdir -p ~/Desktop/sparkapp/src/main/scala`

4. 创建一个Scala程序

   ```
   import org.apache.spark.SparkContext
   import org.apache.spark.SparkContext._
   import org.apache.spark.SparkConf
   
   object SimpleApp
   {
       def main(args: Array[String])
       {
           val logFile = "file:///home/iscas/Downloads/sparkJDK16Bin/README.md"
           val conf = new SparkConf().setAppName("Simple Application")
           val sc = new SparkContext(conf)
           val logData = sc.textFile(logFile, 2).cache()
           val numAs = logData.filter(line => line.contains("a")).count()
           val numBs = logData.filter(line => line.contains("b")).count()
           println("Lines with a: %s, Lines with b: %s".format(numAs, numBs))
       }
   }
   ```

5. 创建一个simple.sbt文件

   `vim ~/Desktop/sparkapp/simple.sbt `

   ```
   name := "Simple Project"
   version := "1.0"
   scalaVersion := "2.12.15"
   libraryDependencies += "org.apache.spark" %% "spark-core" % "3.2.0"
   ```

6. 在sparkapp目录下执行`sbt package`打包

   ![image-20211116233508725](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211116233508725.png)

7. 提交运行

   目标jar所在的路径`/home/iscas/Desktop/sparkapp/target/scala-2.12/simple-project_2.12-1.0.jar`

   运行`SPARK_HOME/bin/spark-submit --conf "spark.driver.extraJavaOptions=--illegal-access=permit"  --conf "spark.executor.extraJavaOptions=--illegal-access=permit" --class "SimpleApp" /home/iscas/Desktop/sparkapp/target/scala-2.12/simple-project_2.12-1.0.jar `

   或者
   
   ```
   ./spark-submit --master=spark://iscas-Precision-3551:7077 --conf "spark.driver.extraJavaOptions=--illegal-access=permit"  --conf "spark.executor.extraJavaOptions=--illegal-access=permit" --class "HelloObj" /home/iscas/Desktop/sparkapp/target/scala-2.12/simple-project_2.12-1.0.jar
   ```
   
   ![image-20211116234501116](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211116234501116.png)

# 用maven编译打包java程序

1. 创建应用程序目录`mkdir -p sparkapp2/src/main/java`和相应的Java程序

   `vim ./sparkapp2/src/main/java/SimpleApp.java`

   ```java
   import org.apache.spark.SparkConf;
   import org.apache.spark.api.java.*;
   import org.apache.spark.api.java.function.Function;
   
   
   public class SimpleApp {
       public static void main(String[] args) {
           String logFile = "file:///home/iscas/Downloads/sparkJDK16Bin/README.md"; // Should be some file on your system
           SparkConf conf = new SparkConf().setMaster("local")
                                           .setAppName("SimpleApp");
           JavaSparkContext sc = new JavaSparkContext(conf);
           JavaRDD<String> logData = sc.textFile(logFile).cache();
           long numAs = logData.filter(new Function<String, Boolean>() {
                       public Boolean call(String s) {
                           return s.contains("a");
                       }
                   }).count();
           long numBs = logData.filter(new Function<String, Boolean>() {
                       public Boolean call(String s) {
                           return s.contains("b");
                       }
                   }).count();
           System.out.println("Lines with a: " + numAs + ", lines with b: " +
               numBs);
       }
   }
   
   ```

2. 创建pom文件`vim ./sparkapp2/pom.xml`

   ```xml
   <project>
       <groupId>cn.edu.xmu</groupId>
       <artifactId>simple-project</artifactId>
       <modelVersion>4.0.0</modelVersion>
       <name>Simple Project</name>
       <packaging>jar</packaging>
       <version>1.0</version>
       <repositories>
           <repository>
               <id>jboss</id>
               <name>JBoss Repository</name>
               <url>http://repository.jboss.com/maven2/</url>
           </repository>
       </repositories>
       <dependencies>
           <dependency> <!-- Spark dependency -->
               <groupId>org.apache.spark</groupId>
               <artifactId>spark-core_2.11</artifactId>
               <version>2.4.0</version>
           </dependency>
       </dependencies>
       <build>
       <plugins>
           <plugin>
               <groupId>org.apache.maven.plugins</groupId>
               <artifactId>maven-compiler-plugin</artifactId>
               <configuration>
                   <source>1.8</source>
                   <target>1.8</target>
               </configuration>
           </plugin>
       </plugins>
   </build>
   </project>  
   ```

3. 检查整个应用程序的文件结构`cd sparkapp2`，`find`

   <img src="https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211117191936414.png" alt="image-20211117191936414" style="zoom:150%;" />

4. 打包`mvn package`

   得到jar文件的路径为`~/Desktop/sparkapp2/target/simple-project-1.0.jar`

5. 在spark上运行`./spark-submit --conf "spark.driver.extraJavaOptions=--illegal-access=permit"  --conf "spark.executor.extraJavaOptions=--illegal-access=permit" --class "SimpleApp" ~/Desktop/sparkapp2/target/simple-project-1.0.jar   `

   ![image-20211117193439210](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211117193439210.png)

# spark具体学习

创建一个list `val numList = List(1,2,3,4,5)`

将该list转为rdd并划分为5个partition

`val numRdd = sc.parallelize(numList,numList.length)`

对每个partition进行map操作

`val rs = numRdd.map(n=>{println("num "+n+"hello");Thread.sleep(n*2000);(n,n*100)})`

调用collect收集结果

`rs.collect().foreach(println)`

保存`:save Hello.session`

载入`:load Hello.session`

在spark-shell中执行后通过web查看`http://localhost:4040/`执行情况

将一个数组变为RDD并进行转换`sc.makeRDD(Array(1,2,3,4,5)).map(x=>x+1).collect`

缓存RDD `sc.makeRDD(Array(1,2,3,4,5)).map(x=>x+1).cache().collect()`

reduce也是常见的action操作，take也是一个常见的action操作，只不过它会触发多个job

# spark RDD 操作

通过file前缀指定读取本地文件

`val textFile = sc.textFile("file:///home/iscas/Downloads/sparkJDK16Bin/README.md")`

统计文本行数`textFile.count()`

统计包含"Spark"的行数`textFile.filter(line=>line.contains("Spark")).count()`

统计每个单词出现的次数

```
val wordCounts = textFile.flatMap(line=>line.split(" ")).map(word=>(word,1)).reduceByKey((a,b)=>a+b)
wordCounts.collect()
```

将numList转为RDD

![IMG_20211119_151733](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/IMG_20211119_151733.jpg)

![IMG_20211119_151745](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/IMG_20211119_151745.jpg)

# RDD编程

获取rdd的size `numRDD.count()`

## 创建RDD

### 使用parallelize/makeRDD创建RDD

makeRDD是通过parallelize实现的

`val numRDD=sc.parallelize(Array(1,2,3,4,5),2)`其中2表示分为2个partition，如果在执行action前array发生了变化，则numRDD为变化后的array转化得到的，解决方法为使得parallelize得到是不变的seq比如list

### 使用textFile创建RDD

使用textFile读取如HDFS，HBase或本地文本文件，读取后生成RDD[String]，每一个string对应文本文件一行数据

path参数中file:///表示本地文件，hdfs:://表示HDFS

`sc.textFile("file:///etc/hosts").collect.foreach(println)`

### 其它RDD创建操作

* wholeTextFiles

  读取指定路径下的多个文本文件，RDD中的记录是一个键值对（filename，content）

* sequenceFiles

  用来读取<Key,value>键值对文件并转为RDD

  生成sequenceFile `sc.makeRDD(Array((1001,"mike"),(1002,"tom"),(1003,"rose"))).saveAsSequenceFile("/home/iscas/Desktop/stu_sequence")`

  使用sequenceFiles读取<Key，value>文件 `sc.sequenceFile[Int,String]("/home/iscas/Desktop/stu_sequence").collect.foreach(println)`

## partition

### 基本操作

获取partition的数量`sc.makeRDD(Array(1,2,3,4)).getNumPartitions`，不指定partition数的话默认partition个数为cpu核的个数

打印partition中的内容

```scala
import org.apache.spark.{SparkConf, SparkContext}

object PrintPartition {

  def main(args: Array[String]): Unit = {
    val conf = new SparkConf()
    conf.setAppName("PrintPartition")
    val sc = new SparkContext(conf)
    val numRDD = sc.makeRDD(Array(1, 3, 3, 5, 7, 9))
    val data = numRDD.mapPartitionsWithIndex((id, iter) => {
      import scala.collection.mutable.ArrayBuffer
      val ar = new ArrayBuffer[(Int, Int)]()
      while (iter.hasNext) {
        ar += ((id, iter.next()))
      }
      ar.iterator
    })

    data.collect().foreach(println)
    sc.stop()
  }
}

```

一个partition如（1,3,3）传入map(n=>n+1)，实质是依次传入一个个参数，总共运行map中的匿名函数三次，如果想要整个partition作为参数传递则使用mapPartitions

### partition个数计算

这里主要是指 **textFile** 生成的RDD的partition个数计算

textFile函数有一个参数为minPartitions，只是决定最终partition个数的一个因素。minPartitions可以指定，如果不指定，则由math.min(spark.default.parallelism,2)决定，如果spark.default.parallelism的值没有指定

1）如果是local模式，spark.default.parallelism的值等于本机所有cores的数量

2）如果是细粒度模式（Mesos fine grained model），则它的值为8

3）如果是其他，则等于已注册的executor的cores的和

**partition划分的总原则：** 最后partition的size不能超过HDFS的Block的size，如果根据minPartitions计算出来的partition的大小小于Block的大小，则采用minPartitions的分区方案，否则采用Block的分区方案

**partition数量的计算规则：** textFile返回的RDD的partitions的数量由split的数量决定，split的划分规则为（不同的文件属于不同的split；单个文件按照下面的式子划分split long splitSize=Math.min(goalSize,blockSize)其中blockSize为HDFS的Block大小，goalSize=文件大小/minPartitions；最后一块split可以溢出10%）

**partition数计算公式：** 当确定了splitSize后，partition数=(((10*文件大小+splitSize-1)/splitSize-1)+9)/10

### partition在textFile中注意

* partition的划分是根据splits来的
* partition与task是一对一的关系，一个partition就一定会启动一个task即使这个task上没有输入数据
* task执行时，具体传入的参数是一个一个的整行，从partition的第一个字节开始扫描，如果扫描到一行的开始，则将此行作为rdd的一个元素，如果partition没有结束，则继续扫描，执行相同的逻辑，直到partition结束，最后将扫描得到的元素组成一个新的partition用于此次task的传参
* partition的划分不能太细，否则会造成空任务
* 如果某行数据特别大，处理时，这行的数据会被送往一个task处理，造成该task负载较重

## Transformation操作

### map

* map case使用（数据清洗）

  ```scala
  val numRDD = sc.makeRDD(Array((5,"tom"),(6,"ke"),(100)))
  numRDD.map(n=>{
      n match {
          case (id,name)=>(id,name)
          case _ =>(0,"error")
      }
  }).collect().foreach(println)
  ```

  进一步简化为`numRDD.map{case (id,name)=>(id,name);case _ =>(0,"error")}.collect().foreach(println)`

* map打标记用于计数

  ```scala
  val numRDD = sc.makeRDD(Array("hello","to","context","hello"))
  numRDD.map(n=>(n,1)).reduceByKey((p,v)=>p+v).collect().foreach(println)
  ```

* map打标记用于分类

  ```scala
  val numRDD = sc.makeRDD(Array("hello","to","context","he","cd"))
  val countRDD = numRDD.map(s=>(s(0),s)).groupByKey()
  countRDD.collect().foreach(x=>println(x._1,x._2.mkString(":")))
  ```

  新建一个Iterator[String]并将其拼接在一起`println(Iterator("Baidu", "Google", "Runoob", "Taobao").mkString(":"))`

### flatMap

flatMap将RDD每个元素传入f函数处理，f会返回0个或多个新元素，最后所有新元素组成新的RDD

### mapPartitions

将整个partition直接传入匿名处理函数（输入是一个迭代器，输出也是迭代器），每个task只需调用匿名函数一次

```scala
sc.makeRDD(Array(1,3,3,5,7,9),2).mapPartitions(partitionIter=>{
      val str = partitionIter.mkString
      println("str"+str)
      val newStr = str.filter(c=>c!='3'&&c!='5')
      newStr.iterator
    }).collect().foreach(println)
```

一般需要newStr类似的来存储数据，如果partition较大的话，这样就比较占空间，使用迭代器来优化

```scala
class NewIter(iter:Iterator[Int]) extends Iterator[Option[Char]] {
  def hasNext:Boolean = {iter.hasNext}
  def next={
    val c =iter.next()
    if((c!=3)&&(c!=5)) Option((c+48).toChar) else None
   }
}
```

```scala
sc.makeRDD(Array(1,3,3,5,7,9),2).
      mapPartitions(partitionIter=>new NewIter((partitionIter)).
        filter(_.isDefined)).collect.foreach(c=>println(c.get))
```

### join

join用于两个<key,value>键值对型RDD间的连接操作，就像natural join一样，key相同，两个RDD的value组成一个元组(value1,value2)

```scala
val thisRDD = sc.makeRDD(Array(("A",1),("A",3),("B",4)))
val otherRDD = sc.makeRDD(Array(("A",4),("A",5),("B",10)))
thisRDD.join(otherRDD).collect.foreach(println)
```

输出结果

```
(B,(4,10))
(A,(1,4))
(A,(1,5))
(A,(3,4))
(A,(3,5))
```

优化1：join前预处理，减少参与join计算的数据

（1）去除两个RDD都不包含的key

```scala
val thisRDD = sc.makeRDD(Array(("A",1),("A",3),("B",4),("C",2)))
val otherRDD = sc.makeRDD(Array(("A",4),("A",5),("B",10)))
val keys = thisRDD.keys.intersection(otherRDD.keys).collect()
val newThisRDD = thisRDD.filter(e=>keys.contains(e._1))
val newoOtherRDD = otherRDD.filter(e=>keys.contains(e._1))
newThisRDD.join(newoOtherRDD).collect.foreach(println)
```

（2）partitionBy重新分区，要求两个RDD的Partitioner相同且具有相同的partition数，这样两个RDD相同的Key基本在同一个分区中，shuffle操作为0

```scala
val thisRDD = sc.makeRDD(Array(("A",1),("A",3),("B",4),("C",2))).partitionBy(new HashPartitioner((3))).cache()
val otherRDD = sc.makeRDD(Array(("A",4),("A",5),("B",10))).partitionBy(new HashPartitioner((3))).cache()
println(thisRDD.count())
println(otherRDD.count())

thisRDD.join(otherRDD).collect.foreach(println)
```

### union

简单合并两个rdd集合不去重，不会导致shuffle操作

```
RDD1.union(RDD2)
```

### intersection

返回两个rdd的交集并去重

```
RDD1.intersection(RDD2)
```

使用partitionBy优化

```scala
val RDD1 = sc.makeRDD(Array(1,3,3,5,7)).map(n=>(n,1)).partitionBy(new HashPartitioner(3)).cache
val RDD2 = sc.makeRDD(Array(2,4,5,3,5)).map(n=>(n,1)).partitionBy(new HashPartitioner(3)).cache
RDD1.count()
RDD2.count()
RDD1.join(RDD2).keys.distinct().collect().foreach(println)
```

### groupBy

groupBy(f)其中f匿名函数的返回值相同的分为一组<key,iterator>，有shuffle开销

划分奇偶数

```scala
sc.makeRDD(Array(1,3,2,6,7,10)).groupBy(n=>n%2).collect().foreach(n=>println(n._1+":"+n._2.mkString("!")))
```

### groupByKey

用于对RDD中<key,value>键值对进行分组，必须在内存中保存<key,valueList>，如果分组的目的是对同组元素操作如求和则建议使用reduceByKey或aggregateByKey，有shuffle开销，如果rdd一开始分好区并cache，后续groupByKey是没有shuffle开销

```scala
sc.makeRDD(Array(("A",1),("A",3),("B",2),("B",4),("C",6),("B",6))).groupByKey().collect().foreach(n=>println(n._1+":"+n._2.mkString("!")))
```

### reduceByKey

对rdd中<key,value>key值相同的元素作合并处理，但不能改变归并后的数据类型

```
sc.makeRDD(Array(("A",1),("A",3),("B",2),("B",4),("C",6),("B",6))).reduceByKey((pre,cur)=>pre+cur).collect().foreach(println)
```

结果

```
(B,12)
(A,4)
(C,6)
```

reduceByKey会在partition内部对相同key对应元素进行func调用，内部归并完成后，相同的key会被shuffle到同一个partition，然后继续归并，直到该key的所有元素都被归并完毕，这样不需要shuffle RDD中的所有元素

### aggregateByKey

如果归并后的结果类型和RDD元素类型不同时使用aggregateByKey

```scala
sc.makeRDD(Array(("A",1),("A",3),("B",2),("B",4),("C",6),("B",6))).aggregateByKey("")((rs,e)=>rs+ " "+e,(pre,cur)=>pre+" "+cur).collect().foreach(println)
```

结果

```
(B, 2 4 6)
(A, 1 3)
(C, 6)
```

aggregateByKey中的第一个参数("")表示初始值（这里指字符串拼接的初始值），(rs,e)=>rs+ " "+e这部分表示的是在partition内部实现的操作（在每个partition内部将相同key对应的元素通过" "拼接起来），(pre,cur)=>pre+" "+cur表示每个partition之间采取的操作

### cogroup

cogroup以key为依据合并多个<key,value>键值对类型的RDD，然后组成(key,(Iter[w1],iter[w2]))

```scala
val thisRDD=sc.makeRDD(Array(("A",1),("A",3),("B",2),("B",4),("C",6),("B",6)))
val otherRDD=sc.makeRDD(Array(("A","hello"),("A","world"),("B","glad")))
thisRDD.cogroup(otherRDD).collect().foreach(n=>println(n._1+":"+n._2._1.mkString(" ")+"||"+n._2._2.mkString(" ")))

```

结果

```
B:2 4 6||glad
A:1 3||hello world
C:6||
```

## Action

### collect

### reduce

用于rdd元素归并

```scala
println(sc.makeRDD(Array(1,3,3,5,7)).reduce((pre,cur)=>pre+cur))
```

### fold

fold用于将rdd归并，它加了一个zero value来赋初始值，zero value在每个partition内部计算时都会用上，内部计算完毕后，计算各partition总的结果时，还会用到zero value作为初始值

```
val numRDD = sc.makeRDD(Array(1,3,3,5,7),3)
println(numRDD.getNumPartitions)
println(numRDD.fold(10)((pre,cur)=>pre+cur))
```

结果

```
3
59
```

### aggregate

用于rdd元素的归并处理，aggregate归并后的结果类型可以和rdd元素类型不一样

```scala
println(sc.makeRDD(Array(1,3,3,5,7)).aggregate("hello")((pre,cur)=>pre+" "+cur, rs,e)=>rs+" "+e))
```

```
hello hello 1 3 3 5 7
```

### foreachPartition

用于遍历和处理rdd中的每个元素

```
val numRDD=sc.makeRDD(Array(1,3,3,5,7),2)
numRDD.foreachPartition(iter=>println(iter.mkString(" ")))
```

```
1 3
3 5 7
```

### saveAsTextFile

可以将rdd存储为指定目录下的文本文件

path要指定为hdfs上的路径，如果存储到本地，则每个partition会输出到task所在的executor上，不会在driver端

```scala
val numRDD=sc.makeRDD(Array(1,3,3,5,7),2) numRDD.saveAsTextFile("/home/iscas/Desktop/he")
```

生成part-编号 文件，每个文件对应一个partition的内容，如果partition的内容为空，也会输出空文件，RDD中的元素会转为string，每个元素占一行

### saveAsObjectFile

可以将rdd存储为一个SequenceFile

```
RDD.saveAsObjectFile("path")
```

读取SequenceFile，转为rdd

```
sc.objectFile[Int]("path/").glom.collect
```

glom可以将partition转为一个Array

## checkpoint

checkpoint可以将RDD序列化为文件存储到HDFS中，当使用此RDD时，可以从HDFS中读取回复，而不需要重新计算

```scala
sc.setCheckpointDir("/home/iscas/Desktop/check")
val numRDD=sc.makeRDD(Array(1,3,3,5,7))
numRDD.checkpoint()
numRDD.collect().foreach(println)
numRDD.collect().foreach(println)
```

## RDD存储方式

可以调用persist指定其他存储方式，由numRDD.persist(StorageLevel.xxxx),xxxx可取DISK_ONLY,MEMORY_ONLY,MEMORY_AND_DISK等，如果后续不再使用，可以调用unpersist来释放资源
