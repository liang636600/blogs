# GC Roots

在Java技术体系里面，固定可作为GC Roots的对象包括以下几种：

* 在虚拟机栈（栈帧中的本地变量表）中引用的对象，譬如各个线程被调用的方法堆栈中使用到的参数、局部变量、临时变量等。
* 在方法区中类静态属性引用的对象，譬如Java类的引用类型静态变量。
* 在方法区中常量引用的对象，譬如字符串常量池（String Table）里的引用。
* 在本地方法栈中JNI（即通常所说的Native方法）引用的对象
* Java虚拟机内部的引用，如基本数据类型对应的Class对象，一些常驻的异常对象（比如NullPointExcepiton、OutOfMemoryError）等，还有系统类加载器
* 所有被同步锁（synchronized关键字）持有的对象
* 反映Java虚拟机内部情况的JMXBean、JVMTI中注册的回调、本地代码缓存等

# 确定对象死亡

要真正宣告一个对象死亡，至少要经历两次标记过程：如果对象在进行可达性分析后发现没有与GC Roots相连接的引用链，那它将会被第一次标记，随后进行一次筛选，筛选的条件是此对象是否有必要执行finalize()方法。假如对象没有覆盖finalize()方法，或者finalize()方法已经被虚拟机调用过，此对象也将被回收。

如果虚拟机认为该对象需要执行一下finalize方法，则会把该对象放入F-Queue队列中，随后由一线程运行该对象的finalize方法（不确保一定能运行完，因为某对象的finalize方法可能用时很长），如果该对象的finalize方法中有其他存活对象引用它，则它可以继续存活

# 回收方法区

方法区垃圾回收的性价比较低，方法区的垃圾收集主要回收两部分内容：废弃的常量和不再使用的类型。

判断常量是否被回收：如果没有对象引用该常量且虚拟机中也没有其他地方引用该常量，则被回收

判断类是否被回收：同时满足三条件

* 该类所有的实例都已经被回收
* 加载该类的类加载器已经被回收，通常是很难达成的
* 该类对应的java.lang.Class对象没有在任何地方被引用，无法在任何地方通过反射访问该类的方法

关于是否要对类型进行回收，HotSpot虚拟机提供了-Xnoclassgc参数进行控制，还可以使用-verbose：class以及-XX：+TraceClass-Loading、-XX：+TraceClassUnLoading查看类加载和卸载信息，其中-verbose：class和-XX：+TraceClassLoading可以在Product版的虚拟机中使用，-XX+TraceClassUnLoading参数需要FastDebug版的虚拟机支持


# 垃圾收集算法
## 分代收集理论

**弱分代假说（Weak Generational Hypothesis）：** 绝大多数对象都是朝生夕灭的

**强分代假说（Strong Generational Hypothesis）：** 熬过越多次垃圾收集过程的对象就越难以消亡。

**跨代引用假说（Intergenerational Reference Hypothesis）：** 跨代引用相对于同代引用来说仅占极少数。如果是年轻代指向老年代的引用我们不用关心，因为即使Minor GC把年轻代的对象清理掉了，程序依然能正常运行，而且随着引用链的断掉，无法被标记到的老年代对象会被后续的Major GC回收。如果是老年代指向年轻代的引用，那这个引用在Minor GC阶段是不能被回收掉的，那如何解决这个问题呢？

最简单的实现方式当然是每个对象中记录这个跨Region引用记录，GC时扫描所有老年代的对象，显然这是一个相当大的Overhead。

最合理的实现方式只需在  **新生代上建立一个全局的数据结构（该结构被称为“记忆集”，Remembered Set），这个结构把老年代划分成若干小块，标识出老年代的哪一块内存会存在跨代引用 。此后当发生Minor GC时，只有包含了跨代引用的老年代小块内存里的对象才会被加入到GCRoots进行扫描**。虽然这种方法需要在对象改变引用关系时维护记录数据的正确性，会增加一些运行时的开销，但比起收集时扫描整个老年代来说仍然是划算的。

* 新生代收集（Minor GC/Young GC）：指目标只是新生代的垃圾收集。

* 老年代收集（Major GC/Old GC）：指目标只是老年代的垃圾收集。目前只有CMS收集器会有单独收集老年代的行为。另外请注意“Major GC”这个说法现在有点混淆，在不同资料上常有不同所指，读者需按上下文区分到底是指老年代的收集还是整堆收集。

* 混合收集（Mixed GC）：指目标是收集整个新生代以及部分老年代的垃圾收集。目前只有G1收集器会有这种行为。

* 整堆收集（Full GC）：收集整个Java堆和方法区的垃圾收集

## 根节点枚举

枚举根节点时是必须要停顿的

**解决枚举根节点问题：** 当用户线程停顿下来之后，并不需要一个不漏地检查完所有执行上下文和全局的引用位置，虚拟机应当是有办法直接得到哪些地方存放着对象引用的。**在HotSpot的解决方案里，是使用一组称为OopMap的数据结构来达到这个目的** 。一旦类加载动作完成的时候，HotSpot就会把对象内什么偏移量上是什么类型的数据计算出来，在即时编译过程中，也会在特定的位置记录下栈里和寄存器里哪些位置是引用。这样收集器在扫描时就可以直接得知这些信息了，并不需要真正一个不漏地从方法区等GC Roots开始查找

## 安全点

**为什么引入安全点：** Hotspot使用新的数据结构保存GC root,但不可能每行指令都保存gc root，因此只在程序的某些地方保存gc root，而这些地方就是安全点。

HotSpot没有为每条指令都生成OopMap，只是在“特定的位置”记录了这些信息，这些位置被称为安全点（Safepoint）。安全点的设定，也就决定了用户程序执行时并非在代码指令流的任意位置都能够停顿下来开始垃圾收集，而是强制要求必须执行到达安全点后才能够暂停。

**何时产生安全点：** 指令序列的复用，例如方法调用、循环跳转、异常跳转等都属于指令序列复用，只有具有这些功能的指令才会产生安全点

**如何在垃圾收集发生时让所有线程都跑到最近的安全点，然后停顿下来：** 

* 抢先式中断（Preemptive Suspension）：在垃圾收集发生时，系统首先把所有用户线程全部中断，如果发现有用户线程中断的地方不在安全点上，就恢复这条线程执行，让它一会再重新中断，直到跑到安全点上。现在几乎没有虚拟机实现采用抢先式中断来暂停线程响应GC事件。
* 主动式中断（Voluntary Suspension）：当垃圾收集需要中断线程的时候，不直接对线程操作，仅仅简单地设置一个标志位，各个线程执行过程时会不停地主动去轮询这个标志，一旦发现中断标志为真时就自己在最近的安全点上主动中断挂起。轮询标志的地方和安全点是重合的，另外还要加上所有创建对象和其他需要在Java堆上分配内存的地方，这是为了检查是否即将要发生垃圾收集，避免没有足够内存分配新对象。

## 安全区域

**为什么引入安全区域：** 某些线程处于sleep状态或blocked状态时，没法通过抢先式中断或主动式中断跑到对应的安全地方，因此引入安全区域解决该问题

**安全区域是指能够确保在某一段代码片段之中，引用关系不会发生变化，因此，在这个区域中任意地方开始垃圾收集都是安全的。** 我们也可以把安全区域看作被扩展拉伸了的安全点

当用户线程执行到安全区域里面的代码时，首先会标识自己已经进入了安全区域，那样当这段时间里 **虚拟机要发起垃圾收集时就不必去管这些已声明自己在安全区域内的线程了** 。当线程要离开安全区域时，它要检查虚拟机是否已经完成了根节点枚举（或者垃圾收集过程中其他需要暂停用户线程的阶段），如果完成了，那线程就当作没事发生过，继续执行；否则它就必须一直等待，直到收到可以离开安全区域的信号为止。

## 记忆集和卡表

**为什么引入记忆集和卡表：** 某些老年代跨代引用新生代，在minor gc的时候，为避免扫描全部的老年代对象，把存在跨代引用的老年代对象所在的区域记录下来为记忆集，以后只需要扫描记忆集而不需要扫描整个老年代

**记忆集和卡表关系：** 记忆集是抽象的数据结构，卡表是记忆集的具体实现

## 写屏障

**为什么引入写屏障：** 解决卡表元素如何维护的问题，例如它们何时变脏、谁来把它们变脏等

**何时变脏：** 有其他分代区域中对象引用了本区域对象时，其对应的卡表元素就应该变脏，变脏时间点原则上应该发生在引用类型字段赋值的那一刻

写屏障就是对一个对象引用进行写操作（即引用赋值）之前或之后附加执行的逻辑

**写屏障就是在将引用赋值写入内存之前，先做一步mark card——即将出现跨代引用的内存块对应的卡页置为dirty**

JVM参数`-XX:+UseCondCardMark`，就是开启有条件的写屏障：在将卡页置为dirty之前，先检查它是否已经为dirty状态，如果已经是了，就不必再执行mark card动作，以避免虚共享

## 并发的可达性分析

**三色标记:** 把遍历对象图过程中遇到的对象，按照“是否访问过”这个条件标记成以下三种颜色

* **白色：表示对象尚未被垃圾收集器访问过** 。显然在可达性分析刚刚开始的阶段，所有的对象都是白色的，若在分析结束的阶段，仍然是白色的对象，即代表不可达
* **黑色：表示对象已经被垃圾收集器访问过，且这个对象的所有引用都已经扫描过** 。黑色的对象代表已经扫描过，它是安全存活的，如果有其他对象引用指向了黑色对象，无须重新扫描一遍。黑色对象不可能直接（不经过灰色对象）指向某个白色对象。
* **灰色：表示对象已经被垃圾收集器访问过，但这个对象上至少存在一个引用还没有被扫描过**

对象只有被黑色对象引用才能存活，扫描完成后，黑色对象就是存活对象，白色对象就是可回收对象

如果用户线程与收集器是并发工作，收集器在对象图上标记颜色，同时用户线程在修改引用关系——即修改对象图的结构，这样可能出现两种后果

* 一种是把原本消亡的对象错误标记为存活，下次收集清理掉就好
* 另一种是把原本存活的对象错误标记为已消亡，程序肯定会因此发生错误

举例：

![image-20211202165217030](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211202165217030.png)

当且仅当以下两个条件同时满足时，会产生“对象消失”的问题，即原本应该是黑色的对象被误标为白色：

* 赋值器插入了一条或多条从黑色对象到白色对象的新引用；

* 赋值器删除了全部从灰色对象到该白色对象的直接或间接引用

解决并发扫描时对象消失问题，只需要破坏这两个条件的任意一个，两种解决方案：增量更新与原始快照

* 增量更新破坏的是第一个条件，当黑色对象插入新的指向白色对象的引用关系时，就将这个新插入的引用记录下来，等并发扫描结束之后，再将这些记录过的引用关系中的黑色对象为根，重新扫描一次。简化理解为，黑色对象一旦新插入了指向白色对象的引用之后，它就变回灰色对象了
* 原始快照当灰色对象要删除指向白色对象的引用关系时，就将这个要删除的引用记录下来，在并发扫描结束之后，再将这些记录过的引用关系中的灰色对象为根，重新扫描一次。简化理解为，无论引用关系删除与否，都会按照刚刚开始扫描那一刻的对象图快照来进行搜索

CMS是基于增量更新来做并发标记的，G1、Shenandoah则是用原始快照来实现

相比起增量更新算法，原始快照能够减少并发标记和重新标记阶段的消耗，避免CMS那样在最终标记阶段停顿时间过长的缺点，但是在用户程序运行过程中确实会产生由跟踪引用变化带来的额外负担

