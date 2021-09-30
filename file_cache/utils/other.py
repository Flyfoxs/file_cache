import numpy as np
import pandas as pd


def is_mini_args(item):
    if isinstance(item, (str, int, float)):
        return True
    if '__len__' in dir(item) and len(item) >=20:
        return False
    elif isinstance(item, (tuple, list, pd.Series, dict)) and len(item) <= 20 :
        return True
    elif type(item) in (tuple, list, dict, pd.DataFrame, pd.SparseDataFrame):
        return False
    elif item is None:
        return False
    else:
        return True


# def get_all_file(path):
#     import os
#     #logger.debug(f'Try to read file from"{path}')
#     file_list = os.listdir(path)
#     file_list = [file for file in file_list if '.h5' in file]
#     return file_list

# def save_result_for_ensemble(name, label_name,  **kwargs,):
#     """"
#     name = '{score}_name'
#     """
#     import os
#     folder = f'./output/1level/{label_name}'
#     if not os.path.exists(folder):
#         os.makedirs(folder)
#
#     file = f'./output/1level/{label_name}/baseline_{name}.h5'
#     file = replace_invalid_filename_char(file)
#     store = pd.HDFStore(file)
#
#     if kwargs is not None:
#         for key, value in kwargs.items():
#             if key is not None:
#                 store[f'{key}'] = value
#                 logger.debug(f'Stove {key} to file#{file}  , size:{value.shape}')
#
#     store.close()
#     logger.debug(f"Ensamble file save to file: {file}")
#     return file

