# 一 配置SSH免密码登录

一个Master，两个slaves

1. 每个设备执行以下相同操作

   **(1) SSH在线安装与启动：** 命令行输入`sudo apt-get install ssh` ，输入`/etc/init.d/ssh start` 

   **(2) 生成公钥和私钥：** 在命令行输入`ssh-keygen -t rsa -P ''`,按回车即可，在`/root/.ssh`文件夹下生成了id_rsa(私钥)与id_rsa.pub(公钥)文件，通过输入`cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys`命令将公钥加到authorized_keys文件（该文件用于保存所有允许以当前用户身份登录到ssh客户端用户的公钥内容）中

   **(3) 修改文件权限** `chmod 600 ~/.ssh/authorized_keys`

   **(4) 测试SSH能否免密码登录** 在终端输入`ssh localhost`,如果出现welcome字样成功

2. 在Slave1节点上的.ssh目录下执行`scp id_rsa.pub driverliang@ubuntu:/home/driverliang/.ssh/id_rsa.pub.slave1 `

3. ssh 192.168.233.129  cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys 

