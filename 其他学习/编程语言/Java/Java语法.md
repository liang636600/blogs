# 注解

## 自定义注解

 public @Interface 注解名 {属性列表/无属性}

定义

```javascript
import java.lang.annotation.ElementType;
import java.lang.annotation.Target;

@Target(ElementType.TYPE) // 修饰了注解的作用范围
public @interface MyAnno {
    //基本数据类型
    int num() default 2;

    //String类型
    String value();

//    //枚举类型
//    Lamp lamp();
//
//    //以上类型的数组
//    String[] values();
//    Lamp[] lamps();
//    int[] nums();
}
```

使用

```java
@MyAnno(num = 1, value = "")
public class Hello {
    public static void main(String[] args) throws InterruptedException {
        System.out.println(Lamp.RED);
    }
}
```

