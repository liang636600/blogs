# 1 安装JDK

# 2 下载并安装Flink

![1653892286158](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/1653892286158.jpg)

# 3 启动集群

```
$ ./bin/start-cluster.sh
Starting cluster.
Starting standalonesession daemon on host.
Starting taskexecutor daemon on host.
```

# 4 提交作业（Job）

```
$ ./bin/flink run examples/streaming/WordCount.jar
$ tail log/flink-*-taskexecutor-*.out
  (nymph,1)
  (in,3)
  (thy,1)
  (orisons,1)
  (be,4)
  (all,2)
  (my,1)
  (sins,1)
  (remember,1)
  (d,4)
```

# 5 Web UI监控集群

打开<http://localhost:8081/>

![image-20220530144548145](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20220530144548145.png)

# 6 停止集群

```
$ ./bin/stop-cluster.sh
```

