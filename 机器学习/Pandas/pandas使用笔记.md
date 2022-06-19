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

