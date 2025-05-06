import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Benchmark')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Csv')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/SQL')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Print')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Helper')))

from typing import List, Tuple
from Config import CONFIG, STATEMENT
import random
import Format
import Helper
import Database
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

    for database in databases:
        if database['create_csv']:
            Create_CSV.create_csv_file(database['csv_file'], database['csv_header'])

    for scenario in scenarios:
        if scenario['ignore']:
            continue
        generate_statement(scenario['lr'], CONFIG['iterations'])
        slope, intercept = generate_regression_line(scenario['max'], scenario['min'])
        generate_points(scenario['p_amount'], scenario['max'], scenario['min'], slope, intercept)
        #normalize_points(points, './points.csv')
        for database in databases:
            for type in database['types']:
                Format.print_title(f'START BENCHMARK - LINEAR-REGRESSION WITH {scenario["p_amount"]} POINTS')
                prep_database = Database.Database(database['execution'], database['start-sql'], database['end-sql'])
                prep_database.create_table('gd_start', ['idx', 'a', 'b'], ['int', type, type])
                prep_database.create_table('points', ['id', 'x', 'y'], ['int', type, type])
                prep_database.insert_from_select('gd_start', 'select 0, 1, 1')
                prep_database.insert_from_csv('points', './points.csv')
                prep_database.execute_sql()

                execution_string = database['execution-bench'].format('Statement.sql')
                time, output = Time.benchmark(execution_string, database['name'], 3, [1,2])
                heap, rss = Memory.benchmark(execution_string, f'{database["name"]}_{type}_{scenario["p_amount"]}')

                tf_slope, tf_intercept = regression_tensorflow('./points.csv', scenario['lr'], CONFIG['iterations'], type)
                db_mape, tf_mape = evaluate_accuracy('./points.csv', output[0][0], output[0][1], tf_slope, tf_intercept, type)

                Create_CSV.append_row(
                    database['csv_file'], 
                    [type, scenario['p_amount'], CONFIG['iterations'], time, heap, rss, db_mape, np.array([output[0][0], output[0][1]]), np.array([tf_slope, tf_intercept]), np.array([slope, intercept])]
                    )
                Helper.remove_files(database['files'])
    Helper.remove_files(['./points.csv', './Statement.sql'])

def generate_statement(learning_rate: float, iterations: int) -> None:
    '''
    This function generates the SQL file.

    :param iterations: The number of iterations in the recursive CTE.
    :param learning_rate: The learning rate for the grandient descent algorithm.
    '''

    with open('./Statement.sql', 'w') as file:
        file.write(STATEMENT.format(learning_rate, learning_rate, iterations, iterations))

def generate_regression_line(upper_bound: int, lower_bound: int) -> Tuple[float, float]:
    '''
    This function generates some random parameter for a linear regression problem (slope and offset).

    :param upper_bound: The maximum value for both parameters.
    :param lower_bound: The minimum value for both parameters.

    :return: A tuple including the slope and the offset of the generated regression line.
    '''

    #slope = "{:.4f}".format(random.gauss(0, 1))
    #intercept = "{:.4f}".format(random.uniform(upper_bound, lower_bound))
    return 0.25, 15


def generate_points(number: int, upper_bound: int, lower_bound: int, slope: float, intercept: float) -> List[List[float]]:
    '''
    This function generates a specified number of random points near a regression line.
    It will further add a random error to the y label.

    :param number: The number of points.
    :param upper_bound: The maximum value for the x value.
    :param lower_bound: The minimum value for the x value.
    :param slope: The slope of the regression line.
    :param intercept: The offset of the regression line.

    :return: A list of point objects.
    '''

    result = []
    for value in range(number):
        x = float("{:.4f}".format(random.random()))
        #error = "{:.4f}".format(random.uniform(upper_bound / 10, lower_bound / 10))
        y = slope * x + intercept #+ float(error)
        result.append([value, float(x), float(y)])
    Create_CSV.create_csv_file('./points.csv', ['id', 'x', 'y'])
    Create_CSV.append_rows('./points.csv', result)
    result.clear()

def normalize_points(points: List[List[float]], file_name: str) -> None:
    '''
    This function normalizes all x values of each point based on the maximum and minimum x values.
    Finally all points will be written into the given csv file.

    :param points: A list of points which should be normalized.
    :param file_name: The name of the csv file.
    '''

    """ max_x = max([entry[1] for entry in points])
    min_x = min([entry[1] for entry in points])
    points = [[entry[0], ((entry[1] - min_x) / (max_x - min_x)), entry[2]] for entry in points] """
    x = np.array([entry[1] for entry in points])
    mean_x = np.mean(x)
    std_dev_x = np.sqrt(np.sum(np.pow(x - mean_x, 2)) / len(points))
    points = [[entry[0], (entry[1] - mean_x) / std_dev_x, entry[2]] for entry in points]

    Create_CSV.create_csv_file(file_name, ['id', 'x', 'y'])
    Create_CSV.append_rows(file_name, points)
    points.clear()
    
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
    slope = tf.Variable(1.0, dtype=datatype)
    intercept = tf.Variable(1.0, dtype=datatype)
    lr = tf.Variable(learning_rate, dtype=datatype)

    for _ in range(iterations):
        Y_pred = slope * tf_X + intercept
        loss = Y_pred - tf_Y
        dev_slope = tf.reduce_mean(2 * tf_X * loss)
        dev_intercept = tf.reduce_mean(2 * loss)
        slope = slope - lr * dev_slope
        intercept = intercept - lr * dev_intercept

    return slope.numpy(), intercept.numpy()

def evaluate_accuracy(points_csv: str, slope_db: float, intercept_db: float, slope_tf: float, intercept_tf: float, type: str) -> Tuple[float, float]:
    '''
    This function evaluates the accuracy of the database and tensorflow by calculating the MAPE score.

    :param points_csv: The name of the csv file where the points are stored.
    :param slope_db: The slope of the regression line from the database.
    :param intercept_db: The offset of the regression line from the database.
    :param slope_tf: The slope of the regression line from tensorflow.
    :param intercept_tf: The offset of the regression line from tensorflow.
    :param type: The datatype of x and y values.

    :returns: Two floats containing the MAPE score of the database and tensorflow.
    '''
    
    Format.print_information('Calculating accuracy - This can take some time', mark=True)
    points = pd.read_csv(points_csv).to_numpy()
    points_X = np.array([entry[1] for entry in points])
    points_Y = np.array([entry[2] for entry in points])
    db_pred = slope_db * points_X + intercept_db
    tf_pred = slope_tf * points_X + intercept_tf

    db_mape = (1 / len(points)) * np.sum(np.absolute((points_Y - db_pred)) / np.absolute(points_Y)) * 100
    tf_mape = (1 / len(points)) * np.sum(np.absolute((points_Y - tf_pred)) / np.absolute(points_Y)) * 100
    
    #print((1 / len(points))*np.sum(np.pow(points_Y - db_pred, 2)))

    slope_db_sign = '' if slope_db >= 0 else '-'
    intercept_db_sign = '+' if intercept_db >= 0 else '-'
    slope_db = slope_db * -1 if slope_db < 0 else slope_db
    intercept_db = intercept_db * -1 if intercept_db < 0 else intercept_db
    Format.print_information(f'Result of Database with {type}: {slope_db_sign}{slope_db} * x {intercept_db_sign} {intercept_db}', tabs=1)
    Format.print_information(f'Average difference between forecast value and actual value is {"{:.2f}".format(db_mape)}%', tabs=2)

    slope_tf_sign = '' if slope_tf >= 0 else '-'
    intercept_tf_sign = '+' if intercept_tf >= 0 else '-'
    slope_tf = slope_tf * -1 if slope_tf < 0 else slope_tf
    intercept_tf = intercept_tf * -1 if intercept_tf < 0 else intercept_tf
    Format.print_information(f'Result of Tensorflow with {type}: {slope_tf_sign}{slope_tf} * x {intercept_tf_sign} {intercept_tf}', tabs=1)
    Format.print_information(f'Average difference between forecast value and actual value is {"{:.2f}".format(tf_mape)}%', tabs=2)

    return db_mape, tf_mape

if __name__ == "__main__":
    main()
