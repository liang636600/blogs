# build hibench

`mvn -Psparkbench -Dspark=3.1 -Dscala=2.12 clean package`

这里Scala版本要与自己默认的一致

报错

```
error: error while loading package, Missing dependency 'object java.lang.Object in compiler mirror', required by /home/iscas/.m2/repository/org/scala-lang/scala-library/2.10.4/scala-library-2.10.4.jar(scala/package.class)
```

