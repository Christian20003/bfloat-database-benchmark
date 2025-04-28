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