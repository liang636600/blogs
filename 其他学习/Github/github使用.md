# 分支比较

当前分支与分支A作比较，会出现behind(n1)与ahead(n2)，假如一个节点表示一次commit

![image-20211209153202551](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211209153202551.png)

上图表示分支A与当前分支在绿色节点一样，截止到橙色节点，分支A commit了三次，当前分支commit了两次，如果当前分支与分支A作比较，会出现behind(3) ahead(2)，把分支A merge到当前分支有一下两种方式

1. **create a merge commit:** 当前分支merge完后，当前分支就有了分支A上的最新状态了。当前分支再次与分支A作比较，behind(0) ahead(2+1)，ahead加1是加上了刚刚merge的一次commit，这样当前分支即有了分支A的最新状态并且ahead分支A 3个commit

   当前分支与分支A产生冲突时（比如当前分支修改了文件F第一行为"master"，分支A修改文件F第一行为"produce"）,当前分支与分支A作比较，behind(1) ahead(1)

   ![image-20211209162605876](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211209162605876.png)

   当前分支merge的时候，产生冲突，如下图

   ![image-20211209160800695](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211209160800695.png)

   这里是在当前分支 `merge 分支A into 当前分支`，因此current change是当前分支做的改变即“master”，incoming change是分支A做的改变即“produce”，以上有四种选择都可（Accept current change，accept incoming change， accept both changes， compare changes），我这里选择`accept both changes`并保存文件F（此时的文件F是当前分支的文件F，分支A的文件F不受影响），下图是当前分支的文件F 

   ![image-20211209161749902](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211209161749902.png)

   merge后，当前分支有了分支A的最新状态，当前分支再次与分支A作比较，behind(0) ahead(1+1)

   当前分支与分支A比较发现，ahead(0)，behind(1)，然后当前分支merge分支A，在history里面出现的是分支A的最新的commit概述，而不是merge branch 分支A

2. **squash and merge：** squash and merge将分支A的多次commit压缩成了一次commit，merge过后，当前分支再次与分支A作比较，发现仍然是behind(3) ahead(2+1)，ahead加1的意思就是刚刚squash一次，但再次选择squash and merge的时候，提示没有什么改变，感觉使用squash and merge容易在compare branch的时候产生混淆

   **可以先在分支A处把3次commit squash一下，后面直接create a merge commit**

3. **rebase：** 如果当前分支相对分支A没有ahead的commit，则无法rebase，如下图

   ![image-20211209171648721](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211209171648721.png)

   示例：

   ![image-20211209172313751](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211209172313751.png)

   当前分支rebase后的结果

   ![image-20211209172410947](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211209172410947.png)

   即当前分支上所做的commit到了最前面（橙色节点），分支A所做的commit镶嵌到了蓝色节点和橙色节点的中间，从当前分支的history中也可以看到

   ![image-20211209172627530](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211209172627530.png)

   没有体现出来rebase操作记录（merge操作时commit有记录），好像是在当前分支上做的一样

   **当有冲突的时候：**

   ![image-20211209203010707](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211209203010707.png)

   ![image-20211209202620257](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211209202620257.png)

   当前分支rebase分支A，以分支A为中心，incoming change就是当前分支的改变即“master”，current change就是分支A上的改变即“produce”。这里选择了incoming changes即“master”

   ![image-20211209203206045](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211209203206045.png)

**比较merge与rebase** ，merge操作过后会留下merge commit而rebase不会有类似的rebase commit，merge commit在当前分支的最新commit位置，而rebase则是把分支A的commit 放在 `两分支的base` 与 `当前分支ahead` 之间

|        | 特点                                                         | 优点                                       | 缺点                                                         |
| ------ | ------------------------------------------------------------ | ------------------------------------------ | ------------------------------------------------------------ |
| marge  | 自动创建一个新的commit，如果合并的时候遇到冲突，仅需要修改后重新commit | 记录了真实的commit情况，包括每个分支的详情 | 因为每次merge会自动产生一个merge commit，所以在使用一些git 的GUI tools，特别是commit比较频繁时，看到分支很杂乱 |
| rebase | 会合并之前的commit历史                                       | 得到更简洁的项目历史，去掉了merge commit   | 如果合并出现代码问题不容易定位，因为re-write了history        |

如果你想要一个干净的，没有merge commit的线性历史树，那么你应该选择git rebase
如果你想保留完整的历史记录，并且想要避免重写commit history的风险，你应该选择使用git merge

# gist

gist主要用于存放一些小的代码片段（以文件的形式）

创建gist：打开<https://gist.github.com/>就是新建一个gist

查看自己的所有gists：选择your gists

![image-20211210140630133](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211210140630133.png)

分享：通过gist链接分享，拷贝链接即可

