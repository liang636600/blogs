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

* 修改GC的种类

  修改在conf文件夹下的jvm11-server.options中的GC种类`-XX:UseZGC`

  可以在Cassandra启动的时候看到如下信息，说明更改GC成功

  ![image-20220710201914166](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20220710201914166.png)

* 修改heap-size的大小

  修改conf文件夹下的cassandra-env.sh文件，MAX_HEAP_SIZE是分给java heap总的内存空间，HEAP_NEWSIZE是分给young generation的内存空间，两个参数要么一起设置，要么不设置

  ```
  The main trade-off for the young generation is that the larger it is,the longer GC pause times will be.The shorter it is,the more expensive GC will be (usually).
  The example HEAP_NEWSIZE assumes a modern 8-core+machine for decent pause times.If in doubt,and if you do not particularly want to tweak,go with 100 MB per phystcal CPU core.
  ```

  HEAP_NEWSIZE取(CPU核数的100倍，¼ of MAX_HEAP_SIZE)两个值中的较小值

  Cassandra默认的heap-size的大小应该是7.750GB，如下图所示

  ![image-20220710205727129](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20220710205727129.png)

  * 尝试修改参数`MAX_HEAP_SIZE="4G"`与`HEAP_NEWSIZE="1200M"`

    如下图所示，参数修改成功

    ![image-20220710211502457](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20220710211502457.png)

