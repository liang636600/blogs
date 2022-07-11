# 多进程的实现

```python
import multiprocessing
import time


def drink():
    for i in range(3):
        print("喝汤……")
        time.sleep(1)


def eat():
    for i in range(3):
        print("吃饭……")
        time.sleep(1)


if __name__ == '__main__':
    # target:指定函数名
    drink_process = multiprocessing.Process(target=drink)
    eat_process = multiprocessing.Process(target=eat)

    drink_process.start()
    eat_process.start()
```

# 带参多进程

这地方用到的是args和kwargs，其中args是使用元素组的方式给指定任务传参，kwargs是使用字典方式给指定任务传参。

```python
import time
import multiprocessing


def eat(num, name):
    for i in range(num):
        print(name + "吃一口……")
        time.sleep(1)


def drink(num, name):
    for i in range(num):
        print(name + "喝一口……")
        time.sleep(1)


if __name__ == '__main__':
    # target：指定执行的函数名
    # args:使用元组方式给指定任务传参
    # kwargs:使用字典方式给指定任务传参
    eat_process = multiprocessing.Process(target=eat, args=(3, "giao"))
    drink_process = multiprocessing.Process(target=drink, kwargs={"num": 4, "name": "giao"})

    eat_process.start()
    drink_process.start()
```

# 获取进程编号

获取当前进程的编号`os.getpid()`

获取当前进程的父进程的编号`os.getppid()`

```python
import time
import multiprocessing
import os


def eat(num, name):
    print("吃饭的进程ID:", os.getpid())
    print("吃饭的主进程ID:", os.getppid())
    for i in range(num):
        print(name + "吃一口……")
        time.sleep(1)


def drink(num, name):
    print("喝汤的进程ID:", os.getpid())
    print("喝汤的主进程ID:", os.getppid())
    for i in range(num):
        print(name + "喝一口……")
        time.sleep(1)


if __name__ == '__main__':
    # target：指定执行的函数名
    # args:使用元组方式给指定任务传参
    # kwargs:使用字典方式给指定任务传参
    eat_process = multiprocessing.Process(target=eat, args=(3, "giao"))
    drink_process = multiprocessing.Process(target=drink, kwargs={"num": 4, "name": "giao"})
    print("主进程ID:", os.getpid())

    eat_process.start()
    drink_process.start()
```

# 其他

* 主进程会等待所有的子进程执行结束再结束

  ```python
  import multiprocessing
  import time
  
  def task():
      for i in range(3):
          print("正在工作中。。。")
          time.sleep(1)
  
  
  if __name__ == '__main__':
      # 创建子进程
      sub_process = multiprocessing.Process(target=task)
      # 启动子进程执行对应的任务
      sub_process.start()
      # 主进程等子进程执行结束后再执行
      sub_process.join()
      print("主线程over了！！！")
  ```

* 子进程守护主进程，主进程结束，子进程也会自动销毁

  ```python
  import multiprocessing
  import time
  
  
  def eat():
      for i in range(10):
          print("我吃我吃……")
          time.sleep(0.5)
  
  
  if __name__ == '__main__':
      eat_process = multiprocessing.Process(target=eat)
      # 设置进程守护
      eat_process.daemon = True
      eat_process.start()
  
      time.sleep(3)
      print("我吃饱了……")
  ```

* 销毁子进程 `进程名.terminate()`