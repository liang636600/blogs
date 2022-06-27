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

* 尝试JDK16运行

  ![image-20220627100431244](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20220627100431244.png)