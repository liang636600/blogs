# idea中运行spark程序

前面参考<https://blog.csdn.net/boling_cavalry/article/details/87510822>

在运行到

![image-20211119184819263](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211119184819263.png)

添加spark/jars时，由于我的spark是从源码编译的，因此添加`sparkJDK16Bin/assembly/target/scala-2.12/jars`这个路径的jars

最后在运行的时候配置vm参数`--illegal-access=permit`即可运行

# 打包成jar

在项目结构界面中选择“Artifacts”,在右边操作界面选择绿色”+”号，选择添加JAR包的”From modules with dependencies”方式，在该界面中选择主函数入口为HelloObj

![image-20211119204934908](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211119204934908.png)

然后选择菜单栏build->build artifacts build，打包编译完成

![image-20211119205127533](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211119205127533.png)

在IDEA中运行jar

在edit configurations中选择+，确定主函数入口为HelloObj，vm参数设置为`--illegal-access=permit -Dspark.master=local -Dspark.jars=/home/iscas/IdeaProjects/HelloScala/out/artifacts/HelloScala_jar/HelloScala.jar`

![image-20211119205257593](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20211119205257593.png)

