要删除 OpenJDK (如果已安装的话)。首先，检查是安装的哪个 OpenJDK包。

```
dpkg --list | grep -i jdk
```

移除 openjdk包:

```
apt-get purge openjdk*
```

卸载 OpenJDK 相关包：

```
apt-get purge icedtea-* openjdk-*
```

检查所有 OpenJDK包是否都已卸载完毕：

```
dpkg --list | grep -i jdk
```