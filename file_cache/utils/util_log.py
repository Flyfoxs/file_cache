
import logging


format_str = '%(asctime)s %(filename)s[%(lineno)d] %(levelname)s %(message)s'
format = logging.Formatter(format_str)
logging.basicConfig(level=logging.DEBUG, format=format_str)

logger = logging.getLogger()

#handler = logging.FileHandler('./log/forecast.log', 'a')
# handler.setFormatter(format)
# logger.addHandler(handler)

def is_mini_args(item):
    from file_cache.utils.other import is_mini_args
    return is_mini_args(item)


def get_mini_args(args):
    from file_cache.utils.other import get_pretty_info
    return get_pretty_info(args)


import functools
import time
def timed(logger=logger, level=None, format='%s: %s ms', paras=True):
    if level is None:
        level = logging.DEBUG


    def decorator(fn):
        @functools.wraps(fn)
        def inner(*args, **kwargs):
            start = time.time()
            args_mini = [item  if is_mini_args(item) else type(item).__name__ for item in args  ]

            kwargs_mini = [ (k, v ) if is_mini_args(v) else (k, type(v).__name__) for k, v in kwargs.items()]
            arg_count = len(args) + len(kwargs)
            if paras:
                logger.info("%s begin with(%s paras) :%r, %r" % (fn.__name__, arg_count, args_mini, kwargs_mini))
            else:
                logger.info(f"{fn.__name__} begin with {arg_count} paras")
            result = fn(*args, **kwargs)
            duration = time.time() - start
            logging.info('%s cost %7.2f sec:(%s paras)(%r, %r), return:%s, end '
                         % (fn.__name__,duration,  arg_count,
                            args_mini, kwargs_mini,
                            result if isinstance(result, (str, int, float)) else type(result).__name__,
                            ))
            #logger.log(level, format, repr(fn), duration * 1000)
            return result
        return inner

    return decorator

def logger_begin_paras(paras):
    import socket
    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    logger.debug(f'Start the program at:{host_name}, {host_ip}, with:{paras}')


logger_begin_paras("Load module")