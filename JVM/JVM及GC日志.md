HotSpot所有功能的日志都收归到了“-Xlog”参数上`-Xlog[:[selector][:[output][:[decorators][:output-options]]]]`

命令行中最关键的参数是选择器（Selector），它由标签（Tag）和日志级别（Level）共同组成。标签可理解为虚拟机中某个功能模块的名字，它告诉日志框架用户希望得到虚拟机哪些功能的日志输出。垃圾收集器的标签名称为“gc”。

日志级别从低到高，共有Trace，Debug，Info，Warning，Error，Off六种级别，日志级别决定了输出信息的详细程度，默认级别为Info，HotSpot的日志规则与Log4j、SLF4j这类Java日志框架大体上是一致的。另外，还可以使用修饰器（Decorator）来要求每行日志输出都附加上额外的内容，支持附加在日志行上的信息包括：

* time：当前日期和时间。

* **uptime**：虚拟机启动到现在经过的时间，以秒为单位。

* timemillis：当前时间的毫秒数，相当于System.currentTimeMillis()的输出。

* uptimemillis：虚拟机启动到现在经过的毫秒数。

* timenanos：当前时间的纳秒数，相当于System.nanoTime()的输出。

* uptimenanos：虚拟机启动到现在经过的纳秒数。

* pid：进程ID。

* tid：线程ID。

* **level**：日志级别。

* **tags**：日志输出的标签集。

如果不指定，默认值是uptime、level、tags这三个，此时日志输出类似于以下形式：

![image-20211211162015822](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211211162015822.png)

1. 查看GC基本信息，在JDK 9之前使用-XX：+PrintGC，JDK 9后使用-Xlog：gc

   ![image-20211211162351166](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211211162351166.png)

2. 查看GC详细信息，在JDK 9之前使用-XX：+PrintGCDetails，在JDK 9之后使用-Xlog：gc* ， 用通配符*将GC标签下所有细分过程都打印出来，如果把日志级别调整到Debug或者Trace，还将获得更多细节信息

   ![image-20211211162624125](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211211162624125.png)

3. 查看GC前后的堆、方法区可用容量变化，在JDK 9之前使用-XX：+PrintHeapAtGC，JDK 9之后使用-Xlog：gc+heap=debug

   ![image-20211211162742489](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211211162742489.png)

4. 查看GC过程中用户线程并发时间以及停顿的时间，在JDK 9之前使用-XX：+PrintGCApplicationConcurrentTime以及-XX：+PrintGCApplicationStoppedTime，JDK 9之后使用-Xlog：safepoint

   ![image-20211211162851543](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211211162851543.png)

5. 查看收集器Ergonomics机制（自动设置堆空间各分代区域大小、收集目标等内容，从Parallel收集器开始支持）自动调节的相关信息。在JDK 9之前使用-XX：+PrintAdaptive-SizePolicy，JDK 9之后使用-Xlog：gc+ergo*=trace

   ![image-20211211163016551](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211211163016551.png)

6. 查看熬过收集后剩余对象的年龄分布信息，在JDK 9前使用-XX：+PrintTenuring-Distribution，JDK 9之后使用-Xlog：gc+age=trace

   ![image-20211211163108620](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211211163108620.png)

---

**gc参数：**

-verbose:gc 控制台打印 gc 日志

-Xms 堆初始大小

-Xmx 堆最大大小

-Xmn 新生代大小

---

**将gc日志输出到文件：**

GC日志输出到文件路径 

* `-Xloggc:/path/to/gc.log`

每次启动用时间戳命名日志文件

* 使用-%t作为日志文件名

  `-Xloggc:/path/to/gc-%t.log`

  生成的文件名是这种：gc-2021-03-29_20-41-47.log

---

**gc日志分析工具：**

* 网站：<https://gceasy.io/>

---

