# Performance evaluation of Java garbage collectors for large heap transaction based applications

# Abstract

对三种GC评测（G1,Shenandoah GC, ZGC），测试数据使用DaCapo Benchmark Suite的子集、两个真实世界transaction-based应用（heap的大小分别为 63GB and 256GB），评测指标主要是 Latency和 throughput。

实验表明一种garbage collector configuration不适用所有应用。Shenandoah GC和ZGC在 latency, average pause time, maximum pause time, and total accumulated stop-the-world time都比G1表现好，在throughput and execution time他们三差不多，G1比另外两个在heap over-provisioning的时候更稳定。

# 1 Introduction

## 1.1 Aim and research questions

* Benchmark I：The Processing Node Server application with heap restrictions of 63GB and a latency requirement of 1 second. 

* Benchmark II：The Query Node Server application, with heap restrictions of 256GB and a latency re- quirement of 10-20 seconds

## 1.2 Research methodology

## 1.3 Scope

## 1.4 Contribution

## 1.5 Ethical sustainability and societal aspects

## 1.6 Outline

# 2 Background

## 2.1 Hotspot JVM

## 2.2 Introduction to garbage collection

## 2.3 Garbage First GC

默认配置中 G1GC 的目标不是最大化吞吐量，也不是具有最低延迟，而是产生均匀的、小的暂停时间。

### 2.3.1 Heap layout

### 2.3.2 Collection cycle

分为两个阶段young-only phase and space-reclamation phase

young-only phase开始于把young generation提升到old generation，当old generation达到阈值时，space-reclamation phase开始

## 2.4 Shenandoah GC

### 2.4.1 Heap layout
### 2.4.2 Collection cycle

## 2.5 Z Garbage Collector
### 2.5.1 Heap layout

### 2.5.2 Collection cycle
## 2.6 DaCapo benchmark suite

**DaCapo benchmark suite：** a set of open-source real-world applications with complex logic and non-trivial memory loads

## 2.7 Real-world application
### 2.7.1 The Processing Node

来自证券交易所的公开或私有市场数据作为主要输入，数据被标准化并被时间序列化。这些数据将以实时流的形式交给The Processing Node处理以分析交易中的异常行为，除此外，它将保持和索引数据以便query node使用。

### 2.7.2 The Query Node

# 未读：3 Related Work

## 3.1 Analysis and optimization

## 3.2 Performance comparison
# 4 Methods

## 4.1 Experimental setup

### 4.1.1 Environment

## 4.2 JVM and GC options

**G1GC specific options**

-XX:MaxGCPauseMillis

increase -XX:InitiatingHeapOccupancyPercent value

**Shenandoah specific options**

**ZGC specific options**

### 4.2.1 Configuration

## 4.3 Execution

### 4.3.1 DaCapo benchmarks

Tradebeans and h2 have the longest execution times and tend to allocate the largest heaps in the set. Avrora and jython are ofmedium size relative to the benchmarks in the set, while lusearch- fix represents the smaller applications.

GC数据通过GCEasy处理

### 4.3.2 Processing node

### 4.3.3 Query node

## 4.4 Metrics definition

**Throughput percentage：** Percentage of time spent in application workload compared to time spent in GC activity of the total time. Concurrent GC work并不视为GC time

# 5 Results

## 5.1 DaCapo

measurement duration (M-Duration) an indicator of throughput

![image-20211122150234610](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211122150234610.png)

## 5.2 Processing node

### 5.2.1 Default configurations

![image-20211122151449231](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211122151449231.png)

### 5.2.2 Modified configuration

这部分作者主要通过调整一个GC变量与默认的GC配置作比较

## 5.3 Query node

### 5.3.1 Default configuration

### 5.3.2 Modified configuration

# 6 Discussion

ZGC在throughput percentages上表现比G1好，但在运行总时间上没差别，G1GC在本实验中吞吐量更好，与SPECJbb2015测试的结果不同，可能是本实验数据量太小

## 6.1 DaCapo applications

小数据，latency的表现来说，ZGC和Shenandoah比G1好，这里heap的空间足够

## 6.2 Processing node

ZGC会经常遇到matadata occupancy问题，shenandoah会使用 Brooks 指针的收集器，意味着占用更多的内存，但这点占用空间影响较小

## 6.3 Query node

## 6.4 Validity

## 6.5 Limitations

# 7 Conclusions

* demonstrate the importance of garbage collector choice, and the impact of GC parameter tuning on application performance
* confirm the general latency advantage given by ZGC and Shenandoah GC compared to the Garbage First GC
* ZGC should always be run in an environment with adjusted maximum mappings per process to avoid memory mapping failures
* Applications with high heap utilization variation, working on large heaps, optimizing for low latency should consider the Z Garbage Collector firstly and Shenandoah GC secondly.
* Applications processing data in near real-time (normalizing, indexing, analyzing, etc.), and optimizing for low latency, are recommended to use the Z Garbage Collector

## 7.1 Future work

* Future work could further investigate the performance effects of tuning options in singularity and in combination for all collectors. For instance, it would be interesting to evaluate the performance of combinations of some of the modified configurations with the "best" results within a collector and see if their benefits are added on top of each other or if one counteracts the other.
* It could also be interesting to run the ZGC and Shenandoah configurations in the same query node environment but with a smaller heap, testing the theory of over-provisioned heap space

