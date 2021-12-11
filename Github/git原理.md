
git放在对象库里的对象只有四种类型

* 块（blob）
  文件的每个版本表示为一个块
  
* 目录树（tree）

* 提交（commit）

  每一个提交对象指向一个目录树对象

* 标签（tag）

---

.gitignore文件
以#开头的行可以用于注释
一个简单的字面置文件名匹配任何目录中的同名文件
目录名由末尾的/标记，能匹配同名的目录和子目录
包含shell通配符如debug/*.o
每个.gitignore只影响该目录及子目录

---

# git命令行

显示版本号`git --version`

初始化仓库`git init`

查看仓库的状态`git status`，可以显示当前在哪个分支，可以看到对git的工作树或仓库进行的操作

向暂存区添加文件`git add`，暂存区是提交前的一个临时区域

保存仓库的历史记录`git commit`，可以将当前暂存区的文件实际保存到仓库的历史记录中，通过这些记录，我们就可以在工作树中复原文件

* 记录提交概述信息，例如`git commit -m "first commit"`
* 记录详细提交信息，执行`git commit`后会提醒输入，第一行是概述，第二行空行，第三行详细信息

一次性执行add与commit命令`git commit -am "概述信息"` 

---

查看提交日志`git log`

![image-20211210143339499](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211210143339499.png)

只显示每个提交的概述信息`git log --pretty=short`

只显示某目录或某文件的log `git log 目录名或文件名`

显示文件的改动`git log -p 目录名或文件名`

以图表形式查看分支`git log --graph`

---

查看工作树与暂存区前后的差别`git diff`，如果工作树和暂存区一样，就只会显示工作树和最新commit的差别

比较暂存区与最近commit的内容`git diff --cached`

比较工作区与最近commit的内容`git diff HEAD`

---

显示所有分支`git branch`，*表示当前所在的分支

显示包括remote在内的所有分支`git branch -a`

创建分支`git branch feature-A`

切换分支`git checkout feature-A`

合并分支，在master分支下`git merge --no-ff feature-A`

以图表形式查看分支`git log --graph`

---

回溯到某历史版本`git reset --hard 哈希值`，从该哈希值之后的commit也全部消失了

假设目前是这样的

![image-20211210153146200](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211210153146200.png)

突然发现master的红色节点的地方有一个bug，于是master通过`git reset --hard 红色节点哈希值`直接回到红色节点，然后新建一个分支fix-B来解决这个bug，解决完后想要merge fix-B分支到master的橙色节点。

git log命令只能查看以当前状态为终点的历史日志，这里使用`git reflog`，查看当前仓库的操作日志，在日志中找出回溯历史之前的哈希值即橙色节点哈希值，通过命令`git reset --hard 橙色节点哈希值`回复到回溯历史之前的状态

总结一下就是以下步骤

1. master分支回溯到红色节点（`git reset实现`）
2. master分支创建新的fix-B branch
3. master分支快进到橙色节点（`git reset`实现）
4. master分支合并fix-B分支（需要仔细解决冲突，而不是全盘接受fix-B的内容）

![image-20211210161122408](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211210161122408.png)

---

添加远程仓库`git remote add origin git@github.com:username/repoName.git`

推送至远程仓库`git push`，`git push -u origin master`，推送当前分支至origin的master分支，-u参数可以在推送的同时，将origin仓库的master分支设置为本地仓库当前分支的upstream

---

克隆远程仓库到本地`git clone https://github.com/RegiusGal/liangTest.git`

列出所有分支`git branch -a`

![image-20211210165030327](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211210165030327.png)

本地只有main分支，如果想要获得远程的my1分支，`git checkout -b my1 origin/my1`

如果整个项目是从用户甲fork过来的，，github desktop采用甲/项目的模式，也可以在github desktop的branch选项点击`upstream/某分支`，自动在本地创建该分支，我的github远端是没有该分支的，在本地修改该分支，有push upstream的选项，但实际上不行（因为权限不够，只能是collaborator才使用这种方法）。

github desktop出现的branch分三部分

* 我本地的branch
* 我github远端的origin修饰（我在本地有一个分支A，要想给upstream发送pull request，我的github远端也要有分支A）
* upstream远端的（必然存在upstream/main）

获取最新的远程仓库分支`git pull origin feature-D`

---

配置提交作者和邮件`git config --global user.name "John"`与`git config --global user.email "abc@163.com"`

