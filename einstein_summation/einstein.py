import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Benchmark')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Csv')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Parsing')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Plot')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Types')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Helper')))

from typing import List, Tuple
from Value import Value
from Format import print_information, print_success, print_title, print_warning
from Parse_Args import parse_args
from Parse_Time import parse_time_metrics
from Parse_Memory import parse_memory_metrics
from Parse_Table import parse_table_output
from Csv import init_csv_file, write_to_csv
from Execute import time_benchmark, memory_benchmark
from Plot import plot_results
from Helper import remove_files, execute_sql, generate_csv, tfloat_switch
from Config import CONFIG
import numpy as np
import random

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
            table_names = ['matrixa', 'matrixb', 'vectorv']
            if type == 'tfloat':
                dummy_tables = ['matrixadummy', 'matrixbdummy', 'vectorvdummy']
                create_tables(dummy_tables, type, args)
                insert_data(tensorA, dummy_tables[0], './matrixa.csv', args)
                insert_data(tensorB, dummy_tables[1], './matrixb.csv', args)
                insert_data(tensorC, dummy_tables[2], './matrixc.csv', args)
                tfloat_switch(table_names[0], dummy_tables[0], args)
                tfloat_switch(table_names[1], dummy_tables[1], args)
                tfloat_switch(table_names[2], dummy_tables[2], args)
            else:
                create_tables(table_names, type, args)
                insert_data(tensorA, table_names[0], './matrixa.csv', args)
                insert_data(tensorB, table_names[1], './matrixb.csv', args)
                insert_data(tensorC, table_names[2], './matrixc.csv', args)
            tensorA_np = Value.values_to_numpy(tensorA, 2)
            tensorB_np = Value.values_to_numpy(tensorB, axis_2)
            tensorC_np = Value.values_to_numpy(tensorC, axis_2)
            output = time_benchmark(args)
            results = parse_time_metrics(output)
            output = parse_table_output(output, 2, 1, 1)
            file = memory_benchmark(args, f'{type}{2*axis_1 + axis_1*axis_2 + axis_2}')
            results = parse_memory_metrics(results, file)
            eval = evaluate_accuray(tensorA_np, tensorB_np, tensorC_np, output, type)
            write_to_csv(results, 'Einstein', type, 2*axis_1 + axis_1*axis_2 + axis_2, eval)
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

def create_tables(table_names: List[str], type: str, paths: dict) -> None:
    '''
    This function creates an SQL table with the provided entries of the tensor object.

    :param tensor: A list of randomly created entries.
    :param table_name: The name of the table
    :param type: The datatype for the value of the entries.
    :param paths: A tuple including the path to the executable.

    :raise RuntimeError: If the tables could not be generated.
    '''
    
    files = []
    for name in table_names:
        files.append(f'{name}.arrow')
        files.append(f'{name}.arrow.sample')
        files.append(f'{name}.metadata.json')
    remove_files(files, paths['storage'])

    statements = ['SET persist=1;\n']
    for name in table_names:
        statements.append(f'CREATE TABLE {name}(rowIndex int, columnIndex int, val {type});\n')
    execute_sql(statements, paths['exe'], paths['storage'])

def insert_data(tensor: List[Value], table_name: str, csv_file: str, paths: dict) -> None:
    '''
    This function inserts all given tensors into a table.

    :param tensor: A list of tensors which should be inserted.
    :param table_name: The name of table in which the tensors should be inserted.
    :param csv_file: The file where the data is stored.
    :param paths: A dictionary with paths to all necessary executables and directories.

    :raise RuntimeError: If the data could not be inserted.
    '''

    print_information(f'Inserting {len(tensor)} of values (This can take a while)', tabs=1)
    data = [[value.row, value.column, value.value] for value in tensor]
    generate_csv(csv_file, ['rowIndex', 'columnIndex', 'val'], data)
    statements = ['SET persist=1;\n']
    copy = f"copy {table_name} from '{csv_file}' delimiter ',' HEADER;\n"
    statements.append(copy)
    execute_sql(statements, paths['exe'], paths['storage'])

def evaluate_accuray(tensorA: np.ndarray, tensorB: np.ndarray, tensorC: np.ndarray, result: np.ndarray, type: str) -> Tuple[str, str]:
    '''
    This function evaluates the precision of the database output with the function of numpy.
    The following calculation take place -> A*B*C

    :param tensorA: The first generated tensor object.
    :param tensorB: The second generated tensor object.
    :param tensorC: The third generated tensor object.
    :param result: The output of the database.
    :param type: The datatype of the current running benchmark.

    :returns: Two strings containing the correct result from numpy and the database result.
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
    return np.array_str(correct_result), np.array_str(result)

if __name__ == "__main__":
    main()
