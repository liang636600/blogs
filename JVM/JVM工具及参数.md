# 一 内存

## heap dump

### jmap

```
jmap -dump:live,format=b,file=d:/beforeGc.hprof 2556
```

file表示输出的文件路径，2556表示进程的pid

### HeapDumpOnOutOfMemoryError

```
-XX:+HeapDumpOnOutOfMemoryError
-XX:HeapDumpPath=JVM_analysis
```

HeapDumpPath表示堆转储快照文件的保存路径和文件名

## IDEA中的profiler

### 名词解释

* shallow

  对象本身占用内存的大小，不包含其引用的对象

* retained

  Retained size是该对象自己的shallow size，加上仅从该对象能直接或间接访问到对象的shallow size之和

  **retained size是该对象被GC之后所能回收到内存的总和**

* 举例1

  <img src="D:%5CBackUp%5C%E5%AD%A6%E4%B9%A0%E8%B5%84%E6%96%99%5C%E5%9B%BE%E7%89%87%5Cimage-20230831201627838.png" alt="image-20230831201627838" style="zoom: 50%;" />

  三个都是Student类型（单个对象大小为36），红色表示retained的值，他们三个的shallow都是36（stu本身大小）

  <img src="D:%5CBackUp%5C%E5%AD%A6%E4%B9%A0%E8%B5%84%E6%96%99%5C%E5%9B%BE%E7%89%87%5Cimage-20230831201408054.png" alt="image-20230831201408054" style="zoom:50%;" />

* 举例2

  <img src="D:%5CBackUp%5C%E5%AD%A6%E4%B9%A0%E8%B5%84%E6%96%99%5C%E5%9B%BE%E7%89%87%5Cimage-20230831210152814.png" alt="image-20230831210152814" style="zoom:50%;" />

  三个都是Student类型（单个对象大小为36），红色表示retained的值，他们三个的shallow都是36（stu本身大小）

  ![image-20230831210110977](D:%5CBackUp%5C%E5%AD%A6%E4%B9%A0%E8%B5%84%E6%96%99%5C%E5%9B%BE%E7%89%87%5Cimage-20230831210110977.png)

#### 某一对象右侧具体内容

* Shortest Path

  从该对象到gc root的最短路径，展示的时候从该对象到gc root

  <img src="file://D:/BackUp/%E5%AD%A6%E4%B9%A0%E8%B5%84%E6%96%99/%E5%9B%BE%E7%89%87/image-20230831201627838.png?lastModify=1693484418" alt="image-20230831201627838" style="zoom:50%;" />

  ![image-20230831202120679](D:%5CBackUp%5C%E5%AD%A6%E4%B9%A0%E8%B5%84%E6%96%99%5C%E5%9B%BE%E7%89%87%5Cimage-20230831202120679.png)

* incoming reference

  查看对象被哪些对象引用

  ![image-20230831202549653](D:%5CBackUp%5C%E5%AD%A6%E4%B9%A0%E8%B5%84%E6%96%99%5C%E5%9B%BE%E7%89%87%5Cimage-20230831202549653.png)

  ![image-20230831203221237](D:%5CBackUp%5C%E5%AD%A6%E4%B9%A0%E8%B5%84%E6%96%99%5C%E5%9B%BE%E7%89%87%5Cimage-20230831203221237.png)

* Dominator Tree 支配树

  与retained相似，在 Dominator tree 中展开树状图，可以查看支配关系路径（与 outgoing reference 的区别是：如果 X 支配 Y，则 X 释放后 Y必然可释放；如果仅仅是 X 引用 Y，可能仍有其他对象引用 Y，X 释放后 Y 仍不能释放，所以 Dominator tree 去除了 incoming reference 中大量的冗余信息）

  

  Dominator tree 的起点并不一定是 GC根，且通过 Dominator tree 可能无法获取到最开始的创建路径，但 incoming references 是可以的

  ![image-20230831203454024](D:%5CBackUp%5C%E5%AD%A6%E4%B9%A0%E8%B5%84%E6%96%99%5C%E5%9B%BE%E7%89%87%5Cimage-20230831203454024.png)

  ![image-20230831205233137](D:%5CBackUp%5C%E5%AD%A6%E4%B9%A0%E8%B5%84%E6%96%99%5C%E5%9B%BE%E7%89%87%5Cimage-20230831205233137.png)

  * 举例

    <img src="D:%5CBackUp%5C%E5%AD%A6%E4%B9%A0%E8%B5%84%E6%96%99%5C%E5%9B%BE%E7%89%87%5Cimage-20230901205403501.png" alt="image-20230901205403501" style="zoom:50%;" />

    stu3为dominator tree的树根

    ![image-20230901205533225](D:%5CBackUp%5C%E5%AD%A6%E4%B9%A0%E8%B5%84%E6%96%99%5C%E5%9B%BE%E7%89%87%5Cimage-20230901205533225.png)

* Dominator

  ![image-20230831203433347](D:%5CBackUp%5C%E5%AD%A6%E4%B9%A0%E8%B5%84%E6%96%99%5C%E5%9B%BE%E7%89%87%5Cimage-20230831203433347.png)

  ![image-20230831205303112](D:%5CBackUp%5C%E5%AD%A6%E4%B9%A0%E8%B5%84%E6%96%99%5C%E5%9B%BE%E7%89%87%5Cimage-20230831205303112.png)

# 参考资料

[一文深度讲解JVM 内存分析工具 MAT及实践](https://zhuanlan.zhihu.com/p/350935330)