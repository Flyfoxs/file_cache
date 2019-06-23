
# 特征工程利器(通过本地文件缓存, 加速特征生成)
- 通过一行代码缓存你的Dataframe或者Series结果, 即使是返回多个DF或者Series也可以. 特别适合一个函数运行了很久计算出来的特征.
- 同时也支持显示函数的运行参数和运行的实际时间


## 安装
pip install file_cache

pip install git+https://github.com/Flyfoxs/file_cache@master

## 简单示例


```python
from  file_cache.cache import file_cache
import numpy  as np
import pandas as pd

@file_cache()
def test_cache_normal(name):
    import time
    import numpy  as np
    time.sleep(3)
    return pd.DataFrame(data= np.arange(0,10).reshape(2,5))

normal_df = test_cache_normal('Felix')
normal_df.head()
```
 



<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>0</th>
      <th>1</th>
      <th>2</th>
      <th>3</th>
      <th>4</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>1</td>
      <td>2</td>
      <td>3</td>
      <td>4</td>
    </tr>
    <tr>
      <th>1</th>
      <td>5</td>
      <td>6</td>
      <td>7</td>
      <td>8</td>
      <td>9</td>
    </tr>
  </tbody>
</table>
</div>



## 函数同时返回了多个DataFrame



```python
import time
from functools import lru_cache

@lru_cache()
@file_cache()
def test_cache_tuple(name):
    time.sleep(3)
    df0 = pd.DataFrame(data= np.arange(5,15).reshape(2,5))
    df1 = pd.DataFrame(data= np.arange(20,30).reshape(2,5))
    return df0, df1

df0, df1 = test_cache_tuple('Felix2')
print(df0 , '\n')
print(df1)
```
 

        0   1   2   3   4
    0   5   6   7   8   9
    1  10  11  12  13  14 
    
        0   1   2   3   4
    0  20  21  22  23  24
    1  25  26  27  28  29


## 如果入参不能缓存,比如如果入参是一个DataFrame

这样的缓存没有意义,这样的缓存会自动忽视,不会造成任何运行异常,只是无法优化性能

```python
@file_cache()
def test_cache_ignore(name):
    df0 = pd.DataFrame(data= np.arange(5,15).reshape(2,5))
    return df0

df = pd.DataFrame(data= np.arange(5,15).reshape(2,5))
ignore = test_cache_ignore(df)

```
 

## 自动记录函数的运行参数和消耗的时间


```python
from file_cache.utils.util_log import *
@timed()
def log_time(arg):
    return f'{arg} msg'

print(log_time("hello"))
```

    2018-12-26 11:08:52,662 util_log.py[61] DEBUG Start the program at:LALI2-M-G0MD, 127.0.0.1, with:Load module
    2018-12-26 11:08:52,665 util_log.py[41] INFO log_time begin with(1 paras) :['hello'], []
    2018-12-26 11:08:52,667 util_log.py[49] INFO log_time cost:   0.00 sec:(1 paras)(['hello'], []), return:hello msg, end 


    hello msg


## 不仅支持DataFrame,同时也支持Series


```python
from  file_cache.cache import file_cache
@file_cache()
def get_train_data():
    from sklearn import datasets
    import pandas as pd
    import numpy as np
    data = datasets.load_boston()
    df = pd.DataFrame( data.data , columns=data.feature_names)
    df['target'] = data.target
    df.head()
    return df, df['target']

df, series = get_train_data()
print(type(df), type(series))

df, series = get_train_data()
print(type(df), type(series))

```

    <class 'pandas.core.frame.DataFrame'> <class 'pandas.core.series.Series'>
    <class 'pandas.core.frame.DataFrame'> <class 'pandas.core.series.Series'>

