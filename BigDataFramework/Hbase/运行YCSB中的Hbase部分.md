在YCSB项目中，有两个hbase相关的目录，这里尝试的是hbase(2.y)目录

# 1 启动hbase server

# 2 Set up YCSB

# 3 创建一张hbase表

```
hbase(main):001:0> n_splits = 10 # HBase recommends (10 * number of regionservers)
hbase(main):002:0> create 'usertable', 'family', {SPLITS => (1..n_splits).map {|i| "user#{1000+i*(9999-1000)/n_splits}"}}
```

在运行create那行命令的时候出错

* 报错1：ERROR: KeeperErrorCode = ConnectionLoss for /hbase/master

  在log日志中的错误是`ERROR master.HMaster: Failed to become active master
  org.apache.hadoop.hbase.DroppedSnapshotException: region: master:store,,1.1595e783b53d99cd5eef43b6debb2682.`

  ```
  Caused by: java.lang.NoSuchMethodError: 'org.apache.hadoop.hdfs.DFSInputStream$ReadStatistics org.apache.hadoop.hdfs.client.HdfsDataInputStream.getReadStatistics()'
  ```

  之后发现运行`status`这种命令也报的是同样的错，说明hbase的环境出了问题（后来认为是hadoop与hbase环境之间不匹配的问题，hbase要使用hadoop以前存在的方法）

  * 尝试1 for 1：重新编译hbase,添加hadoop3.0即-Dhadoop.profile=3.0
  
    `mvn clean install -Denforcer.skip -DskipTests -Dhadoop.profile=3.0 -Psite-install-step`
  
    编译报错
  
    ![image-20221031114812677](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20221031114812677.png)
  
    重新又运行了一次，编译成功了
  
    ![image-20221031210751217](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20221031210751217.png)
  
    直接测试一下`hbase shell`里的status命令，发现还是同样的问题
    
    但报错终于不同了
    
    * 报错1.1：`ERROR master.HMaster: Failed to become active master
      java.lang.NoSuchMethodError: 'org.apache.hadoop.hdfs.protocol.DatanodeInfo[] org.apache.hadoop.hdfs.protocol.LocatedBlock.getLocations()'`
      
      * 失败：尝试1 for 错误1.1：把低版本的hadoop中的该方法拷到高版本中
      
        `ERROR master.HMaster: Failed to become active master
        org.apache.hadoop.ipc.RemoteException(java.lang.NoSuchMethodError): 'boolean org.apache.hadoop.hdfs.protocol.LocatedBlock.isStriped()'`
    

---

**尝试**直接使用官方下载的hbase bin 2.4.14文件

* 报错1：

  ```
  ERROR: org.apache.hadoop.hbase.PleaseHoldException: Master is initializing
  	at org.apache.hadoop.hbase.master.HMaster.checkInitialized(HMaster.java:2812)
  ```

---

**尝试**直接使用官方下载的hbase bin 2.3.0文件（环境为jdk8+hadoop3.3.1+hbase2.3）

* 报错1：`ERROR master.HMaster: Failed to become active master java.io.EOFException: Cannot seek after EOF`

  * 成功：尝试1 for 1：删除hdfs fs里的/hbase/MasterData，结果环境恢复了

    ![image-20221101225150167](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20221101225150167.png)

    ![image-20221101225304915](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20221101225304915.png)

    目前status命令和create命令能够运行

    ```
    hbase(main):001:0> n_splits = 10 # HBase recommends (10 * number of regionservers)
    hbase(main):002:0> create 'usertable', 'family', {SPLITS => (1..n_splits).map {|i| "user#{1000+i*(9999-1000)/n_splits}"}}
    ```

    ![image-20221101225627471](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20221101225627471.png)

    载入workload

    ```
    bin/ycsb load hbase20 -P workloads/workloada -cp /HBASE-HOME-DIR/conf -p table=usertable -p columnfamily=family
    注意修改HBASE-HOME-DIR
    ```
  
    * 报错1.1：
    
      ```
      File "/home/iscas/Downloads/ycsb/ycsb-0.17.0/bin/ycsb", line 228
                except subprocess.CalledProcessError, err:
                                                    ^
            SyntaxError: invalid syntax
      ```
    
      ycsb是python文件，主要原因是我在python3环境中运行ycsb（python2），通过anaconda切换到python27环境中运行解决
    
      成功load
    
      ![image-20221102110930437](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20221102110930437.png)
    
      运行workload
    
      ```
      bin/ycsb run hbase20 -P workloads/workloada -cp /HBASE-HOME-DIR/conf -p table=usertable -p columnfamily=family
      ```
    
      成功运行
    
      ![image-20221102111403236](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20221102111403236.png)


---

* 附一个错误：报的错是`ERROR master.HMaster: Failed to become active master org.apache.hadoop.ipc.RemoteException(java.io.IOException): File /user/iscas/tmp/hbase/.tmp/hbase.version could only be written to 0 of the 1 minReplication nodes. There are 0 datanode(s) running and 0 node(s) are excluded in this operation.`这个错误与hadoop相关，导致dataNode没有启动成功，具体解决是DataNode与NameNode的current文件夹下的version文件中clusterID设置一样（以NameNode为准）

