from file_cache.utils.util_log import timed_block, timed
from file_cache.utils.notebook import adjust_wkdir
from file_cache.utils.cache import file_cache
from file_cache.utils.reduce_mem import *
from file_cache.utils.tqdm_enhance import *

try:
    import os
    import sys
    import itertools
    from functools import lru_cache, partial
    import matplotlib.pyplot as plt
    import pandas as pd
    import numpy as np
    from easydict import EasyDict as edict
    from tqdm import tqdm
    from glob import glob
    import pprint; pp = pprint.PrettyPrinter(indent=4)
    import warnings; warnings.filterwarnings("ignore")
    from .utils.notebook import adjust_wkdir

except Exception as e:
    print('Warning: Some lib import error, No big impact')


try:
    if in_notebook():
        adjust_wkdir()
except Exception as e:
    print('Adjust wk folder for notebook failed')

