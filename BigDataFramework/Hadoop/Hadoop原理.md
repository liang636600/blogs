# HDFS

![IMG_20211117_135304](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/IMG_20211117_135304.jpg)

![IMG_20211117_135843](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/IMG_20211117_135843.jpg)

namenode负责管理，datanode负责数据存储和读取
**缺点:** 不适合低延迟数据访问（数十毫秒），Hbase是更好选择；不允许多个用户对同一个文件执行写操作，只允许追加不允许随机写操作
namenode包含两个核心数据结构即FsImage（维护文件系统树，文件和文件夹的元数据）和EditLog（记录所有针对文件的创建删除和重命名等操作）

![IMG_20211117_142633](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/IMG_20211117_142633.jpg)

名称节点启动时会将FsImage加载到内存，然后执行EditLog里的内容以保持内存中的元数据最新，更新操作写入EditLog而不是直接在FsImage操作（懒操作）
为解决EditLog过大的问题，引入了第二名称节点，每隔一段时间执行EditLog与FsImage的合并操作，第二名称节点也可以作为检查点使用

![IMG_20211117_143225](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/IMG_20211117_143225.jpg)

客户端读取数据采用就近原则读取
数据复制采用击鼓传花似的流水线，每个数据节点传递存储数据节点列表和数据块的数据

![IMG_20211117_143711](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/IMG_20211117_143711.jpg)

冗余存储

![IMG_20211117_150125](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/IMG_20211117_150125.jpg)

HDFS读数据过程

![IMG_20211117_151712](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/IMG_20211117_151712.jpg)

HDFS写数据过程

![IMG_20211122_173151](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/IMG_20211122_173151.jpg)



# HDFS 2.0
## HDFS HA
为解决hdfs只有一个名称节点容易出现单点故障问题，新加一个名称节点作为待命节点以实现热备份，两节点的状态同步可以通过共享存储系统来实现（如network file system或zookeeper）

![IMG_20211117_155012](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/IMG_20211117_155012.jpg)

## HDFS联邦
设计了多个相互独立的名称节点
# YARN
![IMG_20211117_160742](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/IMG_20211117_160742.jpg)

![IMG_20211117_161948](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/IMG_20211117_161948.jpg)

![IMG_20211117_162031](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/IMG_20211117_162031.jpg)

![IMG_20211117_162116](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/IMG_20211117_162116.jpg)

**工作流程**

1. 用户向yarn提交ApplicationMaster程序，启动ApplicationMaster的命令及用户程序等
2. ResouceManager收到用户程序请求后，调度器为其分配一个容器，并与容器所在的NodeManager通信为该应用程序在该容器中启动一个ApplicationMaster
3. ApplicationMaster创建后向ResouceManager注册，使得用户可以通过ResouceManager来查看应用程序的运行状态
4. ApplicationMaster通过轮询方式向ResouceManager申请资源
5. ResouceManager以容器的方式向ApplicationMaster分配资源，一但ApplicationMaster申请到资源后，就与该容器所在的NodeManager通信，要求他启动任务
6. 当ApplicationMaster要求容器启动任务时，他会为任务设置好运行环境（包括环境变量，jar包，二进制程序等），然后将任务启动命令写入到一个脚本中，最后通过在容器中运行该脚本来启动任务
7. 各个任务向ApplicationMaster汇报自己的状态和进度
8. 应用程序完成后，ApplicationMaster向ResouceManager注销并关闭自己，若ApplicationMaster因故失败，则ResouceManager重启启动ApplicationMaster

**核心:** 先在某节点为ApplicationMaster申请容器，然后ApplicationMaster管理任务

![IMG_20211117_163759](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/IMG_20211117_163759.jpg)

