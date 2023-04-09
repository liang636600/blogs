查看spark主目录下的pom文件，发现需要的hadoop版本为3.3.1

# 无密码ssh登录自己

启动 HDFS 集群时，NameNode 会通过 ssh 去启动其它节点上的 DataNode，因此，需要做无密码登录，这样 NameNode 就可以直接启动 DataNode，而不需要输入密码。 

根据 HDFS 部署图，NameNode 和 DataNode 都在scala_dev上，因此，需要做 scala_dev无密码登录自己，操作如下。

![image-20211129111201730](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211129111201730.png)

` ssh-keygen -t rsa`

`cat ./id_rsa.pub >> ./authorized_keys`

# 下载并配置HDFS

链接<https://mirrors.tuna.tsinghua.edu.cn/apache/hadoop/common/hadoop-3.3.1/>

下载后解压并在/etc/profile中配置环境变量

修改hadoop下的`etc/hadoop/hadoop-env.sh`文件中的JAVA_HOME为`export JAVA_HOME=/home/iscas/Downloads/openjdk-16_linux-x64_bin/jdk-16`

修改workers，它存储的是所有DataNode的主机名，原来内容是`localhost`，修改为`iscas-Precision-3551`，后续扩展DataNode，只需要在workers中添加要扩展节点的主机名即可。

修改 hdfs-site.xml，先复制模板文件`cp ./share/doc/hadoop-project/hadoop-project-dist/hadoop-hdfs/hdfs-default.xml etc/hadoop/hdfs-site.xml `，查找 dfs.namenode.rpc-address，第 35 行增加 iscas-Precision-3551:9001，这是 DataNode 连接 NameNode 的 IP 和端口，配置后正常显示：“Starting namenodes on [iscas-Precision-3551]”

查找 dfs.namenode.name.dir，修改为/home/iscas/Desktop/desk/dfs/namenode，此路径用来存储 NameNode 下的元数据（名字空间信息、操作日志等）

查找 dfs.datanode.data.dir，修改为“/home/iscas/Desktop/desk/dfs/datanode”，此路径是 DataNode的存储路径，HDFS 中文件的真实内容都保存在此路径下

修改core-site.xml，复制模板`cp ./share/doc/hadoop-project/hadoop-project-dist/hadoop-common/core-default.xml etc/hadoop/core-site.xml`，配置 defaultFS，将 HDFS 作为默认的文件系统

查找 fs.defaultFS和fs.default.name，修改值为“hdfs://iscas-Precision-3551:9001/”，配置了 defaultFS 和 fs.default.name 后，会自动在路径前面加上 hdfs://iscas-Precision-3551:9001/前缀，这样默认路径就是 hdfs 上的路径，之前的 file:///前缀，表示的是本地文件系统。按照目前的配置，/表示hdfs://iscas-Precision-3551:9001/，表示 HDFS 上的/目录，而 file:///则表示本地文件系统的/目录

修改 tmp 配置，查找 hadoop.tmp.dir,值修改为/home/iscas/Desktop/desk/dfs/tmp，此处用来配置 hadoop 临时文件存储路径

# 格式化并启动HDFS

1. 格式化 `hdfs namenode -format`

2. 启动HDFS 在 hadoop 目录下，运行下面的脚本，一路 Yes，`sbin/start-dfs.sh`

3. 验证

   方法(1) jps查看进程

   ![image-20211129160523456](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211129160523456.png)

   方法(2) `hdfs dfsadmin -report`，此命令可以打印 HDFS 系统信息，包括总的容量，DataNode 信息等

   方法(3) 在web页面打开 `http://localhost:9870/`

   ![image-20211129162137655](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211129162137655.png)

   

