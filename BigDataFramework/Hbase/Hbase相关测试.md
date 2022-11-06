# 1 启动运行

```
1.启动hadoop
2.启动hbase
3.切换python环境 命令 activate python27
4.在ycsb主目录下运行
	4.1 载入数据 bin/ycsb load hbase20 -P workloads/workloada -cp ~/Downloads/hbase-2.3.0-bin/hbase-2.3.0/conf -p table=usertable -p columnfamily=family
	4.2 运行数据 bin/ycsb run hbase20 -P workloads/workloada -cp ~/Downloads/hbase-2.3.0-bin/hbase-2.3.0/conf -p table=usertable -p columnfamily=family
```

把jdk切换成16，hbase启动失败