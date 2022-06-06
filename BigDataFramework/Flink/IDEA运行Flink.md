# 1 新建项目

![image-20220530175219805](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20220530175219805.png)

点击Archetype那个地方得Add

![img](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/flink_idea_03.png)

`org.apache.flink`

`flink-quickstart-java`

`1.13.2`

注释掉dependency中与provide相关的

![image-20220530175850697](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20220530175850697.png)

注释完后一定要点一下小m符号

![image-20220530175923412](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20220530175923412.png)

# 2 修改代码

编写批处理代码并测试执行

修改BatchJob文件内容为

```Java

package org.example;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.api.common.functions.FilterFunction;

public class BatchJob {

    public static void main(String[] args) throws Exception {
        final StreamExecutionEnvironment env =
                StreamExecutionEnvironment.getExecutionEnvironment();

        DataStream<Person> flintstones = env.fromElements(
                new Person("Fred", 35),
                new Person("Wilma", 35),
                new Person("Pebbles", 2));

        DataStream<Person> adults = flintstones.filter(new FilterFunction<Person>() {
            @Override
            public boolean filter(Person person) throws Exception {
                return person.age >= 18;
            }
        });

        adults.print();

        env.execute();
    }

    public static class Person {
        public String name;
        public Integer age;

        public Person() {
        }

        public Person(String name, Integer age) {
            this.name = name;
            this.age = age;
        }

        public String toString() {
            return this.name.toString() + ": age " + this.age.toString();
        }
    }
}
```

执行后的结果为

```
2> Fred: age 35
3> Wilma: age 35
```

# 3 打包

1. 在pom文件里加入插件配置

   ```xml
   <!-- 打jar包插件(会包含所有依赖) -->
   			<plugin>
   				<groupId>org.apache.maven.plugins</groupId>
   				<artifactId>maven-assembly-plugin</artifactId>
   				<version>2.6</version>
   				<configuration>
   					<descriptorRefs>
   						<descriptorRef>jar-with-dependencies</descriptorRef>
   					</descriptorRefs>
   					<archive>
   						<manifest>
   							<!-- 可以设置jar包的入口类(可选) -->
   							<mainClass>org.example.BatchJob</mainClass>
   						</manifest>
   					</archive>
   				</configuration>
   				<executions>
   					<execution>
   						<id>make-assembly</id>
   						<phase>package</phase>
   						<goals>
   							<goal>single</goal>
   						</goals>
   					</execution>
   				</executions>
   			</plugin>
   ```

2. 这里的入口类要修改成main函数在的类

   ![img](https://www.programminghunter.com/images/51/58/58258c95a8ed795ec55d000fe6c4ae93.png)

3. 打包，前提是已经运行了程序生成有target文件夹

   ![image-20220601095205433](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20220601095205433.png)

   ![img](https://www.programminghunter.com/images/865/5f/5f4d60f0a682d00e917db5927d0cbc39.png)

4. 选择with-dependencies的jar发布到集群上

   ```
   ./bin/flink run ~/HelloFlink-1.0-SNAPSHOT-jar-with-dependencies.jar
   ```

# 4 去掉命令行输出的多余INFO信息

打开这个文件

![image-20220531234527587](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20220531234527587.png)



将第一行的内容改了保存即可

```
#rootLogger.level = INFO
rootLogger.level = error,stdout
```



