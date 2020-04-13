
import logging
import numpy as np
import pandas as pd

format_str = '%(asctime)s %(filename)s[%(lineno)d] %(levelname)s %(message)s'
format = logging.Formatter(format_str)
ch = logging.StreamHandler()
ch.setFormatter(format)

logging.basicConfig(level=logging.INFO, format=format_str, handlers=[ch])

logger = logging.getLogger('main')

#logger.setLevel(logging.DEBUG)
#handler = logging.FileHandler('./log/forecast.log', 'a')
# handler.setFormatter(format)
# logger.addHandler(handler)


def get_mini_args(args):
    from file_cache.utils.other import get_pretty_info
    return get_pretty_info(args)

def ex_type_name(item):

    if isinstance(item, (np.ndarray)) and item.ndim==1 and len(item)<=10:
        return str(item)
    elif isinstance(item,(np.ndarray, pd.DataFrame) ):
        return f'{type(item).__name__}:{item.shape}'
    #All type in tuple is DF or numpy
    elif isinstance(item, (tuple, list, set)) and all([ isinstance(one,(pd.DataFrame, np.ndarray, pd.Series) ) for one in item]):
        return [f'{type(one).__name__}:{one.shape}'  for one in item]
    #All type in tuple is simple obj
    elif isinstance(item, (tuple, list, set)) and all([ isinstance(one,(str, int, float) ) for one in item]):
        return [one for one in item]
    elif isinstance(item,(set, list, tuple, dict) ):
        return f'{type(item).__name__}:{len(item)}'
    else:
        return type(item).__name__

import functools
import time
def timed(paras=True, disable=False):
    logger_ = logging.getLogger("timed")
    logger_.setLevel(logging.INFO)
    #logger_.addHandler(ch)
    from file_cache.utils.other import replace_useless_mark

    if disable:
        log = lambda val: val
    else:
        log = logger_.info

    def decorator(fn):

        @functools.wraps(fn)
        def inner(*args, **kwargs):
            start = time.time()
            from file_cache.utils.other import is_mini_args
            args_mini = [item  if is_mini_args(item) else ex_type_name(item) for item in args  ]

            kwargs_mini = [ (k, v ) if is_mini_args(v) else (k, ex_type_name(v)) for k, v in kwargs.items()]
            arg_count = len(args) + len(kwargs)
            if paras:
                log(replace_useless_mark("FN#%s begin with(%s paras) :%s, %s" % (fn.__name__, arg_count, args_mini, kwargs_mini)))
            else:
                log(f"{fn.__name__} begin with {arg_count} paras")
            try:
                result = fn(*args, **kwargs)
            except Exception as e:
                logger_.exception(e)
                logger_.error(f'Exception from: FN#{fn.__name__}({args_mini}, {kwargs_mini}), end with:{type(e)}')

                raise e
            duration = time.time() - start
            if duration < 60:
                duration = f'{duration:04.1f} sec'
            else:
                duration = f'{duration/60.0:04.1f} min'
            log(replace_useless_mark(f'<<cost {duration}>>:FN#{fn.__name__}({args_mini}, {kwargs_mini}), return:{summary_result(result)}, end '))


            #logger.log(level, format, repr(fn), duration * 1000)
            return result
        return inner

    return decorator


def summary_result(result):
    import pandas as pd
    if isinstance(result, (str, int, float)) :
        return result
    elif isinstance(result, pd.DataFrame):
        if result.empty:
            return 'DF:Empty'
        else:
            return f'DF:{result.shape}'
    elif isinstance(result, (list, dict, set, tuple, np.ndarray)):
        return ex_type_name(result)
    else :
        return type(result).__name__

import contextlib
import datetime




@contextlib.contextmanager
def timed_block(name='Default_block'):
    logger_ = logging.getLogger("timed_block")
    logger_.setLevel(logging.INFO)
    #logger_.addHandler(ch)

    begin = datetime.datetime.now()
    logger_.info(f'BLOCK#{name}, begin@{str(begin)[11:19]},id#{id(begin)}')
    try:
        exception = None
        yield begin
    except Exception as e:
        exception = e
        # logger.exception(e)
    finally:
        end = datetime.datetime.now()
        duration = (end - begin).total_seconds()
        if duration < 60:
            duration = f'{duration:04.1f} sec'
        else:
            duration = f'{duration / 60.0:04.1f} min'
        if exception is not None:
            logger_.info(
                f'BLOCK#{name}, End with Exception:{type(exception).__name__}, <<cost {duration}>>, end at:{str(end)[11:19]}, id#{id(begin)}')
            raise exception
        else:
            logger_.info(f'<<cost {duration}>>:BLOCK#{name}, , end@{str(end)[11:19]}, id#{id(begin)}')


timed_bolck = timed_block

#@timed(level='info')
def logger_begin_paras(paras):
    import socket
    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    logger.info(f'Start the program at:{host_name}, {host_ip}, with:{paras}')

logger_begin_paras("Load module")

@timed()
def test(a, b):
    return np.ones(5)

if __name__ == '__main__':


    #with timed_bolck():
        test(1, '2')
        test(1, 2.4)
        test(pd.DataFrame(), pd.DataFrame())