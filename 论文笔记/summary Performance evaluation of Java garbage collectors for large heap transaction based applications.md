* **题目：** Performance evaluation of Java garbage collectors for large heap transaction based applications

* **场景或问题：** ZGC，shenandoah，G1性能比较

* **结论：**

  一种garbage collector configuration不适用所有应用。Shenandoah GC和ZGC在 latency, average pause time, maximum pause time, and total accumulated stop-the-world time都比G1表现好，在throughput and execution time他们三差不多，G1比另外两个在heap over-provisioning的时候更稳定。

* **思路或核心算法：**

  使用三个程序对ZGC，shenandoah，G1评测，评测时第一次使用默认配置，第二次更改某一个配置变量

  