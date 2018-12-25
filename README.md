
# File Case
- This is used to cache the Dataframe result, even there are multiply Dataframe
- It also support to log the function time cost and parameters


## Sample case


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

    2018-12-25 22:40:42,026 util_log.py[61] DEBUG Start the program at:LALI2-M-G0MD, 127.0.0.1, with:Load module
    2018-12-25 22:40:42,029 util_log.py[41] INFO Begin:test_cache_normal(1 paras) with:['Felix'], []
    2018-12-25 22:40:42,178 cache.py[29] DEBUG try to read cache from file:./cache/test_cache_normal=Felix=.h5, (h5, key:['/df_0'])
    2018-12-25 22:40:42,189 util_log.py[49] INFO Cost:   0.16 sec:'test_cache_normal'(1 paras)(['Felix'], []), return:DataFrame, end 





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
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



## Return mulpiple DF with tuple
Support to cache multiple DF with tuple


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

    2018-12-25 22:40:42,227 util_log.py[41] INFO Begin:test_cache_tuple(1 paras) with:['Felix2'], []
    2018-12-25 22:40:42,252 cache.py[29] DEBUG try to read cache from file:./cache/test_cache_tuple=Felix2=.h5, (h5, key:['/df_0', '/df_1'])
    2018-12-25 22:40:42,273 util_log.py[49] INFO Cost:   0.05 sec:'test_cache_tuple'(1 paras)(['Felix2'], []), return:tuple, end 


        0   1   2   3   4
    0   5   6   7   8   9
    1  10  11  12  13  14 
    
        0   1   2   3   4
    0  20  21  22  23  24
    1  25  26  27  28  29


## For the input paras can not be cached
If the input is DF or cannot be hashed, ignore the cache, run the function directly


```python
@file_cache()
def test_cache_ignore(name):
    df0 = pd.DataFrame(data= np.arange(5,15).reshape(2,5))
    return df0

df = pd.DataFrame(data= np.arange(5,15).reshape(2,5))
ignore = test_cache_ignore(df)

```

    2018-12-25 22:40:42,302 util_log.py[41] INFO Begin:test_cache_ignore(1 paras) with:['DataFrame'], []
    2018-12-25 22:40:42,307 cache.py[112] DEBUG There is DataFrame in the args
    2018-12-25 22:40:42,309 cache.py[94] WARNING Don not support cache for fn:test_cache_ignore, para:DataFrame, kw:{}
    2018-12-25 22:40:42,312 util_log.py[49] INFO Cost:   0.01 sec:'test_cache_ignore'(1 paras)(['DataFrame'], []), return:DataFrame, end 


## Log the function time and parameter


```python
from file_cache.utils.util_log import *
@timed()
def log_time(arg):
    return f'{arg} msg'

print(log_time("hello"))
```

    2018-12-25 22:40:42,332 util_log.py[41] INFO Begin:log_time(1 paras) with:['hello'], []
    2018-12-25 22:40:42,339 util_log.py[49] INFO Cost:   0.01 sec:'log_time'(1 paras)(['hello'], []), return:hello msg, end 


    hello msg

