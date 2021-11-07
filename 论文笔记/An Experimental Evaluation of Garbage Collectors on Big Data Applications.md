* **题目：**An Experimental Evaluation of Garbage Collectors on Big Data Applications
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
3.  为应用开发人员提供经验性的建议，为设计出大数据友好的垃圾回收器提供了优化策略

---

#### 1 INTRODUCTION

由于原因

**1）**当对象很多的时候自动垃圾管理并不好

**2）**大数据应用不同于传统应用，具有**数据密集**和**内存密集**的特点

**3）**在内存中的对象有不同的生命周期

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

#### 2 BACKGROUND

##### 2.1 Spark memory management

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

##### 3.2 Experimental setup
###### 3.2.1 Input data variation
###### 3.2.2 Dataflow and GC configuration
###### 3.2.3 Experimental environments
##### 3.3 Analytical approaches
##### 3.3.1 Application profiling
##### 3.3.2 Performance comparison and analysis
---
#### 4 EXPERIMENTAL RESULTS
##### 4.1 Overall results
##### 4.1.1 Key contributors to the performance differences
##### 4.2 GroupBy results
###### 4.2.1 Performance comparison results
###### 4.2.2 Findings and their implications Finding
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







