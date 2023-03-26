# 镜像

* 查看镜像列表 `docker images`
* 给镜像取名字 `docker tag imageID 名字` 如 `docker tag e6f dansoncut/nodejs:v1.0`这里repository是dansoncut/nodejs（用户名/镜像名）,tag是v1.0（版本）
* 删除镜像 `docker rmi -f dansoncut/nodejs:v1.0`,-f表示强制执行

# 容器

* 运行容器 `docker run 镜像名 ls -al` （ls -al可覆盖Dockerfile中CMD ["ls","-a"]）

  * 运行时定义容器名字 加上`--name myname`

  * 将本地文件夹与容器执行文件夹绑定 `-v /users/Desktop/yi/:/egg`

    本地文件夹内容只可读（即容器文件改变，本地文件不变） `-v /users/Desktop/yi/:/egg:ro`

    想要容器中的文件不随本地文件改变而改变 新加`-v /egg/node_modules`,表示容器中文件/egg/node_modules不随本地文件改变而改变

* 与容器进行交互 `docker exec -it 容器名 /bin/sh` 

  * -it表示交互，以terminal的形式
  * `/bin/sh`表示执行一个新的bash shell，想要退出输入`exit`

* 列出所有容器 `docker ps`，返回 容器ID Image Command 使用端口号

  * 所有容器包括停止的 `-a`

* 停止容器运行 `docker stop 容器ID`

* 删除容器 `docker rm -f 容器ID`

# 数据卷

* 删除数据卷
  *  删除某容器的所有volume`docker rm -fv 容器名`

# Docker hub

* 登录账号 `docker login`
* 推送镜像到docker hub ` docker push dansoncut/nodejs:v1.0`