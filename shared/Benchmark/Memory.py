import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Print')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Helper')))

from typing import Tuple
from pathlib import Path
import subprocess
import Format
import re
import Helper

def benchmark_server(execution: str, server_start: str, server_stop: str, file_name: str) -> Tuple[float, float]:
    '''
    This function executes the memory benchmark with 'heaptrack'.

    :param execution: The execution string of the database.
    :param file_name: The name of the file where the results should be stored. Must
                      be unique otherwise the current content will be overriden.
    
    :returns: A tuple including the used peak heap and rss memory of the process.
    '''

    Format.print_information('Start the memory benchmark - This will take some time', mark=True)
    stop = subprocess.Popen(server_stop.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stop.communicate()
    _  = subprocess.Popen(['heaptrack', '-o', 'mem_data'] + server_start.split())

    execute_sql = subprocess.Popen(execution.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    _, error = execute_sql.communicate()
    if error:
        Format.print_error('Something went wrong during the memory-benchmark', error)
    
    stop = subprocess.Popen(server_stop.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stop.communicate()

    data_file = './mem_data.zst'
    if not Path('mem_data.zst').exists():
        data_file = './mem_data.gz'
    heap = 0
    rss = 0
    with open(file_name, 'w+') as file:
        analyze = subprocess.Popen(
            ['heaptrack', '-a', '-p', '0', '-a', '0', '-T', '0', '-l', '0', data_file],
            stdout=file
        )
        analyze.communicate()
        file.seek(0)
        for item in file.readlines():
            if 'peak heap memory consumption' in item or 'peak RSS (including heaptrack overhead)' in item:
                index = item.find(':')
                value = item[index+1:]
                number = float(re.findall(r'-?\d+\.\d+e[+-]?\d+|-?\d+\.\d+|-?\d+', value)[0])
                if 'B' in value:
                    number = number / (1024*1024*1024)
                if 'K' in value:
                    number = number / (1024*1024)
                if 'M' in value:
                    number = number / 1024
                
                if 'heap memory' in item:
                    heap = number
                else:
                    rss = number
    Helper.remove_files([data_file])
    return heap, rss

def benchmark(execution: str, file_name: str) -> Tuple[float, float]:
    '''
    This function executes the memory benchmark with 'heaptrack'.

    :param execution: The execution string of the database.
    :param file_name: The name of the file where the results should be stored. Must
                      be unique otherwise the current content will be overriden.
    
    :returns: A tuple including the used peak heap and rss memory of the process.
    '''

    Format.print_information('Start the memory benchmark - This will take some time', mark=True)
    bench_execution  = subprocess.Popen(
        ['heaptrack', '-o', 'mem_data'] + execution.split(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    _, error = bench_execution.communicate()
    if error:
        Format.print_error('Something went wrong during the memory-benchmark', error)
    
    data_file = './mem_data.zst'
    if not Path('mem_data.zst').exists():
        data_file = './mem_data.gz'
    heap = 0
    rss = 0
    with open(file_name, 'w+') as file:
        analyze = subprocess.Popen(
            ['heaptrack', '-a', '-p', '0', '-a', '0', '-T', '0', '-l', '0', data_file],
            stdout=file
        )
        analyze.communicate()
        file.seek(0)
        for item in file.readlines():
            if 'peak heap memory consumption' in item or 'peak RSS (including heaptrack overhead)' in item:
                index = item.find(':')
                value = item[index+1:]
                number = float(re.findall(r'-?\d+\.\d+e[+-]?\d+|-?\d+\.\d+|-?\d+', value)[0])
                if 'B' in value:
                    number = number / (1024*1024*1024)
                if 'K' in value:
                    number = number / (1024*1024)
                if 'M' in value:
                    number = number / 1024
                
                if 'heap memory' in item:
                    heap = number
                else:
                    rss = number
    Helper.remove_files([data_file])
    return heap, rss