Write Barrier：前面修改的变量如果还在store buffer中，后面修改的变量也要在store buffer中，而不能直接到cache line中（修改变量的有序性，防止出现先修改的变量对其他CPU不可见，后修改的变量对其他CPU可见）

```
void foo(void) 
{ 
    a = 1; 
    smp_wmb(); // write barrier
    b = 1; 
} 
```

Read Barrier：解决因为 Invalidate Queue 的存在，CPU 可能读到旧值的问题，遇到read barrier，将invalidate queue中的数据做标记，当CPU读数据时，先处理invalidate queue中的标记数据

```
// CPU 0 执行 foo(), a 处于 Shared，b 处于 Exclusive
void foo(void) 
{ 
    a = 1; 
    smp_wmb();
    b = 1; 
} 
// CPU 1 执行 bar()，a 处于 Shared 状态
void bar(void)
{
    while (b == 0) continue; 
    smp_rmb();
    assert(a == 1);
} 
```

----

硬件层的内存屏障
硬件层的内存屏障分为两种：Load Barrier 和 Store Barrier即读屏障和写屏障。

Load Barrie：在指令前插入Load Barrier，可以让高速缓存中的数据失效，强制从新从主内存加载数据；

Store Barrie：在指令后插入Store Barrier，能让写入缓存中的最新数据更新写入主内存，让其他线程可见。

---

如果GC有load barrier(读屏障)，则在从堆读取引用时，GC需要执行一些额外操作。在Java中,也就是当每次执行像这样的代码 obj.field 时需要额外操作

# 参考资料

内存屏障及其在-JVM 内的应用（上）：https://segmentfault.com/a/1190000022497646?utm_source=sf-similar-article

内存屏障及其在 JVM 内的应用（下）：https://segmentfault.com/a/1190000022508589

