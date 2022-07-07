Cassandra使用的是jdk14编译后的版本，运行时jdk使用的jdk16版本

Cassandra的heap size在`cassandra-env.sh`中设置（与JVM相关的参数都可以在该文件中设置）

```
bin/ycsb.sh load cassandra-cql -P workloads/workloada
bin/ycsb.sh run cassandra-cql -P workloads/workloada
```

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

* 运行

  ```
  ./bin/ycsb run basic -P workloads/workloada -P large.dat -s > transactions.dat
  ```

  

