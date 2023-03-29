# 安装

https://segmentfault.com/a/1190000043336588?utm_source=sf-similar-article

# 运行Hello World

## Clone

* `docker run --name repo alpine/git clone https://github.com/docker/getting-started.git`

  运行容器（容器名repo），镜像名`alpine/git`，本地找不到镜像`alpine/git:latest`，远端下载`alpine/git`镜像

* `docker cp repo:/git/getting-started/ .`

  移动文件夹，在本地有了getting-started文件夹

  ![image-20230328210811808](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20230328210811808.png)

## Build

* `cd getting-started`

* `docker build -t docker101tutorial .`

  镜像名docker101tutorial

## Run

* `docker run -d -p 80:80 --name docker-tutorial docker101tutorial`

  容器名docker-tutorial

## Share

* `docker tag docker101tutorial liang22/docker101tutorial`

  镜像名重命名

* `docker push liang22/docker101tutorial`

  push到docker hub

# vscode连接docker容器

右键具体container->attach in new window，即进入容器内部

![image-20230329163447518](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20230329163447518.png)

可以通过拖拽的方式上传文件

* 安装vscode插件

  `docker`，`dev-containers`，`remote-ssh`

## ssh连接容器

增加用户权限`sudo gpasswd -a 当前登录用户名 docker`

重启服务器`sudo reboot`

