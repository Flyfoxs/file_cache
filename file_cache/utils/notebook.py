import os
import sys

def adjust_wkdir(cut_folder='notebook'):
    abspath = os.path.abspath('.')
    wk_dir = abspath.replace(cut_folder,'')
    os.chdir(wk_dir)
    sys.path.append('.')
    print(f'File_cache: Adjust notebook work fold to:{wk_dir}')
    return wk_dir

