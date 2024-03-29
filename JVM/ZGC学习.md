主要参考链接<https://www.secpulse.com/archives/137305.html>

ZGC适用于大内存低延迟服务的内存管理和回收

ZGC希望在对吞吐量影响不大的前提下，短暂停顿也只与GC Roots大小相关而与堆内存大小无关，实现在任意堆内存大小下都可以把垃圾收集的停顿时间限制在10ms以内的低延迟

# 理论学习

ZGC收集器是一款基于Region内存布局的，（暂时）不设分代的，使用了读屏障、染色指针和内存多重映射等技术来实现可并发的标记-整理算法的，以低延迟为首要目标的一款垃圾收集器

---

ZGC采用基于Region的堆内存布局，ZGC的Region具有动态性——动态创建和销毁，以及动态的区域容量大小，在x64硬件平台下，ZGC的Region可以具有大、中、小三类容量

* 小型Region（Small Region）：容量固定为2MB，用于放置小于256KB的小对象。

* 中型Region（Medium Region）：容量固定为32MB，用于放置大于等于256KB但小于4MB的对象。

* 大型Region（Large Region）：容量不固定，可以动态变化，但必须为2MB的整数倍，用于放置4MB或以上的大对象。每个大型Region中只会存放一个大对象，这也预示着虽然名字叫作“大型Region”，但它的实际容量完全有可能小于中型Region，最小容量可低至4MB。大型Region在ZGC的实现中是不会被重分配（重分配是ZGC的一种处理动作，用于复制对象的收集器阶段，稍后会介绍到）的，因为复制一个大对象的代价非常高昂。

![image-20211202165050817](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211202165050817.png)

---

**染色指针技术**：  

**背景：** 

追踪式收集算法的标记阶段就可能存在只跟指针打交道而不必涉及指针所引用的对象本身的场景。例如对象标记的过程中需要给对象打上三色标记，这些标记本质上就只和对象的引用有关，而与对象本身无关——某个对象只有它的引用关系能决定它存活与否，对象上其他所有的属性都不能够影响它的存活判定结果。

HotSpot虚拟机的几种收集器有不同的标记实现方案，有的把标记直接记录在对象头上（如Serial收集器），有的把标记记录在与对象相互独立的数据结构上（如G1、Shenandoah使用了一种相当于堆内存的1/64大小的，称为BitMap的结构来记录标记信息），而 **ZGC的染色指针是最直接的、最纯粹的，它直接把标记信息记在引用对象的指针上** 。

**内容：** 

染色指针是一种直接将少量额外的信息存储在指针上的技术。在AMD64架构中只支持到52位（4PB）的地址总线和48位（256TB）的虚拟地址空间，所以目前64位的硬件实际能够支持的最大内存只有256TB。此外，操作系统一侧也还会施加自己的约束，64位的Linux则分别支持47位（128TB）的进程虚拟地址空间和46位（64TB）的物理地址空间，64位的Windows系统甚至只支持44位（16TB）的物理地址空间。

![image-20211202194530161](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211202194530161.png)

* Finalizable：表示是否只能通过finalize()方法才能被访问到，其他途径不行；

* Remapped：表示是否进入了重分配集（即被移动过）；

* Marked1、Marked0：表示是否被标记，在gc周期性更换，这样可以不要重复去复原（就像以前survivor的复制回收算法，也就是这次用mark0表示，下次就用mark1，在用mark1标记时顺便把mark0复原，在用mark0标记时顺便把mark1复原）

对于linux而言，剩下的46位中将其高4位提取出来存储四个标志信息。通过这些标志位，虚拟机可以直接从指针中看到其引用对象的三色标记状态、是否进入了重分配集（即被移动过）、是否只能通过finalize()方法才能被访问到。缺点是直接导致ZGC能够管理的内存不可以超过4TB（2的42次幂），也不能支持压缩指针（-XX:+UseCompressedOops）

**优点：**

* **染色指针可以使得一旦某个Region的存活对象被移走之后，这个Region立即就能够被释放和重用掉，而不必等待整个堆中所有指向该Region的引用都被修正后才能清理**
* 染色指针可以大幅减少在垃圾收集过程中内存屏障的使用数量，ZGC目前不支持分代收集没有使用写屏障，只使用了读屏障，ZGC对吞吐量的影响也相对较低
* 染色指针可以作为一种可扩展的存储结构用来记录更多与对象标记、重定位过程相关的数据，以便日后进一步提高性能。现在Linux下的64位指针还有前18位并未使用，可以通过其他手段用于信息记录

**染色指针随意重新定义内存中某些指针的其中几位，操作系统是否支持？处理器是否支持？**

Linux/x86-64平台上的ZGC使用了多重映射（Multi-Mapping）将多个不同的虚拟内存地址映射到同一个物理内存地址上，这是一种多对一映射，意味着ZGC在虚拟内存中看到的地址空间要比实际的堆内存容量来得更大。把染色指针中的标志位看作是地址的分段符，那只要将这些不同的地址段都映射到同一个物理内存空间，经过多重映射转换后，就可以使用染色指针正常进行寻址了

![image-20211207104900724](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211207104900724.png)

---

**工作流程：**

![image-20211207112125792](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211207112125792.png)

![image.png](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image203-1024x399.png)

* 并发标记（Concurrent Mark）：与G1、Shenandoah一样，并发标记是遍历对象图做可达性分析的阶段，前后也要经过类似于G1、Shenandoah的初始标记、最终标记（尽管ZGC中的名字不叫这些）的短暂停顿，而且这些停顿阶段所做的事情在目标上也是相类似的。与G1、Shenandoah不同的是， **ZGC的标记是在指针上而不是在对象上进行的，标记阶段会更新染色指针中的Marked 0、Marked 1标志位** 。
* 并发预备重分配（Concurrent Prepare for Relocate）： **这个阶段需要根据特定的查询条件统计得出本次收集过程要清理哪些Region，将这些Region组成重分配集（Relocation Set）** 。重分配集与G1收集器的回收集（Collection Set）还是有区别的，ZGC划分Region的目的并非为了像G1那样做收益优先的增量回收。相反， **ZGC每次回收都会扫描所有的Region，用范围更大的扫描成本换取省去G1中记忆集的维护成本** 。因此， **ZGC的重分配集只是决定了里面的存活对象会被重新复制到其他的Region中，里面的Region会被释放，而并不能说回收行为就只是针对这个集合里面的Region进行** ，因为 **标记过程是针对全堆的** 。此外，在JDK 12的ZGC中开始支持的类卸载以及弱引用的处理，也是在这个阶段中完成的。
* 并发重分配（Concurrent Relocate）：重分配是ZGC执行过程中的核心阶段，这个过程要把 **重分配集中的存活对象复制到新的Region上，并为重分配集中的每个Region维护一个转发表（Forward Table），记录从旧对象到新对象的转向关系** 。得益于染色指针的支持， **ZGC收集器能仅从引用上就明确得知一个对象是否处于重分配集之中** （relocate指针）， **如果用户线程此时并发访问了位于重分配集中的对象，这次访问将会被预置的内存屏障所截获，然后立即根据Region上的转发表记录将访问转发到新复制的对象上，并同时修正更新该引用的值，使其直接指向新对象，ZGC将这种行为称为指针的“自愈”（Self-Healing）能力** 。这样做的好处是只有第一次访问旧对象会陷入转发，也就是只慢一次，对比Shenandoah的Brooks转发指针，那是每次对象访问都必须付出的固定开销，简单地说就是每次都慢，因此ZGC对用户程序的运行时负载要比Shenandoah来得更低一些。还有另外一个直接的好处是由于染色指针的存在， **一旦重分配集中某个Region的存活对象都复制完毕后，这个Region就可以立即释放用于新对象的分配（但是转发表还得留着不能释放掉）** ，哪怕堆中还有很多指向这个对象的未更新指针也没有关系，这些旧指针一旦被使用，它们都是可以自愈的。
* 并发重映射（Concurrent Remap）：重映射所做的就是 **修正整个堆中指向重分配集中旧对象的所有引用** ，这一点从目标角度看是与Shenandoah并发引用更新阶段一样的，但是ZGC的并发重映射并不是一个必须要“迫切”去完成的任务，因为前面说过，即使是旧引用，它也是可以自愈的，最多只是第一次使用时多一次转发和修正操作。重映射清理这些旧引用的主要目的是为了不变慢（还有清理结束后可以释放转发表这样的附带收益），所以说这并不是很“迫切”。因此，ZGC很巧妙地把并发重映射阶段要做的工作， **合并到了下一次垃圾收集循环中的并发标记阶段里去完成** ，反正它们都是要遍历所有对象的，这样合并就节省了一次遍历对象图[9]的开销。一旦所有指针都被修正之后，原来记录新旧对象关系的转发表就可以释放掉了。

**概念补充：**

* **读屏障：**当对象从堆中加载的时候，就会使用到读屏障（Load Barrier）。这里使用读屏障的主要作用就是检查指针上的三色标记位，根据标记位判断出对象是否被移动过，如果没有可以直接访问，如果移动过就需要进行“自愈”（对象访问会变慢，但也只会有一次变慢），当“自愈”完成后，后续访问就不会变慢了。

* **自愈能力：** **在ZGC中，当读取处于重分配集的对象时，会被读屏障拦截，通过 转发表 记录将访问转发到新复制的对象上，并同时修正更新该引用的值，使其直接指向新对象。**

---

**对比ZGC与Shenandoah：**

他们主要在解决对象移动与用户线程并发时采用策略不同

* ZGC使用 **转发表** 记录对象旧地址与新地址的对应关系，通过自愈完成引用从旧地址到新地址的更改
* Shenandoah在对象旧地址处使用Brooks指针，当引用访问旧地址时，Brooks指针指向新地址

Shenandoah每次访问旧地址都涉及到转向开销（每个引用次次慢），而ZGC只是引用自愈的时候涉及到转向开销（每个引用只慢一次）， **ZGC的运行负载低**

ZGC在重分配集中的某个region存活对象移动完后，可以立即释放该region（只保存转发表即可），而Shenandoah则要在所有引用更新后才能释放该region， **ZGC的region释放快**

---

**对比ZGC和G1：**

* G1需要通过写屏障来维护记忆集，才能处理跨代指针，得以实现Region的增量回收。

  **缺点：** 记忆集要占用大量的内存空间，写屏障也对正常程序运行造成额外负担

* ZGC就完全没有使用记忆集，连分代都没有

  **优点：** 给用户线程带来的运行负担小得多

  **缺点：** 由于没有设置分代，能承受的对象分配速率不会太高

---

![image-20211211153139419](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211211153139419.png)

![image-20211211153247929](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211211153247929.png)

# ZGC实践

**重要参数配置样例：**

-Xms10G -Xmx10G 

-XX:ReservedCodeCacheSize=256m -XX:InitialCodeCacheSize=256m 

-XX:+UnlockExperimentalVMOptions -XX:+UseZGC 

-XX:ConcGCThreads=2 -XX:ParallelGCThreads=6 

-XX:ZCollectionInterval=120 -XX:ZAllocationSpikeTolerance=5 

-XX:+UnlockDiagnosticVMOptions -XX:-ZProactive 

-Xlog:safepoint,classhisto*=trace,age*,gc*=info:file=/opt/logs/logs/gc-%t.log:time,tid,tags:filecount=5,filesize=50m 



**-Xms：** 初始堆大小

**-Xmx：** 最大堆大小

这里都设置为10G，程序的堆内存将保持10G不变。

**-XX:ReservedCodeCacheSize -XX:InitialCodeCacheSize**: 设置CodeCache的大小， JIT编译的代码都放在CodeCache中，一般服务64m或128m就已经足够。

**-XX:+UnlockExperimentalVMOptions -XX:+UseZGC**：启用ZGC的配置。

**-XX:ConcGCThreads**：并发回收垃圾的线程。默认是总核数的12.5%，8核CPU默认是1。调大后GC变快，但会占用程序运行时的CPU资源，吞吐会受到影响。

**-XX:ParallelGCThreads**：STW阶段使用线程数，默认是总核数的60%。

**-XX:ZCollectionInterval**：ZGC发生的最小时间间隔，单位秒。

**-XX:ZAllocationSpikeTolerance**：ZGC触发自适应算法的修正系数，默认2，数值越大，越早的触发ZGC。

**-XX:+UnlockDiagnosticVMOptions -XX:-ZProactive**：是否启用主动回收，默认开启，这里的配置表示关闭。

**-Xlog**：设置GC日志中的内容、格式、位置以及每个日志的大小。

---

**理解ZGC触发时机**

ZGC有多种GC触发机制，总结如下：

- **阻塞内存分配请求触发**：当垃圾来不及回收，垃圾将堆占满时，会导致部分线程阻塞。我们应当避免出现这种触发方式。日志中关键字是“Allocation Stall”。
- **基于分配速率的自适应算法**：最主要的GC触发方式，其算法原理可简单描述为”ZGC根据近期的对象分配速率以及GC时间，计算出当内存占用达到什么阈值时触发下一次GC”。自适应算法的详细理论可参考彭成寒《新一代垃圾回收器ZGC设计与实现》一书中的内容。通过ZAllocationSpikeTolerance参数控制阈值大小，该参数默认2，数值越大，越早的触发GC。我们通过调整此参数解决了一些问题。日志中关键字是“Allocation Rate”。
- **基于固定时间间隔**：通过ZCollectionInterval控制，适合应对突增流量场景。流量平稳变化时，自适应算法可能在堆使用率达到95%以上才触发GC。流量突增时，自适应算法触发的时机可能会过晚，导致部分线程阻塞。我们通过调整此参数解决流量突增场景的问题，比如定时活动、秒杀等场景。日志中关键字是“Timer”。
- **主动触发规则**：类似于固定间隔规则，但时间间隔不固定，是ZGC自行算出来的时机，我们的服务因为已经加了基于固定时间间隔的触发机制，所以通过-ZProactive参数将该功能关闭，以免GC频繁，影响服务可用性。日志中关键字是“Proactive”。
- **预热规则**：服务刚启动时出现，一般不需要关注。日志中关键字是“Warmup”。
- **外部触发**：代码中显式调用System.gc()触发。日志中关键字是“System.gc()”。
- **元数据分配触发**：元数据区不足时导致，一般不需要关注。日志中关键字是“Metadata GC Threshold”。

---

**理解ZGC日志**

![image-20211212110539434](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211212110539434.png)

注意：该日志过滤了进入安全点的信息。正常情况，在一次GC过程中还穿插着进入安全点的操作。

GC日志中每一行都注明了GC过程中的信息，关键信息如下：

- **Start**：开始GC，并标明的GC触发的原因。上图中触发原因是自适应算法。
- **Phase-Pause Mark Start**：初始标记，会STW。
- **Phase-Pause Mark End**：再次标记，会STW。
- **Phase-Pause Relocate Start**：初始转移，会STW。
- **Heap信息**：记录了GC过程中Mark、Relocate前后的堆大小变化状况。High和Low记录了其中的最大值和最小值，我们一般关注High中Used的值，如果达到100%，在GC过程中一定存在内存分配不足的情况，需要调整GC的触发时机，更早或者更快地进行GC。
- **GC信息统计**：可以定时的打印垃圾收集信息，观察10秒内、10分钟内、10个小时内，从启动到现在的所有统计信息。利用这些统计信息，可以排查定位一些异常点。

---

**理解ZGC停顿原因**

在实战过程中共发现了6种使程序停顿的场景，分别如下：

- **GC时，初始标记**：日志中Pause Mark Start。

- **GC时，再标记**：日志中Pause Mark End。

- **GC时，初始转移**：日志中Pause Relocate Start。

- **内存分配阻塞**：当内存不足时线程会阻塞等待GC完成，关键字是"Allocation Stall"。

- **安全点**：所有线程进入到安全点后才能进行GC，ZGC定期进入安全点判断是否需要GC。先进入安全点的线程需要等待后进入安全点的线程直到所有线程挂起。

- **dump线程、内存**：比如jstack、jmap命令。

  ![image.png](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image207-1024x61.png)

  ![image.png](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image208-1024x85.png)

---

