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



