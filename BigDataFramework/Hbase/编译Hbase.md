# 1 下载源码

使用hbase版本2.4.14稳定版

![image-20221025193446193](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20221025193446193.png)

下载链接https://hbase.apache.org/downloads.html

# 2 编译hbase

在hbase源码的主目录下，运行命令`mvn package -DskipTests`

* 报错：Failed to execute goal org.apache.maven.plugins:maven-enforcer-plugin:3.0.0-M3:enforce (hadoop3-profile-required) on project hbase: Some Enforcer rules have failed. Look above for specific messages explaining why the rule failed. -> [Help 1]

  ![image-20221025201622214](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20221025201622214.png)

  * 失败 尝试1：修改pom文件部分内容

    ```xml
     <plugin>
              <groupId>org.apache.maven.plugins</groupId>
              <artifactId>maven-compiler-plugin</artifactId>
              <version>${maven.compiler.version}</version>
              <configuration>
                <source>${compileSource}</source>
                <target>${compileSource}</target>
                <showWarnings>true</showWarnings>
                <showDeprecation>false</showDeprecation>
                <!-- <compilerArgument>-Xlint:-options</compilerArgument> -->
                <compilerArgs>
                  <arg>--add-exports=java.base/jdk.internal.access=ALL-UNNAMED</arg>
                  <arg>--add-exports=java.base/jdk.internal=ALL-UNNAMED</arg>
                  <arg>--add-exports=java.base/jdk.internal.misc=ALL-UNNAMED</arg>
                  <arg>--add-exports=java.base/sun.security.pkcs=ALL-UNNAMED</arg>
                  <arg>--add-exports=java.base/sun.nio.ch=ALL-UNNAMED</arg>
                </compilerArgs>
              </configuration>
            </plugin>
    ```

    重新运行编译命令`mvn clean package -DskipTests`

  * **解决** 尝试2：运行命令`mvn clean package -DskipTests -Denforcer.skip=true`

编译成功

![image-20221025211257981](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20221025211257981.png)

# 3 简单测试

先运行`start-hbase.sh`

`./bin/hbase shell`

![image-20221025212505789](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20221025212505789.png)

`create 'test', 'cf'`

`list 'test'`