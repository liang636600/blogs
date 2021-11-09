* **题目：** An Experimental Evaluation of Garbage Collectors on Big Data Applications
* **场景或问题：**
* **结论：**
* **思路或核心算法：**
* **自我总结：**

---

### An Experimental Evaluation of Garbage Collectors on Big Data Applications

---

#### ABSTRACT:

缺乏对GC性能的深刻理解--->阻碍大数据应用的性能提升

**本文工作：**

1. 使用四个独立的Spark应用，对目前流行的垃圾回收器（Parallel，CMS,G1）进行了第一次全面评测
2. 通过调查这些大数据应用**内存使用模式**和**垃圾回收模式**之间的关系，获得许多关于GC低效的发现
3. 为应用开发人员提供经验性的建议，为设计出大数据友好的垃圾回收器提供了优化策略

---

#### 1 INTRODUCTION

由于原因

**1）** 当对象很多的时候自动垃圾管理并不好

**2）** 大数据应用不同于传统应用，具有**数据密集**和**内存密集**的特点

**3）** 在内存中的对象有不同的生命周期

导致大量gc开销

大数据应用的gc低效原因有3：

* 大量输入和中间计算结果，一些可重用的中间结果被缓存在内存
* 大数据框架目前处理data-level层次的内存管理（粗放）
* object-level层次的内存管理不考虑大数据应用中对象的特点

本文工作：

* 分析四个广泛应用的spark程序的**计算特点和内存使用模式**
* 全面评测三种垃圾回收算法在四个spark程序的表现。通过分析**应用内存使用和gc模式**之间的相关性，我们得到影响不同垃圾回收器之间性能的根本原因

重要发现：

* 造成不同垃圾回收器性能不同的原因主要是大数据应用**独特的内存使用模式和计算特点**
* 在回收long-lived shuffled数据的同时，并发的垃圾回收器（CMS与G1）可以减少gc暂停时间，但由于CPU争抢严重也会阻碍CPU密集型的数据算子
* 在管理大量数据对象方面，这三个垃圾回收器仍然低效

建议：

* 由于三种垃圾回收器不能正确分配容纳long-lived shuffled数据的堆的大小，我们建议使用通过**内存使用预测和动态内存空间调整**的堆内存重整策略
* 当回收long-lived shuffled and cached数据，三种垃圾回收器都会经历非必要的连续gc，通过利用数据的生命周期，我们提出一种**新的对象标记算法**
* 对每一次迭代都需要回收大量shuffled 数据的迭代型应用，三种垃圾回收算法性能均低效。利用这些shuffled数据独特的生命周期和固定的大小，我们提出一种**新的对象清除算法**来实现迭代应用不会有gc暂停的目的

除此外，我们确定了两种OOM错误的根本原因，即spark框架在处理连续shuffle溢出的内存泄漏与G1的堆碎片问题

---

#### 2 ~~BACKGROUND~~

##### 2.1 Spark memory management

在spark中，输入输出和中间数据被建模为RDD，spark根据RDD间的依赖关系，自动将driver程序转为DAG_based数据流图，数据流图进一步被转化为一个MapReduce-like的运行计划，包括一些被shuffle依赖分割的阶段。**本文中**，map阶段指的是不需要数据shuffle的阶段，reduce阶段指的是需要shuffle从以前阶段获得的数据。在运行阶段，spark分配多个跑map/reduce task的executors（例如jvm）

spark程序使用的内存分为三部分：

1. **cached data**

   缓存reusable data，对象具有long-lived与跨越多个阶段的特点,spark为其分配了一个逻辑的storage space

2. **shuffled data**

   

3. **operator-generated data**

##### 2.2 JVM memory management

----

#### 3 METHODOLOGY

##### 3.1 Application Selection

spark应用的内存使用被数据特点（cached数据，shuffled数据及算子产生的数据）和计算特点（迭代计算）所影响

选择四个spark应用，特点：

* 来自不同领域（SQL查询，机器学习，图计算）
* 具有不同计算模式（多/少的数据shuffle，不同空间复杂度的数据聚合，有数据缓存的迭代计算）
* 有不同的内存使用模式（long-lived 积累结果，临时输出记录，大量数据对象）
  ![image-20211103184722089](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211103184722089.png)

四个spark程序：

* GroupBy

  ![image-20211108111450892](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211108111450892.png)

  map阶段把每行变为<(sourceIP, visitDate), adRevenue> record，reduce阶段使用reduceByKey()，reduceByKey() 展示了long-lived accumulated records的内存使用方式，主要是**上图中后面的紫色部分数据长时间占用内存** 

* Join

  ![image-20211108112153690](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211108112153690.png)

  ![image-20211108112332028](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211108112332028.png)

  在map阶段，Rankings表被分为<URL, pageRank>，UserVisits表被分为<URL, adRevenue>；reduce阶段，合并相同的URL为<URL, list(pageRanks, adRevenues)>，这些<URL, list(pageRanks, adRevenues)>记录为long-lived ac- cumulated records。join遭受**heavy shuffle**问题

* SVM

  ![image-20211108121319382](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211108121319382.png)

  light shuffle，**训练数据被视为long-lived cached records（他们被放在了cache中）**

* PageRank

  ![image-20211108121257644](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211108121257644.png)

  **long-lived accumulated records在每个阶段被产生和回收**

##### 3.2 Experimental setup

###### 3.2.1 Input data variation

###### 3.2.2 Dataflow and GC configuration

###### 3.2.3 Experimental environments

##### 3.3 Analytical approaches

统计应用平均运行时间，选择五次的中等时间来比较stage和task execution time

##### 3.3.1 Application profiling

三种profilers：

* **execution time profiler**：measure execution time of each application and map/reduce task
* **dataflow profiler：** collects the number and size of the records in each data processing phase
* **resource profiler：** collects the CPU, memory usage, and GC metrics of each task.

##### 3.3.2 Performance comparison and analysis

三个指标：

* **Application execution time：**

* **Task execution time**：identifies where the performance difference occurs since map tasks and reduce tasks have different memory usage patterns.

  can be decomposed to: data computation time, shuffle spill time, and GC time. 如果gc时间是差异主要原因，我们对gc时间比较

* **Fine-grained task execution time：** identifies the po- tential causes of the performance difference

**gc模式比较：**

研究的gc模式包括：

1. **Memory allocation pattern**：analyze how different allocation policies affect the GC time

2. **GC time and GC fre- quency pattern**：

   像并发gc，gc time包含 **young GC time, full GC time, and concurrent GC time**，We compare these types of GC time across three collectors and **identify the most time-consuming GC phases**



---

#### 4 EXPERIMENTAL RESULTS

##### 4.1 Overall results

![image-20211108145726623](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211108145726623.png)

* 生成long-lived accumulated records（指的是大量shuffled records）的应用更有可能出现垃圾回收器的低效
* 并发的垃圾回收器gc time比parallel垃圾回收器的减少了8.3%~94%
* G1垃圾回收器在处理SVM应用的大量对象出现OOM错误

##### 4.1.1 Key contributors to the performance differences

造成差异的实质原因是：**the patterns of long-lived accumulated records and humongous data objects**

* **Long-lived accumulated records**：指的是内存中的shuffled records，这些数据很多且没有匹配的gc回收算法，造成经常和长时间的full gc

  1. 这些records需要大量old generation来容纳，因此不正确的young/full generation sizing policy会导致经常full gc

  2. 回收这些records is time-consuming及CPU-intensive

     * object marking/sweeping algorithms需要遍历整个object graph来确定live reference objects，time-consuming and CPU-intensive

     * Stop-the-world marking/sweeping algorithm依次Mark和sweep导致long individual full gc

     * Concurrent marking/sweeping algorithms可以通过并行mark，sweep及应用运行，减少了full gc time

       缺陷：suffer from concurrent mode failures problem and degrade the CPU-intensive data operators like join() 

  3. 缺乏对数据对象生命周期的了解，当前gc算法利用静态gc触发阈值 导致在gc cycle的重复工作

* **Humongous data objects**：指的是比G1 maximum region size（32MB）大的对象，当大数据应用中存在许多的humongous对象时，G1的非连续的region策略会失效，可能导致OOM错误

##### 4.2 GroupBy results

探究long-lived accumulated records的影响

###### 4.2.1 Performance comparison results

![image-20211108161332578](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211108161332578.png)

###### 4.2.2 Findings and their implications Finding

1. **ParallelGC tasks trigger 1.5x more shuffle spills than CMS and G1 tasks**: 主要是Parallel collector可用heap size最小，原因是Parallel collector有交换区占用一定空间，CMS也有同样的问题，但由于它的幸存区较小，影响不大

   implication：设计动态的dynamic spill threshold根据运行时可用的堆大小来平衡spill time和spill frequency
   
2. 不同的young/old大小分配策略导致不同gc频率（因为long-lived accumulated records需要更大空间的老年区），通过分配大的老年区空间，CMS相比ParallelGC与G1，full gc次数减少约48%

   三种gc算法都有适应性调整young/old heap size的策略（统计GC pause time与heap占用），然而这三种gc低效的generation sizing patterns导致high young或 high full gc频率。

   * ParallelGC更倾向于根据heap occupancy来扩大或缩小老年代空间，ParallelGC限制了老年代的大小为66.6%的堆大小，并且当shuffle spill过后，ParallelGC减少了老年代大小，较小的老年区导致频繁的full gc
   * CMS倾向于扩大老年代空间（并且不会缩小），与Parallel/g1相比，较大的老年区使得他有更少的full gc，但是，由于新生代空间减少，使得它的young gc频率是另外两个的两倍
   * G1倾向于根据GC pause time与heap usage的统计结果来平衡调整young/old heap space，在shuffle spill过后，它增大了新生代的大小以容纳读取的磁盘上的spilled records（这些records是long-lived的），需要更大的老年代空间，因此导致比CMS更高的full gc频率

   **implication：** 当前的young/old generation sizing policy不适合容纳long-lived accumulated records，需要设计知晓在每个数据处理阶段


​     

##### 4.3 Join results

###### 4.3.1 Performance comparison results

###### 4.3.2 Findings and their implications

##### 4.4 SVM results

###### 4.4.1 Performance comparison results

###### 4.4.2 Findings and their implications

##### 4.5 PageRank results

###### 4.5.1 Performance comparison results

###### 4.5.2 Findings and their implications

---

#### 5 LESSONS AND INSIGHTS

---

#### 6 DISCUSSION

---

#### 7 RELATED WORK

---

#### 8 CONCLUSION
