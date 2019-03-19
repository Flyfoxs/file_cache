
import logging

from file_cache.utils.other import replace_useless_mark

format_str = '%(asctime)s %(thread)d %(filename)s[%(lineno)d] %(levelname)s %(message)s'
format = logging.Formatter(format_str)
logging.basicConfig(level=logging.DEBUG, format=format_str)

logger = logging.getLogger()

#handler = logging.FileHandler('./log/forecast.log', 'a')
# handler.setFormatter(format)
# logger.addHandler(handler)


# def is_mini_args(item):
#     from file_cache.utils.other import is_mini_args
#     return is_mini_args(item)


def get_mini_args(args):
    from file_cache.utils.other import get_pretty_info
    return get_pretty_info(args)


import functools
import time
def timed(logger=logger, level='info', format='%s: %s ms', paras=True):

    if level.lower() == 'info':
        log = logger.info
    else:
        log = logger.debug


    def decorator(fn):

        @functools.wraps(fn)
        def inner(*args, **kwargs):
            start = time.time()
            from file_cache.utils.other import is_mini_args
            args_mini = [item  if is_mini_args(item) else type(item).__name__ for item in args  ]

            kwargs_mini = [ (k, v ) if is_mini_args(v) else (k, type(v).__name__) for k, v in kwargs.items()]
            arg_count = len(args) + len(kwargs)
            if paras:
                log(replace_useless_mark("%s begin with(%s paras) :%r, %r" % (fn.__name__, arg_count, args_mini, kwargs_mini)))
            else:
                log(f"{fn.__name__} begin with {arg_count} paras")
            try:
                result = fn(*args, **kwargs)
            except Exception as e:
                logger.exception(e)
                logger.error(f'Exception from: {fn.__name__}({args_mini}, {kwargs_mini}), end with:{type(e)}')

                raise e
            duration = time.time() - start
            if duration < 60:
                duration = f'{duration:04.1f} sec'
            else:
                duration = f'{duration/60.0:04.1f} min'
            log(replace_useless_mark(f'cost {duration}:{fn.__name__}({args_mini}, {kwargs_mini}), return:{summary_result(result)}, end '))


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
    elif isinstance(result, (list, dict, set, tuple)):
        return f'{type(result).__name__}:{len(result)}',
    else :
        return type(result).__name__,


#@timed(level='info')
def logger_begin_paras(paras):
    import socket
    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    logger.info(f'Start the program at:{host_name}, {host_ip}, with:{paras}')

print('yes')
logger_begin_paras("Load module")

@timed()
def test(a, b):
    raise Exception('XXX')

if __name__ == '__main__':
    test()