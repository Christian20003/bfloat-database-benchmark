import sys

sys.path.append('../Types/')

from typing import Tuple
from Format import color
import subprocess

def time_benchmark(paths: Tuple[str, str, str]) -> str:
    '''
    This function executes the actual benchmark.

    :param paths: A tuple with the paths to the executable and directories.

    :returns: The complete output of the database.
    
    :raise RuntimeError: If the database could not run the benchmark.
    '''
    
    print('Start the time benchmark')
    database = subprocess.Popen(
        [f'{paths[0]}/run-sql', paths[2], paths[1], 'json'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    output, error = database.communicate()
    if error:
        raise RuntimeError(f'{color.RED}Something went wrong during the time-benchmark{color.END}: \n {error}')
    return output

def memory_benchmark(paths: Tuple[str, str, str]):
    print('Start the memory benchmark (This will take some time)')
    database  = subprocess.Popen(
        ['valgrind', '--quiet', '--tool=massif', '--stacks=yes', '--massif-out-file=kmeans', f'{paths[0]}/run-sql', paths[2], paths[1], 'none']
    )
    _, error = database.communicate()
    if error:
        raise RuntimeError(f'{color.RED}Something went wrong during the memory-benchmark{color.END}: \n {error}')