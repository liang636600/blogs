设置两个分支，一个main分支，一个dev分支（dev分支是两个主版本之间短暂存活的，进行许多次小的修改）

![image-20211209145613753](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211209145613753.png)

如图所示，main分支里面的每个节点都是经过审核过的（节点可以创建tag表示一下），然后在蓝色节点的时候，新建一个branch为dev分支，dev分支进行修改（比如说重新排版，由一栏变为两栏），修改完后，经过审核，merge dev into main（可以选择squash and merge这样可以合并commit为一个），不会发生冲突

如果dev分支在排版的时候总是排不对（即原文件已经排版混乱了），想要恢复到蓝色节点时候，就可以选择对提交的commit进行revert操作，这样就可以实现对论文的版本管理
