import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Benchmark')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Csv')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/SQL')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Print')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Helper')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Global')))

from typing import Tuple
from Config import CONFIG, STATEMENT_FILE
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
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf

def main():
    databases = CONFIG['databases']
    scenarios = CONFIG['setups']
    data_file = './data.csv'
    setup_file = './points.csv'

    for database in databases:
        if database['create_csv'] and not database['ignore']:
            Create_CSV.create_csv_file(database['csv_file'], database['csv_header'])

    parameter_count = 0
    for scenario in scenarios:
        if scenario['ignore']:
            continue
        if scenario['param_amount'] != parameter_count:
            number_points = CONFIG['max_points'] if scenario['use_max_points'] else scenario['p_amount']
            generate_points(number_points, scenario['param_amount'], CONFIG['param_value'], data_file)
            parameter_count = scenario['param_amount']
        for database in databases:
            if database['ignore']:
                continue
            for type in database['types']:
                for agg in database['aggregations']:
                    print_setting(scenario['p_amount'], database['name'], type, scenario['iterations'], scenario['lr'], agg)
                    generate_statement(scenario['statement'], agg, scenario['lr'], scenario['iterations'], scenario['param_amount'])
                    prepare_benchmark(database, type, CONFIG['param_start'], scenario['param_amount'], scenario['p_amount'], data_file, setup_file)

                    number_columns = scenario['param_amount'] + 1
                    relevant_columns = [1, number_columns - 1]
                    time, output = Time.benchmark(database['execution-bench'], database['name'], number_columns, relevant_columns)
                    #heap, rss = Memory.benchmark(database['execution-bench'], f'{database["name"]}_{type}_{scenario["p_amount"]}')

                    print(output)

                    #tf_slope, tf_intercept = regression_tensorflow(setup_file, scenario['lr'], scenario['iterations'], type)
                    #db_mae, tf_mae, db_mse, tf_mse, db_mape, tf_mape, db_smape, tf_smape, db_mpe, tf_mpe = evaluate_accuracy(setup_file, output[0][0], output[0][1], tf_slope, tf_intercept, type)

                    """ Create_CSV.append_row(
                        database['csv_file'], 
                        [
                            type, 
                            scenario['p_amount'], 
                            scenario['iterations'], 
                            time, 
                            heap, 
                            rss,
                            db_mae,
                            tf_mae,
                            db_mse,
                            tf_mse, 
                            db_mape,
                            tf_mape,
                            db_smape,
                            tf_smape,
                            db_mpe,
                            tf_mpe, 
                            np.array([output[0][0], output[0][1]]), 
                            np.array([tf_slope, tf_intercept]), 
                            np.array([CONFIG['slope'], CONFIG['intercept']])]
                        ) """
                    Helper.remove_files(database['files'])
                    if database['name'] == 'postgres':
                        Postgres.stop_database(database['prep'][3])
                        Helper.remove_dir(Settings.POSTGRESQL_DIR)
    Helper.remove_files([data_file, setup_file, STATEMENT_FILE])

def prepare_benchmark(database: dict, type: str, param_start: int, number_parameter: int, number_points: int, data_file: str, setup_file: str) -> None:
    '''
    This function prepares the benchmark by creating the database and inserting the data.

    :param database: The database name.
    :param type: The datatype for x and y values.
    :param param_start: The starting point for the parameters.
    :param number_parameter: The number of parameters.
    :param number_points: The number of points.
    :param data_file: The name of the csv file where the points are stored.
    :param setup_file: The name of the setup file.
    '''

    Format.print_information('Preparing benchmark - This can take some time', mark=True)
    Helper.copy_csv_file(data_file, setup_file, number_points + 1)  
    if database['name'] == 'postgres':
        executables = database['prep']
        Postgres.create_database(executables[0], executables[1], executables[2])
    
    letters = 'abcdefghijklmnopqrstuvwxyz'
    select_stmt = 'SELECT 0, '
    for _ in range(number_parameter):
        select_stmt += str(param_start) + ', '
    select_stmt = select_stmt[:-2]
    prep_database = Database.Database(database['execution'], database['start-sql'], database['end-sql'])
    prep_database.create_table('gd_start', ['idx'] + [letters[value] for value in range(number_parameter)], ['int'] + [type for _ in range(number_parameter)])
    prep_database.create_table('points', ['id', 'y'] + [f'x{i}' for i in reversed(range(number_parameter))], ['int'] + [type for _ in range(number_parameter)])
    prep_database.insert_from_select('gd_start', select_stmt)
    prep_database.insert_from_csv('points', setup_file)
    prep_database.execute_sql()

def print_setting(points: int, database: str, type: str, iterations: int, learning_rate: float, agg_func: str) -> None:
    '''
    This function prints the settings for the current benchmark.

    :param points: The number of points.
    :param database: The database name.
    :param type: The datatype for x and y values.
    :param iterations: The number of update iterations.
    :param learning_rate: The learning rate for the simple gradient descent algorithm.
    :param agg_func: The aggregation function to be used in the recursive CTE.
    '''
    Format.print_title(f'START BENCHMARK - LINEAR-REGRESSION WITH THE FOLLOWING SETTINGS')
    Format.print_information(f'Points: {points}', tabs=1)
    Format.print_information(f'Database: {database}', tabs=1)
    Format.print_information(f'Type: {type}', tabs=1)
    Format.print_information(f'Iterations: {iterations}', tabs=1)
    Format.print_information(f'Learning Rate: {learning_rate}', tabs=1)
    Format.print_information(f'Aggregation Function: {agg_func}', tabs=1)

def generate_statement(statement: str, agg_func: str, learning_rate: float, iterations: int, number_parameters: int) -> None:
    '''
    This function generates the SQL file.

    :param statement: The SQL statement to be executed.
    :param agg_func: The aggregation function to be used in the recursive CTE.
    :param iterations: The number of iterations in the recursive CTE.
    :param learning_rate: The learning rate for the grandient descent algorithm.
    :param number_parameters: The number of parameters.
    '''

    agg_func = 'avg' if agg_func == 'standard' else 'favg'
    with open(STATEMENT_FILE, 'w') as file:
        content = []
        for _ in range(number_parameters):
            content.append(learning_rate)
            content.append(agg_func)
        content.append(iterations)
        content.append(iterations)
        statement = statement.format(*content)
        file.write(statement)


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
    header = ['id', 'y']
    header += [f'x{i}' for i in reversed(range(number_parameter))]
    Create_CSV.create_csv_file(file_name, header)

    result = []
    for value in range(number_points):
        x_s = [float("{:.4f}".format(random.random())) for _ in range(number_parameter)]
        y = sum([parameter_value * (x ** idx) for idx, x in reversed(list(enumerate(x_s)))])
        result.append([value, float(y)] + list(reversed(x_s)))
        # Write chunks of 100.000.000 to the csv file to avoid memory issues
        if len(result) >= 100000000:
            Create_CSV.append_rows(file_name, result)
            result.clear()
            Format.print_information(f'{(value + 1) * 100 / number_points}% points generated', tabs=1)
    Create_CSV.append_rows(file_name, result)
    result.clear()
    
def regression_tensorflow(points_csv: str, learning_rate: float, iterations: int, type: str) -> Tuple[float, float]:
    '''
    This function calculates the regression line parameters with tensorflow.

    :param points_csv: The name of the csv file where the points are stored.
    :param learning_rate: The learning rate for the simple gradient descent algorithm.
    :param iterations: The number of update iterations.
    :param type: The datatype for x and y values.

    :returns: The calculated slope and intercept of the regression line.
    '''

    Format.print_information('Calculating tensorflow result - This can take some time', mark=True)
    points = pd.read_csv(points_csv).to_numpy()
    datatype = tf.bfloat16 if type == 'bfloat' else tf.float32
    tf_X = tf.constant([entry[1] for entry in points], datatype)
    tf_Y = tf.constant([entry[2] for entry in points], datatype)
    slope = tf.Variable(0, dtype=datatype)
    intercept = tf.Variable(0, dtype=datatype)
    lr = tf.Variable(learning_rate, dtype=datatype)

    for _ in range(iterations):
        Y_pred = slope * tf_X + intercept
        loss = Y_pred - tf_Y
        dev_slope = tf.reduce_mean(2 * tf_X * loss)
        dev_intercept = tf.reduce_mean(2 * loss)
        slope = slope - lr * dev_slope
        intercept = intercept - lr * dev_intercept

    return slope.numpy(), intercept.numpy()

def evaluate_accuracy(points_csv: str, slope_db: float, intercept_db: float, slope_tf: float, intercept_tf: float, type: str) -> Tuple[float, float, float, float, float, float, float, float, float, float]:
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
    points = pd.read_csv(points_csv).to_numpy()
    points_X = np.array([entry[1] for entry in points])
    points_Y = np.array([entry[2] for entry in points])
    db_pred = slope_db * points_X + intercept_db
    tf_pred = slope_tf * points_X + intercept_tf

    db_mae = np.mean(np.abs(points_Y - db_pred))
    tf_mae = np.mean(np.abs(points_Y - tf_pred))

    db_mse = np.mean(np.power(points_Y - db_pred, 2))
    tf_mse = np.mean(np.power(points_Y - tf_pred, 2))

    db_mape = np.mean(np.abs((points_Y - db_pred) / points_Y)) * 100
    tf_mape = np.mean(np.abs((points_Y - tf_pred) / points_Y)) * 100

    db_smape = np.mean(np.abs(db_pred - points_Y) / ((points_Y + db_pred) / 2)) * 100
    tf_smape = np.mean(np.abs(tf_pred - points_Y) / ((points_Y + tf_pred) / 2)) * 100

    db_mpe = np.mean((points_Y - db_pred) / points_Y) * 100
    tf_mpe = np.mean((points_Y - tf_pred) / points_Y) * 100

    slope_db_sign = '' if slope_db >= 0 else '-'
    intercept_db_sign = '+' if intercept_db >= 0 else '-'
    slope_db = slope_db * -1 if slope_db < 0 else slope_db
    intercept_db = intercept_db * -1 if intercept_db < 0 else intercept_db
    Format.print_success(f'Result of Database with {type}: {slope_db_sign}{slope_db} * x {intercept_db_sign} {intercept_db}', tabs=1)

    slope_tf_sign = '' if slope_tf >= 0 else '-'
    intercept_tf_sign = '+' if intercept_tf >= 0 else '-'
    slope_tf = slope_tf * -1 if slope_tf < 0 else slope_tf
    intercept_tf = intercept_tf * -1 if intercept_tf < 0 else intercept_tf
    Format.print_success(f'Result of Tensorflow with {type}: {slope_tf_sign}{slope_tf} * x {intercept_tf_sign} {intercept_tf}', tabs=1)

    return db_mae, tf_mae, db_mse, tf_mse, db_mape, tf_mape, db_smape, tf_smape, db_mpe, tf_mpe

if __name__ == "__main__":
    main()
