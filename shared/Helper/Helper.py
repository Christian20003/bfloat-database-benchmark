import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Types')))

from typing import List
from Format import print_error, print_warning
import subprocess

def execute_sql(statements: List[str], exe: str, dir: str) -> str:
    '''
    This function executes a list of SQL statements (without benchmarking).

    :param statements: A list of SQL statements (Every element should end with ";\n").
    :param exe: The path to the executable of the database.
    :param dir: The path to the directory where the data should be stored.

    :returns: The output of the executions

    :raise RuntimeError: If the database process failed.
    '''

    database = subprocess.Popen(
        [exe, dir], 
        stdout=subprocess.PIPE,
        stdin=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    for statement in statements:
        database.stdin.write(statement)
        database.stdin.flush()
    output, error = database.communicate()
    if error:
        print_error('Something went wrong by creating the table', error)
    return output

def remove_files(files: List[str], dir: str) -> None:
    '''
    This function deletes a list of files.

    :param files: A list of file names.
    :param dir: The directory of the files.

    :raise RuntimeError: If something went wrong during deletion. 
    '''
    for file in files:
        try:
            os.unlink(os.path.join(dir, file))
        except FileNotFoundError:
            print_warning(f'{file} does not exist. Ignore deletion')
        except Exception as e:
            print_error(f'Failed to remove {file}', e)