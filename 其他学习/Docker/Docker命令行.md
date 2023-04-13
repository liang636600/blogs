# docker服务

```shell
service docker start #启动docker 
service docker restart #重启docker 
service docker status #查看运行状态
service docker stop #停掉服务
```

```SHELL
systemctl start docker  #启动docker
systemctl restart docker  #重启docker
systemctl status docker  #查看运行状态
systemctl enable docker #设置开机自动启动
```

# 镜像

* 查看镜像列表 `docker images`

* 给镜像取名字 `docker tag imageID 名字` 如 `docker tag e6f dansoncut/nodejs:v1.0`这里repository是dansoncut/nodejs（用户名/镜像名）,tag是v1.0（版本）

* 删除镜像 `docker rmi -f dansoncut/nodejs:v1.0`,-f表示强制执行

* 根据容器生成新镜像 `docker commit -a="作者" -m="描述信息" -c 容器id 目标镜像名:[TAG]`

  `-p`，在commit时，将容器暂停

# 容器

* 运行新容器 `docker run 镜像名 ls -al` （ls -al可覆盖Dockerfile中CMD ["ls","-a"]）

  如果没有运行docker pull 命令，而直接运行docker run命令，则该run命令会自动运行pull从远程仓库抽取镜像，然后自动运行容器

  * 运行时定义容器名字 加上`--name myname`

  * 退出容器后删除容器 加上`--rm`，--rm选项不能与-d同时使用，即只能自动清理foreground容器，不能自动清理detached容器

  * 将本地文件夹与容器执行文件夹绑定 `-v /users/Desktop/yi/:/egg`

    本地文件夹内容只可读（即容器文件改变，本地文件不变） `-v /users/Desktop/yi/:/egg:ro`

    想要容器中的文件不随本地文件改变而改变 新加`-v /egg/node_modules`,表示容器中文件/egg/node_modules不随本地文件改变而改变

* 启动被停止的容器 `docker start 容器名` 或 重启容器`docker restart 容器名`

* 停止容器 `docker stop 容器名`

* 与容器进行交互 `docker exec -it 容器名 /bin/sh` 

  * -it表示交互，以terminal的形式
  * `/bin/sh`表示执行一个新的bash shell，想要退出输入`exit`

* 列出所有容器（存活） `docker ps`，返回 容器ID Image Command 使用端口号

  * 所有容器包括停止的 `-a`

* 停止容器运行 `docker stop 容器ID`

* 删除容器 `docker rm -f 容器ID`

  删除容器时同时删除数据卷 `docker rm -fv  容器名`

* 保存容器为image `docker commit <CONTAINER ID> <your-image-name>`

# 容器与主机之间

* 数据拷贝 `docker cp`
  * 将主机/www/runoob目录拷贝到容器96f7f14e99ab的/www目录下 
  
    `docker cp /www/runoob 96f7f14e99ab:/www/`
  
  * 将容器96f7f14e99ab的/www目录拷贝到主机的/tmp目录中 `docker cp  96f7f14e99ab:/www /tmp/`
  
  * `-r`参数表示递归复制

# 数据卷

* 删除数据卷
  *  删除某容器的所有volume`docker rm -fv 容器名`

# Docker hub

* 登录账号 `docker login`
* 推送镜像到docker hub ` docker push dansoncut/nodejs:v1.0`
* 从docker hub上拉镜像 `docker pull 镜像名<:tags>`

# 镜像保存与载入

* 保存镜像为tar压缩包 `docker save -o my_ubuntu_v3.tar runoob/ubuntu:v3`
* 载入tar压缩包镜像 `docker load -i my_ubuntu_v3.tar`