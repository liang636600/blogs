# ubuntu anaconda切换python3到python2

1. 确保安装conda

   `conda --version`

2. 查看你的系统当前已有的Python环境，执行命令：**conda info --envs**

3. 现在，我想添加一个Python2.7的环境，执行命令：**conda create --name python27 python=2.7**，命令中我制定了环境名称是python27，指定了Python版本是2.7，执行命令后，Conda会自动下载最新版的Python2.7，并自动部署

4. 查看我们当前使用的Python版本，执行命令：**python --version**

5. 切换Python环境到刚才新添加的Python2.7，执行命令：**activate python27**，然后执行命令：**python --version**，查看是否切换成功

6. 在Python27环境下，完成工作后，切回原来的Python环境，执行命令：**deactivate python27/ activate base** 两个都可以

7. 如果刚才添加的Python27环境，不再使用，可通过执行命令：**conda remove --name python27 --all**，进行删除