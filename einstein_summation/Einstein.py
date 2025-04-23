import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Benchmark')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Csv')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/SQL')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Print')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Helper')))

from typing import List
from Config import CONFIG, STATEMENT
import random
import Format
import Database
import Create_CSV
import Helper
import numpy as np
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
        matrix_a = generate_tensor(scenario['dimension_1'], scenario['dimension_2'], CONFIG['max'], CONFIG['min'])
        matrix_b = generate_tensor(scenario['dimension_2'], scenario['dimension_3'], CONFIG['max'], CONFIG['min'])
        vector_v = generate_tensor(scenario['dimension_3'], 1, CONFIG['max'], CONFIG['min'])
        for database in databases:
            for type in database['types']:
                Format.print_title(f'START BENCHMARK - EINSTEIN-SUMMATION WITH {scenario["dimension_1"]}X{scenario["dimension_2"]} * {scenario["dimension_2"]}X{scenario["dimension_3"]} * {scenario["dimension_3"]}X1')
                prep_database = Database.Database(database['execution'], database['start-sql'], database['end-sql'])
                prep_database.create_table('matrixa', ['rowIndex', 'columnIndex', 'val'], ['int', 'int', type])
                prep_database.create_table('matrixb', ['rowIndex', 'columnIndex', 'val'], ['int', 'int', type])
                prep_database.create_table('vectorv', ['rowIndex', 'columnIndex', 'val'], ['int', 'int', type])
                prep_database.insert_from_csv('matrixa', './matrixa.csv', ['rowIndex', 'columnIndex', 'val'], matrix_a)
                prep_database.insert_from_csv('matrixb', './matrixb.csv', ['rowIndex', 'columnIndex', 'val'], matrix_b)
                prep_database.insert_from_csv('vectorv', './vectorv.csv', ['rowIndex', 'columnIndex', 'val'], vector_v)
                prep_database.execute_sql()

                time = 0
                memory = 0

                tf_output = einstein_tensorflow(matrix_a, matrix_b, vector_v, type)
                loss = evaluate_accuray(_, tf_output)

                Create_CSV.append_row(database['csv_file'], [time, memory])
                Helper.remove_files(database['files'], './')

def generate_statement() -> None:
    '''
    This function generates the SQL file.
    '''

    with open('./Statement.sql', 'w') as file:
        file.write(STATEMENT)

def generate_tensor(rows: int, columns: int, upper_bound: int, lower_bound: int) -> List[List[float]]:
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
            result.append([row, column, value])
    return result

def list_to_array(tensor: List[List[float]]) -> np.ndarray:
    '''
    This function transforms a list of values with row and column indicies into a numpy array.

    :param tensor: The list of values that should be transformed.

    :returns: The data as numpy array.
    '''

    rows = [entry[0] for entry in tensor]
    rows = set(rows)
    result = []
    for row in rows:
        result.append(entry[2] for entry in tensor if entry[0] == row)
    return np.array(result)

def einstein_tensorflow(matrix_a: List[List[float]], matrix_b: List[List[float]], vector_v: List[List[float]], type: str) -> np.ndarray:
    '''
    This function executes a matrix multiplication with tensorflow.

    :param matrix_a: The first matrix.
    :param matrix_b: The second matrix.
    :param vector_v: The third matrix / vector.
    :param type: The datatype of each value.

    :returns: The result as numpy array.
    '''

    datatype = tf.bfloat16 if type == 'tfloat' else tf.float32
    tf_a = tf.convert_to_tensor(list_to_array(matrix_a), datatype)
    tf_b = tf.convert_to_tensor(list_to_array(matrix_b), datatype)
    tf_v = tf.convert_to_tensor(list_to_array(vector_v), datatype)

    result = tf.matmul(tf_a, tf_b)
    result = tf.matmul(result, tf_v)

    return result.numpy()

def evaluate_accuray(tensor_db: np.ndarray, tensor_tf: np.ndarray) -> float:
    '''
    This function calculates the loss of the database output with the output of tensorflow.

    :param tensor_db: The result of the database.
    :param tensor_tf: The result of tensorflow.

    :returns: The loss between these two results.
    '''

    loss = np.sqrt(np.sum(np.power(tensor_db - tensor_tf, 2)))
    Format.print_success(f'Loss between database and tensorflow: {loss}', tabs=1)
    return loss

if __name__ == "__main__":
    main()
