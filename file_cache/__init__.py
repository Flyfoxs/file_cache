from .utils.util_log import timed_bolck, timed
from .utils.notebook import adjust_wkdir
from .cache import file_cache
from .utils.reduce_mem import *



#from .utils.util_pandas import *

# try:
#     from pyforest import *
# except Exception:
#     print('Warning: Import pyforest, No impact at all')


try:
    import os
    import sys
    import itertools
    from functools import lru_cache, partial
    import matplotlib.pyplot as plt
    import pandas as pd
    import numpy as np
    from easydict import EasyDict as edict

    # from tqdm import tqdm
    # from glob import glob

    import pprint; pp = pprint.PrettyPrinter(indent=4)

    import warnings; warnings.filterwarnings("ignore")

    import cv2
    from .utils.tqdm_enhance import *
    import nibabel as nib
    import pydicom

except Exception as e:
    print(e)
    print('Warning: Import Error, No big impact')


try:
    if in_notebook(): 
        adjust_wkdir()
        from file_cache.utils.visual import *
except Exception as e:
    print('Adjust wk folder for notebook failed')

