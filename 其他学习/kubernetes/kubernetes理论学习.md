# kubernetes
kubernetes用于管理云平台中多个主机的容器化应用，在docker技术的基础上，为容器化的应用提供部署运行，资源调度，服务发现和动态伸缩等一系列功能，提高了大规模容器集群管理的便捷性。
kubernetes的主要目标是让部署容器化的应用简单且高效，提供了一种应用部署，规划，更新和维护机制

# 核心概念
## Master
负责管理集群，提供了集群的资源数据访问入口，包含以下关键组件
**API Server:** kubernetes中所有资源的增删改查等操作指令的唯一入口，任何对资源进行操作的指令都要交给API Server处理后再提交给etcd
**Controller Manager:** kubernetes所有资源对象的自动化控制中心。可以理解为每个资源都对应一个控制器，而controller manager负责管理这些控制器
**Scheduler:** 负责资源调度（Pod调度），负责调度Pod到合适的node上
**etcd:** 一个高可用的键值存储系统，kubernetes使用它来存储各个资源的状态，从而实现restful的api。kubernetes所有持久化状态都保存在etcd中

这些服务提供了API来收集和展现集群的当前状态，并在节点之间分配Pod，用户始终与master的API直接交互，其为整个集群提供了一个统一视图
## Node
Node是kubernetes集群架构中运行Pod的服务节点，每个Node主要由3个模块组成
**runtime:** 容器运行环境，目前kubernetes支持docker环境
**kube-proxy:** 实现kubernetes service的通信和负载均衡机制的重要组件
**kubelet:** 是master在每个node上的代理，它负责维护和管理该node上的所有容器，但如果某容器不是通过kubernetes创建的，则node不会管理此容器。负责控制docker，向master报告自己的状态和配置节点级别的资源

## Pod
Pod是若干容器的组合，一个Pod内的容器必须运行在同一台宿主机上，这些容器使用相同的命名空间，IP地址和端口，可以通过localhost互相发现和通信，可以共享一块存储卷空间
Pod有两种类型:静态Pod和普通Pod。

* 静态Pod并不存在于etcd存储中，而是存放在某个node的具体文件中，且只能在此node上启动。

* 普通Pod一但被创建，就会被放入到etcd存储中，随后会被master调度到某个具体的node上进行绑定，该Pod被对应的node上的kubelet进程实例化为一组相关的Docker容器并启动，一个Pod中的应用容器共享一组资源

## replication controller
当应用托管在kubernetes后，replication controller负责保证应用持续运行。RC用于管理Pod的副本，保证集群中存在指定数量的Pod副本。当集群中副本的数量大于指定数量时，会终止指定数量之外的多余容器，反之，会启动少于指定数量的容器，以保证数量不变
## Service
Service是真实应用服务的抽象，定义了Pod的逻辑上的集合和访问Pod集合的策略。Service将代理Pod对外表现为一个单一的访问接口，外部不需要了解Pod如何运行
## Label
kubernetes中的任意API对象都是通过Label进行标识的，Label以key/value的形式附加到各种对象上，如Pod，Service，RC，Node等，以识别这些对象并管理关联关系等，如管理Service和Pod的关联关系。一个资源对象可以定义任意数量的Label，同一个Label也可以被添加到任意数量的资源对象上
## Volume
Volume是Pod中能够被多个容器访问的共享目录。Volume被定义在Pod上，Pod内的容器可以访问挂载volume。volume与Pod的生命周期相同，与具体的docker容器的生命周期不相关，某个docker容器删除或终止时，volume中的数据不会丢失
![IMG_20211217_113027](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/IMG_20211217_113027.jpg)

# kubernetes的操作流程
1. 通过kubectl和kubernetes API，提交一个创建RC的请求，该请求通过API Server被写入到etcd中。该RC请求包含一个Pod模板和一个希望得副本数。
2. controller manager通过API Server监听资源变化的接口监听到该RC请求，如果当前集群中没有其所对应的Pod实例，则根据RC中的Pod模板定义生成一个Pod对象，并通过API Server写入etcd
3. Scheduler通过查看集群的当前状态（有那些可用节点及各节点有哪些可用资源）执行相应的调度流程，将新的pod绑定到指定节点上，并通过API Server将该结果写入到etcd
4. 该节点上的kubelet会监测分配给其所在节点的Pod组中的变化，并根据情况来启动和终止Pod。其过程包括在需要时对存储卷进行配置，将docker镜像下载到指定节点中，以及通过docker API来启动和终止某个容器
