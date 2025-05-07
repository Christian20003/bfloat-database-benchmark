import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Benchmark')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Csv')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/SQL')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Print')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Helper')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Global')))

from typing import List
from Config import CONFIG, STATEMENT, STATEMENT_FILE
from collections import defaultdict
import random
import Format
import Database
import Postgres
import Create_CSV
import Time
import Memory
import Settings
import Helper
import numpy as np
import pandas as pd
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf

def main():
    databases = CONFIG['databases']
    scenarios = CONFIG['setups']

    generate_statement()

    for database in databases:
        if database['create_csv']:
            Create_CSV.create_csv_file(database['csv_file'], database['csv_header'])

    for scenario in scenarios:
        if scenario['ignore']:
            continue
        generate_tensor(scenario['dimension_1'], scenario['dimension_2'], './matrixa.csv')
        generate_tensor(scenario['dimension_2'], scenario['dimension_3'], './matrixb.csv')
        generate_tensor(scenario['dimension_3'], 1, './vectorv.csv')
        for database in databases:
            if database['ignore']:
                continue
            for type in database['types']:
                Format.print_title(f'START BENCHMARK - EINSTEIN-SUMMATION WITH {scenario["dimension_1"]}X{scenario["dimension_2"]} * {scenario["dimension_2"]}X{scenario["dimension_3"]} * {scenario["dimension_3"]}X1, TYPE {type} AND DATABASE {database["name"]}')
                if database['name'] == 'postgres':
                    executables = database['prep']
                    Postgres.create_database(executables[0], executables[1], executables[2])
                prep_database = Database.Database(database['execution'], database['start-sql'], database['end-sql'])
                prep_database.create_table('matrixa', ['rowIndex', 'columnIndex', 'val'], ['int', 'int', type])
                prep_database.create_table('matrixb', ['rowIndex', 'columnIndex', 'val'], ['int', 'int', type])
                prep_database.create_table('vectorv', ['rowIndex', 'columnIndex', 'val'], ['int', 'int', type])
                prep_database.insert_from_csv('matrixa', './matrixa.csv' if database['name'] != 'postgres' else '../matrixa.csv')
                prep_database.insert_from_csv('matrixb', './matrixb.csv' if database['name'] != 'postgres' else '../matrixa.csv')
                prep_database.insert_from_csv('vectorv', './vectorv.csv' if database['name'] != 'postgres' else '../matrixa.csv')
                prep_database.execute_sql()

                time, output = Time.benchmark(database['execution-bench'], database['name'], 2, [1])
                heap, rss = Memory.benchmark_server(database['execution-bench'], database['prep'][1] , database['prep'][3], f'{database["name"]}_{type}_{scenario["dimension_1"]}')
                output = np.array([entry[0] for entry in output])

                tf_output = einstein_tensorflow('./matrixa.csv', './matrixb.csv', './vectorv.csv', type)
                loss = evaluate_accuray(output, tf_output)

                Create_CSV.append_row(database['csv_file'], [type, scenario['dimension_1']*scenario['dimension_2'], scenario['dimension_2']*scenario['dimension_3'], scenario['dimension_3'], time, heap, rss, loss, np.sum(output), np.sum(tf_output)])
                Helper.remove_files(database['files'])
                if database['name'] == 'postgres':
                    Postgres.stop_database(database['prep'][3])
                    Helper.remove_dir(Settings.POSTGRESQL_DIR)
    Helper.remove_files(['./matrixa.csv', './matrixb.csv', './vectorv.csv', './Statement.sql'])

def generate_statement() -> None:
    '''
    This function generates the SQL file.
    '''

    with open(f'./{STATEMENT_FILE}', 'w') as file:
        file.write(STATEMENT)

def generate_tensor(rows: int, columns: int, file_name: str) -> None:
    '''
    This function generates a list of tensor entries with random values and stores them in a csv file.

    :param rows: The number of rows in the tensor.
    :param columns: The number of columns in the tensor.
    :param file_name: The name of the csv file where the data should be stored.
    '''

    result = []
    for row in range(rows):
        for column in range(columns):
            value = random.random()
            result.append([row, column, value])

    Create_CSV.create_csv_file(file_name, ['rowIndex', 'columnIndex', 'val'])
    Create_CSV.append_rows(file_name, result)
    result.clear()

def list_to_array(tensor: List[List[float]]) -> np.ndarray:
    '''
    This function transforms a list of values with row and column indicies into a numpy array.

    :param tensor: The list of values that should be transformed.

    :returns: The data as numpy array.
    '''

    # Use a defaultdict to group elements by their row index
    grouped = defaultdict(list)
    
    for entry in tensor:
        row_index = entry[0]
        value = entry[2]
        grouped[row_index].append(value)
    
    # Create the result array from the grouped values
    result = [values[0] if len(values) == 1 else values for values in grouped.values()]
    
    return np.array(result)

def einstein_tensorflow(matrix_a_csv: str, matrix_b_csv: str, vector_v_csv: str, type: str) -> np.ndarray:
    '''
    This function executes a matrix multiplication with tensorflow.

    :param matrix_a: The name of the csv file where the values of matrix-a are stored.
    :param matrix_b: The name of the csv file where the values of matrix-b are stored.
    :param vector_v: The name of the csv file where the values of vector-v are stored.
    :param type: The datatype of each value.

    :returns: The result as numpy array.
    '''

    Format.print_information('Calculating tensorflow result - This can take some time', mark=True)
    datatype = tf.bfloat16 if type == 'bfloat' else tf.float32
    tf_a = tf.convert_to_tensor(list_to_array(pd.read_csv(matrix_a_csv).to_numpy()), datatype)
    tf_b = tf.convert_to_tensor(list_to_array(pd.read_csv(matrix_b_csv).to_numpy()), datatype)
    tf_v = tf.convert_to_tensor(list_to_array(pd.read_csv(vector_v_csv).to_numpy()), datatype)

    result = tf.einsum('ac,bc,b->a', tf_a, tf_b, tf_v)

    return result.numpy()

def evaluate_accuray(tensor_db: np.ndarray, tensor_tf: np.ndarray) -> float:
    '''
    This function calculates the loss of the database output with the output of tensorflow.

    :param tensor_db: The result of the database.
    :param tensor_tf: The result of tensorflow.

    :returns: The loss between these two results.
    '''

    loss = np.sqrt(np.sum(np.power(tensor_db - tensor_tf, 2)))
    Format.print_success(f'Loss between database and tensorflow: {"{:.4f}".format(loss)}', tabs=1)
    return loss

if __name__ == "__main__":
    main()
