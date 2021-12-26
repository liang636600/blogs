OpenSSH是目前最流行的远程系统注册与文件传输应用。其中SSH可以替代Telnet；SCP与SFTP能够替代FTP。

OpenSSH采用密钥的方式对数据加密。在正式开始传输数据之前，双方首先要交换密钥。当收到对方的数据时，再利用密钥和相应的程序对数据进行解密。

OpenSSH采用随机的方式生成公私密钥。密钥通常只需生成一次，必要时也可以重新制作。当使用ssh命令注册到远程系统时，OpenSSH服务器的sshd守护进程将会发送一个公钥，OpenSSH客户端软件ssh将会请用户确认是否接受发送的公钥。同时，OpenSSH客户机也会向服务器回送一个密钥，使OpenSSH连接双方的每个系统都拥有对方的密钥，因而能够解密对方经由加密链路发送的加密数据。

OpenSSH服务器的公钥与私钥均存储在/etc/ssh目录中。在OpenSSH客户端，用户收到的所有公钥，以及提供密钥的OpenSSH服务器的IP地址均存储在用户主目录下的~/.ssh/known_hosts文件中。

## 1 安装OpenSSH服务器

`sudo apt install openssh-server`，安装后，可以使用`pidof sshd`验证OpenSSH服务器的sshd守护进程是否已开始运行

## 2 sshd_config配置文件

/etc/ssh/sshd_config是OpenSSH服务器的默认配置文件。语法格式`parameter value`

## 3 使用ssh注册到远程系统

语法格式

`ssh [-l login_name] [-p port] [user@]hostname [command]`

-l 用于指定用户名，表示以哪一个用户身份注册到远程系统。如果不提供用户名，则以当前用户的身份注册到远程系统。

-p 指定TCP端口

## 4 执行远程系统命令

ssh能够在注册后执行远程系统中的单个命令后立即返回。例如`ssh iscas "uname -r"`

## 5 使用SCP代替FTP

scp是OpenSSH中另外一个重要客户端软件，能够在不同系统间复制文件，格式如下

`scp [-P port][[user@]host1:] file1 [[user@]host2:] file2`

-P 指定TCP端口

第一个参数是源文件，第二个参数是目的文件

### 利用scp命令下载文件

例如`scp gqxing@iscas:/etc/profile /tmp`

### 利用scp命令上传文件

例如`scp /etc/hosts gqxing@iscas:/tmp`

## 6 使用SFTP代替FTP 

语法格式

```
sftp [-b batchfile] host
sftp -b batchfile [user@]host
sftp [[user@]host[:file [file]]]
```

例如`sftp iscas`

### 下载文件或文件夹

get命令实现`get -r blog`表示下载blog文件夹，本地的哪里？可以借助`lpwd`

### 上传文件或文件夹

put命令，例如`put -r blog`

## 7 SSH与SCP的无密码注册

**实质：**

* 客户端与服务器同一用户名
* 客户端的公钥由服务器保存在.ssh/authorized_keys文件中

为了实现无密码注册，客户端应首先建立OpenSSH连接，然后自动向服务器发送其密钥（公钥）。之后，服务器即可根据相应用户主目录中预定义的密钥列表，对收到的密钥进行比较。如果存在匹配的密钥，服务器将会允许ssh或scp自动注册。

用于远程系统注册与数据传输的密钥文件需要事先单独生成，生成后的密钥文件存储在服务器用户主目录的~/.ssh目录中。其中，私钥和公钥分别存储在id_dsa和id_dsa.pub文件中，authorized_keys文件则用于存储所有授权的远程客户系统的公钥，使得远程客户系统能够以此用户身份注册到本地系统而无需提供密码。

### OpenSSH客户端配置

为了实现无密码的系统注册，OpenSSH客户端需要完成下列准备工作。

首先，在客户端与服务器系统中分别创建一个同名的gqxing用户，然后以gqxing用户的身份注册到客户端系统，使用`ssh-keygen`命令生成一对密钥。当系统提示输入一个与密钥相关联的密码时，直接按下enter

其次，验证上述步骤生成的两个密钥文件是否均存储在gqxing用户主目录的.ssh子目录中。

最后，采用下列命令，把生成的公钥文件id_dsa.pub复制到远程系统的gqxing用户主目录中

`scp id_dsa.pub gqxing@iscas:pub_key`

### OpenSSH服务器配置

在OpenSSH服务器中，以gqxing用户的身份注册到系统，然后使用cat命令和>>重定向符号，把pub_key文件中的数据附加到authorized_keys文件的后面

`cat ~/pub_key >> .ssh/authorized_keys`

`rm ~/pub_key`

authorized_keys文件包含所有OpenSSH客户端系统的公钥列表，如果表中列举的客户系统gqxing用户仍以同一用户身份连接到服务器，则无需提供密码