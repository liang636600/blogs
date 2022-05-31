# 1 基础概念

## 数据集和数据流

DataSet和DataStream不可变的，可包含重复数据的数据集合

DataSet API的所有核心类可在org.apache.flink.api.java包中找到，而DataStream API的所有核心类可在org.apache.flink.streaming.api包中找到

StreamExecutionEnvironment和ExecutionEnvironment分别是基于DataStream API和DataSet API开发Flink程序的基础类

* 推荐getExecutionEnvironment：创建一个执行环境，该环境代表当前在其中执行Flink程序的上下文

```
final StreamExecutionEnvironment env =
                StreamExecutionEnvironment.getExecutionEnvironment();
```

* createLocalEnvironment：创建一个本地执行环境，本地执行环境将在与创建该环境相同的JVM进程中以多线程方式运行Flink程序，除非手动设置了Flink程序中操作符的并行度，否则本地环境中操作符的默认并行度是硬件上下文的数量
* createRemoteEnvironment(String host, int port,String ...)：创建一个远程执行环境，远程环境将Flink程序发送到Flink集群中执行。除非手动设置了Flink程序中操作符的并行度，否则执行Flink程序的操作符任务的默认并行度为1。将JAR文件提交到远程服务器中，需要在调用时指定Flink集群中的作业管理器的IP地址和端口号，并指定要在集群中运行的JAR文件。

**逐行读取文本文件内数据**

```
DataStream<String> input = env.readTextFile("file:///home/intmaze/flink/in/file")
```

**Map转换操作**

```
DataStream<Integer> parsedStream = input.map(new MapFunction<String, Integer>(){
	// 将String类型的元素转换为Integer类型
	@Override
	public Integer map(String value){
		return Integer.parseInt(value)
	}
})
```

**输出到文本文件或标准输出流中**

```
parsedStream.writeAsText("file:///home/iscas/flink/out/file")
parsedStream.print()
```

**触发程序运行**

```
JobExecutionResult execute = env.execute("hello iscas");
```

## 指定分组数据集合的键

键是虚拟的，他们被定义成实际数据的函数以指导分组操作

在使用DataSet API的程序中指定Key的方式

```
DataSet<T> input = ...
DataSet<T> reduced = input.groupBy(/*在这里定义分组数据集的Key*/).reduceGroup(/*执行逻辑操作*/)
```

在使用DataStream API的程序中指定Key的方式

```
DataStream<T> input = ...
DataStream<T> windowed = input.keyBy(/*在这里定义分组数据流的Key*/).window(/*窗口格式*/)
```

### 使用索引定义键

对于**元组（Tuple）**数据，可以使用tuple2.f0表示第一个字段

````
DataStream<Tuple3<Integer, String, Long>> input = ...
KeyedStream<Tuple3<Integer, String, Long>> keyed = input.keyBy(0)
KeyedStream<Tuple3<Integer, String, Long>> keyed = input.keyBy(0, 1)
````

### 使用字段表达式定义键

```java
//一个嵌套的POJO
public static class City {
	public Person person;
	public int count;
}
public static class	Person{
	public String name;
	public float age;
	public Tuple3<Long,Long,String> bankCard;
}
// 对于类型为City的数据流，按字段person进行分组
DataStream<City> cityDataStream =...
KeyedStream<City> resultDataStream = cityDataStream.keyBy("person");
// 按Person类型的某个字段分组数据流
KeyedStream<City> resultDataStream= cityDataStream.keyBy("person.age");
```

### 使用键选择器函数定义键

使用KeySelector函数，接受单个元素作为输入，并返回元素的键，返回的键可以是任何类型，且由任意的计算推导出来

```java
// 将返回Person对象的CityCode字段作为分组数据流的键
public class Person{
	public String name;
	public Integer cityCode;
}
DataStream<Person> words =...
KeyedStream<Person> Keyed = words.KeyBy(new KeySelector<Person,Integer>(){
	public Integer getKey(Person person) {
		return person.cityCode;
	}
})
```

## 指定转换函数

### 实现Interface

所有用户自定义函数都可以实现对应操作符提供的接口，例如下面Map操作符对应的MapFunction接口

```java
import org.apache.flink.api.common.functions.MapFuntion;
public class MyMapFunction implements MapFuntion<String,Integer> {
	public Integer map(String value){
		return Integer.parseInt(value);
	}
}
// 将用户自定义函数用于Map操作符上
dataStream.map(new MyMapFuntion());
```

### 继承富函数

所有用户自定义函数都可以继承对应操作符提供的富函数抽象类

```java
import org.apache.flink.api.common.functions.RichMapFunction;
public class MyMapFunction extends RichMapFunction<String, Integer> {
	public Integer map(String value) {
		return Integer.parseInt(value);
	}
}
// 将用户自定义函数用于Map操作符上
dataStream.map(new MyMapFuntion());
```

### 匿名类

通过匿名类的方式将用户定义的函数传递到对应数据流的操作上

```java
import org.apache.flink.api.common.functions.MapFunction;
dataStream.map(new MapFunction<String, Integer>(){
	public Integer map(String value) {
		return Integer.parseInt(value);
	}
});
import org.apache.flink.api.common.functions.RichMapFunction;
dataStream.map(new RichMapFunction<String, Integer>(){
	public Integer map(String value) {
		return Integer.parseInt(value);
	}
});
```

### Java8 的Lambdayufa

```java
dataStream.map(value->value+"iscas");
```

## 支持的数据类型

### Tuples和Case类

### POJO

满足：类的访问权限必须是public，类必须有一个没有参数的公共构造函数，类的所有字段都是可以访问的，字段的类型必须是Flink支持的

# 2 Flink程序模型

## 窗口

![1653962858143](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/1653962858143.jpg)

## 时间

Flink提供了三种时间语义

* Event time：是每个事件在其生产设备上发生的时间
* Ingestion time（摄入时间）：是事件进入流处理程序的时间
* Processing time：执行基于时间操作的每个操作符的本地时间

![1653963341537](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/1653963341537.jpg)

# 3 Flink程序的分布式执行模型

## 任务和任务链

![1653965036077](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/1653965036077.jpg)

## 任务槽和资源

在任务管理器中引入任务槽的概念，每个任务槽都表示任务管理器的一个固定资源子集，Flink将任务管理器的内存划分到多个任务槽中（每个子任务运行在一个任务槽中）

![1653965911775](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/1653965911775.jpg)

![1653966079245](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/1653966079245.jpg)

### 共享任务槽

默认情况下，Flink允许子任务共享同一个任务槽，即使他们是不同操作符的子任务，只要他们来自同一个Flink程序即可

![1653966587560](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/1653966587560.jpg)

一个好的默认任务槽数量最好是极其的CPU核心的数量

Flink默认启动共享任务槽机制

# 4 Java的Lambda表达式

## 类型擦除

```java
// 获取执行环境
final StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
// 根据指定的对象序列创建一个数据流
DataStream<Long> dataStream = env.fromElements(1L,5L);
DataStream<Long> resultStream = dataStream.map(i -> i*i);
resultStream.print();
//触发程序执行
env.execute();
```

```java
final StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
DataStream<Tuple2<Long,Long>> dataStream = env.fromElements(Tuple2.of(1L,1L),Tuple2.of(5L,5L));
DataStream<Tuple2<Long,Long>> resultStream = dataStream.map(i->i).returns(Types.TUPLE(Types.LONG,Types.LONG));
resultStream.print();
env.execute();
```

