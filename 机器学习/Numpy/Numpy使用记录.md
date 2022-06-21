# 数组初始化

```python
import numpy as np
# dtype表示array里每个数值的类型, np.float
array = np.array([[1,2,3],[2,3,4]],dtype=np.int)
# 全为0的矩阵 (3,4)表示数据shape
zeros = np.zeros((3,4))
zerolike = np.zeros_like(array)
# 全为1的矩阵
ones = np.ones((3,4))
onelike = np.ones_like(array)
# 单位矩阵
np.eye(2) # 2表示行数和列数
# 生成序列 [10,20)起始值10，终止值20，步长为2
a = np.arange(10,20,2)
# np.arange(12)生成[0,12)
ab = np.arange(12)
# 改变形状
ab = ab.reshape((3,4))
# 把[1,10]线段取5个点（即平均分为4份，每份长度为9/4=2.25） 结果为[1,1+2.25,...,10]
a = np.linspace(1,10,5)
x = np.linspace(-1,1,5) # 从[-1,1]中线性地取5个点， [-1.  -0.5  0.   0.5  1. ]
# 按特定顺序选取子集
array = np.arange(12).reshape((3,4))
# b的值为 array的行按[2,0,1]排列后的结果
b = array[[2,0,1]]
# 选取某些值组成新的数组
# array中坐标点为(0,2),(1,1)的值组成新的数组
b = array[[0,1],[2,1]]
```

## 生成随机数据

### numpy.random.normal(0 均值,1 方差,num 数量)

高斯分布

### numpy.random.randn(d0,d1)

标准正态分布(standard normal)

### numpy.random.uniform(low, high, size)

[low, high)均匀分布

### numpy.random.random(size)

[0.0, 1.0)随机生成一个小数

### numpy.random.random_sample(size)

[0.0, 1.0)，均匀分布

### numpy.random.rand(d0,d1...)

[0.0, 1.0)，均匀分布

### numpy.random.randint(low,high,size)

生成在[low,high)范围内的随机整数（均匀分布）,size=(,) 或 num，如果没有指定high的值，范围为[0,low)

```python
# 二项分布的样本值 binomial(n,p,size) n次实验，p：实验成功的概率
# beta分布的样本值 beta
# 产生卡方分布的样本值 chisquare
# 产生gamma分布样本值 gamma
```

## 随机打乱序列

```python
a = np.array([1, 2, 3, 4])
# 返回一个序列的随机排列，不改变原序列
b = np.random.permutation(a)
# 对一个序列就地随机打乱
np.random.shuffle(a)
```

# 从文件载入数据

## numpy.loadtxt

从一个文本文件中加载数据

**要求：**每一行必须有相同数量的值

**参数：**

* **comments**：注释开始的符号，这行不会被读入
* **skiprows**：默认值为0表示从第一行开始读，假设值为2从第三行开始读
* **usecols**：读取哪些列，从0开始，usecols = (1,4,5)表示读取第2,5,6列，只读取一列（usecols = 3或usecols = (3,)），其中usecols=range(0, 9)表示读取[0,9)列
* **max_rows**：在skiprows确定从第几行开始读取后，读取行的数量为max_rows行

# 访问数据

```python
A = np.arange(12).reshape((3,4))
# 切片所得的数据与原数组数据关联
# 索引行数
b = A[2]
# 对某行某列
b = A[1,2]
# 行数选0,1，所有列
b= A[0:2,:]
# 某一列 数据shape为 (2,)
b = array[:2,1]
# 如果在切片的时候用了:，则数据维度不变
b = array[:1,1:2] # [[100]]
# 布尔型数据索引，得到的结果与原数组不关联是一个副本
boolarr = [True,False,True] # 对行，这里选取第0,2行
b = A[boolarr]
# for循环默认迭代array的行
for row in A:
    print(row)
```

# array的属性

```python
import numpy as np
array = np.array([[1,2,3],[2,3,4]])
# 查看数据类型
array.dtype
# array.ndim表示数据维度 2
print(array.ndim)
# array的形状 (2,3)
print(array.shape)
# array里面有多少数据 6
print(array.size)
# 转换数据类型
array = array.astype(np.float64)
```

# array的运算

```python
import numpy as np
b = np.arange(4)
# b里面的值与3作比较[ True  True  True False]
# b==3
print(b<3)

array1 = np.arange(4).reshape((2,2)).astype(np.float64)
array2 = np.random.normal(2,1,(2,2))
print(array1)
print(array2)
# 获得两数组每个位置的较大值，返回原大小的数组
print(np.maximum(array1,array2))
# 返回浮点数组的整数部分和小数部分（两个数组）
# remainder表示小数部分，whole表示整数部分，两者均为数组
remainder,whole = np.modf(array2)
```

---

**np.meshgrid(x,y)**

```python
x = np.array([1,2,3])
y = np.array([4,5,6])
# meshgrid()方法接受两个一维向量，生成一个坐标矩阵
xx, yy = np.meshgrid(x,y)
```

![img](https://wangyeming.github.io/img/2018-11-12-numpy-meshgrid-01.png)

![img](https://wangyeming.github.io/img/2018-11-12-numpy-meshgrid-02.png)

---

```python
# np.where(condition, x, y)
# np.where(arr>0,2,-2)
# 满足条件输出x，不满足条件输出y
print(np.where([[True, False], [True, True]],  # 官网上的例子
         [[1, 2], [3, 4]],
         [[9, 8], [7, 6]]))
# [[1 8]
#  [3 4]]
# 输出数组中满足条件的坐标
# np.where(condition)
a = np.array([2,4,6,8,10])
print(np.where(a > 5)) # 返回(array([2, 3, 4]),)
# 获得这些索引的值
print(a[np.where(a>5)]) # 返回[ 6  8 10]

# 检查数组中所有值是否均为TRUE np.all(array)
# 测试数组中至少有一个TRUE np.any(array)
# 计算数组中TRUE的数量 np.sum(array)

# 排序
array = np.array([2,1,3])
# 按从小到大的顺序
b = np.sort(array)

# 去重并排序
b = np.unique(array)

arr1 = np.array([2,1,5])
arr2 = np.array([2,3,1,4])
# 返回arr1 shape相同的array，对arr1的每一个元素判断是否在arr2中，如果在，则该位置为TRUE
b = np.in1d(arr1,arr2) # [ True  True False]

# 集合运算
arr1 = np.array([2,1,5])
arr2 = np.array([2,3,1])
# 交
b = np.intersect1d(arr1,arr2)
# 并
b = np.union1d(arr1,arr2)
# 差
b = np.setdiff1d(arr1,arr2)
# 两个集合的并除去公共部分的元素
b = np.setxor1d(arr1,arr2)

# 沿x轴复制原数组
a = np.array([[1, 2], [3, 4]])
# 沿x轴复制a两次
b = np.tile(a,2)
# [[1 2 1 2], [3 4 3 4]]

a = np.array([[1, 2], [3, 4]])
# (2,1)第一个2表示沿y轴复制倍数，1表示沿x轴复制倍数
b = np.tile(a,(2,1))
# [[1 2], [3 4], [1 2], [3 4]]

a = np.array([[1, 2], [3, 4]])
# 二维数组下添加一行
b = np.concatenate((a,[[0,0]]),axis=0)
b = np.append(a,[[0,1]],axis=0)
b=np.insert(a,0,[[0,2]],axis=0)
```

## 常见数学运算

```python
# 乘法
# a*b表示矩阵每个对应的元素相乘
# np.dot(a,b) 表示矩阵的乘法
# a.dot(b)
# 如果向量a的shape是(3,)如[1,2,3]，向量b的shape也是(3,)如[0,1,2]
# np.dot(a,b)表示向量a与向量b的点积 即8

# 如果矩阵a的shape为(2,2)例如[[1,2],[3,1]]，如果向量b的shape为(2.)例如[1,2]
# 则np.dot(a,b) 这里是矩阵的乘法，把b向量当做列向量，shape为(2,1)，结果为[5,5],shape为(2,)

# 如果一个向量a的shape为(2,1)例如[[2],[3]]，另一个向量b的shape为(2,)例如[1,2]
# a*b表示向量a与向量b进行矩阵的乘法，结果的shape为(2,2)
# 另一种矩阵乘法表示一个向量a的shape为(2,1)，另一个向量b的shape为(1,2)，表示两向量的矩阵乘法np.dot(a,b)

import numpy as np
a = np.arange(12).reshape((3,4))
print(a)
# 对整个array进行
# 求和
print(np.sum(a))
# 求最小值
print(np.min(a))
# 求最大值
print(np.max(a))
# 标准差
np.std(a)
# 方差
np.var(a)

# 求最大值
# axis=0表示对每一列求最大值
print(np.max(a, axis=0))
# axis=1表示对每一行求最大值
print(np.max(a, axis=1))

a = np.arange(2,14).reshape((3,4))
# 求最小值所在的索引（以size的大小为总数，上面例子中索引最大为11）
b = np.argmin(a) # 返回0
# 求最大值所在的索引
b = np.argmax(a) # 返回11
# 计算平均值
b = np.mean(a)
b = a.mean()
# 计算中位数
b = np.median(a)
# 累加过程，第一个的值就是本身，第二个的值是第一个加原来第二个的值
# 第三个的值是原来第1,2,3个值之和...
b = np.cumsum(a)
# 累乘过程
b =np.cumprod(a)
# 累差过程
# 每行中，后一个值与前一个值的差值
b = np.diff(a)
# 返回非0的数所在的位置
b = np.nonzero(a) # 返回两个数组，第一个数组为横坐标位置，第二个数组为纵坐标的位置，第一个数组和第二个数组对应位置的数值组成的坐标表示非0数所在的位置
# 排序,对每一行按从小到大的顺序排序
b = np.sort(a)
# 矩阵转置
b = np.transpose(a)
b = a.T
# clip功能,对a里面的数处理，所有小于5的值都变为5，所有大于9的值都变为9
b = np.clip(a,5,9)

array = np.arange(4).reshape((2,2)).astype(np.float64)
# 求平方根
print(np.sqrt(array))
# 求e的多少次方
print(np.exp(array))
# 可加一个参数表示原地操作，即改变array里面的值
print(np.sqrt(array,array))
# 还有运算如 abs log log10 log2
# rint元素四舍五入
print(np.rint(array))
print(array)
```

## 线性代数

```python
a = np.array([[1, 2], [3, 4]])
# 求矩阵的逆矩阵
inva = np.linalg.inv(a)

# 以一维数组形式返回对角线元素或将一维数组转化为方阵
b =np.diag(a)
c =np.diag(np.array([1,2]))

# 矩阵的迹 对角线元素之和 trace
# 行列式 det
# 特征值和特征向量 eig 返回 w,v 其中w为特征值，v为特征向量
# 解线性方程组AX=b,A为方阵 np.linalg.solve(A,b)
# AX=b的最小二乘解 lstsq
```

### 范数计算np.linalg.norm(array)

默认情况下，是求整体的矩阵元素平方和，再开根号

### 求解线性方程组numpy.linalg.solve(a, b)

a表示系数矩阵，b表示值，返回方程组ax=b的解，shape与b一样

## array的合并

````python
import numpy as np
A = np.array([1,1,1])
B = np.array([2,2,2])
# 合并两个array,把B放在A的下方，变成2*3
b = np.vstack((A,B)) # vertical stack
b = np.hstack((A,B)) # 左右合并 (6,)
# 多个array合并,axis=0表示纵向合并，axis=1表示横向合并
a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6]])
b=np.concatenate((a, b), axis=0)
# [[1 2]
#  [3 4]
#  [5 6]]
````

## array的分割

```python
import numpy as np
A = np.arange(12).reshape((3,4))
# [[ 0  1  2  3]
#  [ 4  5  6  7]
#  [ 8  9 10 11]]
# 分割
# 横向来看，分成两块，画十字
b= np.split(A,2,axis=1)
# [array([[0, 1],
#        [4, 5],
#        [8, 9]]), array([[ 2,  3],
#        [ 6,  7],
#        [10, 11]])]

# 纵向来看，分成3块
b = np.split(A,3,axis=0)
# [array([[0, 1, 2, 3]]), array([[4, 5, 6, 7]]), array([[ 8,  9, 10, 11]])]

# 不等量的分割,横着来看
b = np.array_split(A,3,axis=1)
# [array([[0, 1],
#        [4, 5],
#        [8, 9]]), array([[ 2],
#        [ 6],
#        [10]]), array([[ 3],
#        [ 7],
#        [11]])]

# 纵向来看，分割成3份
b = np.vsplit(A,3)
# 横向来看，分割成2份
b = np.hsplit(A, 2)
```

## array的赋值

**浅拷贝**：如果b=a，那么a与b指向的内存位置相同

**深拷贝**：b=a.copy()

# 数据处理

## 维度处理

### 多维变一维

numpy中的ravel()、flatten()、squeeze()都有将多维数组转换为一维数组的功能，区别：
ravel()：如果没有必要，不会产生源数据的副本
flatten()：返回源数据的副本
squeeze()：只能对维数为1的维度降维

另外，reshape(-1)也可以“拉平”多维数组

![这里写图片描述](https://img-blog.csdn.net/20180109095535985?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdHltYXRsYWI=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

### 增加维度

```python
A = np.array([1,1,1])
# 增加array的维度
b = A[np.newaxis,:] # 把维度(3,)变成(1,3)
b = A[:,np.newaxis] # 把维度(3,)变成(3,1)
```

# 保存

```python
arr1 = np.array([2,1,5])
# 把array写入文件
np.save('b',arr1) # 默认加上后缀b.npy
# 从文件中读入arr
a = np.load('b.npy') # 文件名写上完整的b.npy
```

# 其他

* 对0,1标签的一维数组，转成one-hot编码

  ```python
  a = np.array([0,1,1,0])
  b = np.eye(2)[a] # eye(2)这里的2表示类别数
  # [[1. 0.], [0. 1.], [0. 1.], [1. 0.]]
  ```

  