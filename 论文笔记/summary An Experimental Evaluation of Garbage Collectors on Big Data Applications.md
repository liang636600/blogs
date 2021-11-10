* **题目：** An Experimental Evaluation of Garbage Collectors on Big Data Applications

* **场景或问题：** 目前在大数据环境下，gc算法无法适应大数据应用的数据特点

* **结论：** 

  * 造成不同垃圾回收器性能不同的原因主要是大数据应用**独特的内存使用模式和计算特点** (the patterns of **long-lived accumulated records** and **humongous data objects**)
  * 在回收long-lived shuffled数据的同时，并发的垃圾回收器（CMS与G1）可以减少gc暂停时间，但由于CPU争抢严重也会阻碍CPU密集型的数据算子
  * 缺乏对数据对象生命周期的了解，在管理大量数据对象方面，这三个垃圾回收器仍然低效
  * 由于三种垃圾回收器不能正确分配容纳long-lived shuffled数据的堆的大小，我们建议使用通过**内存使用预测和动态内存空间调整**的堆内存重整策略
  * 当回收long-lived shuffled and cached数据，三种垃圾回收器都会经历非必要的连续gc，通过利用数据的生命周期，我们提出一种**新的对象标记算法**（**lifecycle-aware object marking algorithm**）
  * 对每一次迭代都需要回收大量shuffled 数据的迭代型应用，三种垃圾回收算法性能均低效。利用这些shuffled数据独特的生命周期和固定的大小，我们提出一种**新的对象清除算法** （分配一个固定的连续空间来容纳这些每个迭代产生的long-lived accumulated records）来实现迭代应用不会有gc暂停的目的

  除此外，我们确定了两种OOM错误的根本原因，即spark框架在处理连续shuffle溢出的内存泄漏与G1的堆碎片问题

* **思路或核心算法：** 通过对三种gc在四种大数据应用下的性能评测，分析比较三种gc的表现，然后提出针对性建议