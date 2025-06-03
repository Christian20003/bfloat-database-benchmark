import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Print')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Parsing')))

from typing import List, Tuple
from datetime import datetime
import numpy as np
import subprocess
import Format
import Parse_Table

def benchmark(execution: str, database_name: str, total_columns: int, relevant_columns: List[int], ignore_output: bool) -> Tuple[float, np.ndarray]:
    '''
    This function executes the provided statement and measures the execution time. If the 
    process takes longer than 3600 seconds it will be cancelled and returns a negative
    execution time and emtpy output.

    :param execution: The execution command of the database.
    :param database_name: The name of the database.
    :param total_columns: The number of columns in the output.
    :param relevant_columns: The number of the columns which should be considered in the resulting array
                             (Starting with 0).
    :param ignore_output: If the database output should be parsed and returned as numpy array. If not the 
                          resulting numpy array will be empty

    :returns: A tuple including the execution time and the database output as numpy array.
    '''

    time = -1
    output = ''
    if database_name == 'duckdb' or database_name == 'umbra' or database_name == 'postgres' or database_name == 'lingodb':
        time, output = python_time(execution)
    if time != -1 and not ignore_output:
        array = Parse_Table.output_to_numpy(database_name, output, total_columns, relevant_columns)
        return time, array
    elif ignore_output:
        return time, np.array([])
    else:
        return -1, np.array([])

def python_time(execution: str) -> Tuple[float, str]:
    '''
    This function executes the given statement and measures the execution time. If the 
    process takes longer than 3600 seconds it will be cancelled and returns a negative
    execution time and emtpy output.

    :param execution: The execution command of the database.

    :returns: The measured execution time and the database output.
    '''

    Format.print_information('Start the time benchmark', mark=True)
    start = datetime.now()
    database = subprocess.Popen(
        execution.split(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    try:
        output, error = database.communicate(timeout=3600)
        time = (datetime.now() - start).total_seconds()
        if error:
            Format.print_error('An error has been printed during time benchmark', error)
        return time, output
    except subprocess.TimeoutExpired:
        database.kill()
        return -1, ''