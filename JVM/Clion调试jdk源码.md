环境：ubuntu20+jdk16源码

主要步骤参考`https://blog.csdn.net/qq_25117137/article/details/118122978`

![在这里插入图片描述](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/20210623003207697.png)

在Edit Configurations的时候，这里选择的java文件是`build/linux-x86_64-server-fastdebug/jdk`目录下的，如果选择images目录下的jdk，就会没有效果

还需要注意的是如果要使用clion调试jdk的话，不要随意移动位置

![image-20221105213446499](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20221105213446499.png)

# 命令行java调试

如图，配置Run/Debug Configurations如下

![image-20230312154744800](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20230312154744800.png)

# 问题

## 1 debug时碰到optimized out，看不到变量值

![image-20230312171446633](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20230312171446633.png)

* 尝试1？

  使用c++的话，CMakeLists增加：

  ```cpp
  set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} -O0")
  ```