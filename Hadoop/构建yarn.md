# 暂时失败 配置yarn

1. 复制yarn-site.xml 模板文件

   `cp ./share/doc/hadoop-project/hadoop-yarn/hadoop-yarn-common/yarn-default.xml ./etc/hadoop/yarn-site.xml `

   查找`yarn.resourcemanager.hostname`，值修改为`iscas-Precision-3551`这 个 用 来 配 置ResourceManager 的主机名，NodeManager 根据它来连接 ResourceManager

   查找 yarn.nodemanager.aux-services修改值为mapreduce_shuffle

2. 复制 mapred-site.xml 模板文件

   此文件用来配置 MapReduce 程序的执行 `cp ./share/doc/hadoop-project/hadoop-mapreduce-client/hadoop-mapreduce-client-core/mapred-default.xml etc/hadoop//mapred-site.xml`

   查找 mapreduce.framework.name，修改值为yarn，这个其实只有 Client 需要，启动 MapReduce 任务时，用来决定MapReduce 是分布式的，还是本地的

3. 启动yarn

   `sbin/start-yarn.sh`

   验证

   方法(1) 使用 jps，查看是否有 ResourceManger，它是 Yarn 的管理节点，以及 NodeManager， 它是 Yarn 中各个节点上运行的程序，因为我们现在只有 iscas-Precision-3551这一个节点，因此，此 NodeManager 和 ResourceManager 是在一起的，如果有多个节点，则会有多个 NodeManager, ResourceManager 只有 1 个

   **目前验证失败**

