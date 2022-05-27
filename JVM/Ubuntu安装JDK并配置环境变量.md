一.下载JDK

下载链接:https://www.oracle.com/java/technologies/downloads/

二.解压

三.配置环境变量

(安装vim: `sudo apt install vim`)

1.解压后打开terminal，输入`sudo vim /etc/profile`

2.在`/etc/profile`前面部分输入

```
export JAVA_HOME=~/openjdk-11/jdk-11（这里是bin目录的上一级）
export PATH=$JAVA_HOME/bin:$PATH
```

3.输入命令`source /etc/profile`

4.重启电脑在terminal中输入`java -version`查看效果

