import sys
sys.path.append('../Types/')

from typing import Dict
from Format import print_error
from time import time
import subprocess

def time_benchmark(paths: Dict) -> str:
    '''
    This function performs a benchmark to measure the total time to complete the statement. 

    :param paths: A dictionary with the paths to the needed executables and directories.

    :returns: The complete output of the database.
    
    :raise RuntimeError: If the database could not run the benchmark.
    '''
    
    print('Start the time benchmark')
    database = subprocess.Popen(
        [paths['exe_bench'], paths['statement'], paths['storage'], 'json'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    output, error = database.communicate()
    if error:
        print_error('Something went wrong during the time-benchmark', error)
    return output

def memory_benchmark(paths: Dict, key_name: str) -> str:
    '''
    This function performs a benchmark to measure the amount of memory needed to execute the provided statement.

    :param paths: A dictionary with the paths to the needed executables and directories.
    :param key_name: Part of the file name for identification.

    :returns: The name of the file which includes every data from the memory benchmark.

    :raise RuntimeError: If the database could not run the benchmark.
    '''

    print('Start the memory benchmark (This will take some time)')
    file_name = f'massif.{key_name}.{int(time() * 1000)}'
    database  = subprocess.Popen(
        ['valgrind', '--quiet', '--tool=massif', '--stacks=yes', f'--massif-out-file={file_name}', paths['exe_bench'], paths['statement'], paths['storage'], 'none']
    )
    _, error = database.communicate()
    if error:
        print_error('Something went wrong during the memory-benchmark', error)
    return file_name
