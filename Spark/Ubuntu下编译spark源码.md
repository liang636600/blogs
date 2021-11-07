# Ubuntu下编译spark源码

第一部分跟着博客（https://blog.csdn.net/jy02268879/article/details/81009217）做，做到

![image-20211031155826652](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/e36257f90b3569adc71c86c988c78314.png)

这一步的时候，进入Spark源码解压目录，然后输入命令`./build/mvn -DskipTests clean package`，慢慢等待编译，如果编译过程中遇到curl啥的，一般等一段时间后重新打开一个终端再输入`./build/mvn -DskipTests clean package`多试几次都能解决了。

**测试Spark：** 输入`./bin/spark-shell`可以看到“Spark”字样。
再运行`spark.range(1000 * 1000 * 1000).count()`如果有如下输出结果，则配好了spark
![在这里插入图片描述](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/8018c55703354722a7c10510af77d6a7.png)


**踩过的坑：**

* 如果使用的jdk是从源码编译的话，需要注意的是jdk有两个路径选择，第一个是`jdk13\build\linux-x86_64-server-release\images\jdk\lib`，第二个是`jdk13\build\linux-x86_64-server-release\jdk\lib`，如果系统使用的是第二个路径的jdk的话，在编译spark的时候会报错，找不到modules文件，而在第一个路径的jdk里面就有这个modules文件。如果在`jdk13\build\linux-x86_64-server-release`文件夹下没有images文件夹，说明前面make的时候是直接选择make了，重新编译jdk源码把make改为make images就行。
* **编译耗时漫谈：** 第一次编译我使用的下载好的jdk15，编译大概40分钟。第二次使用的是从jdk16源码编译的jdk16，花了1天7小时，初步判断是jdk16当时bash configure的时候采用的是slowdebug版，可能有点慢。



