# 1 下载源码

使用hbase版本2.4.14稳定版

![image-20221025193446193](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20221025193446193.png)

下载链接https://hbase.apache.org/downloads.html

# 2 编译hbase

在hbase源码的主目录下，运行命令`mvn package -DskipTests`

* 报错1：Failed to execute goal org.apache.maven.plugins:maven-enforcer-plugin:3.0.0-M3:enforce (hadoop3-profile-required) on project hbase: Some Enforcer rules have failed. Look above for specific messages explaining why the rule failed. -> [Help 1]

  ![image-20221025201622214](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20221025201622214.png)

  * 失败 尝试1：修改pom文件部分内容

    ```xml
     <plugin>
              <groupId>org.apache.maven.plugins</groupId>
              <artifactId>maven-compiler-plugin</artifactId>
              <version>${maven.compiler.version}</version>
              <configuration>
                <source>${compileSource}</source>
                <target>${compileSource}</target>
                <showWarnings>true</showWarnings>
                <showDeprecation>false</showDeprecation>
                <!-- <compilerArgument>-Xlint:-options</compilerArgument> -->
                <compilerArgs>
                  <arg>--add-exports=java.base/jdk.internal.access=ALL-UNNAMED</arg>
                  <arg>--add-exports=java.base/jdk.internal=ALL-UNNAMED</arg>
                  <arg>--add-exports=java.base/jdk.internal.misc=ALL-UNNAMED</arg>
                  <arg>--add-exports=java.base/sun.security.pkcs=ALL-UNNAMED</arg>
                  <arg>--add-exports=java.base/sun.nio.ch=ALL-UNNAMED</arg>
                </compilerArgs>
              </configuration>
            </plugin>
    ```

    重新运行编译命令`mvn clean package -DskipTests`

  * **解决** 尝试2：运行命令`mvn clean package -DskipTests -Denforcer.skip=true`

编译成功

![image-20221025211257981](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20221025211257981.png)

## jdk16编译hbase2.3.0源码

编译成功

![image-20221108144708829](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20221108144708829.png)

### jdk8运行

* 报错`ERROR master.HMaster: Failed to become active master
  java.lang.IncompatibleClassChangeError: Found interface org.apache.hadoop.hdfs.protocol.HdfsFileStatus, but class was expected`

### jdk16运行

* 报错与jdk8一样`ERROR master.HMaster: Failed to become active master
  java.lang.IncompatibleClassChangeError: Found interface org.apache.hadoop.hdfs.protocol.HdfsFileStatus, but class was expected`

  * 尝试1：修改`hbase-2.2.4/dev-support/hbase-personality.sh`文件中` hbase_hadoop3_versions`为对应的版本

    ![image-20221108151748169](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20221108151748169.png)

    修改`hbase-2.2.4/pom.xml`文件中`<hadoop-three.version>`为系统的hadoop版本

    ![image-20221108152311388](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20221108152311388.png)

    重新在jdk16环境下编译`mvn clean package -DskipTests -Denforcer.skip=true -Dhadoop.profile=3.0 -Dhadoop-three.version=3.3.1`

    ![image-20221108153741872](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20221108153741872.png)

    在运行hbase shell的时候terminal界面报了`error,connection closed`，但打开日志里面，最开始没有error的信息，然后出现master exit的信息

## jdk8编译hbase2.3.0源码



# 3 简单测试

先运行`start-hbase.sh`

`./bin/hbase shell`

![image-20221025212505789](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20221025212505789.png)

`create 'test', 'cf'`

* 报错1：ERROR: KeeperErrorCode = ConnectionLoss for /hbase/master

  该错误与是否自己编译hbase 还是 用官方提供的bin 无关

  尝试了jdk11，也是同样的错

  打开log日志，里面出现的是不一样的错误

  ```
  regionserver.HRegionServer: Failed construction RegionServer
  java.lang.NumberFormatException: For input string: "30s"
  ```

  * 尝试1：注释掉hadoop文件夹下`hdfs-site.xml`中的30s所在的property两处 以及`core-site.xml`中的30s一处

    * 报错1.1

      ```
      ERROR master.HMaster: Failed to become active master
      java.net.ConnectException: Call From iscas-Precision-3551/127.0.1.1 to iscas-Precision-3551:9001 failed on connection exception: java.net.ConnectException: Connection refused; For more details see:  http://wiki.apache.org/hadoop/ConnectionRefused
      ```

      * 未解决：尝试1 for 报错1.1：

        ![image-20221028213222969](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20221028213222969.png)

        我的hbase下的`hbase-site.xml`中没有property `hbase.rootdir`，在该文件中添加一个property

      * 解决：尝试2 for 报错1.1：

        在启动hbase之前，在hadoop的sbin文件夹下启动`./start-all.sh`（一定要主要hadoop和hbase版本之间的匹配问题，不然可能报方法找不到的错误）

先启动hadoop后可以解决报错1

* 报错2：`ERROR: org.apache.hadoop.hbase.ipc.ServerNotRunningYetException: Server is not running yet`

  * **解决：**尝试1 for 报错2：修改`hbase-site.xml`文件

    ```
    <property>
      <name>hbase.wal.provider</name>
      <value>filesystem</value>
    </property>
    ```

成功解决报错

插入数据

```
put 'test', 'row1', 'cf:a', 'value1'
put 'test', 'row2', 'cf:b', 'value2'
put 'test', 'row3', 'cf:c', 'value3'
```

查看表

`scan 'test'`

获得一行数据

`get 'test', 'row1'`
