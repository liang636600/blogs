# Spark阅读记录

一个Application由一个driver和多个job组成，一个job由多个stage组成，一个stage由多个task组成

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

