# Spark阅读记录

一个Application由一个driver和多个job组成，一个job由多个stage组成，一个stage由多个task组成

一个spark程序对应一组client，driver和executor
如果client和driver在一个进程内，则为client模式，如果分开则为cluster模式

**Spark运行基本流程：**

1. 由Driver生成一个SparkContext，由SparkContext负责与cluster manager通信和申请资源（例如Executor）等操作
2. SparkContext根据RDD的依赖关系构建DAG图，DAG图提交给DAG调度器，将图分为多个stage，由task调度器将stage上的多个task分配给executor运行
3. executor将运行结果返给task调度器，task调度器再返给DAG调度器，运行结束后写入数据并释放资源

一个RDD本身不变，对RDD的操作使用惰性调用，最后需要输出的时候才对以前的操作进行运算转换
有检查点和记录日志持久化RDD
通过对DGA反向解析，遇到宽依赖断开遇到窄依赖尽量划分到同一个stage

![IMG_20211116_172810](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/IMG_20211116_172810.jpg)

![IMG_20211116_173117](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/IMG_20211116_173117.jpg)

![IMG_20211116_173849](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/IMG_20211116_173849.jpg)

![IMG_20211118_170933](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/IMG_20211118_170933.jpg)

spark程序提交给yarn运行

![IMG_20211118_191215](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/IMG_20211118_191215.jpg)

spark程序在yarn上的执行图（client deploy mode）

![IMG_20211118_192233](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/IMG_20211118_192233.jpg)

spark程序在yarn上的执行图（cluster deploy mode）

![IMG_20211118_192558](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/IMG_20211118_192558.jpg)

spark在standalone上的执行过程（client deploy mode）

![IMG_20211118_193726](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/IMG_20211118_193726.jpg)

spark在standalone上的执行过程（cluster deploy mode）

![IMG_20211118_194125](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/IMG_20211118_194125.jpg)

spark-shell运行方式和运行模式配置

![IMG_20211118_195215](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/IMG_20211118_195215.jpg)

## RDD

rdd可以被分成多个分区在不同节点上并行处理，若想访问rdd中的值，通过driver拉取不同节点中的分区到一起，然后查看（collect函数）
action将rdd转换为可以在driver端访问的结果的操作，action操作会调用启动spark job
新建SparkContext的时候会启动application
**job:** rdd的action和action所触发的操作（包括rdd创建和transform操作）
在一个stage中的可以管道化（将一个分区的多个操作合并到一个executor串行运行），比如一个stage里面有map和filter操作，一个分区可以map完直接进入filter操作而不需要等其他分区完成map后再统一filter操作
一个stage中不同分区可以在各自的executor运行stage中所有操作而不需要考虑与其他分区的协同
在一个stage中，一个rdd对应多个partition每个partition对应一个task，这些task被分配到executor上运行（可能出现两个task在同一个executor上运行的情况，executor以线程的方式运行task）

![IMG_20211119_144500](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/IMG_20211119_144500.jpg)

**窄依赖:** 子rdd的一个partition只由父rdd的一个或少数partition计算而来
**宽依赖:** 子rdd的一个partition由父rdd所有partition计算而来
DAG划分stage是向上溯源的

![IMG_20211119_145526](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/IMG_20211119_145526.jpg)

