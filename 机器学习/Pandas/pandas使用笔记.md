字典形式的numpy

# 数据初始化

Series 一维数组，但 带有index索引

dataframe 二维数组 带有index 和columns索引

```python
import pandas as pd
import numpy as np
s = pd.Series([1,3,6,np.nan])
# 自动加上了序号
# 0    1.0
# 1    3.0
# 2    6.0
# 3    NaN
# dtype: float64
a = pd.Series([1,5,2],index=['a',1,0])
a = pd.Series({'a':2,1:1,3:2})
dates = pd.date_range('20160101',periods=6)
# DatetimeIndex(['2016-01-01', '2016-01-02', '2016-01-03', '2016-01-04',
#                '2016-01-05', '2016-01-06'],
#               dtype='datetime64[ns]', freq='D')
# index表示每一行的名称，columns表示每一列的名称
df = pd.DataFrame(np.random.randn(6,4),index=dates,columns=['a','b','c','d'])
# 默认每一行每一列的名称为0,1,2...
df1 = pd.DataFrame(np.arange(12).reshape((3,4)))
# 'A':1其中'A'表示列名,表示每一列的列名和里面的值
# 'A':1其中'A'表示列名,表示每一列的列名和里面的值
df2 = pd.DataFrame({'A':1,
                   'B':pd.Timestamp('20130102'),
                   'C':pd.Series(1,index=list(range(4)),dtype='float32'),
                    'D':np.array([3]*4,dtype='int32'),
                    'E':pd.Categorical(['test','train','test','train']),
                    'F':'foo'})
```

# DataFrame的属性与运算

````python
# 'A':1其中'A'表示列名,表示每一列的列名和里面的值
df2 = pd.DataFrame({'A':1,
                   'B':pd.Timestamp('20130102'),
                   'C':pd.Series(1,index=list(range(4)),dtype='float32'),
                    'D':np.array([3]*4,dtype='int32'),
                    'E':pd.Categorical(['test','train','test','train']),
                    'F':'foo'})
# 每一列数据type
b = df2.dtypes
# A             int64
# B    datetime64[ns]
# C           float32
# D             int32
# E          category
# F            object

# 行名，返回的是index类型 Index(['a', 1, 3], dtype='object')
print(df2.index)
# 列名
b = df2.columns
# 所有的值，返回的是ndarray类型
b = df2.values
# 描述一些常用的数学属性，例如平均值，方差，最大最小值
b = df2.describe()
# 对DataFrame进行转置，包括交换行和列以及转置dataframe.values中的内容
df2.T

# 排序列名或行名
# axis=1从行的角度看，画十字排序，对行名排序
b = df2.sort_index(axis=1,ascending=False)
#      F      E  D    C          B  A
# 0  foo   test  3  1.0 2013-01-02  1
# 1  foo  train  3  1.0 2013-01-02  1
# 2  foo   test  3  1.0 2013-01-02  1
# 3  foo  train  3  1.0 2013-01-02  1

# axis=0从列的角度看，画十字排序，对列名排序
b = df2.sort_index(axis=0,ascending=False)
#    A          B    C  D      E    F
# 3  1 2013-01-02  1.0  3  train  foo
# 2  1 2013-01-02  1.0  3   test  foo
# 1  1 2013-01-02  1.0  3  train  foo
# 0  1 2013-01-02  1.0  3   test  foo

# 排序
# 对Series排序
series = pd.Series(np.array([1,4,2,3]),index=[0,2,5,3])
print(series)
# 对值排序，前面的index也跟着值的变化而变化
print(series.sort_values())
# 对index排序，后面的值也跟着变化
print(series.sort_index())

df = pd.DataFrame(np.array([[3,2,0],[4,1,3],[2,1,2]]))
# 对dataframe排序，排序时，缺省值被放在末尾
# 对每一行，按第一列的大小递增排序，如果想按递减排序（加上ascending=False）
# 如果按多列排序 by=[1,2]
b = df.sort_values(by=[0])
print(b)
# 对每一列，按第一行的大小递增顺序排序
b= df.sort_values(by=[0],axis=1)
# 对值排序
b = df2.sort_values(by='E')

# rank
# 对相同值的处理
# 1 顺序排名，值相同时，谁在前，谁排名靠前（有点先到先得的意思）
# df['顺序排名'] = df.成绩.rank(method='first',ascending=False)
# 2 跳跃排名，成绩相同时，排名相同，其他元素按其‘位置’排名（可参考顺序排名），1,2,2,4,5
# df['跳跃排名'] = df.成绩.rank(method='min',ascending=False)
# 3 密集排名，成绩相同时，排名相同，其他同学依次累加（+1) 1，2，2，3，4
# df['密集排名'] = df.成绩.rank(method='dense',ascending=False)
# DataFrame.rank(axis=0,method='average',numeric_only=None,na_option='keep',ascending=True,pct=False)
# pct：是否以排名的百分比显示排名（所有排名与最大排名的百分比）
# 怎么样利用rank()函数得到各个班级排名为第二名的学生信息呢？
def get_second(x):
    return x[x.成绩.rank(method='dense', ascending=False) == 2.0]

df.groupby('班级').apply(get_second).reset_index(drop=True)

# dataframe与series作差
# series先转成一行,默认dataframe的每一行与series（一维数组）作差，
# 结果的列名为dataframe的列名与series的index的并集（index相同的作差）
df = pd.DataFrame(np.arange(12).reshape(((3,4))))
series = pd.Series(np.arange(4)+1,index=[1,2,3,4])
res = df.sub(series)
# dataframe的每一列与series作差
series = pd.Series(np.arange(3)+1)
res = df.sub(series,axis='index')

# 对每一列应用函数，如果想对每一行应用，则加上axis='columns'
# 将函数应用到由各列或行所形成的一维数组上 apply
# 下面的结果为series
res = df.apply(lambda x:x.max()-x.min())
res =df.apply(lambda x:pd.Series([x.max(),x.min()],index=['max','min']))

# NumPy的ufuncs（元素级数组方法）也可用于操作pandas对象
np.abs(df)

# 将函数应用到每一个元素
res = df.applymap(lambda x:'%.2f' % x)

# Series中有一个map方法,df[0]表示一列
res = df[0].map(lambda x:x+1)
# map方法可以接受一个函数 data['k1'].map(str.upper)

series = pd.Series([0,0,1,1,2])
# 计算series中每个值出现的频率
res = series.value_counts() # 返回一个series，index为每个值，value为次数
print(res[res>1]) # 把series中值大于1的打印出来

df = pd.DataFrame(np.array([[2, 1, 2], [10, 1, 3], [3, 2, 0]]))
# 统计dataframe每一列中各值的数量
# 结果中index的值为df所有不同值按递增顺序，结果的列数为df的列数，统计每一列中各index的个数
a = df.apply(pd.value_counts).fillna(0)
      0    1    2
0   0.0  0.0  1.0
1   0.0  2.0  0.0
2   1.0  1.0  1.0
3   1.0  0.0  1.0
10  1.0  0.0  0.0

# 判断series中的值是否在一个集合中
mask = series.isin([1,0,4]) # 返回一个series
# 0     True
# 1     True
# 2    False
# 找出一个series在一个指定集合中的值
series[mask]

df = pd.DataFrame(np.array([['乌黑'], ['浅白'], ['青绿'],['乌黑']]))
# 对df的某一列，如果是离散的值，使用hotkey编码
a=pd.get_dummies(df[0],prefix='色泽')
   色泽_乌黑  色泽_浅白  色泽_青绿
0      1      0      0
1      0      1      0
2      0      0      1
3      1      0      0
````

# 值的选择

```python
import pandas as pd
import numpy as np

a = pd.Series({'a':2,1:1,3:2})
# 可以直接通过索引的方式访问值
a['a'] # 其值为2，就像map一样，这里a[0]其值也为2
# 对于series选择值，传入想选的index值组成的列表
b=a[['a',3]] # ('a', 2) (3, 2)
# 也可以传入一个布尔型数组，也可以为布尔型series 例如obj2[obj2 > 0]
a[[True,True,False]] #则表示选取的值为前两个

a = pd.Series([1,3,4],index=['a','c','b'])
# [0,2]表示选择series中的index值为0和2所在的行（即使这里的index为字符串也不影响）
b = a[[0,2]]
# [0:2]表示选择index值为0,1所在的行
b =a[0:2]
# 根据字符串index选择行
b = a[['b','c']]

dates = pd.date_range('20130101', periods=6)
df = pd.DataFrame(np.arange(24).reshape((6, 4)),
                  index=dates,
                  columns=['A', 'B', 'C', 'D'])
# 选择前五行
df.head()

# 选择某一列 df['列名']或df.列名(列名如果是字符串类型的话，不用加引号，例如df.D)
# 返回结果是Series类型
print(df['A'])
# 选择多列 ['a','c']表示列名
b=df[['a','c']]

# 选择某几行 下面表示选择第0~2行，返回的是dataframe类型
print(df[0:3])

# 选择行列
# 第一种方式 loc 通过行和列的名称
# 选择某行名为three的那行
df.loc['three']
# 下面表示选择所有行，列名为'A','B'的列
print(df.loc[:,['A','B']])
# 打印某一行，某一列数据
# 选择一行多列返回结果类型为series，原列名为series的index，原index为series的values
print(df.loc['20130102',['A','B']])

# 第二种方式 iloc 通过行和列的数字index
# 第三行，所有列
print(df.iloc[3,:])
# 第1，3,5行，1:3列
print(df.iloc[[1,3,5],1:3])

# 选取单一标量
# 通过index与columns名称选取
b=df.at[1,'b']
# 通过坐标位置选取
b=df.iat[0,0]

# 筛选列满足条件的
# 列名为A的列，选出其中值<8的行
print(df[df.A < 8])
# 布尔型DataFrame进行索引
# 把data中值小于5的全部改为0
data[data < 5] = 0
```

# 对索引和值操作

![img](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/7178691-5499d14f0e2cd639.jpg)

```python
import pandas as pd
import numpy as np

dates = pd.date_range('20130101', periods=6)
df = pd.DataFrame(np.arange(24).reshape((6, 4)),
                  index=dates,
                  columns=['A', 'B', 'C', 'D'])
# 修改坐标为（2,2）的值
df.iloc[2,2]=1111
# 通过横坐标标签名和纵坐标标签名称修改值
df.loc['20130101','B']=2222
# 对列名为'A'所在的列，值>4的值所在的行全变为0
# df[df.A>4]=0
# 对列名为'A'所在的列，值>4的值变为0
df.A[df.A>4]=0
# df.B[df.A>4]=0

# 加一个新的列，为不存在的列赋值会添加一个新列
df['F'] = np.nan
# 如果是series，必须要指定index，如果series的index与dataframe的index不完全一样，则index值相同的修改
# 如果赋值的是一个Series，就会精确匹配DataFrame的索引，所有的空位都将被填上缺失值
df['E'] = pd.Series([1,2,3,4,5,6], index=dates)
# 通过索引方式返回的列只是相应数据的视图而已，并不是副本
print(df)

# 修改某一列的值，修改列名为a整列的值
df.a = [0]*6

# 修改index的值
a.index = pd.Index([1,2,3])
a.index = [1,2,3]
# 获得index的数字顺序
pd.Index(['c','b','a']).get_indexer(['c','a','b']) # 返回结果为ndarray [0,2,1]
# 修改index和columns的值
data = pd.DataFrame({'k1': ['one', 'two'] * 3 + ['two'], 'k2': [1, 1, 2, 3, 3, 4, 4]})
# dataframe的index也可以修改
data.index = data.index.map(lambda x:x+1)
data.rename(index=str.title,columns=str.upper,inplace=True)
# 把index中值为1的改为5，把columns中值为K1的改为12
data.rename(index={1:5},columns={'K1':12},inplace=True)
# 为index添加一个名字
data.index.name = 'state'
        k1  k2
state         
0      one   1
1      two   1
2      one   2
3      two   3
4      one   3
5      two   4
6      two   4
# 为columns添加一个名字
data.columns.name = 'col'
col     k1  k2
state         
0      one   1
1      two   1
2      one   2
3      two   3
4      one   3
5      two   4
6      two   4
# 索引的is_unique属性可以告诉你它的值是否是唯一的
df.index.is_unique

# 修改行或列的顺序
df = pd.DataFrame(np.arange(24).reshape((6,4)), index=np.arange(6)+1, columns=['a', 'b', 'c', 'd'])
# 修改行的顺序
b = df.reindex([2,3,5,6,1,4])
# 修改列的顺序
b = df.reindex(columns=['b','c','a','d'])

# 删除dataframe的一列，直接原地修改
del df['d']

df = pd.DataFrame(np.arange(24).reshape((6,4)), index=np.arange(6)+1, columns=['a', 'b', 'c', 'd'])
# 删除dataframe中的行 index的值为[2,4]
b = df.drop([2,4])
# 删除dataframe中的列 列名的值列表为['a']
b = df.drop(['a'],axis=1)

# 删除series中指定index的值
a = pd.Series([1,3,4])
# 就地删除a中index为0的值
a.drop(0,inplace=True)
a.drop(['d', 'c']) # 删除index为d和c的
# 不修改a本身的值
b= a.drop(0)

# 把dataframe中的某列作为新的index
df.set_index(["Column"], inplace=True)

df = pd.DataFrame(np.arange(12).reshape(((3,4))))
# 把df转为ndarray
a=np.asarray(df,'float64')
a=df.values

# 把series或dataframe中的某些值替换为新的值
df.replace({'one':'one1',1:'one'}) # 字典中 原值:替换值
data.replace([-999, -1000], np.nan)
```

# 处理缺失数据NaN

```python
import pandas as pd
import numpy as np

dates = pd.date_range('20130101', periods=6)
df = pd.DataFrame(np.arange(24).reshape((6, 4)),
                  index=dates,
                  columns=['A', 'B', 'C', 'D'])
df.iloc[0,1]=np.nan
df.iloc[1,2]=np.nan
# 对dataframe而言，dropna()默认去掉含有缺陷值的行
# 丢掉值为nan所在的行
# axis=0表示丢掉行,how='any'表示只要该行中有一个值为nan，就丢掉
# 如果how='all'，则表示所有值为nan丢掉
# 参数thresh=n,即这一行去除na值，剩余值的数量>=n
df.dropna(axis=0, how='any')
# 对series而言，dropna()返回非空数据,data[data.notnull()]


# 把值为nan的变为其他数值,下面变为0
df.fillna(value=0)
# 对df不同的列中的nan填充不同的值，第0列填充0.5，第1列填充1.5，
# 默认返回新对象，若就地修改，inplace=True
a=df.fillna({0:0.5,1:1.5})

# 检查每个值是否是nan，如果是则该位置为True，否则为false
df.isnull()
#                 A      B      C      D
# 2013-01-01  False   True  False  False
# 2013-01-02  False  False   True  False
# 2013-01-03  False  False  False  False
# 2013-01-04  False  False  False  False
# 2013-01-05  False  False  False  False
# 2013-01-06  False  False  False  False

# 判断里面是否有一个满足条件，满足则为TRUE
np.any(df.isnull() == True)
print(df)
# 判断哪些行（有一个TRUE）满足条件
(np.abs(data) > 3).any(1)

# 两个dataframe做运算，如果有缺失值，把缺省值用指定值替代
df1 = pd.DataFrame(np.arange(12).reshape(((3,4))))
df2 = pd.DataFrame((np.arange(12)-1).reshape(((3,4))))
df2.iloc[0,0] = np.nan
res = df1.add(df2,fill_value=0)
# 除了add，sub，div /,floordiv //, pow, mul同理
df.sum() # 按列求和，返回一个series，如果传入axis='columns'则按行求和，nan值自动排除
df.mean(skipna=False) # 加上了skipna=False表示nan运算结果仍为nan
df.idxmax() #对每一列，其最大值所在的行索引index，返回series，最小值为idxmin
# 常用统计方法 对每一列 count(非nan值数)，
# median中位数
```

# 处理重复行

```python
data = pd.DataFrame({'k1': ['one', 'two'] * 3 + ['two'], 'k2': [1, 1, 2, 3, 3, 4, 4]})
# duplicated方法返回一个布尔型Series 表示各行是否在前面出现过
b=data.duplicated()
# drop_duplicates方法去除重复行，返回dataframe，如果指定按某些列过滤，用drop_duplicates([])
# 若保留最后一次出现的，使用参数keep='last'
b=data.drop_duplicates()

# 得到Series中的values唯一值数组
series.unique()
```

# 离散化和面元划分

连续数据常常被离散化或拆分为“面元”（bin）

```python
ages = [20, 22, 25, 27, 21, 23, 37, 31, 61, 45, 41, 32]
# 这些数据划分为“18到25”、“26到35”、“35到60”以及“60以上”几个面元
bins = [18, 25, 35, 60, 100]
# 默认情况下左开右闭，如果想左闭右开可以通过right=False进行修改
# 如果age中的值不在bins包含的区间中，则为nan
# 可以通过传递一个列表或数组到labels，设置自己的面元名称，例如group_names = ['Youth', 'YoungAdult', 'MiddleAged', 'Senior']
# pd.cut(ages, bins, labels=group_names)
cats = pd.cut(ages, bins) # 返回的是一个特殊的Categorical对象，可以将其看做一组表示面元名称的字符串
# cats.codes表示age中每个元素新的表示[0 0 0 1 0 0 2 1 3 2 2 1]
b=cats.codes
# cats.categories有点分类标准，与bins差不多
c=cats.categories

# 如果向cut传入的是面元的数量而不是确切的面元边界，则它会根据数据的最小值和最大值计算等长面元
# 我们将一些均匀分布的数据分成四组
data = np.random.rand(20)
pd.cut(data, 4, precision=2) #选项precision=2，限定小数只有两位

# qcut是一个非常类似于cut的函数，它可以根据样本分位数对数据进行面元划分
# qcut由于使用的是样本分位数，因此可以得到大小基本相等的面元：
data = np.random.randn(1000)
# 分成4部分
cats = pd.qcut(data, 4)
```

# 检测和过滤异常值

```python
# 将绝对值超过3的变为-3或3
data[np.abs(data) > 3] = np.sign(data) * 3
```

# 排列和随机采样

```python
# 对0-4的五个数字生成一个随机整数数组
b = np.random.permutation(5)
# 打乱dataframe的行的顺序，首先有一个permutation生成的随机整数数组
df.take(b)

# 随机采样sample方法，对行进行采样，每行元素不会被重复选择，下面表示选取三行
df.sample(n=3)
# 如果想每行元素可以被重复选择，传递参数replace=True即可
```

# 计算指标/哑变量

将分类变量（categorical variable）转换为“哑变量”或“指标矩阵”

如果DataFrame的某一列中含有k个不同的值，则可以派生出一个k列矩阵或DataFrame（其值全为1和0）

```python
df = pd.DataFrame({'key': ['b', 'b', 'a', 'c', 'a', 'b']})
print(pd.get_dummies(df['key']))
# get_dummies参数prefix可以在列名前加上前缀，例如下面列名a，b，c可以都有前缀
   key
0   b
1   b
2   a
3   c
4   a
5   b
   a  b  c
0  0  1  0
1  0  1  0
2  1  0  0
3  0  0  1
4  1  0  0
5  0  1  0
```

# 字符串操作

```python
# 子串定位
'guido' in val
val.index(',') # 如果找不到字符串index会抛出异常，而find不会
val.find(':') # 返回-1表示不在其中

# count可以返回指定子串出现的次数
val.count(',')

# replace用于替换字符串，如果替换后的字符串为空字符串，则表示删除
val.replace(',', '::')
```

![img](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/7178691-087fe67bf6db0701.png)

![img](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/7178691-d1f0d4ed3e895016.png)

# 层次化索引（多级索引）

```python
data = pd.Series(np.random.randn(9),
                 index=[['a', 'a', 'a', 'b', 'b', 'c', 'c', 'd', 'd'],
                        [1, 2, 3, 1, 3, 1, 2, 2, 3]])
a  1    2.161872
   2    0.234322
   3    0.819109
b  1   -1.369456
   3   -0.081444
c  1    1.299434
   2    1.160797
d  2   -0.508928
   3   -0.976582
# 层次化索引 可以使用部分索引
# 一级索引访问
data['b']
data.loc[['b', 'd']]

# 访问二级索引，一级索引全选，二级索引中选为2的
data.loc[:, 2]
# 按行访问，访问数据集中的第一和第二行
data[0:2]

# series的多级索引 可以通过unstack方法变为一个dataframe，默认一级索引为行索引，二级索引为列索引，传入分层级别的编号或名称即可对其它级别进行unstack操作，例如result.unstack(0) result.unstack('state')
# unstack的逆运算是stack
# 默认情况下，unstack操作的是最内层（stack也是如此）
data.unstack()

# 把多级索引的某级索引变为列
# 把class所在的索引变为列，如果不加level参数，则表示把原index变为列
# 如果只是想去掉原index， df.reset_index(drop=True)
df.reset_index(level='class')

# 对于一个DataFrame，每条轴都可以有分层索引
df = pd.DataFrame(np.arange(12).reshape((4, 3)),
                     index=[['a', 'a', 'b', 'b'], [1, 2, 1, 2]],
                     columns=[['Ohio', 'Ohio', 'Colorado'],
                              ['Green', 'Red', 'Green']])
     Ohio     Colorado
    Green Red    Green
a 1     0   1        2
  2     3   4        5
b 1     6   7        8
  2     9  10       11
# 各级索引都可以指定名字
df.index.names = ['key1', 'key2']
df.columns.names = ['state', 'color']

# 根据列的一级索引访问
df['Ohio']
# 可以单独创建MultiIndex然后复用
MultiIndex.from_arrays([['Ohio', 'Ohio', 'Colorado'], ['Green', 'Red', 'Green']],names=['state', 'color'])

# 重排与分级排序
# 需要重新调整某条轴上 各级索引的顺序
# swaplevel接受两个级别编号或名称，并返回一个互换了级别的新对象（但数据不会发生变化）
df.swaplevel('key1', 'key2')
# sort_index则根据单个级别中的值对数据进行排序
# swaplevel(0, 1)是对行的一级索引和二级索引排序
# level的值默认取行的索引名
df.swaplevel(0, 1).sort_index(level=0)

# 根据级别汇总统计
# 列不变，默认在行索引上操作，根据level的值选择是在几级索引上统计求和
# 实际用的groupby功能
df.sum(level='key2')
# 在列索引上操作
df.sum(level='color', axis=1)

df = pd.DataFrame({'a': range(7), 'b': range(7, 0, -1),
                      'c': ['one', 'one', 'one', 'two', 'two',
                            'two', 'two'],
                      'd': [0, 1, 2, 0, 1, 2, 3]})
# set_index函数会将其一个或多个列转换为行索引，并创建一个新的DataFrame
# 默认情况下，那些列会从DataFrame中移除，但也可以将其保留下来 df.set_index(['c', 'd'], drop=False)
df.set_index(['c', 'd'])
# reset_index的功能跟set_index刚好相反，层次化index会被转移到列里面
df.reset_index()
```

# 合并DataFrame

pandas.merge可根据一个或多个键将不同DataFrame中的行连接起来。SQL或其他关系型数据库的用户对此应该会比较熟悉，因为它实现的就是数据库的join操作。

pandas.concat可以沿着一条轴将多个对象堆叠到一起。

实例方法combine_first可以将重复数据拼接在一起，用一个对象中的值填充另一个对象中的缺失值。

```python
import pandas as pd
import numpy as np

# 拼接多个series为一个series
s1 = pd.Series([0, 1], index=['a', 'b'])
s2 = pd.Series([2, 3, 4], index=['c', 'd', 'e'])
s3 = pd.Series([5, 6], index=['f', 'g'])
pd.concat([s1, s2, s3])

df1 = pd.DataFrame(np.ones((3,4))*0,columns=['a','b','c','d'])
df2 = pd.DataFrame(np.ones((3,4))*1,columns=['a','b','c','d'])
df3 = pd.DataFrame(np.ones((3,4))*2,columns=['a','b','c','d'])

# 拼接df1，df2，df3
# 纵向合并,可能出现行的index名称重复的情况，解决采用ignore_index
res= pd.concat([df1,df2,df3],axis=0,ignore_index=True)

# join, ['inner','outer']
df1 = pd.DataFrame(np.ones((3,4))*0,columns=['a','b','c','d'],index=[1,2,3])
df2 = pd.DataFrame(np.ones((3,4))*1,columns=['b','c','d','e'],index=[2,3,4])
print(df1)
print(df2)

# 纵向合并,默认为outer，即列为df1与df2列的并集
res = pd.concat([df1,df2])
#      a    b    c    d    e
# 1  0.0  0.0  0.0  0.0  NaN
# 2  0.0  0.0  0.0  0.0  NaN
# 3  0.0  0.0  0.0  0.0  NaN
# 2  NaN  1.0  1.0  1.0  1.0
# 3  NaN  1.0  1.0  1.0  1.0
# 4  NaN  1.0  1.0  1.0  1.0

# 默认为纵向合并，inner表示列为df1与df2的列名的交集
res = pd.concat([df1,df2],join='inner')

# 横向合并，横向的index取并集
res = pd.concat([df1,df2],axis=1)
print(res)
```

```python
import pandas as pd
import numpy as np

left = pd.DataFrame({'key': ['K0', 'K1', 'K2', 'K3'],
                     'A': ['A0', 'A1', 'A2', 'A3'],
                     'B': ['B0', 'B1', 'B2', 'B3']})
right = pd.DataFrame({'key': ['K0', 'K1', 'K2', 'K3'],
                      'C': ['C0', 'C1', 'C2', 'C3'],
                      'D': ['D0', 'D1', 'D2', 'D3']})
# print(left)
# print(right)
# 像join，默认情况下merge做的是内连接，两个df 列名为key所在的列的值，如果df1与df2相同，则合并
# 如果不指定on='key'，merge会将相同列名的列当做键
# 在进行列－列连接时，DataFrame对象中的索引会被丢弃
res = pd.merge(left, right, on='key')
# 如果两个对象的列名不同，也可以分别进行指定
pd.merge(df3, df4, left_on='lkey', right_on='rkey')

left = pd.DataFrame({'key1': ['K0', 'K0', 'K1', 'K2'],
                     'key2': ['K0', 'K1', 'K0', 'K1'],
                     'A': ['A0', 'A1', 'A2', 'A3'],
                     'B': ['B0', 'B1', 'B2', 'B3']})
right = pd.DataFrame({'key1': ['K0', 'K1', 'K1', 'K2'],
                      'key2': ['K0', 'K0', 'K0', 'K0'],
                      'C': ['C0', 'C1', 'C2', 'C3'],
                      'D': ['D0', 'D1', 'D2', 'D3']})
# print(left)
# print(right)
# 默认合并方法参数中 how=‘inner’还可以取值'outer','left','right'
res = pd.merge(left, right, on=['key1', 'key2'])

left = pd.DataFrame({
    'A': ['A0', 'A1', 'A2'],
    'B': ['B0', 'B1', 'B2']},
    index=['K0', 'K1', 'K2'])
right = pd.DataFrame({'C': ['C0', 'C1', 'C2'],
                      'D': ['D0', 'D1', 'D2']},
                     index=['K0', 'K2', 'K3'])
# print(left)
# print(right)
# 按照index合并，两个df 如果df1与df2的index名相同，则合并
res = pd.merge(left, right, left_index=True, right_index=True, how='outer')
pd.merge(left1, right1, left_on='key', right_index=True)
pd.merge(lefth, righth, left_on=['key1', 'key2'], right_index=True)

# 重命名列名,如果df1与df2都有相同的列名但合并的时候没有用（on=‘’没有用），则用suffixes重新命名
boys = pd.DataFrame({'k':['K0','K1','K2'],'age':[1,2,3]})
girls = pd.DataFrame({'k':['K0','K0','K3'],'age':[4,5,6]})
print(boys)
print(girls)
res = pd.merge(boys,girls,on='k',suffixes=['_boy','_girl'])
print(res)
```

# 数据聚合和分组运算

对数据集进行分组并对各组应用一个函数（无论是聚合还是转换）

![img](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/7178691-e5c671e09ecf94be.png)

```python
df = pd.DataFrame({'key1': ['a', 'a', 'b', 'b', 'a'],
                   'key2': ['one', 'two', 'one', 'two', 'one'],
                   'data1': np.random.randn(5),
                   'data2': np.random.randn(5)})
print(df)
# 按key1进行分组 然后计算data1列的平均值
df['data1'].groupby(df['key1']).mean()
# 按key1，key2进行分组 然后计算data1列的平均值
df['data1'].groupby([df['key1'], df['key2']]).mean()

# 将列名用作分组键
df.groupby('key1').mean()
df.groupby(['key1', 'key2']).mean()

# GroupBy的size方法，它可以返回一个含有分组大小的Series
df.groupby(['key1', 'key2']).size()
# key1  key2
# a     one     2
#       two     1
# b     one     1
#       two     1

# 对分组进行迭代，GroupBy对象支持迭代，可以产生一组二元元组（由分组名和数据块组成）
for name, group in df.groupby('key1'):
    print(name)
    print(group)

# 对于多重键的情况，元组的第一个元素将会是由键值组成的元组
for (k1, k2), group in df.groupby(['key1', 'key2']):
    print((k1, k2))
    print(group)
# 把分组做成 name:数据块 字典
pieces = dict(list(df.groupby('key1')))

# 选取一列或列的子集
df.groupby('key1')['data1']
df.groupby('key1')[['data2']]
# 下面等价
df['data1'].groupby(df['key1'])
df[['data2']].groupby(df['key1'])
```

```python
# 通过字典或series进行分组（自定义分组规则，比如把某几列分为一组）
people = pd.DataFrame(np.random.randn(5, 5),
                      columns=['a', 'b', 'c', 'd', 'e'],
                      index=['Joe', 'Steve', 'Wes', 'Jim', 'Travis'])
people.iloc[2:3, [1, 2]] = np.nan  # Add a few NA values
print(people)
# 假设已知列的分组关系，并希望根据分组计算列的和
mapping = {'a': 'red', 'b': 'red', 'c': 'blue',
           'd': 'blue', 'e': 'red', 'f': 'orange'}
# 这里的mapping也可以改为series
map_series = pd.Series(mapping)
people.groupby(mapping, axis=1).sum()

# 通过函数分组
# 该函数应用在各个索引值上，其返回值就会被用作分组名称
people.groupby(len).sum()

# 根据索引级别(多级索引)分组
columns = pd.MultiIndex.from_arrays([['US', 'US', 'US', 'JP', 'JP'],
                                     [1, 3, 5, 1, 3]],
                                    names=['cty', 'tenor'])
hier_df = pd.DataFrame(np.random.randn(4, 5), columns=columns)
print(hier_df)
# 要根据级别分组，使用level关键字传递级别序号或名字
hier_df.groupby(level='cty', axis=1).count()
```

## 数据聚合

![img](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/7178691-ba8de524e08b1b6f.png)

```python
# 在分组中使用自己的聚合函数
def peak_to_peak(arr):
    return arr.max() - arr.min()

df = pd.DataFrame({'key1': ['a', 'a', 'b', 'b', 'a'],
                   'key2': ['one', 'two', 'one', 'two', 'one'],
                   'data1': np.array([1,2,3,4,5]),
                   'data2': np.array([6,7,8,9,10])})
print(df)
# 对各列执行peak_to_peak函数
df.groupby('key1').agg(peak_to_peak)

df = pd.DataFrame({'key1': ['a', 'a', 'b', 'b', 'a'],
                   'key2': ['one', 'two', 'one', 'two', 'one'],
                   'data1': np.array([1,2,3,4,5]),
                   'data2': np.array([6,7,8,9,10])})
print(df)
# 每一列一次应用多个函数
# 传入一组函数或函数名，DataFrame的每一列就会以相应的函数命名（生成二级索引）
df.groupby('key1').agg(['mean', 'sum'])
# 对聚合后的列名重命名，对mean重命名为foo，对sum重命名为bar
df.groupby('key1').agg([('foo', 'mean'), ('bar', 'sum')])

# 对不同的列应用不同的函数。向agg传入一个从列名映射到函数的字典
# data1所在的列应用max函数，data2所在的列应用sum函数
df.groupby('key1').agg({'data1' : np.max, 'data2' : 'sum'})
df.groupby('key1').agg({'data1' : ['min', 'max'],'data2' : 'sum'})

# 返回某列最大的两个值所在的行
def top(df, n=2, column='data1'):
    return df.sort_values(by=column)[-n:]

df = pd.DataFrame({'key1': ['a', 'a', 'b', 'b', 'a'],
                   'key2': ['one', 'two', 'one', 'two', 'one'],
                   'data1': np.array([1, 4, 3, 2, 5]),
                   'data2': np.array([6, 10, 8, 9, 7])})
print(df)
# 对分组后的每组都找到最大的两行
df.groupby('key1').apply(top)
# 如果不想构成层次化索引 在groupby的参数中加上group_keys=False，这样groupby的key还是一列
```

# plot

![img](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/7178691-6d9fbf863c09370a.png)

![img](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/7178691-44e50562aeb5eb49.png)

````python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# Series
data = pd.Series(np.random.randn(1000),index=np.arange(1000))
data = data.cumsum()
# 展示数据 series，默认为线型图
# Series对象的索引会被传给matplotlib，并用以绘制X轴。可以通过use_index=False禁用该功能
data.plot()

# dataframe
# 每一列表示一个数据y，这里有4列，因此有4条线
data = pd.DataFrame(np.random.randn(1000,4),
                    index=np.arange(1000),
                    columns=list('ABCD'))
data = data.cumsum()
data.plot()

# 柱状图 plot.bar()和plot.barh()分别绘制水平和垂直的柱状图
# 柱状图有一个非常不错的用法：利用value_counts图形化显示Series中各值的出现频率，比如s.value_counts().plot.bar()
fig, axes = plt.subplots(2, 1)
data = pd.Series(np.random.rand(16), index=list('abcdefghijklmnop'))
data.plot.bar(ax=axes[0], color='k', alpha=0.7)
data.plot.barh(ax=axes[1], color='k', alpha=0.7)
# 对于DataFrame，柱状图会将每一行的值分为一组，并排显示
df = pd.DataFrame(np.random.rand(6, 4),
                  index=['one', 'two', 'three', 'four', 'five', 'six'],
                  columns=pd.Index(['A', 'B', 'C', 'D'], name='Genus'))
df.plot.bar()

# 散点图
# x='A'表示x的数据为列名A对应的数据，y=‘B’表示y的数据为列名B对应而数据
ax = data.plot.scatter(x='A',y='B',color='b',label='Class 1')
data.plot.scatter(x='A',y='C',color='r',label='Class 2',ax=ax)

plt.show()
````

