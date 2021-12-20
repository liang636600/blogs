# 分支策略

## 主线分支开发

![1639148453102](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/1639148453102.jpg)

![1639148509298](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/1639148509298.jpg)

## 功能分支部署

![1639148688042](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/1639148688042.jpg)

![1639149082904](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/1639149082904.jpg)

## 状态分支

git项目使用的分支命名约定是状态分支策略的一个很有意思的变种，它拥有以下四种专门命名的集成分支

* maint

  这个分支包含了git最近一次稳定发布的代码以及小数点版本的额外提交（维护）

* master

  这个分支包含应该进入下一次发布的提交

* next

  这个分支用于测试一些主题在进入master分支后的稳定性

* pu

  这个建议的更新（proposed updates）分支包含尚未准备好合并的提交

![1639187400327](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/1639187400327.jpg)

## 计划部署

计划部署与git工作流里的“以发布为中心的开发模式”一样

![1639187885821](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/1639187885821.jpg)

