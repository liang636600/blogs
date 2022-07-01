# 1 配置好Java

# 2 Ant的安装与配置

前往Ant官网https://ant.apache.org/，选择Ant安装包进行下载

![在这里插入图片描述](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/20191109154052953.png)

解压，然后配置环境变量

```
sudo vim /etc/profile  
```

在其中输入

```
export ANT_HOME=/opt/apache-ant-1.10.12
export PATH=$JAVA_HOME/bin:$ANT_HOME/bin:$PATH
```

检查是否安装成功

```
ant -version
```

![image-20220623145802092](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20220623145802092.png)

# 3 Cassandra的安装与配置

下载源码安装包<http://archive.apache.org/dist/cassandra/>,下载apache-cassandra-4.0-src.tar.gz安装包

![image-20220623150021203](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20220623150021203.png)

解压，然后进入Cassandra主目录下输入`ant`进行编译

---

报错

![image-20220623150504080](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20220623150504080.png)

```
Java 15 has removed Nashorn, you must provide an engine for running JavaScript yourself. GraalVM JavaScript currently is the preferred option.

BUILD FAILED
/home/iscas/Downloads/apache-cassandra-4.0-alpha4-src/build.xml:148: Unable to create javax script engine for javascript
```

* 尝试GraalVM JavaScript（不行）

  下载相关的包

  graal-sdk-21.0.0.jar https://mvnrepository.com/artifact/org.graalvm.sdk/graal-sdk/21.1.0

  truffle-api-21.0.0.jar  https://mvnrepository.com/artifact/org.graalvm.truffle/truffle-api/21.1.0

  compiler-21.0.0.jar https://mvnrepository.com/artifact/org.graalvm.compiler/compiler

  compiler-management-21.0.0.jar https://mvnrepository.com/artifact/org.graalvm.compiler/compiler-management

  launcher-common-21.0.0.jar  https://mvnrepository.com/artifact/org.graalvm/launcher-common 

  js-launcher-21.0.0.jar https://mvnrepository.com/artifact/org.graalvm.js/js-launcher

  js-21.0.0.jar https://mvnrepository.com/artifact/org.graalvm.js/js

  js-scriptengine https://mvnrepository.com/artifact/org.graalvm.js/js-scriptengine

  regex-21.0.0.jar  https://mvnrepository.com/artifact/org.graalvm.regex/regex

  icu4j-67.1.jar https://mvnrepository.com/artifact/com.ibm.icu/icu4j

  ```
  $JDK/bin/java -XX:+UnlockExperimentalVMOptions -XX:+EnableJVMCI -XX:+UseJVMCICompiler --module-path=$JAVA_HOME/graal-sdk-21.1.0.jar:$JAVA_HOME/truffle-api-21.1.0.jar --upgrade-module-path=$JAVA_HOME/compiler-21.1.0.jar:$JAVA_HOME/compiler-management-21.1.0.jar -cp $JAVA_HOME/launcher-common-1.0.0-rc7.jar:$JAVA_HOME/js-launcher-21.3.1.jar:$JAVA_HOME/js-21.1.0.jar:$JAVA_HOME/truffle-api-21.1.0.jar:$JAVA_HOME/graal-sdk-21.1.0.jar:$JARS/js-scriptengine-21.1.0.jar:$JAVA_HOME/regex-21.1.0.jar:$JAVA_HOME/icu4j-67.1.jar com.oracle.truffle.js.shell.JSLauncher
  ```

  

---

## JDK版本换为11编译

报错

```
-Duse.jdk11=true or $CASSANDRA_USE_JDK11=true must be set when building from java 11
```

* 解决：在命令行中尝试`ant -Duse.jdk11=true`

  ![image-20220626111242738](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20220626111242738.png)

## JDK版本换为14编译



# 4 启动运行与退出运行

进入Cassandra主目录下的bin文件夹，然后输入`./cassandra -R`

没有什么报错ERROR，看到最后输出的为Node/x.x.x.x state jump to NORMAL，就表示Cassandra安装完成了

![image-20220626112303798](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20220626112303798.png)

可以通过查看集群信息进行确认`./nodetool status `。UN表示的是该服务器的状态，UN是运行中，DN是宕机

![image-20220626112427198](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20220626112427198.png)

退出Cassandra（结束后台运行）

首先进入到Cassandra的bin目录下，输入

```java
ps -ef |grep cassandra
```

查询到该进程的pid，然后kill：

```java
sudo kill pid
```

这里pid替换成实际的pid即可

# 5 CQHSH

在Cassandra的bin目录下输入`./cqlsh localhost`报错

```
No appropriate Python interpreter found.
```

* 解决：尝试安装Python2.7

  ```
  sudo apt install python2.7
  ```

在Cassandra的bin目录下输入`./cqlsh localhost`，然后输入`SELECT cluster_name, listen_address FROM system.local;`，出现如下结果成功

![image-20220626120100538](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20220626120100538.png)

