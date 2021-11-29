创建用户目录`hdfs dfs -mkdir -p /user/iscas`

在hadoop目录下再创建一个input文件夹`hdfs dfs -mkdir /user/iscas/input`

在根目录下创建一个input文件夹`hdfs dfs -mkdir /input`

删除在根目录下面创建的input文件夹`hdfs dfs -rm -r /input`

查询`hdfs dfs -ls /user`

根目录为/，比如在根目录下创建一个文件夹为`hdfs dfs -mkdir /input` 

查看文件内容`hdfs dfs -cat /user/iscas/input/he.txt`

创建文件的两种方式

1. `touch hello.txt`
2. 本地写好，上传文件至指定目录

上传文件至hdfs指定路径`hdfs dfs -put /home/iscas/Desktop/hello.txt  /user/iscas/input`

下载hdfs文件系统中的文件到本地`hdfs dfs -get /user/iscas/input/he.txt /home/iscas/Desktop`

运行一个小样例`hadoop jar ~/Downloads/hadoop-3.3.1/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.3.1.jar grep input output 'dfs[a-z.]+'`，查看结果`hdfs dfs -cat output/*`

![image-20211129195435609](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211129195435609.png)

在hdfs文件系统中拷贝文件`hdfs dfs -cp input/myLocalFile.txt  /input`
