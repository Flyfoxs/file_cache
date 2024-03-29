
import os
import pandas as pd
from file_cache.utils.other import is_mini_args
from file_cache.utils.util_log import logger, get_mini_args, timed
import time
import numpy as np


class Cache_File:
    def __init__(self):
        self.df_key = 'df'
        self.cache_path='./.cache/'
        self.enable=True
        self.date_list = ['start','close','start_base','weekbegin', 'tol_day_cnt_min',	'tol_day_cnt_max']
        if not os.path.exists(self.cache_path):
            os.mkdir(self.cache_path)

    def get_path(self, key, type):
        return f'{self.cache_path}{key}.{type}'

    def readFile(self, key, file_type):
        if self.enable:
            path = self.get_path(key, file_type)
            if os.path.exists(path):

                if file_type == 'h5':
                    with pd.HDFStore(path, mode='r') as store:
                        key_list = store.keys()
                    logger.debug(f"Read cache from file:{path},key:{key_list}")
                    if len(key_list) == 0:
                        return None
                    elif len(key_list) == 1 :
                        return pd.read_hdf(path, key_list[0])
                    else:
                        return tuple([ pd.read_hdf(path, key) for key in key_list])
                elif file_type == 'pickle':
                    return pd.read_pickle(path)
                elif file_type == 'parquet':
                    return pd.read_parquet(path)

            else:
                logger.debug(f"Can not find cache from file:{path}")
                return None
        else:
            logger.debug( "disable cache")


    def writeFile(self, key, val, file_type):
        if not self.enable :
            logger.debug('Cache is disable')
            return None

        if val is None or len(val)==0:
            logger.debug('Return value is None or empty')
            return val
        elif isinstance(val, tuple):
            val_tuple = val
        else:
            val_tuple = (val,)

        if all([ isinstance(item, (pd.DataFrame, pd.Series)) for item in val_tuple]) :
            path = self.get_path(key, file_type)
            if file_type == 'h5':
                for index, df in enumerate(val_tuple):
                    key = f'{self.df_key}_{index}'
                    logger.debug(f"====Write {len(df)} records to File#{path}, with:{key}")
                    df.to_hdf(path, key)
            elif file_type == 'pickle':
                pd.to_pickle(val, path)
            elif file_type == 'parquet':
                val.to_parquet(path)
            return val
        else:
            logger.warning(f'The return is not DataFrame or it is None:{[ isinstance(item, pd.DataFrame) for item in val_tuple]}')
            return val


cache = Cache_File()

import functools
def file_cache(overwrite=False, type='pickle', prefix=None):
    """
    :param time: How long the case can keep, default is 1 week
    :param overwrite: If force overwrite the cache
    :return:
    """
    def decorator(f):
        #@timed()
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            mini_args = get_mini_args(args)
            mini_kwargs = get_mini_args(kwargs)
            """Ignore the file cache, if the input parameter don't support cache"""
            if not is_support_cache(*args, **kwargs):
                logger.warning(f'Do not support cache for fn:{f.__name__}, para:{str(mini_args)}, kw:{str(kwargs)}')
                return f(*args, **kwargs)

            key = '='.join([f.__name__, str(mini_args), str(mini_kwargs)])
            key = key.replace('.', '_')
            key = key.replace('/', '_')
            while '__' in key:
                key = key.replace('__', '_')

            if prefix:
                key = '_'.join([prefix, key])
            if overwrite is False:
                val = cache.readFile(key, type)
            if val is None or overwrite is True:
                val = f(*args, **kwargs) #call the wrapped function, save in cache
                cache.writeFile(key, val, type)
            return val # read value from cache
        return wrapper
    return decorator


def is_support_cache(*args, **kwargs):
    for arg in args:
        if not is_mini_args(arg) and arg is not None:
            logger.debug(f'There is {type(arg).__name__} in the args')
            return False
    for _, arg in kwargs.items():
        if not is_mini_args(arg) and arg is not None:
            logger.debug(f'There is {type(arg).__name__} in the kwargs')
            return False
    return True


if __name__ == '__main__':

    @timed()
    @file_cache(type='parquet')
    def test_cache(name):
        import time
        import numpy  as np
        time.sleep(3)
        return pd.DataFrame(data= np.arange(0,10).reshape(2,5))


    @timed()
    @file_cache(type='parquet')
    def test_cache_2(name):

        time.sleep(3)
        df = pd.DataFrame(data= np.arange(0,10).reshape(2,5))
        return (df, df)


    print(test_cache('Felix'))
    #print(test_cache_2('Felix'))
    df = test_cache('Felix')
    df = test_cache('Felix')
    df = test_cache('Felix')
    df = test_cache('Felix')
    df = test_cache('Felix')

    #test_cache(df)
    #print(test_cache('Felix'))




