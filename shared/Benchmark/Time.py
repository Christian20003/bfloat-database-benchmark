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

def benchmark(execution: str, database_name: str, total_columns: int, relevant_columns: List[int]) -> Tuple[float, np.ndarray]:
    '''
    This function executes the provided statement and measures the execution time.

    :param execution: The execution command of the database.
    :param database_name: The name of the database.
    :param total_columns: The number of columns in the output.
    :param relevant_columns: The number of the columns which should be considered in the resulting array.
                             (Starting with 0)

    :returns: A tuple including the execution time and the database output as numpy array.
    '''

    if database_name == 'duckdb' or database_name == 'umbra' or database_name == 'postgres':
        time, output = python_time(execution)
        array = Parse_Table.output_to_numpy(database_name, output, total_columns, relevant_columns)
        return time, array

def python_time(execution: str) -> Tuple[float, str]:
    '''
    This function executes the given statement and measures the execution time.

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
    output, error = database.communicate()
    time = (datetime.now() - start).total_seconds()
    if error:
        Format.print_error('Something went wrong during the time-benchmark', error)
    return time, output