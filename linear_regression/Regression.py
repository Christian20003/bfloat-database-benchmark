import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Benchmark')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Csv')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/SQL')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Print')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Helper')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Global')))

from typing import Tuple
from Config import CONFIG
import random
import Format
import Helper
import Database
import Postgres
import Settings
import Create_CSV
import Memory
import Time
import numpy as np
import pandas as pd
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf

def main():
    databases = CONFIG['databases']
    scenarios = CONFIG['setups']
    correct_param_value = CONFIG['param_value']
    init_param_value = CONFIG['param_start']
    overall_points = CONFIG['max_points']
    data_file = './data.csv'
    setup_file = './points.csv'

    for database in databases:
        if database['create_csv'] and not database['ignore']:
            Create_CSV.create_csv_file(database['csv_file'], database['csv_header'])

    parameter_count = 0
    for scenario in scenarios:
        if scenario['ignore']:
            continue
        params = scenario['params_amount']
        points = scenario['points_amount']
        iter = scenario['iterations']
        lr = scenario['lr']
        statement = scenario['statement']
        fromPool = scenario['use_max_points']
        calc_tensorflow = scenario['tensorflow']

        # Generate the maximum number of points ones instead of generating points for each setup
        # If the number of parameters is the same
        if params != parameter_count:
            number_points = overall_points if fromPool else points
            generate_points(number_points, params, correct_param_value, data_file)
            parameter_count = params
        for database in databases:
            if database['ignore']:
                continue
            name = database['name']
            time_exe = database['time-executable']
            memory_exe = database['memory-executable']
            for type in database['types']:
                for agg in database['aggregations']:
                    if not check_execution(name, number_points, parameter_count):
                        continue

                    print_setting(points, params, name, type, iter, lr, agg)
                    generate_statement(statement, params, name, type, iter, lr, agg)
                    prepare_benchmark(database, type, init_param_value, params, points, data_file, setup_file)

                    number_columns = params + 1
                    relevant_columns = [value + 1 for value in range(number_columns - 1)]
                    time, output = Time.benchmark(time_exe, name, number_columns, relevant_columns, False)
                    if time == -1:
                        if name == 'postgres' or name == 'umbra' or name == 'lingodb':
                            Helper.remove_dir(database['files'])
                        else:
                            Helper.remove_files(database['files'])
                        continue
                    output = output[len(output) - 1]
                    if database['name'] == 'postgres':
                        Postgres.stop_database(database['server-preparation'][3])
                    heap, rss = Memory.benchmark(name, memory_exe, '', f'{name}_{type}_{params}_{points}_{agg}', Settings.STATEMENT_FILE)

                    tf_params = np.array([-1])
                    db_mae, tf_mae, db_mse, tf_mse, db_mape, tf_mape, db_smape, tf_smape, db_mpe, tf_mpe = -1, -1, -1, -1, -1, -1, -1, -1, -1, -1
                    
                    if calc_tensorflow:
                        tf_params = regression_tensorflow(setup_file, params, init_param_value, lr, iter, type)
                        db_mae, tf_mae, db_mse, tf_mse, db_mape, tf_mape, db_smape, tf_smape, db_mpe, tf_mpe = evaluate_accuracy(setup_file, output, tf_params, type)

                    truth = [correct_param_value for _ in range(params)]
                    Create_CSV.append_row(
                        database['csv_file'], 
                        [
                            type, agg, params, points, iter, time, heap, rss,
                            db_mae, tf_mae, db_mse, tf_mse, db_mape, tf_mape, db_smape, tf_smape, db_mpe, tf_mpe, 
                            output, tf_params, truth
                        ])
                    if name == 'postgres' or name == 'umbra' or name == 'lingodb':
                        Helper.remove_dir(database['files'])
                    else:
                        Helper.remove_files(database['files'])
    Helper.remove_files([data_file, setup_file, Settings.STATEMENT_FILE])

def check_execution(database: str, number_points: int, number_parameters: int) -> bool:
    if database == 'duckdb':
        pass
    elif database == 'umbra':
        pass
    elif database == 'postgres':
        pass
    elif database == 'lingodb':
        pass
    return True

def print_setting(points: int, parameters: int, database: str, type: str, iterations: int, learning_rate: float, agg_func: str) -> None:
    '''
    This function prints the settings for the current benchmark.

    :param points: The number of points.
    :param parameters: The number of parameters.
    :param database: The database name.
    :param type: The datatype for x and y values.
    :param iterations: The number of update iterations.
    :param learning_rate: The learning rate for the simple gradient descent algorithm.
    :param agg_func: The aggregation function to be used in the recursive CTE.
    '''
    Format.print_title(f'START BENCHMARK - LINEAR-REGRESSION WITH THE FOLLOWING SETTINGS')
    Format.print_information(f'Points: {points}', tabs=1)
    Format.print_information(f'Parameters: {parameters}', tabs=1)
    Format.print_information(f'Database: {database}', tabs=1)
    Format.print_information(f'Type: {type}', tabs=1)
    Format.print_information(f'Iterations: {iterations}', tabs=1)
    Format.print_information(f'Learning Rate: {learning_rate}', tabs=1)
    Format.print_information(f'Aggregation Function: {agg_func}', tabs=1)

def generate_statement(statement: str, params: int, database: str, type: str, iter: int, lr: float, agg: str) -> None:
    '''
    This function generates the SQL file.

    :param statement: The SQL statement to be executed.
    :param params: The number of parameters.
    :param database: The database which should execute the benchmark.
    :param type: The datatype of the output.
    :param iter: The number of iterations in the recursive CTE.
    :param lr: The learning rate for the grandient descent algorithm.
    :param agg: The aggregation function to be used in the recursive CTE.
    '''

    function = 'AVG' if agg == 'standard' else 'FAVG'
    with open(Settings.STATEMENT_FILE, 'w') as file:
        content = []
        # Add aggregation function and lr to the statement
        for _ in range(params):
            content.append(lr)
            content.append(function)
        # Add type casts if necessary
        for _ in range(params):
            if database == 'postgres' and type == 'float4':
                content.append(f'::{type}')
            else:
                content.append('')
        content.append(iter)
        statement = statement.format(*content)
        file.write(statement)

def prepare_benchmark(database: dict, type: str, param_start: int, params: int, points: int, data_file: str, setup_file: str) -> None:
    '''
    This function prepares the benchmark by creating the database and inserting the data.

    :param database: The database name.
    :param type: The datatype for x and y values.
    :param param_start: The starting point for the parameters.
    :param params: The number of parameters.
    :param points: The number of points.
    :param data_file: The name of the csv file where the points are stored.
    :param setup_file: The name of the setup file.
    '''

    Format.print_information('Preparing benchmark - This can take some time', mark=True)
    Helper.copy_csv_file(data_file, setup_file, points + 1)  
    extend_file_path = '.' if database['name'] == 'postgres' else ''
    if database['name'] == 'postgres':
        Helper.create_dir(Settings.POSTGRESQL_DIR)
        executables = database['server-preparation']
        Postgres.create_database(executables[0], executables[1], executables[2])
    elif database['name'] == 'umbra':
        Helper.create_dir(Settings.UMBRA_DIR)
    
    # Create statement for gd_start table
    select_stmt = 'SELECT 0, '
    for _ in range(params):
        select_stmt += str(param_start) + ', '
    select_stmt = select_stmt[:-2]

    letters = 'abcdefghijklmnopqrstuvwxyz'
    prep_database = Database.Database(database['client-preparation'], database['start-sql'], database['end-sql'])
    prep_database.create_table('gd_start', ['idx'] + [letters[value] for value in range(params)], ['int'] + [type for _ in range(params)])
    prep_database.create_table('points', ['id'] + [f'x{i + 1}' for i in reversed(range(params - 1))] + ['y'], ['int', type] + [type for _ in range(params - 1)])
    # LingoDB needs special treatment because copy with bfloat not supported
    if database['name'] == 'lingodb' and type == 'bfloat':
        prep_database.create_table('data', ['id'] + [f'x{i + 1}' for i in reversed(range(params - 1))] + ['y'], ['int', 'float'] + ['float' for _ in range(params - 1)])
        prep_database.insert_from_csv('data', extend_file_path + setup_file)
        prep_database.insert_from_select('points', 'SELECT * FROM data')
    else:
        prep_database.insert_from_csv('points', extend_file_path + setup_file)
    prep_database.insert_from_select('gd_start', select_stmt)
    prep_database.execute_sql()

    # Remove float tables, because that should not be there for bfloat benchmark
    if database['name'] == 'lingodb' and type == 'bfloat':
        Helper.remove_files([
            f'{Settings.LINGODB_DIR}/data.arrow', 
            f'{Settings.LINGODB_DIR}/data.arrow.sample', 
            f'{Settings.LINGODB_DIR}/data.metadata.json',
        ])


def generate_points(number_points: int, number_parameter: int, parameter_value: float, file_name: str) -> None:
    '''
    This function generates a specified number of random points near a regression line.
    It will store all generated points into the given csv file.

    :param number_points: The number of points.
    :param number_parameter: The number of parameters.
    :param parameter_value: The value of the parameter.
    :param file_name: The name of the csv file where the points are stored.
    '''

    Format.print_information('Generating points - This can take some time', mark=True)
    number_parameter -= 1
    header = ['id'] + [f'x{i + 1}' for i in reversed(range(number_parameter))] + ['y']
    Create_CSV.create_csv_file(file_name, header)

    result = []
    for value in range(number_points):
        x_s = [float("{:.4f}".format(random.random())) for _ in range(number_parameter)]
        y = sum([parameter_value * x for x in x_s]) + parameter_value
        result.append([value]+ x_s + [float(y)])
        # Write chunks of 100.000.000 to the csv file to avoid memory issues
        if len(result) >= 100000000:
            Create_CSV.append_rows(file_name, result)
            result.clear()
            Format.print_information(f'{(value + 1) * 100 / number_points}% points generated', tabs=1)
    Create_CSV.append_rows(file_name, result)
    result.clear()
    
def regression_tensorflow(points_csv: str, number_parameters: int, param_start: int, learning_rate: float, iterations: int, type: str) -> np.ndarray:
    '''
    This function calculates the regression line parameters with tensorflow.

    :param points_csv: The name of the csv file where the points are stored.
    :param learning_rate: The learning rate for the simple gradient descent algorithm.
    :param iterations: The number of update iterations.
    :param type: The datatype for x and y values.

    :returns: The calculated slope and intercept of the regression line.
    '''

    Format.print_information('Calculating tensorflow result - This can take some time', mark=True)
    points = pd.read_csv(points_csv)
    datatype = None
    if type == 'bfloat':
        datatype = tf.bfloat16
    elif type == 'float' or type == 'float4':
        datatype = tf.float32
    elif type == 'double' or type == 'float8':
        datatype = tf.float64
    tf_data = [tf.constant(points[column].values, datatype) for column in points.columns[1:]]
    tf_Y = tf_data.pop()

    tf_params = [tf.Variable(param_start, dtype=datatype) for _ in range(number_parameters)]
    lr = tf.Variable(learning_rate, dtype=datatype)

    for _ in range(iterations):
        Y_preds = tf.reduce_sum([tf_params[idx] * x for idx, x in enumerate(tf_data)], axis=0)
        Y_preds += tf_params[-1]
        loss = Y_preds - tf_Y
        dev_param = tf.reduce_mean([2 * x * loss for x in tf_data], axis=1)
        dev_last_param = tf.reduce_mean(2 * loss)
        tf_params = [param - lr * dev_param[idx] for idx, param in enumerate(tf_params[:-1])] + [tf_params[-1] - lr * dev_last_param]

    return [value.numpy() for value in tf_params]

def evaluate_accuracy(points_csv: str, db_params: np.ndarray, tf_params: np.ndarray, type: str) -> Tuple[float, float, float, float, float, float, float, float, float, float]:
    '''
    This function evaluates the accuracy of the database and tensorflow by calculating different error metrics.

    :param points_csv: The name of the csv file where the points are stored.
    :param slope_db: The slope of the regression line from the database.
    :param intercept_db: The offset of the regression line from the database.
    :param slope_tf: The slope of the regression line from tensorflow.
    :param intercept_tf: The offset of the regression line from tensorflow.
    :param type: The datatype of x and y values.

    :returns: The following metrics for the database and tensorflow output: MAE, MSE, MAPE, sMAPE and MPE.
    '''
    
    Format.print_information('Calculating accuracy metrics - This can take some time', mark=True)
    points = pd.read_csv(points_csv)
    points_X = [np.array(points[column].values) for column in points.columns[1:]]
    points_Y = points_X.pop(0)

    db_pred = np.sum([db_params[idx] * x for idx, x in enumerate(points_X)], axis=0)
    tf_pred = np.sum([tf_params[idx] * x for idx, x in enumerate(points_X)], axis=0)

    db_mae = np.mean(np.abs(points_Y - db_pred))
    tf_mae = np.mean(np.abs(points_Y - tf_pred))

    db_mse = np.mean(np.power(points_Y - db_pred, 2))
    tf_mse = np.mean(np.power(points_Y - tf_pred, 2))

    db_mape = np.mean(np.abs((points_Y - db_pred) / points_Y)) * 100
    tf_mape = np.mean(np.abs((points_Y - tf_pred) / points_Y)) * 100

    db_smape = np.mean(np.abs(db_pred - points_Y) / ((points_Y + db_pred) / 2))
    tf_smape = np.mean(np.abs(tf_pred - points_Y) / ((points_Y + tf_pred) / 2))

    db_mpe = np.mean((points_Y - db_pred) / points_Y) * 100
    tf_mpe = np.mean((points_Y - tf_pred) / points_Y) * 100

    Format.print_success(f'Parameter result of Database with {type}: {[value for value in db_params]}', tabs=1)

    Format.print_success(f'Parameter result of Tensorflow with {type}: {[value for value in tf_params]}', tabs=1)

    return db_mae, tf_mae, db_mse, tf_mse, db_mape, tf_mape, db_smape, tf_smape, db_mpe, tf_mpe

if __name__ == "__main__":
    main()
