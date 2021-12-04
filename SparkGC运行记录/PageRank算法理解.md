# 理论

1. 数据格式
   links 的数据结构是 （pageId, linkList）元素组成； ranks 的数据结构是 （pageId , rank）组成 。 

2. 算法逻辑
   （1） 每个页面rank值初始化 位 1 
   （2） 针对page m页 面 .，向其每个邻页面发送一个 贡献值c，贡献值 c = rank(p) /numberneighbors(p)  
   （3） 将每个页面的排序值 计算值设置为 0.15 + 0.85 * 贡献值 c

   针对 （2）和（3）步骤进行无限迭代，最终每个页面的排序值 rank是收敛的，此时认为该值是 页面的排序值 rank

3. PageRank算法原理 
   PageRank的计算充分利用了两个假设：数量假设和质量假设。步骤如下：       1）在初始阶段：网页通过链接关系构建起Web图，每个页面设置相同的PageRank值，通过若干轮的计算，会得到每个页面所获得的最终PageRank值。随着每一轮的计算进行，网页当前的PageRank值会不断得到更新。       2）在一轮中更新页面PageRank得分的计算方法：在一轮更新页面PageRank得分的计算中， **每个页面将其当前的PageRank值平均分配到本页面包含的出链上** ，这样每个链接即获得了相应的权值。 **而每个页面将所有指向本页面的入链所传入的权值求和，即可得到新的PageRank得分** 。当每个页面都获得了更新后的PageRank值，就完成了一轮PageRank计算。  
   如果网页T存在一个指向网页A的连接，则表明T的所有者认为A比较重要，从而把T的一部分重要性得分赋予A。这个重要性得分值为：PR（T）/L(T) 　    其中PR（T）为T的PageRank值，L(T)为T的出链数         则A的PageRank值为一系列类似于T的页面重要性得分值的累加。         即一个页面的得票数由所有链向它的页面的重要性来决定，到一个页面的超链接相当于对该页投一票。一个页面的PageRank是由所有链向它的页面（链入页面）的重要性经过递归算法得到的。一个有较多链入的页面会有较高的等级，相反如果一个页面没有任何链入页面，那么它没有等级。 

---

# 模拟

输入数据

第一列包含指向第二列的链接

```
2	1
2	4
3	2
3	5
4	1
5	3
6	7
```

把数据转为links即

```
2->(1,4)
3->(2,5)
4->1
5->3
6->7
```

拓扑图如下

![image-20211203194714720](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211203194714720.png)

经过第一次迭代ranks值如下，ID为(1,2,3,4,5,7)有rank值

```
1 1.5
2 0.5
3 1
4 0.5
5 0.5
7 1
```

后续从第2次迭代到第10次迭代只有ID为(1,2,3,4,5)有rank值

最后输出为

```
(4,0.293960882548143)
(5,0.33873148834857175)
(2,0.33873148834857175)
(3,0.437921765096286)
(1,0.5464423708967147)
```

分析：正常来讲，最终有rank值的id为原输入中的第二列数据的子集

```scala
for (i <- 1 to iters) {
    // ranks是最新的，即（id，rankValue），因为不一定links中原始key每个在ranks中都存在，所以join一下，这样也会导致links中贡献权值的key减少
    val contribsTemp = links.join(ranks).values
    // contribsTemp is like List((list(follower),rankValue))
    // 计算links中贡献权值的key对neighbor的权值贡献值大小，简单而言neighbor均分了links中key的权值
    val contribs = contribsTemp.flatMap{ case (urls, rank) =>
        val size = urls.size
        urls.map(url => (url, rank / size))
    }
    // contribs is like list((follower, rank)), for example (618183,0.1111111111111111)
    // 对neighbor进行reduceByKey操作，这样得到每个neighbor的rank值（不是最终的）
    val ranksTemp = contribs.reduceByKey(_ + _)
    // 最后进行加权得到最终的rank值
    ranks=ranksTemp.mapValues(0.15 + 0.85 * _)
    // ranks is like list((numberID,rankValue)), for example (24589345,0.15084999999999998)
}
```

