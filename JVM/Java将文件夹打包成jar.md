在命令窗口下跳转到存放MANIFEST.MF文件的目录下执行下面的命令：

```
jar cvfm classes.jar MANIFEST.MF 要打包的文件夹路径名称
```

以上命令将要打包的文件夹下所有文件打包到classes.jar,生成在当前目录下

---

[参考链接](https://www.cnblogs.com/mq0036/p/8566427.html#a11)

* 打包单个class文件

  最终生成的jar包结构

  > META-INF
  > Hello.class

  1. 创建jar包 `jar -cvf hello.jar Hello.class`

     c表示要创建一个新的jar包，v表示创建的过程中在控制台输出创建过程的一些信息，f表示给生成的jar包命名

  2. 添加Main-Class属性

     用压缩软件打开hello.jar，会发现里面多了一个META-INF文件夹，里面有一个MENIFEST.MF的文件，用记事本打开

     在第三行的位置写入 Main-Class: Hello （注意冒号后面有一个空格，整个文件最后有一行空行），保存

  3. 运行jar包 `java -jar hello.jar`

* 含有两个类的jar包

  最终生成的jar包结构

  > META-INF
  > Tom.class
  > Hello.class

  1. 用记事本写一个Hello.java和一个Tom.java的文件

     ```java
     public class Tom{
         public static void speak() {
             System.out.println("hello");
         }
     }
     ```

     ```java
     public class Hello{
         public static void main(String[] args) throws Exception {
             Tom.speak();
         }
     }
     ```

  2. 编译 ` javac Hello.java`

     此时Hello.java和Tom.java同时被编译，因为Hello中调用了Tom，在编译Hello的过程中发现还需要编译Tom

  3. 生成jar包

     创建META-INF文件夹，准备MENIFEST.MF文件，内容为

     ```
     Manifest-Version: 1.0
     Created-By: 1.8.0_121 (Oracle Corporation)
     Main-Class: Hello
     
     ```

     注意：最后有一个换行符

     打包命令 `jar -cvfm hello.jar META-INF\MENIFEST.MF Hello.class Tom.class`

     该命令表示用第一个文件当做MENIFEST.MF文件，hello.jar作为名称，将Hello.class和Tom.class打成jar包。其中多了一个参数m，表示要定义MENIFEST文件

  4. 运行jar包 `java -jar hello.jar`

* 有目录结构的jar包

  最终生成的jar包结构

  > META-INF
  > com
  > 　Tom.class
  > Hello.class

  1. 新建Hello.java和一个Tom.java文件

     > META-INF
     > com
     > 　Tom.java
     > Hello.java

     ```JAVA
     package com;
     public class Tom{
         public static void speak() {
             System.out.println("hello");
         }
     }
     ```

     ```java
     import com.Tom;
     public class Hello{
         public static void main(String[] args) throws Exception {
             Tom.speak();
         }
     }
     ```

  2. 编译Hello.java

  3. 生成jar包，同样准备好MENIFEST文件

     ` jar -cvfm hello.jar META-INF\MENIFEST.MF Hello.class com `

     最后一个com表示把com这个文件夹下的所有文件都打进jar包

  4. 运行jar包 ` java -jar hello.jar`

  5. 优化

     com包下是有Tom.java源文件的，也被打进了jar包里，这样不太好，能不能优化一下javac命令，使所有的编译后文件编译到另一个隔离的地方呢，答案是可以的

     在编译Hello.java时，先新建一个target文件夹。然后我们用如下命令`javac Hello.java -d target `

     将META-INF文件夹也复制到target目录下，**进入这个目录**，输入如下命令`jar -cvfm hello.jar META-INF\MENIFEST.MF * `注意最后一个位置变成了*，表示把当前目录下所有文件都打在jar包里

