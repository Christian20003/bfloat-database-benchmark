import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Types')))

from typing import List
from Format import print_error, print_warning

def remove_files(files: List[str]) -> None:
    '''
    This function deletes a list of files.

    :param files: A list of file names.

    :raise RuntimeError: If something went wrong during deletion. 
    '''

    for file in files:
        try:
            os.remove(file)
        except FileNotFoundError:
            print_warning(f'{file} does not exist. Ignore deletion')
        except Exception as e:
            print_error(f'Failed to remove {file}', e)

def remove_dir(dirs: List[str]) -> None:
    '''
    This function deletes a list of directories.

    :param dirs: A list of directory names.
    '''
    
    for dir_name in dirs:
        try:
            os.system(f'rm -rf {dir_name}')
        except Exception as e:
            print_error(f'Failed to remove {dir_name}', e)

def create_dir(dir: str) -> None:
    '''
    This function generates a new directory. If the directory already
    exists, it will be deleted.

    :param dir: The name of the directory.
    '''
    
    if os.path.exists(dir):
        remove_dir([dir])
    os.mkdir(dir)

def copy_csv_file(src: str, dst: str, lines: int, columns: int) -> None:
    '''
    This function copies a CSV file from src to dst with n lines and m columns.

    :param src: The source file name.
    :param dst: The destination file name.
    :param lines: The number of lines to copy.
    :param columns: The number of columns to copy
    '''

    column = [value for value in range(1, columns+1)]
    column_str = ', '.join(str(column))
    try:
        os.system(f'head -n {lines} {src} | cut -d "," -f {column_str} > {dst}')
    except Exception as e:
        print_error(f'Failed to copy {src} to {dst}', e)