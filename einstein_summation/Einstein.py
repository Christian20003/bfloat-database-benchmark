import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Benchmark')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Csv')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/SQL')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Print')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Helper')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Global')))

from typing import List, Tuple
from Config import CONFIG, STATEMENT_1, STATEMENT_2, STATEMENT_3, STATEMENT_4, STATEMENT_FILE
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
    maxtrix_a_file = './matrixa.csv'
    maxtrix_b_file = './matrixb.csv'
    vector_v_file = './vectorv.csv'

    for database in databases:
        if database['create_csv'] and not database['ignore']:
            Create_CSV.create_csv_file(database['csv_file'], database['csv_header'])

    for scenario in scenarios:
        if scenario['ignore']:
            continue
        generate_tensor(scenario['dimension_1'], scenario['dimension_2'], maxtrix_a_file)
        generate_tensor(scenario['dimension_2'], scenario['dimension_3'], maxtrix_b_file)
        generate_tensor(scenario['dimension_3'], 1, vector_v_file)
        for database in databases:
            if database['ignore']:
                continue
            for type in database['types']:
                for statement in scenario['statements']:
                    statement_number = 0
                    if (statement == STATEMENT_1):
                        statement_number = 1
                    elif (statement == STATEMENT_2):
                        statement_number = 2
                    elif (statement == STATEMENT_3):
                        statement_number = 3
                    elif (statement == STATEMENT_4):
                        statement_number = 4
                    for agg in database['aggregations']:
                        print_setting(scenario['dimension_1'], scenario['dimension_2'], scenario['dimension_3'], database['name'], type, statement_number, agg)
                        generate_statement(statement, agg)
                        prepare_benchmark(database, type, maxtrix_a_file, maxtrix_b_file, vector_v_file)

                        time, output = Time.benchmark(database['execution-bench'], database['name'], 2, [1])
                        heap, rss = Memory.benchmark(database['execution-bench'], f'{database["name"]}_{type}_{scenario["dimension_1"]}_{agg}_{statement_number}')
                        output = np.array([entry[0] for entry in output])

                        tf_output = None
                        l2_db, l2_tf, mse_db, mse_tf = None, None, None, None
                        if statement_number != 2:
                            tf_output, tf_truth = einstein_tensorflow(maxtrix_a_file, maxtrix_b_file, vector_v_file, type, True if statement_number == 3 else False)
                            l2_db, l2_tf, mse_db, mse_tf = evaluate_accuray(output, tf_output, tf_truth)

                        Create_CSV.append_row(database['csv_file'], 
                                              [
                                                  type, 
                                                  scenario['dimension_1']*scenario['dimension_2'], 
                                                  scenario['dimension_2']*scenario['dimension_3'], 
                                                  scenario['dimension_3'],
                                                  time, 
                                                  heap, 
                                                  rss, 
                                                  l2_db,
                                                  l2_tf,
                                                  mse_db,
                                                  mse_tf, 
                                                  np.sum(output), 
                                                  np.sum(tf_output)
                                               ])
                        Helper.remove_files(database['files'])
                        if database['name'] == 'postgres':
                            Postgres.stop_database(database['prep'][3])
                            Helper.remove_dir(Settings.POSTGRESQL_DIR)
    Helper.remove_files([maxtrix_a_file, maxtrix_b_file, vector_v_file, STATEMENT_FILE])

def print_setting(dimension1: int, dimension2: int, dimension3: int, database: str, type: str, statement: int, agg_func: str) -> None:
    '''
    This function prints the settings for the current benchmark.

    :param dimension1: The number of rows in the first matrix.
    :param dimension2: The number of columns in the first matrix and rows in the second matrix.
    :param dimension3: The number of columns in the second matrix and rows in the vector.
    :param database: The database name.
    :param type: The datatype for tensor entries.
    :param statement: The number of the statement that should be used.
    :param agg_func: The aggregation function to be used in the recursive CTE.
    '''

    Format.print_title(f'START BENCHMARK - EINSTEIN SUMMATION WITH THE FOLLOWING SETTINGS')
    Format.print_information(f'Matrix A: {dimension1}x{dimension2}', tabs=1)
    Format.print_information(f'Matrix B: {dimension2}x{dimension3}', tabs=1)
    Format.print_information(f'Vector V: {dimension3}x1', tabs=1)
    Format.print_information(f'Database: {database}', tabs=1)
    Format.print_information(f'Type: {type}', tabs=1)
    Format.print_information(f'Statement: {statement}', tabs=1)
    Format.print_information(f'Aggregation Function: {agg_func}', tabs=1)

def prepare_benchmark(database: dict, type: str, matrixa_file: str, matrixb_file: str, vectorv_file: str) -> None:
    '''
    This function prepares the benchmark by creating the database and inserting the data.

    :param database: The database name.
    :param type: The datatype for x and y values.
    :param matrixa_file: The name of the csv file where the values of matrix-a are stored.
    :param matrixb_file: The name of the csv file where the values of matrix-b are stored.
    :param vectorv_file: The name of the csv file where the values of vector-v are stored.
    '''

    Format.print_information('Preparing benchmark - This can take some time', mark=True)
    if database['name'] == 'postgres':
        executables = database['prep']
        Postgres.create_database(executables[0], executables[1], executables[2])
    prep_database = Database.Database(database['execution'], database['start-sql'], database['end-sql'])
    prep_database.create_table('matrixa', ['rowIndex', 'columnIndex', 'val'], ['int', 'int', type])
    prep_database.create_table('matrixb', ['rowIndex', 'columnIndex', 'val'], ['int', 'int', type])
    prep_database.create_table('vectorv', ['rowIndex', 'columnIndex', 'val'], ['int', 'int', type])
    prep_database.insert_from_csv('matrixa', matrixa_file)
    prep_database.insert_from_csv('matrixb', matrixb_file)
    prep_database.insert_from_csv('vectorv', vectorv_file)
    prep_database.execute_sql()

def generate_statement(statement: str, aggr_func: str) -> None:
    '''
    This function generates the SQL statement for the database.
    
    :param statement: The type of statement that should be used.
    :param aggr_func: The aggregation function that should be used.
    '''

    aggr_func = 'SUM' if aggr_func == 'standard' else 'KAHAN_SUM'
    with open(STATEMENT_FILE, 'w') as file:
        if statement == STATEMENT_1 or statement == STATEMENT_3:
            file.write(statement.format(aggr_func))
        elif statement == STATEMENT_4:
            file.write(statement.format(aggr_func, aggr_func))
        else:
            file.write(statement)

def generate_tensor(rows: int, columns: int, file_name: str) -> None:
    '''
    This function generates a list of tensor entries with random values and stores them in a csv file.

    :param rows: The number of rows in the tensor.
    :param columns: The number of columns in the tensor.
    :param file_name: The name of the csv file where the data should be stored.
    '''

    Format.print_information(f'Generating tensor with {rows} rows and {columns} columns', mark=True)
    result = []
    for row in range(rows):
        for column in range(columns):
            value = random.random()
            result.append([row, column, value])

    Create_CSV.create_csv_file(file_name, ['rowIndex', 'columnIndex', 'val'])
    Create_CSV.append_rows(file_name, result)
    result.clear()

def list_to_array(tensor: List[List[float]], datatype: tf.DType) -> Tuple[tf.Tensor, tf.Tensor]:
    '''
    This function transforms a list of values with row and column indicies into a tensor.

    :param tensor: The list of values that should be transformed.

    :returns: The data in float64 and defined type tensor.
    '''

    # Use a defaultdict to group elements by their row index
    grouped = defaultdict(list)
    
    for entry in tensor:
        row_index = entry[0]
        value = entry[2]
        grouped[row_index].append(value)
    
    # Create the result array from the grouped values
    result = [values[0] if len(values) == 1 else values for values in grouped.values()]
    
    return tf.Variable(result, dtype=datatype), tf.Variable(result, dtype=tf.float64)

def einstein_tensorflow(matrix_a_csv: str, matrix_b_csv: str, vector_v_csv: str, type: str, single_mult: bool) -> Tuple[np.ndarray, np.ndarray]:
    '''
    This function executes a matrix multiplication with tensorflow.

    :param matrix_a: The name of the csv file where the values of matrix-a are stored.
    :param matrix_b: The name of the csv file where the values of matrix-b are stored.
    :param vector_v: The name of the csv file where the values of vector-v are stored.
    :param type: The datatype of each value.

    :returns: The result as numpy array in the specified type as well as float64.
    '''

    Format.print_information('Calculating tensorflow result - This can take some time', mark=True)
    datatype = tf.bfloat16 if type == 'bfloat' else tf.float32
    tf_a, tf_a_double = None, None
    if not single_mult:
        tf_a, tf_a_double = list_to_array(pd.read_csv(matrix_a_csv).to_numpy(), datatype)
    tf_b, tf_b_double = list_to_array(pd.read_csv(matrix_b_csv).to_numpy(), datatype)
    tf_v, tf_v_double = list_to_array(pd.read_csv(vector_v_csv).to_numpy(), datatype)

    result, result_double = None, None
    if single_mult:
        result = tf.einsum('ij,j->i', tf_b, tf_v)
        result_double = tf.einsum('ij,j->i', tf_b_double, tf_v_double)
    else:
        result = tf.einsum('ac,bc,b->a', tf_a, tf_b, tf_v)
        result_double = tf.einsum('ac,bc,b->a', tf_a_double, tf_b_double, tf_v_double)

    return result.numpy(), result_double.numpy()

def evaluate_accuray(tensor_db: np.ndarray, tensor_tf: np.ndarray, truth: np.ndarray) -> Tuple[float, float, float, float]:
    '''
    This function calculates different error metrics of the database and tensorflow output.

    :param tensor_db: The result of the database.
    :param tensor_tf: The result of tensorflow.
    :param truth: The truth value of the result.

    :returns: The L2 loss (as norm) and MSE of the database and tensorflow result.
    '''

    Format.print_information('Evaluating accuracy - This can take some time', mark=True)
    L2_loss_db = np.sqrt(np.sum(np.power(truth - tensor_db, 2)))
    L2_loss_tf = np.sqrt(np.sum(np.power(truth - tensor_tf, 2)))

    mse_db = np.mean(np.power(truth - tensor_db, 2))
    mse_tf = np.mean(np.power(truth - tensor_tf, 2))

    Format.print_success(f'L2 norm of database: {"{:.4f}".format(L2_loss_db)}', tabs=1)
    Format.print_success(f'L2 norm of tensorflow: {"{:.4f}".format(L2_loss_tf)}', tabs=1)

    return L2_loss_db, L2_loss_tf, mse_db, mse_tf

if __name__ == "__main__":
    main()
