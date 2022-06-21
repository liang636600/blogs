字典形式的numpy

# 数据初始化

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

# 行名
print(df2.index)
# 列名
b = df2.columns
# 所有的值
b = df2.values
# 描述一些常用的数学属性，例如平均值，方差，最大最小值
b = df2.describe()
# 把df里的values值当做矩阵，转置
df2.T

# 排序列名或行名
# axis=1从行的角度看，画十字排序
b = df2.sort_index(axis=1,ascending=False)
#      F      E  D    C          B  A
# 0  foo   test  3  1.0 2013-01-02  1
# 1  foo  train  3  1.0 2013-01-02  1
# 2  foo   test  3  1.0 2013-01-02  1
# 3  foo  train  3  1.0 2013-01-02  1

# axis=0从列的角度看，画十字排序
b = df2.sort_index(axis=0,ascending=False)
#    A          B    C  D      E    F
# 3  1 2013-01-02  1.0  3  train  foo
# 2  1 2013-01-02  1.0  3   test  foo
# 1  1 2013-01-02  1.0  3  train  foo
# 0  1 2013-01-02  1.0  3   test  foo

# 对值排序
b = df2.sort_values(by='E')
````

# 值的选择

```python
import pandas as pd
import numpy as np

dates = pd.date_range('20130101', periods=6)
df = pd.DataFrame(np.arange(24).reshape((6, 4)),
                  index=dates,
                  columns=['A', 'B', 'C', 'D'])
# 选择某一列 df['列名']或df.列名
# print(df['A'])

# 选择某几行 下面表示选择第0~2行
# print(df[0:3])

# 选择行列
# 第一种方式 loc 通过行和列的名称
# 下面表示选择所有行，列名为'A','B'的列
# print(df.loc[:,['A','B']])
# 打印某一行，某一列数据
# print(df.loc['20130102',['A','B']])

# 第二种方式 iloc 通过行和列的数字index
# 第三行，所有列
# print(df.iloc[3,:])
# 第1，3,5行，1:3列
print(df.iloc[[1,3,5],1:3])

# 筛选列满足条件的
# 列名为A的列，选出其中值<8的行
print(df[df.A < 8])
```

# 设置值

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

# 加一个新的列
df['F'] = np.nan
# 如果是series，必须要指定index
df['E'] = pd.Series([1,2,3,4,5,6], index=dates)
print(df)
```

# 处理丢失数据NaN

```python
import pandas as pd
import numpy as np

dates = pd.date_range('20130101', periods=6)
df = pd.DataFrame(np.arange(24).reshape((6, 4)),
                  index=dates,
                  columns=['A', 'B', 'C', 'D'])
df.iloc[0,1]=np.nan
df.iloc[1,2]=np.nan
# 丢掉值为nan所在的行
# axis=0表示丢掉行,how='any'表示只要该行中有一个值为nan，就丢掉
# 如果how='all'，则表示所有值为nan丢掉
df.dropna(axis=0, how='any')

# 把值为nan的变为其他数值,下面变为0
df.fillna(value=0)

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
```

# 合并DataFrame

```python
import pandas as pd
import numpy as np

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
# 像join，两个df 列名为key所在的列的值，如果df1与df2相同，则合并
res = pd.merge(left, right, on='key')

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

# 重命名列名,如果df1与df2都有相同的列名但合并的时候没有用（on=‘’没有用），则用suffixes重新命名
boys = pd.DataFrame({'k':['K0','K1','K2'],'age':[1,2,3]})
girls = pd.DataFrame({'k':['K0','K0','K3'],'age':[4,5,6]})
print(boys)
print(girls)
res = pd.merge(boys,girls,on='k',suffixes=['_boy','_girl'])
print(res)
```

# plot

````python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# Series
data = pd.Series(np.random.randn(1000),index=np.arange(1000))
data = data.cumsum()
# 展示数据 series
data.plot()

# dataframe
# 每一列表示一个数据y，这里有4列，因此有4条线
data = pd.DataFrame(np.random.randn(1000,4),
                    index=np.arange(1000),
                    columns=list('ABCD'))
data = data.cumsum()
data.plot()
# 散点图
# x='A'表示x的数据为列名A对应的数据，y=‘B’表示y的数据为列名B对应而数据
ax = data.plot.scatter(x='A',y='B',color='b',label='Class 1')
data.plot.scatter(x='A',y='C',color='r',label='Class 2',ax=ax)

plt.show()
````

