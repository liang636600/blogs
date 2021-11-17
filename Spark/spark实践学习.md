# **启动spark：**

在bin目录下，运行

```
./spark-shell --conf "spark.driver.extraJavaOptions=--illegal-access=permit"  --conf "spark.executor.extraJavaOptions=--illegal-access=permit"
```

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

