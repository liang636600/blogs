# Docker

用户可以将镜像内容和创建步骤描述在一个文本文件中，这个文件被称为Dockerfile，通过执行`docker build <docker-file>`命令可以构建出docker镜像
仓库注册服务器（registry）是存放仓库的地方，仓库是存放镜像的地方（每个仓库集中存放一类镜像），通过不同标签区分
docker镜像采用了写时复制（copy on write）的策略，在多个容器之间共享镜像，每个容器在启动的时候并不需要单独复制一份镜像文件，而是将所有镜像层以只读的方式挂载到一个挂载点，再在上面覆盖一个可读写的容器层。如果Docker容器需要改动底层Docker镜像中的文件，则会启动copy on write机制，即先将此文件从镜像层中复制到最上层的可写层中，再对可写层中的副本进行操作。
docker镜像采用统一文件系统（union file system）对各层进行管理。统一文件系统技术能将不同的层整合成一个文件系统，为这些层提供一个统一的视角，这样隐藏了多层的存在，从用户的角度看，只存在一个文件系统
一个镜像仓库中可以包含同一个软件的不同镜像，利用标签进行区别。可以利用`仓库名:标签名`的格式来指定相关软件镜像的版本。例如，`hbliti/nginx:version1.0.test`表示仓库名为hbliti，镜像名为nginx，标签名为version1.0.test。如果要将镜像推送到一个私有的registry，则必须指定一个主机名和端口号来标记此镜像，如192.168.1.103:5000/nginx:version1.1.test

<img src="https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20230326103330470.png" alt="image-20230326103330470" style="zoom: 67%;" />

<img src="https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20230326103542778.png" alt="image-20230326103542778" style="zoom:67%;" />

# Dockerfile

就像自动化脚本（类似于虚拟机中安装操作系统与软件），主要用来创建镜像image

## RUN指令
执行**创建镜像时**的命令。RUN指令有以下两种格式
```
RUN <command>
RUN ["executable","param1","param2"]
```
Dockerfile的每一个指令都会构建新文件层。在AUFS中，所有的镜像最多只能保存126层，而执行一次RUN就会产生一个新文件，并在其上执行命令，执行完毕后提交这一层的修改构成新的镜像。对于一些需要合并为一层的操作，可以使用&&符号将多个命令分割开，使其先后执行
## CMD指令
容器运行镜像后执行的命令
```
格式1 CMD ["executable","param1","param2"]
格式2 CMD ["param1","param2"]
格式3 CMD command param1 param2
```
* 当用户需要脱离shell环境来执行命令时，可以使用格式1的用法，其设定的命令将作为容器启动时的默认执行命令
* 当使用指令格式2时，其中的param作为ENTRYPOINT的默认参数使用
* 当使用指令格式3时，以"/bin/sh -c"的方法执行命令`CMD "/usr/sbin/nginx -c /etc/nginx/nginx.conf"`

在一个Dockerfile中只有最后一条CMD指令生效。
CMD指令与RUN指令的区别是，RUN指令在docker build时执行，而CMD指令在docker run时运行，CMD的首要目的在于为指定的容器指定默认要运行的程序，程序运行结束，容器也就结束了。

CMD指令指定的程序可被docker run命令行参数中指定的要运行的程序覆盖，例如`docker run 镜像名 ls -al` （ls -al可覆盖Dockerfile中CMD ["ls","-a"]）

## ENTRYPOINT指令
容器运行镜像后执行的命令，类似CMD指令，但其不会被docker run的命令行参数指定的指令所覆盖，且这些命令行参数会被当作参数送给ENTRYPOINT指令指定的程序。但是，如果运行docker run时使用了--entrypoint选项，则此选项的参数可当作要运行的程序覆盖ENTRYPOINT指令指定的程序
```
ENTRYPOINT command
ENTRYPOINT ["executable","param1","param2"]
```
当指定了ENTRYPOINT指令时，CMD指令中的命令性质将会发生改变，CMD指令中的内容将会以参数形式传递给ENTRYPOINT指令中的命令。把可能需要变动的参数写到CMD中并在docker run命令中指定参数，这样CMD指令中的参数就会被覆盖，而ENTRYPOINT指令中的参数不会被覆盖

例如，如果Dockerfile中有`ENTRYPOINT ["ls","-a"]`,运行容器`docker run 镜像名 -l`表示`ls -al`，-l 命令是直接拼接在 ENTRYPOINT 命令的后面

```
// 这里表示ENTRYPOINT与CMD结合使用，ENTRYPOINT表示固定不变的命令，CMD表示传入可变的参数，可通过docker run时传入的参数覆盖CMD的参数达到参数可变化的目的
ENTRYPOINT ["ls","-l"]
CMD ["data"]
// 即Dockerfile表示 ls -l data
docker run 镜像名 usr // 表示 ls -l usr，usr覆盖了CMD的data参数
```

## ENV指令
设置环境变量
```
ENV key value
ENV key1=value1 key2=value2
```
## ARG指令
定义构建时需要的参数
`ARG <参数名>[=<默认值>]`
使用ARG指令定义参数，在利用docker build命令创建镜像的时候可使用格式`--build-arg <varname>=<value>`来指定参数

## ADD指令
将主机目录中的文件，目录及一个URL标记的文件复制到镜像中
```
ADD src dest
```
dest指定的路径必须是绝对路径或相对于WORKDIR的相对路径。如果dest指定的路径不存在，则当ADD指令执行时，将会在容器中自动创建此目录
## COPY指令
COPY指令与ADD指令的功能及使用方法基本相同，只是COPY指令不会做自动解压工作
## VOLUME指令
可实现挂载功能，可以将本地文件夹或其他容器的文件夹挂载到某个容器中
```
VOLUME 路径
VOLUME ["路径1","路径2"]
```
VOLUME指令可以将容器及容器产生的数据分离开来，这样，当利用docker rm container命令删除容器时，不会影响相关数据
## EXPOSE指令
声明运行时的容器服务端口
`EXPOSE 端口`
EXPOSE指令只是声明了容器应该打开的端口，实际上并没有打开该端口，在容器启动时，如果不用-p指定要映射的端口，则容器是不会将端口映射出去的，外部网络也无法访问这些端口，这些端口只能被主机中的其他容器访问

## WORKDIR指令
用于设置容器的工作目录
`WORKDIR 工作目录`，Dockerfile文件中允许出现多个WORKDIR，但最终生效的路径是所有WORKDIR指定路径的叠加，WORKDIR可以通过docker run命令中的-w参数进行覆盖

# .dockerignore文件

里面内容如

```
node_modules
Dockerfile
.dockerignore
```

# CGroups

CGroups是Linux内核提供的一种可以限制单个进程或多个进程所使用资源的机制
# 数据卷和数据容器
**数据卷:** 通过在容器中创建数据卷，将本地的目录或文件挂载到数据卷中。数据卷是一个可供容器使用的特殊目录，它将本地主机目录直接映射到容器，可以很方便地将数据添加到容器中供其中的进程使用，多个容器可以共享一个数据卷
**数据卷容器:** 通过使用数据卷容器在容器和主机，容器和容器之间共享数据，实现数据的备份和恢复。如果用户需要在多个容器之间共享一些持久化数据，则可以使用数据卷容器，数据卷容器专门用于提供数据卷供其他容器挂载

---

当删除一个容器时，之前所做的修改，新添加的数据会全部丢失，如果希望保留容器中的数据，Docker提供了volume数据卷

![image-20230326111723103](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20230326111723103.png)

创建数据卷`docker volume create my-finance-data`

随后启动docker容器时通过-v参数指定将这个数据卷挂载到容器中的哪一个路径上`docker run -dp 80:5000 -v my-finance-data:/etc/finance my-finance`，向`/etc/finance`路径写入的任何数据都会被永久保存在这个数据卷中

# Docker Compose
定义和运行**多个Docker容器**应用的工具。Compose用YMAL配置文件来创建和运行所有服务
**服务:** 一个应用的容器，实际上可以包含若干运行相同镜像的容器实例。每个服务都有自己的名称，使用的镜像，挂载的数据卷，所属的网络，依赖的服务等

![image-20230326112649638](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20230326112649638.png)

docker compose管理多个容器，创建docker-compose.yml（在原项目的根目录下创建）文件，通过services来定义多个container

```yml
version:"3" // 表示ymal文件版本

services:
	web: // 容器名字
		build:
		ports:
			- "80:5000"
		volumes:
			- ./:/egg:ro
			- /egg/node_modules
	db:
		image:"mysql"
		environment:
			MYSQL_DATABASE:finance-db // 指定数据库名字
			MYSQL_ROOT_PASSWORD:secret // 指定数据库密码
		volumes:
			- my-finance-data:/var/lib/mysql // 指定数据卷永久存放数据
volumes:
	my-finance-data:
```

![image-20230326112938673](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20230326112938673.png)

使用`docker compose up -d`来运行所有容器，-d表示后台运行; `--build`表示如果镜像有修改，docker-compose就会重建，创建的镜像名为`当前目录名-容器名`

`docker compose down`停止并删除所有容器，新创建的数据卷需要手动删除，除非加了--volumes参数即`docker compose down --volumes`

# 应用程序部署在Docker上

## 1 创建应用程序运行所需环境镜像

**准备Dockerfile**（规定了创建镜像的规则以及运行容器后的CMD）：当前，已经写好了应用程序，在应用程序根目录下创建Dockerfile

![image-20230326110142615](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20230326110142615.png)

```dockerfile
FROM python:3.8-slim-buster // 3.8-slim-buster为tag名
WORKDIR /app //指定了之后所有docker命令的工作路径，若路径不存在，docker会自动创建
COPY . . // 将所有程序拷贝到docker镜像中，第一个参数表示本地路径（.表示程序根目录下的所有文件），第二个参数表示Docker镜像中的路径（.代表当前工作路径，这里为/app）
RUN pip3 install -r requirements.txt // 允许在创建镜像时运行任意的shell命令（RUN是创建镜像时使用的，即docker build）
// 前面的是运行docker build时运行的命令
CMD ["python3", "app.py"] // 指定当docker容器运行起来以后要执行的命令（CMD ["可执行文件","参数1","参数2"]，运行容器时使用的命令）
// CMD是运行docker run后的命令
```

---

**docker build创建镜像：**在命令行中运行`docker build -t my-finance .`（这里my-finance是repository名字，Tag是latest）

docker build创建一个镜像，-t即tag指定了镜像的名字及标签（通常 name:tag或者name），最后的.表示打包当前目录所有文件给docker引擎（表示build构建上下文，需要上传Dockerfile中ADD、COPY命令所需文件的上下文目录，便于这两个命令使用上下文中的文件，就好比使用自己本地的文件一样,build构建成功后，上下文文件会被自动清理）

-f 指定Dockerfile所在的路径，例如`docker build -f /xxx/yyy/zzz -t xxx .`表示Dockerfile 在 /xxx/yyy下，名为zzz；`docker build -f ./Dockerfile -t xxx .`等同于`docker build -t xxx .`

## 2. 启动容器运行镜像

命令行中运行`docker run -p 80:5000 -d my-finance`，返回容器的ID

docker run启动一个容器

-p表示将本地主机端口(80)映射到docker容器中的某个端口(5000)，这样才能从主机上访问容器中的web应用

-d表示让容器在后台运行，容器的输出不会显示在控制台

<img src="https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20230326110818520.png" alt="image-20230326110818520" style="zoom:50%;" />

![image-20230326111412870](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20230326111412870.png)

# docker与kubernetes的区别和联系

我们想使用一个集群的电脑来提供服务并做到负载均衡，故障转移等等

![image-20230326114035280](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20230326114035280.png)

![image-20230326114112301](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20230326114112301.png)

kubernetes就是将你的各个容器分发到一个集群上运行，并进行全自动化管理，包括应用的部署与升级

[参考视频链接](https://www.bilibili.com/video/BV1s54y1n7Ev/?spm_id_from=333.999.0.0&vd_source=85a922d117de064365f871766fa90e4a)