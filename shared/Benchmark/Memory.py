import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Print')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Helper')))

from typing import Tuple, List
from pathlib import Path
from datetime import datetime
from threading import Thread, Event
import subprocess
import Format
import re
import Helper
import time
import psutil

def _parse_output(file_name: str, source_file: str) -> Tuple[float, float]:
    '''
    This function parses the output of the heaptrack analysis.

    :param file_name: The name of the file where the results are stored.
    :param source_file: The name of the file where the raw data are stored.
    
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
    return heap, rss

def heaptrack_memory(execution: str, file_name: str, statement: str = None, keep_raw_file: bool = False) -> Tuple[float, float]:
    '''
    This function executes the memory benchmark with the tool 'heaptrack'.

    :param execution: The execution string of the database.
    :param file_name: Parts of the file name of the analysed data from heaptrack.
    :param statement: The SQL-Query if it is not possible to push it through the database executable.
    :param keep_raw_file: If the generated file from heaptrack should not be deleted.

    :returns: A tuple including the used peak heap and rss memory of the process (everything in GB).
    '''

    Format.print_information('Start the memory benchmark - This will take some time', mark=True)
    date = datetime.now()
    formatted_date = date.strftime('%d-%m-%Y-%H-%M')
    file_name_raw = f'{formatted_date}-{file_name}-raw'
    file_name_analysed = f'{formatted_date}-{file_name}-analysed'
    database  = subprocess.Popen(
        ['heaptrack', '-o', file_name_raw] + execution.split(),
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True
    )
    if statement:
        statement = statement.replace('\n', ' ')
        time.sleep(1)
        database.stdin.write(statement)
        database.stdin.flush()
    _, error = database.communicate()
    if error:
        Format.print_error('An error has been printed during memory benchmark', error)
    heap, rss = _parse_output(file_name_analysed, file_name_raw)
    if not keep_raw_file:
        Helper.remove_files([file_name_raw])
    return heap, rss

def memory_thread(life_signal: Event, process_signal: Event, file_name: str, used_memory: float, sleep: float) -> None:
    '''
    This function will be executed by another thread. Reads the current memory consumption of a process
    and writes it into a file.

    :param life_signal: If the thread should be alive.
    :param process_signal: If the measured process is active.
    :param file_name: The name of the file in which to write the memory values.
    :param used_memory: The memory usage before the activation of the process.
    :param sleep: How many seconds should be ignored after reading the next memory value.
    '''

    with open(file_name, 'w') as file:
        while life_signal.is_set():
            if not process_signal.is_set():
                continue
            try:
                memory = psutil.virtual_memory()
                file.write(str(used_memory - memory.used) + '\n')
                time.sleep(sleep)
            except psutil.NoSuchProcess:
                Format.print_error('Psutil-Thread did not find process', None)
                break

def python_memory(execution: str, time: float, statement: str = None, memory_over_time: bool = False) -> List[float]:
    '''
    This function executes the memory benchmark with the python tool 'psutil'.

    :param execution: The execution string of the database.
    :param time: The execution time of the process (to add sleep times if too long)
    :param statement: The SQL-Query if it is not possible to push it through the database executable.
    :param memory_over_time: If a list of memory values should be returned (development of the memory
                             over running time). If false it will only return the peak.

    :returns: The peak memory consumption of the process if memory_over_time is false, otherwise a list
              of multiple memory values (everything in bytes).
    
    '''

    Format.print_information('Start the memory benchmark - This will take some time', mark=True)
    life_signal = Event()
    process_signal = Event()
    life_signal.set()
    file_name = 'memory_data'
    result = []
    sleep = 0.001 if time > 60 or memory_over_time else 0
    current_memory = psutil.virtual_memory().used
    thread = Thread(target=memory_thread, args=(life_signal, process_signal, file_name, current_memory, sleep))
    thread.start()

    database = subprocess.Popen(
        execution.split(),
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True
    )
    process_signal.set()
    if statement:
        statement = statement.replace('\n', ' ')
        time.sleep(1)
        database.stdin.write(statement)
        database.stdin.flush()
    _, error = database.communicate()
    life_signal.clear()
    if error:
        Format.print_error('An error has been printed during memory benchmark', error)
    thread.join()

    with open(file_name, 'r') as file:
        if memory_over_time:
            result = [float(value) for value in file.readlines()]
        else:
            peak = 0
            for entry in file.readlines():
                if float(entry) > peak:
                    peak = float(entry)
            result.append(peak)
    Helper.remove_files([file_name])
    return result