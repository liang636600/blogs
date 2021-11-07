# Ubuntu编译flink源码

## 一 官网下载flink源码

官网链接：https://flink.apache.org/downloads.html

## 二 解压文件并编译

在flink源码主目录下运行`mvn clean install -DskipTests`(前提是安装好了maven)，同时注意查看自己的maven版本，官方提示maven版本3.3.x需要进入flink-dist再次运行`mvn clean install`

注：以后运行`mvn clean install -DskipTests -Dcheckstyle.skip`

![image-20211106113314523](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211106113314523.png)

---

在编译过程中碰到

`Failed to execute goal com.github.siom79.japicmp:japicmp-maven-plugin:0.11.0:cmp (default) on project flink-core: Execution default of goal com.github.siom79.japicmp:japicmp-maven-plugin:0.11.0:cmp failed: A required class was missing while executing com.github.siom79.japicmp:japicmp-maven-plugin:0.11.0:cmp: javax/xml/bind/JAXBException`

![image-20211106120711755](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211106120711755.png)

* 失败：尝试修改flink主目录下的pom文件为

  

  ![image-20211106142828182](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211106142828182.png)

  后来发现在flink的pom文件中存在上述配置

* 失败：尝试添加--add-modules java.xml.bind

  在pom.xml的build的plugin中添加

  ![image-20211107111207117](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211107111207117.png)

发现not allowed

![image-20211107111351557](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211107111351557.png)

* 尝试在出错的模块flink-matrix-core里（pom文件）修改japicmp的依赖

  `<build>
  <plugins>
  <!--  activate API compatibility checks  -->
  <plugin>
  <groupId>com.github.siom79.japicmp</groupId>
  <artifactId>japicmp-maven-plugin</artifactId>
  <dependencies>
  <dependency>
  <groupId>javax.xml.bind</groupId>
  <artifactId>jaxb-api</artifactId>
  <version>2.3.0</version>
  </dependency>
  <dependency>
  <groupId>com.sun.xml.bind</groupId>
  <artifactId>jaxb-impl</artifactId>
  <version>2.3.0</version>
  </dependency>
  <dependency>
  <groupId>com.sun.xml.bind</groupId>
  <artifactId>jaxb-core</artifactId>
  <version>2.3.0</version>
  </dependency>
  <dependency>
  <groupId>javax.activation</groupId>
  <artifactId>activation</artifactId>
  <version>1.2.0</version>
  </dependency>
  </dependencies>
  </plugin>
  <plugin>
  <groupId>org.apache.maven.plugins</groupId>
  <artifactId>maven-jar-plugin</artifactId>
  <executions>
  <execution>
  <goals>
  <goal>test-jar</goal>
  </goals>
  </execution>
  </executions>
  </plugin>
  </plugins>
  </build>`
  
  ![image-20211107113028758](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211107113028758.png)
  
  报错显示javax.activation:activation:jar:1.2.0 这个版本的包在maven找不到
  
  ![image-20211107113257577](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211107113257577.png)
  
  修改javax.activation:activation版本为1.1.1，报错
  
  ![image-20211107113639758](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211107113639758.png)
  
  配置MAVEN_OPTS的参数值`export MAVEN_OPTS="--illegal-access=permit"`,参数配置生效
  
  ![image-20211107114833515](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211107114833515.png)
  
  flink-matrix-core编译成功，但出现新的问题，flink-test-utils-junit模块编译出错
  
  ![image-20211107114903456](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211107114903456.png)

---

### 尝试解决flink-test-utils-junit模块编译出错

* 找到对应的文件查看源码

  ![image-20211107145337279](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211107145337279.png)

  据官网jdk9后该方法被遗弃

  ![image-20211107145430455](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211107145430455.png)

  尝试修改源码：把sun改为jdk.internal

  ![image-20211107161456097](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211107161456097.png)

  报错

  ![image-20211107160738606](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211107160738606.png)

  通过运行mvn命令时，在后面加上`-Dcheckstyle.skip`解决

  该模块编译成功

  

* 失败：尝试修改flink-test-utils-junit模块下的pom文件

  ![image-20211107152945004](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211107152945004.png)

  加上参数`--add-exports=java.base/sun.misc=ALL-UNNAMED`，出错
  
  ![image-20211107153120350](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211107153120350.png)
  
  说明参数配置不正确

---

  ### 尝试解决flink-core模块出错

`java.lang.ExceptionInInitializerError: com.sun.tools.javac.code.TypeTags`

![image-20211107162009293](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211107162009293.png)

* 尝试修改flink-core中lombok的版本为`1.18.4`

  ![image-20211107162636127](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211107162636127.png)

  成功
---

### 尝试解决flink-hadoop-fs模块错误

`Failed to execute goal on project flink-hadoop-fs: Could not resolve dependencies for project org.apache.flink:flink-hadoop-fs:jar:1.9.3: Could not find artifact jdk.tools:jdk.tools:jar:1.6 at specified path /home/iscas/Downloads/openjdk-16_linux-x64_bin/jdk-16/../lib/tools.jar`

![image-20211107165522534](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211107165522534.png)

* 尝试在主目录的pom文件中添加

  	<dependency>
  			<groupId>jdk.tools</groupId>
  			<artifactId>jdk.tools</artifactId>
  			<version>1.7</version>
  			<scope>system</scope>
  			<systemPath>${JAVA_HOME}/lib/tools.jar</systemPath>
  	</dependency>
  失败，目前发现是自己的jdk的lib下没有tools.jar，据说jdk8过后移出了，尝试将jdk8的tools.jar文件移到jdk16中去，成功

---

### 尝试解决flink-runtime模块的错

`[ERROR] /home/iscas/Downloads/flink-1.9.3-src/flink-1.9.3/flink-runtime/src/test/java/org/apache/flink/runtime/util/SerializedThrowableTest.java:[97,60] cannot find symbol
[ERROR]   symbol:   method defineClass(java.lang.String,byte[],int,int,java.lang.ClassLoader,java.security.ProtectionDomain)
[ERROR]   location: variable UNSAFE of type sun.misc.Unsafe`这个错误前面出现过，原因是`sun.misc.Unsafe`模块里面没有defineClass方法，打开源码发现`org.apache.flink.core.memory.MemoryUtils`里面用了sun.misc.Unsafe，修改MemoryUtils文件，将里面的`sun.misc`改为`jdk.internal.misc`

![image-20211107190027659](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211107190027659.png)

遇到报错

![image-20211107190705067](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211107190705067.png)

![image-20211107190808595](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211107190808595.png)

![image-20211107193139103](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211107193139103.png)

![image-20211107194458398](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211107194458398.png)

同理修改sun为jdk.internal

---

最后终于完成

![image-20211107203301308](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211107203301308.png)









