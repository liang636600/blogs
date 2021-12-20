# fork模式

整个开发流程大致如下：

1. 在github上进行fork
2. 将1的仓库克隆至本地开发环境
3. 在本地环境中创建feature分支
4. 在feature分支进行代码修改和提交
5. 将feature分支push到1的仓库中
6. 在github上对fork来源仓库发送pull request

**具体例子：**

初始的时候

![image-20211211110155017](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211211110155017.png)

然后我在本地进行开发，先根据upstream/main（即甲的main分支）创建一个feature-A分支并且将feature-A分支publish到我的github远端去

![image-20211211111026763](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211211111026763.png)

然后我在本地进行feature-A分支的功能开发，开发完后（我的github远端的feature-A分支与本地同步即一样），feature-A分支先与upstream/main分支作比较，然后把upstream/main merge into feature-A分支，有冲突解决冲突，最后feature-A分支发送pull request给upstream/main分支（即甲的main分支）

![image-20211211112933021](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211211112933021.png)

# 不进行fork的开发流程

![IMG_20211210_201505](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/IMG_20211210_201505.jpg)

# 以部署为中心的开发模式

整个开发流程大致如下：

1. 令master分支时常保持可以部署的状态
2. 进行新的作业时要从master分支创建新分支，新分支名称要具有描述性
3. 在2新建的本地仓库分支中进行提交
4. 在github端仓库创建同名分支，定期push
5. 需要帮助或反馈时创建pull request，以pull request进行交流
6. 让其他开发者进行审查，确认作业完成后与master分支合并
7. 与master分支合并后立即部署

**核心：** 从master分支上创建一个新的feature分支，在该feature分支上开发，开发完后pull request到master分支（pull request的时候需要其他人的review及自己所做的新功能有效和不影响前面功能的测试）

![1639139383973](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/1639139383973.jpg)

如果想要特定人来审查，可以在评论中加上@用户名

pull request不一定非要在与master分支合并时才使用，尽早创建pull request让其他开发者进行审查，一边听取反馈一边写代码，pull request具有显示差别以及对单行代码插入评论的功能

比如我提交了一个pull request，甲帮忙review发现问题，他可以在出现问题的行进行评论，然后我在本地仓库上修改后push到远端，不需要新建一个pull request，我的修改在刚刚那个pull request中看的到。评论的人如果有权限也可以直接修改，同样会有commit记录。

![image-20211210205838872](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211210205838872.png)

自己在feature分支上实现了新功能过后，一般还需要测试（测试新功能没有问题并且没有影响前面的功能），从克隆代码起到最后提交pull request需要有一下 **测试过程：**

1. 将master分支更新到最新状态
2. 在自己的开发环境中确认通过所有测试
3. 从master分支创建新分支
4. 编写新功能测试代码
5. 编写实现目标功能的代码
6. 确认通过所有测试并且没有出现退步现象（Regression）
7. 发送pull request请求合并到master分支

**建议：**

* 减少pull request的体积
* 不要积攒pull request3

# 以发布为中心的开发模式

整个开发流程大致如下：

1. 从develop分支创建feature分支，进行功能的实现或修正
2. feature分支修改结束后，与develop分支进行合并
3. 重复1,2不断实现功能直到可以发布
4. 创建用于发布的release分支，处理发布的各项工作
5. 发布工作完成后与master分支合并，打上版本tag标签进行发布
6. 如果发布的软件出现bug，以打了标签的版本为基础进行修正（hotfixes）

**核心：** master分支，hotfixes分支，release分支，develop分支，feature分支

![1639142612631](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/1639142612631.jpg)

**master分支：** 时常保持软件可以运行的状态，不允许开发者直接对master分支的代码进行修改和提交，发布时附加包含tag

**develop分支：** 开发过程中的代码中心分支，不允许开发者直接进行修改和提交，develop分支维持着开发过程中的最新源代码

**feature分支：** 开发按下述流程进行

1. 从develop分支创建feature分支
2. 在feature分支中实现目标功能
3. 通过github向develop分支发送pull request
4. 接受其他开发者审查后，将pull request合并到develop分支，合并后，可以删除该feature分支

**release分支：**

只处理与发布前准备相关的提交比如版本编号变更，如果软件部署到预演环境后经测试发现bug，相关的修正也要提交给这个分支。该分支绝不可以包含需求变更或功能变更等重大修正

![1639147177401](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/1639147177401.jpg)

**hotfix分支：** 是一个紧急应对措施，只有当前发布的版本中出现bug或漏洞，而且其严重程度要求开发方立即处理，无法等到下一个版本发布时，hotfix分支才会被创建。因此，hotfix分支都是以发布版本的标签或master分支为起点

如果hotfix分支与develop分支合并时出现异常，在develop分支中尽快修复相关问题。hotfix分支只对master分支的内容进行最小限度的修改，hotfix分支在于master分支和develop分支合并之后可以被删除。

![1639147919193](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/1639147919193.jpg)

---

## 版本号的分配规则

在用x.y.z格式进行版本管理时规则如下

* x在重大功能变更或新版本不向下兼容时加1，此时y与z数字归为0
* y在添加新功能或删除已有功能时加1，此时z的数字归为0
* z只在进行内部修改后加1

![1639148239265](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/1639148239265.jpg)
