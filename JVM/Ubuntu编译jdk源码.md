# Ubuntu 编译jdk源码

## 一 下载需要的依赖文件

```
sudo apt-get install libfreetype6-dev
sudo apt-get install libcups2-dev
sudo apt-get install libx11-dev libxext-dev libxrender-dev libxrandr-dev libxtst-dev libxt-dev
sudo apt-get install libasound2-dev
sudo apt-get install libffi-dev
sudo apt-get install autoconf
sudo apt-get install -y autoconf zip libx11-dev libxext-dev libxrender-dev libxtst-dev libxt-dev libcups2-dev libfontconfig1-dev libasound2-dev
```



## 二 下载需要编译的jdk源码

比如我想要编译jdk16的源码，源码的[GitHub链接](https://github.com/openjdk/jdk16)，通过git clone到本地，本文中所有的jdk均为openjdk



## 三 下载上一个版本可用jdk

如果想要编译jdk版本为n的源码，一般需要下载版本为n-1的可运行的jdk，这里我下载的是jdk15作为boot jdk，下载openjdk15我尝试了两种方式。

* **使用sudo apt install openjdk-15-jdk**

    这种方式很容易但不推荐，运行后系统自动安装好了jdk15并且配置好了环境变量，输入java -version也是能看到响应信息为jdk15的，缺点就是我找不到jdk15在哪配置的环境变量，比如说我后面想把自己编译好的jdk16作为默认jdk（即输入java -version显示的是jdk16版本），我在/etc/profile文件中修改了JAVA_HOME和path并source后，输入java -version依然是jdk15的版本

* **使用下载的jdk15压缩包并配置环境变量**

  1. 到官网上下载jdk15压缩包（链接：http://jdk.java.net/java-se-ri/15）
  
  2. 解压缩jdk15（tar -zxvf 压缩文件名）

  3. 配置环境变量（修改/etc/profile 文件），添加
  
     `export JAVA_HOME=/usr/lib/jvm/jdk-15
     export CLASSPATH=$JAVA_HOME/lib
     export PATH=:$PATH:$JAVA_HOME/bin`

     JAVA_HOME右边的需要修改成自己的jdk15所在的路径
  
  4. `source /etc/profile`

## 四 编译jdk源码

 1. 进入jdk16的主目录，运行

    `bash configure --with-debug-level=slowdebug --disable-warnings-as-errors`

    或直接运行（跳过之后的2,3部分）`bash configure --enable-option-checking=fatal --with-extra-cxxflags=-Wno-error --with-extra-cflags=-Wno-error --disable-warnings-as-errors --with-debug-level=slowdebug`

    这里的slowdebug是为了更好的看源码设置的

    ```
    bash configure --enable-option-checking=fatal --with-extra-cxxflags=-Wno-error --with-extra-cflags=-Wno-error --disable-warnings-as-errors --with-debug-level=release --with-boot-jdk=/home/yicheng/jdk/jdk16/jdk-16/
    ```

2. 安装bear  `sudo apt install -y bear` 或者直接 `make compile-commands`

3. 最后`bear make images`慢慢等待编译过程了

4. 如果需要使用clion对jdk16源码调试参考博客（https://blog.csdn.net/qq_25117137/article/details/118122978）或直接参考官方博客(https://blog.jetbrains.com/clion/2020/03/openjdk-with-clion/)
