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
import time

def benchmark(database_name: str, execution_client: str, execution_server: str, file_name: str, statement_file: str) -> Tuple[float, float]:
    '''
    This function executes the memory benchmark with 'heaptrack'.

    :param database_name: The name of the database.
    :param execution_client: The execution string of the database client.
    :param execution_server: The execution strings of the database server (optional).
    :param file_name: The name of the file where the results should be stored. Must
                      be unique otherwise the current content will be overriden.
    :param statement_file: The name of the file where the SQL statements are stored.
    
    :returns: A tuple including the used peak heap and rss memory of the process.
    '''

    Format.print_information('Start the memory benchmark - This will take some time', mark=True)
    if database_name == 'postgres':
        benchmark_server(execution_client, statement_file)
    elif database_name == 'duckdb' or database_name == 'umbra' or database_name == 'lingodb':
        benchmark_client(execution_client)
    return parse_output(file_name)

def benchmark_server(execution_server: str, statement_file: str) -> None:
    '''
    This function executes the memory benchmark with 'heaptrack' by tracking a server executable.

    :param execution_server: The execution strings of the database server.
    :param statement_file: The name of the file where the SQL statements are stored.
    '''

    server = subprocess.Popen(
        ['heaptrack', '-o', 'mem_data'] + execution_server.split(),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    time.sleep(1)
    with open(statement_file, 'r') as file:
        content = file.read()
        content = content.replace('\n', ' ')
        server.stdin.write(content)
        server.stdin.flush()
    _, error = server.communicate()
    if error:
        Format.print_error('Something went wrong during the memory-benchmark', error)
    

def parse_output(file_name: str, source_file: str = 'mem_data') -> Tuple[float, float]:
    '''
    This function parses the output of the heaptrack analysis.

    :param file_name: The name of the file where the results are stored.
    
    :returns: A tuple including the used peak heap and rss memory of the process.
    '''

    data_file = f'./{source_file}.zst'
    if not Path(f'{source_file}.zst').exists():
        data_file = f'./{source_file}.gz'
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
    #Helper.remove_files([data_file])
    return heap, rss

def benchmark_client(execution: str) -> None:
    '''
    This function executes the memory benchmark with 'heaptrack' by tracking only a client executable.

    :param execution: The execution string of the database.
    '''

    bench_execution  = subprocess.Popen(
        ['heaptrack', '-o', 'mem_data'] + execution.split(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    _, error = bench_execution.communicate()
    if error:
        Format.print_error('Something went wrong during the memory-benchmark', error)