在Cassandra中创建一张表

```
cqlsh> create keyspace ycsb WITH REPLICATION = {'class' : 'SimpleStrategy', 'replication_factor': 3 };
cqlsh> USE ycsb;
cqlsh> create table usertable (
    y_id varchar primary key,
    field0 varchar,
    field1 varchar,
    field2 varchar,
    field3 varchar,
    field4 varchar,
    field5 varchar,
    field6 varchar,
    field7 varchar,
    field8 varchar,
    field9 varchar);
```

先下载

```
curl -O --location https://github.com/brianfrankcooper/YCSB/releases/download/0.17.0/ycsb-0.17.0.tar.gz
```

解压后进入主目录

运行YCSB

```
bin/ycsb.sh load basic -P workloads/workloada
bin/ycsb.sh run basic -P workloads/workloada
```

![image-20220627100138759](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20220627100138759.png)

* 尝试JDK11编译Cassandra JDK16运行

  ![image-20220627100431244](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20220627100431244.png)

* 尝试JDK14编译Cassandra然后jdk16运行

  在jdk16环境中执行命令`./cassandra -R`报错

  ```
  Exception (java.lang.AssertionError) encountered during startup: java.lang.reflect.InaccessibleObjectException: Unable to make field private int java.io.FileDescriptor.fd accessible: module java.base does not "opens java.io" to unnamed module @32b260fa
  java.lang.AssertionError: java.lang.reflect.InaccessibleObjectException: Unable to make field private int java.io.FileDescriptor.fd accessible: module java.base does not "opens java.io" to unnamed module @32b260fa
  	at org.apache.cassandra.utils.FBUtilities.getProtectedField(FBUtilities.java:672)
  	at org.apache.cassandra.utils.NativeLibrary.<clinit>(NativeLibrary.java:81)
  	at org.apache.cassandra.service.CassandraDaemon.setup(CassandraDaemon.java:198)
  	at org.apache.cassandra.service.CassandraDaemon.activate(CassandraDaemon.java:620)
  	at org.apache.cassandra.service.CassandraDaemon.main(CassandraDaemon.java:732)
  Caused by: java.lang.reflect.InaccessibleObjectException: Unable to make field private int java.io.FileDescriptor.fd accessible: module java.base does not "opens java.io" to unnamed module @32b260fa
  	at java.base/java.lang.reflect.AccessibleObject.checkCanSetAccessible(AccessibleObject.java:357)
  	at java.base/java.lang.reflect.AccessibleObject.checkCanSetAccessible(AccessibleObject.java:297)
  	at java.base/java.lang.reflect.Field.checkCanSetAccessible(Field.java:177)
  	at java.base/java.lang.reflect.Field.setAccessible(Field.java:171)
  	at org.apache.cassandra.utils.FBUtilities.getProtectedField(FBUtilities.java:667)
  	... 4 more
  ERROR [main] 2022-07-03 01:21:48,848 CassandraDaemon.java:754 - Exception encountered during startup
  java.lang.AssertionError: java.lang.reflect.InaccessibleObjectException: Unable to make field private int java.io.FileDescriptor.fd accessible: module java.base does not "opens java.io" to unnamed module @32b260fa
  	at org.apache.cassandra.utils.FBUtilities.getProtectedField(FBUtilities.java:672)
  	at org.apache.cassandra.utils.NativeLibrary.<clinit>(NativeLibrary.java:81)
  	at org.apache.cassandra.service.CassandraDaemon.setup(CassandraDaemon.java:198)
  	at org.apache.cassandra.service.CassandraDaemon.activate(CassandraDaemon.java:620)
  	at org.apache.cassandra.service.CassandraDaemon.main(CassandraDaemon.java:732)
  Caused by: java.lang.reflect.InaccessibleObjectException: Unable to make field private int java.io.FileDescriptor.fd accessible: module java.base does not "opens java.io" to unnamed module @32b260fa
  	at java.base/java.lang.reflect.AccessibleObject.checkCanSetAccessible(AccessibleObject.java:357)
  	at java.base/java.lang.reflect.AccessibleObject.checkCanSetAccessible(AccessibleObject.java:297)
  	at java.base/java.lang.reflect.Field.checkCanSetAccessible(Field.java:177)
  	at java.base/java.lang.reflect.Field.setAccessible(Field.java:171)
  	at org.apache.cassandra.utils.FBUtilities.getProtectedField(FBUtilities.java:667)
  	... 4 common frames omitted
  ```

  * 解决：尝试在`cassandra-env.sh`文件末尾添加JVM_OPTS参数

    ````
    JVM_OPTS="$JVM_OPTS --illegal-access=permit"
    ````

  成功运行

  ![image-20220703165317622](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20220703165317622.png)

  ![image-20220703165347637](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20220703165347637.png)


---

Cassandra的heap size在`cassandra-env.sh`中设置（与JVM相关的参数都可以在该文件中设置）

* 修改workload的recordcount

  * 方法1：

    创建一个文件large.dat里面一行内容recordcount=100000000

    ```
    ./bin/ycsb load basic -P workloads/workloada -P large.dat
    ```

  * 方法2：

    ```
    ./bin/ycsb load basic -P workloads/workloada -p recordcount=100000000
    ```

* 保存状态到文件中去

  ```
  ./bin/ycsb load basic -P workloads/workloada -P large.dat -s > load.dat
  ```

  


