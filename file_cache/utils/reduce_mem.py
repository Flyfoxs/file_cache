import functools

import numpy as np
import pandas as pd

from file_cache.utils.util_log import logger, timed_bolck, ex_type_name

"""
core function is copy from below link, just wrap it with decorator
https://www.kaggle.com/artgor/elo-eda-and-models

"""


def reduce_mem():
    def decorator(fn):
        #@timed()
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            val = fn(*args, **kwargs)
            with timed_bolck(f'Reduce_Mem({fn.__name__}:{ex_type_name(val)})'):
                if isinstance(val, (pd.DataFrame,)) :
                    val = _reduce_mem_usage(val, verbose=True)
                if isinstance(val, tuple) and all([ isinstance(df, (pd.DataFrame, pd.Series )) for df in val]):
                    val = tuple([  _reduce_mem_usage(df, verbose=True)  for df in val])
                else:
                    logger.warning(f'The return type for fun#{fn.__name__} is:{type(val)}')
            return val
        return wrapper
    return decorator


def _reduce_mem_usage(df, verbose=True):
    if isinstance(df, pd.Series):
        return df
    numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
    mem = df.memory_usage()
    mem = mem if isinstance(mem, (int, float)) else mem.sum()
    start_mem = mem / 1024**2
    for sn, col in enumerate(df.columns):
        col_type = df[col].dtypes
        if col_type in numerics:
            c_min = df[col].min()
            c_max = df[col].max()
            if str(col_type)[:3] == 'int':
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    df[col] = df[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)
                elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
                    df[col] = df[col].astype(np.int64)
            else:
                if c_min > np.finfo(np.float16).min and c_max < np.finfo(np.float16).max:
                    df[col] = df[col].astype(np.float16)
                else:
                    df[col] = df[col].astype(np.float32)
                # else:
                #     df[col] = df[col].astype(np.float64)
            if col_type == df[col].dtypes:
                logger.info(f'No need to change type for:{col}#{col_type}, {sn}/{len(df.columns)}')
            else:
                logger.info(f'Change {col}#{col_type} => {df[col].dtypes}, {sn}/{len(df.columns)}')
    mem = df.memory_usage()
    mem = mem if isinstance(mem, (int, float)) else mem.sum()
    end_mem = mem / 1024**2
    if verbose:
        logger.info(f'Current dtypes:\n {df.dtypes.value_counts()}')
        logger.debug('Mem. usage decreased from {:7.2f} to {:7.2f} Mb ({:.1f}% reduction)'.format(start_mem, end_mem, 100 * (start_mem - end_mem) / start_mem))
    return df


if __name__ == '__main__':
    from file_cache.cache import file_cache
    #@file_cache()
    @reduce_mem()
    def test_df(test):
        from sklearn import datasets
        import pandas as pd
        import numpy as np
        data = datasets.load_boston()
        df = pd.DataFrame(data.data, columns=data.feature_names)
        print(df.dtypes)
        return df#, df.copy(), df.copy()


    logger.debug(len(test_df('xx')))
