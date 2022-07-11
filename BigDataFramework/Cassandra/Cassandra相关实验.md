Cassandra使用的是jdk14编译后的版本，运行时jdk使用的jdk16版本

* 加载数据

  命令`bin/ycsb.sh load cassandra-cql -p "hosts=127.0.0.1" -P workloads/workloada -p recordcount=3000`(每次运行该命令时，Cassandra数据库里的数据都是重新载入的? 在400000行后，重新load行数30000行，但数据库中的行数仍然为400000行)

  在cqlsh命令行中使用`select * from usertable;`查看发现数据加载进了

  在cqlsh命令行中使用`select count(*) from usertable;`查看数据的条数

  当数据条数为6000000时，出现`ReadTimeout Error from server: code=1200`

  * 解决

    修改cassandra.yaml中的

    ```
    # How long the coordinator should wait for read operations to complete
    read_request_timeout_in_ms: 50000
    # How long the coordinator should wait for seq or index scans to complete
    range_request_timeout_in_ms: 100000
    # How long the coordinator should wait for writes to complete
    write_request_timeout_in_ms: 20000
    # How long the coordinator should wait for counter writes to complete
    counter_write_request_timeout_in_ms: 50000
    # How long a coordinator should continue to retry a CAS operation
    # that contends with other proposals for the same row
    cas_contention_timeout_in_ms: 10000
    # How long the coordinator should wait for truncates to complete
    # (This can be much longer, because unless auto_snapshot is disabled
    # we need to flush first so we can snapshot before removing the data.)
    truncate_request_timeout_in_ms: 600000
    # The default timeout for other, miscellaneous operations
    request_timeout_in_ms: 100000
    
    # How long before a node logs slow queries. Select queries that take longer than
    # this timeout to execute, will generate an aggregated log message, so that slow queries
    # can be identified. Set this value to zero to disable slow query logging.
    slow_query_log_timeout_in_ms: 5000
    ```
    
    然后出现错误`OperationTimedOut:errors={'127.0.0.1':'Client request timeout.See Session.execute[_async](timeout)'},last_host=127.0.0.1`
    
    * 解决：修改cqlsh.py文件的参数DEFAULT_REQUEST_TIME为更大的值

  | recordcount | time/s  | 数据库中的行数 |
  | ----------- | ------- | -------------- |
  | 300000      | 41.664  |                |
  | 20000       |         |                |
  | 400000      | 54.910  | 400000         |
  | 600000      | 80.621  | 600000         |
  | 6000000     | 779.327 |                |

* 运行

  命令`bin/ycsb.sh run cassandra-cql -p "hosts=127.0.0.1" -P workloads/workloada -p recordcount=3000 -p operationcount=1000`

  参数operationcount决定运算次数

---

# 测试方案

| GC         | workload种类 | workload的recordcount | workload的operationcount | MAX_HEAP_SIZE |
| ---------- | ------------ | --------------------- | ------------------------ | ------------- |
| ZGC        | workloada    | 6,000,000             | 6,000,000                | 4G            |
| G1         | workloadb    | 12,000,000            | 12,000,000               | 8G            |
| Shenandoah | workloadc    | 24,000,000            | 24,000,000               | 16G           |
| parallel   | workloadd    |                       |                          |               |
|            | workloade    |                       |                          |               |
|            | workloadf    |                       |                          |               |

| GC   | MAX_HEAP_SIZE | Cassandra数据库中总条数 |      | workload的recordcount | workload的operationcount | 总体用时/s |
| ---- | ------------- | ----------------------- | ---- | --------------------- | ------------------------ | ---------- |
| ZGC  | 4G            | 600,000                 | load | 500,000               | 100,000                  | 68.548     |
| ZGC  | 4G            | 600,000                 | run  | 500,000               | 100,000                  | 17.268     |
|      |               |                         | load | 50,000                | 600,000                  | 9.931      |
|      |               |                         | run  | 50,000                | 600,000                  | 74.456     |
|      |               | 1,200,000               | load | 500,000               | 100,000                  | 68.686     |
|      |               |                         | run  | 500,000               | 100,000                  | 17.743     |
|      |               |                         | load | 50,000                | 600,000                  | 10.038     |
|      |               |                         | run  | 50,000                | 600,000                  | 68.819     |



