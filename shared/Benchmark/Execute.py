import sys
sys.path.append('../Types/')

from typing import Dict
from Format import print_error
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
        [paths['exe_bench'], paths['file'], paths['storage'], 'json'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    output, error = database.communicate()
    if error:
        print_error('Something went wrong during the time-benchmark', error)
    return output

def memory_benchmark(paths: Dict) -> None:
    '''
    This function performs a benchmark to measure the amount of memory needed to execute the provided statement.

    :param paths: A dictionary with the paths to the needed executables and directories.

    :raise RuntimeError: If the database could not run the benchmark.
    '''

    print('Start the memory benchmark (This will take some time)')
    database  = subprocess.Popen(
        ['valgrind', '--quiet', '--tool=massif', '--stacks=yes', '--massif-out-file=memperfom', paths['exe_bench'], paths['file'], paths['storage'], 'none']
    )
    _, error = database.communicate()
    if error:
        print_error('Something went wrong during the memory-benchmark', error)