import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Benchmark')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Csv')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/SQL')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Print')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Helper')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Global')))

from typing import List, Tuple
from Config import CONFIG
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
        rowsA = scenario['dimension_1']
        rowsB = scenario['dimension_2']
        rowsC = scenario['dimension_3']
        generate_tensor(rowsA, rowsB, maxtrix_a_file)
        generate_tensor(rowsB, rowsC, maxtrix_b_file)
        generate_tensor(rowsC, 1, vector_v_file)
        for database in databases:
            if database['ignore']:
                continue
            name = database['name']
            time_exe = database['time-executable']
            memory_exe = database['memory-executable']
            for type in database['types']:
                for statement in scenario['statements']:
                    number = statement['number']
                    content = statement['statement']
                    for agg in database['aggregations']:
                        if not check_execution(name, rowsA, number):
                            continue

                        print_setting(rowsA, rowsB, rowsC, name, type, number, agg)
                        generate_statement(content, number, agg)
                        prepare_benchmark(database, type, maxtrix_a_file, maxtrix_b_file, vector_v_file)

                        time, output = Time.benchmark(time_exe, name, 2, [1], False)
                        if time == -1:
                            if name == 'postgres' or name == 'umbra' or name == 'lingodb':
                                Helper.remove_dir(database['files'])
                            else:
                                Helper.remove_files(database['files'])
                            continue
                        if database['name'] == 'postgres':
                            Postgres.stop_database(database['server-preparation'][3])
                        heap, rss = Memory.benchmark(name, memory_exe, '', f'{name}_{type}_{rowsA}_{agg}_{number}', Settings.STATEMENT_FILE)
                        output = np.array([entry[0] for entry in output])

                        tf_output = -1
                        l2_db, l2_tf, mse_db, mse_tf = -1, -1, -1, -1
                        if number != 2:
                            tf_output, tf_truth = einstein_tensorflow(maxtrix_a_file, maxtrix_b_file, vector_v_file, type, True if number == 3 else False)
                            l2_db, l2_tf, mse_db, mse_tf = evaluate_accuray(output, tf_output, tf_truth)

                        Create_CSV.append_row(database['csv_file'], 
                                              [
                                                  type,
                                                  agg,
                                                  number,
                                                  rowsA*rowsB, 
                                                  rowsB*rowsC, 
                                                  rowsC,
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
                        
                        if name == 'postgres' or name == 'umbra' or name == 'lingodb':
                            Helper.remove_dir(database['files'])
                        else:
                            Helper.remove_files(database['files'])
    Helper.remove_files([maxtrix_a_file, maxtrix_b_file, vector_v_file, Settings.STATEMENT_FILE])

def check_execution(database: str, setup_id: int, number: int) -> bool:
    if database == 'duckdb':
        pass
    elif database == 'umbra':
        pass
    elif database == 'postgres':
        pass
    elif database == 'lingodb':
        pass
    return True

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
    extend_file_path = '.' if database['name'] == 'postgres' else ''
    if database['name'] == 'postgres':
        Helper.create_dir(Settings.POSTGRESQL_DIR)
        executables = database['server-preparation']
        Postgres.create_database(executables[0], executables[1], executables[2])
    elif database['name'] == 'umbra':
        Helper.create_dir(Settings.UMBRA_DIR)
    elif database['name'] == 'lingodb':
        Helper.create_dir(Settings.LINGODB_DIR)
    prep_database = Database.Database(database['client-preparation'], database['start-sql'], database['end-sql'])
    prep_database.create_table('matrixa', ['rowIndex', 'columnIndex', 'val'], ['int', 'int', type])
    prep_database.create_table('matrixb', ['rowIndex', 'columnIndex', 'val'], ['int', 'int', type])
    prep_database.create_table('vectorv', ['rowIndex', 'columnIndex', 'val'], ['int', 'int', type])
    # Copy with bfloat does not work (apache arrow does not support it)
    if database['name'] == 'lingodb' and type == 'bfloat':
        prep_database.create_table('data1', ['rowIndex', 'columnIndex', 'val'], ['int', 'int', 'float'])
        prep_database.create_table('data2', ['rowIndex', 'columnIndex', 'val'], ['int', 'int', 'float'])
        prep_database.create_table('data3', ['rowIndex', 'columnIndex', 'val'], ['int', 'int', 'float'])
        prep_database.insert_from_csv('data1', extend_file_path + matrixa_file)
        prep_database.insert_from_csv('data2', extend_file_path + matrixb_file)
        prep_database.insert_from_csv('data3', extend_file_path + vectorv_file)
        prep_database.insert_from_select('matrixa', 'SELECT * FROM data1')
        prep_database.insert_from_select('matrixb', 'SELECT * FROM data2')
        prep_database.insert_from_select('vectorv', 'SELECT * FROM data3')
    else:
        prep_database.insert_from_csv('matrixa', extend_file_path + matrixa_file)
        prep_database.insert_from_csv('matrixb', extend_file_path + matrixb_file)
        prep_database.insert_from_csv('vectorv', extend_file_path + vectorv_file)
    prep_database.execute_sql()

    if database['name'] == 'lingodb' and type == 'bfloat':
        Helper.remove_files([
            f'{Settings.LINGODB_DIR}/data1.arrow', 
            f'{Settings.LINGODB_DIR}/data1.arrow.sample', 
            f'{Settings.LINGODB_DIR}/data1.metadata.json',
            f'{Settings.LINGODB_DIR}/data2.arrow', 
            f'{Settings.LINGODB_DIR}/data2.arrow.sample', 
            f'{Settings.LINGODB_DIR}/data2.metadata.json',
            f'{Settings.LINGODB_DIR}/data3.arrow', 
            f'{Settings.LINGODB_DIR}/data3.arrow.sample', 
            f'{Settings.LINGODB_DIR}/data3.metadata.json',
        ])

def generate_statement(statement: str, number: int, aggr_func: str) -> None:
    '''
    This function generates the SQL statement for the database.
    
    :param statement: The type of statement that should be used.
    :param number: The number of the statement.
    :param aggr_func: The aggregation function that should be used.
    '''

    function = 'SUM' if aggr_func == 'standard' else 'KAHAN_SUM'
    with open(Settings.STATEMENT_FILE, 'w') as file:
        if number == 1 or number == 3:
            file.write(statement.format(function))
        elif number == 4:
            file.write(statement.format(function, function))
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
    datatype = None
    if type == 'bfloat':
        datatype = tf.bfloat16
    elif type == 'float' or type == 'float4':
        datatype = tf.float32
    elif type == 'double' or type == 'float8':
        datatype = tf.float64
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
