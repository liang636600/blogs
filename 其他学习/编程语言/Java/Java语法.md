# 注解

在类、方法、Field等注解部分插入一些额外key-value对，通过反射获得插入的注解键值对

## 自定义注解

 public @Interface 注解名 {属性列表/无属性}

定义

```javascript
import java.lang.annotation.Documented;
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

@Documented
@Target(value = {ElementType.FIELD, ElementType.METHOD, ElementType.TYPE})
@Retention(RetentionPolicy.RUNTIME)
public @interface LogAnnotation {
    String value() default "";
}
```

使用

* 类上注解

  ```java
  @LogAnnotation(value="Test 测试类, 测试日志注解的功能")
  public class Test {
  
      @LogAnnotation("定义变量用于存放对应的招呼的字符串")
      private String sayMsg = "hello, Java 学习者!";
  
      @LogAnnotation("打招呼的方法。")
      public String sayHello(){
          System.out.println(sayMsg);
          return sayMsg;
      }
  
      public void test(){
          System.out.println("不加注解");
      }
  
      public static void main(String[] args) throws ClassNotFoundException {
          Class clazz = Class.forName("Test");
          LogAnnotation logAnnotation = (LogAnnotation)clazz.getAnnotation(LogAnnotation.class);
          if(logAnnotation == null){
              System.out.println("没有注解");
              return ;
          }
          System.out.println("类上注解内容：" + logAnnotation.value());
      }
  }
  ```

  结果：`类上注解内容：Test 测试类, 测试日志注解的功能`

* 方法上的注解

  ```JAVA
  import java.lang.reflect.Method;
  
  @LogAnnotation(value = "Test 测试类, 测试日志注解的功能")
  public class Test {
  
      @LogAnnotation("定义变量用于存放对应的招呼的字符串")
      private String sayMsg = "hello, Java 学习者!";
  
      @LogAnnotation("打招呼的方法。")
      public String sayHello() {
          System.out.println(sayMsg);
          return sayMsg;
      }
  
      public void test() {
          System.out.println("不加注解");
      }
  
      public static void main(String[] args) throws ClassNotFoundException {
          Class clazz = Class.forName("Test");
          Method[] methods = clazz.getMethods();
          for (Method method : methods) {
          // 判断是否包含需要用到的 LogAnnotation 注解， 没有直接跳出， 不用在进行 if 嵌套
              if (!method.isAnnotationPresent(LogAnnotation.class)) {
                  continue;
              }
              LogAnnotation logAnnotation = (LogAnnotation) method.getAnnotation(LogAnnotation.class);
              if (logAnnotation == null) {
                  return;
              }
              System.out.println("方法上注解：" + logAnnotation.value());
          }
      }
  }
  ```

  结果：`方法上注解：打招呼的方法。`

* Field上的注解

  ```java
  import java.lang.reflect.Field;
  
  @LogAnnotation(value = "Test 测试类, 测试日志注解的功能")
  public class Test {
  
      @LogAnnotation("定义变量用于存放对应的招呼的字符串")
      private String sayMsg = "hello, Java 学习者!";
  
      @LogAnnotation("打招呼的方法。")
      public String sayHello() {
          System.out.println(sayMsg);
          return sayMsg;
      }
  
      public void test() {
          System.out.println("不加注解");
      }
  
      public static void main(String[] args) throws ClassNotFoundException {
          Class clazz = Class.forName("Test");
          Field[] fields = clazz.getDeclaredFields();
          for (Field field : fields) {
              if(!field.isAnnotationPresent(LogAnnotation.class)){
                  continue;
              }
              LogAnnotation logAnnotation = (LogAnnotation) field.getAnnotation(LogAnnotation.class);
              if(logAnnotation == null){
                  return ;
              }
              System.out.println("字段上注解：" + logAnnotation.value());
          }
      }
  }
  ```

  结果：`字段上注解：定义变量用于存放对应的招呼的字符串`





-----

相关资料：

* https://baijiahao.baidu.com/s?id=1720532898155477867&wfr=spider&for=pc