import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Benchmark')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Csv')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Parsing')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Plot')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Types')))

from typing import List, Tuple
from Value import Value
from Format import print_error, print_information, print_success, print_title, print_warning
from Parse_Args import parse_args
from Parse_Time import parse_time_metrics
from Parse_Memory import parse_memory_metrics
from Parse_Table import parse_table_output
from Csv import init_csv_file, write_to_csv
from Execute import time_benchmark, memory_benchmark
from Plot import plot_results
from Config import CONFIG
import numpy as np
import random
import subprocess
import time

def main():
    args = parse_args('Einstein_Summation')
    types = CONFIG['types']
    init_csv_file()
    # Iterate over all cluser benchmarks
    for key, value in CONFIG.items():
        if 'setup' not in key:
            continue
        axis_1 = value['size_axis_1']
        axis_2 = value['size_axis_2']
        print_title(f'### START BENCHMARKING EINSTEIN SUMMATION WITH 2x{axis_1}*{axis_1}x{axis_2}*{axis_2}x1 ###')
        tensorA = generate_tensor(2, axis_1, CONFIG['value_upper_bound'], CONFIG['value_lower_bound'])
        tensorB = generate_tensor(axis_2, axis_1, CONFIG['value_upper_bound'], CONFIG['value_lower_bound'])
        tensorC = generate_tensor(axis_2, 1, CONFIG['value_upper_bound'], CONFIG['value_lower_bound'])
        # Iterate over all specified types
        for type in types:
            print_information(f'Execute benchmark with type: {type}', mark=True)
            create_table(tensorA, 'matrixa', type, args)
            create_table(tensorB, 'matrixb', type, args)
            create_table(tensorC, 'vectorv', type, args)
            tensorA_np = values_to_numpy(tensorA, 2)
            tensorB_np = values_to_numpy(tensorB, axis_2)
            tensorC_np = values_to_numpy(tensorC, axis_2)
            output = time_benchmark(args)
            results = parse_time_metrics(output)
            output = parse_table_output(output, 2, 1, 1)
            memory_benchmark(args)
            results = parse_memory_metrics(results)
            write_to_csv(results, 'Einstein', type, 2*axis_1 + axis_1*axis_2 + axis_2)
            evaluate_accuray(tensorA_np, tensorB_np, tensorC_np, output, type)
        print('\n')
    plot_results('Number of tensor entries')

def generate_tensor(rows: int, columns: int, upper_bound: int, lower_bound: int) -> List[Value]:
    '''
    This function generates a list of tensor entries with random values.

    :param rows: The number of rows in the tensor.
    :param columns: The number of columns in the tensor.
    :param upper_bound: The maximum value for the entries in the tensor.
    :param lower_bound: The minimum value for the entries in the tensor.

    :return: A list of values objects (tensor entries).
    '''
    result = []
    for row in range(rows):
        for column in range(columns):
            value = "{:.4f}".format(random.uniform(lower_bound, upper_bound))
            result.append(Value(row, column, value))
    return result

def values_to_sql(values: List[Value], table_name: str) -> str:
    '''
    This function transforms a list of value objects into a string containing 
    an SQL-INSERT statement with all entries.

    :param values: The list of values which should be considered in the SQL statement.
    :param table_name: The name of the table in which they should be inserted.

    :return: The SQL-INSERT statement with all provided entries.
    '''
    result = f'INSERT INTO {table_name}(rowIndex, columnIndex, val) VALUES '
    for idx, value in enumerate(values):
        result += value.to_sql_value()
        if idx != len(values) - 1:
            result += ","
    result += ";"
    return result

def values_to_numpy(values: List[Value], rows: int) -> np.ndarray:
    '''
    This function changes the given list of value objects to a numpy array.

    :param values: The list of values which should be converted.
    :param rows: The number of rows of the resulting array.

    :return: The tensor as numpy array.
    '''
    list = []
    for row in range(rows):
        entries = [element for element in values if element.row == row]
        entries = sorted(entries, key=lambda x: x.column)
        entries = [element.value for element in entries]
        # Could be a vector
        if len(entries) == 1:
            list.append(entries[0])
        else:
            list.append(entries)
    return np.array(list, dtype=float)

def remove_table(paths: Tuple[str, str, str], table_name: str) -> None:
    '''
    This function removes files which corresponds to the given table name.

    :param paths: A tuple including the path to the directory of the persistent database.
    :param table_name: The name of the table whic files should be removed.

    :raise RuntimeError: If the corresponding files could not be removed. 
    '''

    files = [f'{table_name}.arrow', f'{table_name}.arrow.sample', f'{table_name}.metadata.json']
    for file in files:
        try:
            os.unlink(os.path.join(paths['storage'], file))
        except FileNotFoundError:
            print_warning(f'{table_name} table does not exist. Ignore deletion')
        except Exception as e:
            print_error(f'Failed to remove {table_name} table files', e)
    # Ensure files are removed
    time.sleep(1)

def create_table(tensor: List[Value], table_name: str, type: str, paths: Tuple[str, str, str]) -> None:
    '''
    This function creates an SQL table with the provided entries of the tensor object.

    :param tensor: A list of randomly created entries.
    :param table_name: The name of the table
    :param type: The datatype for the value of the entries.
    :param paths: A tuple including the path to the executable.

    :raise RuntimeError: If the tables could not be generated.
    '''
    
    print(f'Create table {table_name} with {len(tensor)} entries.')
    remove_table(paths, table_name)
    # Define all statements to create tables with the help of LingoDB
    persist = 'SET persist=1;\n'
    create_table = f'CREATE TABLE {table_name}(rowIndex int, columnIndex int, val {type});\n'
    number_tuples = len(tensor) if len(tensor) <= 1000 else 1000
    database = subprocess.Popen(
        [paths['exe'], paths['storage']], 
        stdout=subprocess.PIPE,
        stdin=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    # Create all table and insert cluster values
    statements = [persist, create_table]
    for statement in statements:
        database.stdin.write(statement)
        database.stdin.flush()
    # Insert point values. Limit to 1000 at a time, otherwise LingoDB stops working
    for index in range(0, len(tensor), number_tuples):
        insert = values_to_sql(tensor[index:index + number_tuples], table_name)
        database.stdin.write(f'{insert}\n')
        database.stdin.flush()
        # Print after some steps the progress
        inserted = (index + number_tuples)*100/len(tensor)
        if inserted % 10 == 0:
            print_information(f'{inserted}% tuples inserted')
    _, error = database.communicate()
    if error:
        print_error('Something went wrong by creating the table', error)

def evaluate_accuray(tensorA: np.ndarray, tensorB: np.ndarray, tensorC: np.ndarray, result: np.ndarray, type: str):
    '''
    This function evaluates the precision of the database output with the function of numpy.
    The following calculation take place -> A*B*C

    :param tensorA: The first generated tensor object.
    :param tensorB: The second generated tensor object.
    :param tensorC: The third generated tensor object.
    :param result: The output of the database.
    :param type: The datatype of the current running benchmark.
    '''

    print('Evaluate accuracy of the database output with numpy')
    correct_result = np.einsum('ac, bc, b->a', tensorA, tensorB, tensorC)
    distance = np.sum(result - correct_result)

    print_information('Result:', True, 1)
    print_information(f'Lingo-DB with {type}: {result}', tabs=2)
    print_information(f'Numpy with float: {correct_result}', tabs=2)
    value = f'{distance:.2f}'
    if value.startswith('0.00'):
        print_success(f'Distance: {distance:.2f}', tabs=2)
    else:
        print_warning(f'Distance: {distance:.2f}', tabs=2)

if __name__ == "__main__":
    main()
